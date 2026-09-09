#!/usr/bin/env python3
"""
lexicon_proxy.py — compute the lexicon proxy for the TPG organizational strand.

WHAT THIS IS
    A SAMPLING AID. For each enumerated organization, it fetches the homepage
    and records whether any frozen lexicon term appears in the visible text.
    The result stratifies the coding queue (registration: Sampling and sample
    size, "Draw rule").

WHAT THIS IS NOT
    It is NOT the tier assignment. Tier is a human judgment that requires the
    placement of the phrase and the identity of the speaker — whether the
    organization is describing itself or quoting a funder. A string match on
    homepage text establishes neither. Never report this column as tier, and
    never let it prefill the tier field.

OUTPUT
    A CSV with one row per input record, carrying the proxy value, the terms
    matched, short verifying snippets, and full fetch provenance.

    lexicon_proxy takes three values, not two:
        TRUE          at least one lexicon term found
        FALSE         page fetched and read successfully, no term found
        UNDETERMINED  could not be established (fetch failed, no URL, or the
                      page yielded too little text to read)

    UNDETERMINED is not FALSE. A site that failed to load has not told us it
    lacks the vocabulary. Records marked UNDETERMINED are resolved by hand
    before the queue is built; they are never silently swept into FALSE.

USAGE
    python lexicon_proxy.py --in enumerated.csv --out proxy.csv
    python lexicon_proxy.py --in enumerated.csv --out proxy.csv --retry-undetermined
    python lexicon_proxy.py --print-lexicon

    Input needs an id column and a URL column (defaults: org_id, website_url;
    override with --id-col / --url-col).

    The lexicon is read from frozen_lexicon.json alongside this script, or
    from the path given by --lexicon. It is not duplicated in this file.

    Responses are cached on disk, so re-running is cheap and does not re-hit
    sites. Delete the cache directory to force a clean re-fetch.

REPRODUCIBILITY
    Every row records the URL requested, the final URL after redirects, the
    HTTP status, the fetch timestamp (UTC), the length of extracted text, and
    the SHA-256 of that text. The run writes a sidecar JSON with the lexicon
    as loaded, its declared version, the SHA-256 of the lexicon file itself,
    and the script version, so a reader can tell exactly what was matched
    against and can verify it against the copy deposited on OSF.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urlunparse
from urllib import robotparser

SCRIPT_VERSION = "1.1.0"

# --------------------------------------------------------------------------
# FROZEN LEXICON
# --------------------------------------------------------------------------
# The lexicon is NOT defined in this file. It lives in frozen_lexicon.json,
# which is the single authoritative copy: attached to the registration,
# mirrored in the Codebook sheet for coders, and read here at runtime.
#
# A second copy in this script would agree with the file until the day it did
# not, and a run would then match against a list no reader of the deposited
# lexicon could see. There is deliberately no built-in fallback: if the file
# is missing or malformed the run stops rather than proceeding on something
# else.
#
# Do not add terms. A term surfaced during the review that is absent from the
# file is a FINDING, recorded in nonlexicon_self_description and reported as a
# result — not added to the lexicon mid-collection. Patterns are surface
# variants of one canonical term; they absorb spelling and spacing differences
# and never broaden the concept.

DEFAULT_LEXICON_PATH = Path(__file__).resolve().parent / "frozen_lexicon.json"


def load_lexicon(path: Path) -> tuple[dict[str, list[str]], dict]:
    """Read the frozen lexicon file.

    Returns (canonical term -> list of patterns, provenance record). Every
    failure below is fatal: silently degrading to a partial or built-in
    lexicon is the exact failure this function exists to prevent.
    """
    try:
        raw = path.read_bytes()
    except OSError as exc:
        sys.exit(f"cannot read lexicon file {path}: {exc}")

    try:
        doc = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        sys.exit(f"lexicon file {path} is not valid JSON: {exc}")

    entries = doc.get("terms")
    if not isinstance(entries, list) or not entries:
        sys.exit(f"lexicon file {path} has no non-empty 'terms' list")

    lexicon: dict[str, list[str]] = {}
    for i, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            sys.exit(f"lexicon entry {i} in {path} is not an object")
        term = entry.get("term")
        patterns = entry.get("patterns")
        if not isinstance(term, str) or not term.strip():
            sys.exit(f"lexicon entry {i} in {path} has no usable 'term'")
        if not isinstance(patterns, list) or not patterns:
            sys.exit(f"lexicon term {term!r} has no non-empty 'patterns' list")
        if term in lexicon:
            sys.exit(f"lexicon term {term!r} appears more than once in {path}")
        for pat in patterns:
            if not isinstance(pat, str):
                sys.exit(f"lexicon term {term!r} has a non-string pattern")
            try:
                re.compile(pat)
            except re.error as exc:
                sys.exit(f"lexicon term {term!r}: pattern {pat!r} "
                         f"does not compile: {exc}")
        lexicon[term] = list(patterns)

    declared = doc.get("term_count")
    if isinstance(declared, int) and declared != len(lexicon):
        sys.exit(f"lexicon file {path} declares term_count {declared} "
                 f"but contains {len(lexicon)} terms")

    provenance = {
        "lexicon_file": str(path),
        "lexicon_version": doc.get("version", ""),
        "lexicon_term_count": len(lexicon),
        "lexicon_sha256": hashlib.sha256(raw).hexdigest(),
    }
    return lexicon, provenance


def compile_lexicon(lexicon: dict[str, list[str]]) -> dict:
    return {
        term: [re.compile(p, re.IGNORECASE) for p in pats]
        for term, pats in lexicon.items()
    }

# A page yielding less than this many characters of extracted text is treated
# as unread rather than as containing no lexicon term. JavaScript-rendered
# sites are the usual cause: the HTML arrives, the words do not.
MIN_TEXT_CHARS = 400

SNIPPET_PAD = 60          # characters of context kept either side of a match
MAX_SNIPPETS = 3          # snippets retained per record, for verification
USER_AGENT = (
    "TPG-research-crawler/1.0 (academic research; homepage text only; "
    "one request per organization)"
)


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------
def normalize_url(raw: str) -> str | None:
    """Return a fetchable http(s) URL, or None if the value is unusable."""
    if not raw:
        return None
    raw = raw.strip()
    if not raw or raw.lower() in {"na", "n/a", "none", "null", "-"}:
        return None
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw.lstrip("/")
    parts = urlparse(raw)
    if not parts.netloc:
        return None
    # Homepage only. The registration specifies the organization's own
    # homepage, so paths, queries and fragments are discarded rather than
    # quietly turning this into a site crawl.
    return urlunparse((parts.scheme, parts.netloc, "", "", "", ""))


def cache_path(cache_dir: Path, url: str) -> Path:
    return cache_dir / (hashlib.sha256(url.encode()).hexdigest()[:24] + ".json")


def robots_allows(url: str, cache: dict) -> bool:
    """Respect robots.txt. On any failure, proceed — absence of a robots file
    is not a prohibition, and we make one request per host."""
    host = urlparse(url).netloc
    if host in cache:
        rp = cache[host]
    else:
        rp = robotparser.RobotFileParser()
        rp.set_url(f"https://{host}/robots.txt")
        try:
            rp.read()
        except Exception:
            rp = None
        cache[host] = rp
    if rp is None:
        return True
    try:
        return rp.can_fetch(USER_AGENT, url)
    except Exception:
        return True


def extract_text(html: str) -> str:
    """Visible text from HTML. Uses BeautifulSoup when available and falls
    back to a regex strip, so the script runs without extra packages."""
    try:
        from bs4 import BeautifulSoup  # type: ignore
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg", "template"]):
            tag.decompose()
        text = soup.get_text(separator=" ")
    except ImportError:
        text = re.sub(
            r"<(script|style|noscript)\b.*?</\1>", " ", html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;?", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def fetch(url: str, cache_dir: Path, robots_cache: dict,
          delay: float, timeout: float) -> dict:
    """Fetch a homepage, using the on-disk cache when present."""
    cp = cache_path(cache_dir, url)
    if cp.exists():
        rec = json.loads(cp.read_text())
        rec["from_cache"] = True
        return rec

    rec = {
        "url_requested": url, "final_url": "", "http_status": "",
        "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "text": "", "error": "", "from_cache": False,
    }

    if not robots_allows(url, robots_cache):
        rec["error"] = "disallowed_by_robots"
        cp.write_text(json.dumps(rec))
        return rec

    try:
        import requests  # type: ignore
    except ImportError:
        sys.exit("requests is required: pip install requests beautifulsoup4 --break-system-packages")

    try:
        resp = requests.get(
            url, timeout=timeout, allow_redirects=True,
            headers={"User-Agent": USER_AGENT,
                     "Accept": "text/html,application/xhtml+xml"},
        )
        rec["http_status"] = resp.status_code
        rec["final_url"] = resp.url
        ctype = resp.headers.get("Content-Type", "")
        if resp.status_code != 200:
            rec["error"] = f"http_{resp.status_code}"
        elif "html" not in ctype.lower():
            rec["error"] = f"non_html_content_type:{ctype[:40]}"
        else:
            rec["text"] = extract_text(resp.text)
    except Exception as exc:
        rec["error"] = f"{type(exc).__name__}: {str(exc)[:120]}"

    cp.write_text(json.dumps(rec))
    time.sleep(delay)
    return rec


# --------------------------------------------------------------------------
# Matching
# --------------------------------------------------------------------------
def match_lexicon(text: str, compiled: dict) -> tuple[list[str], list[str]]:
    """Return (canonical terms matched, verifying snippets)."""
    hits, snippets = [], []
    for term, pats in compiled.items():
        for pat in pats:
            m = pat.search(text)
            if m:
                hits.append(term)
                if len(snippets) < MAX_SNIPPETS:
                    a = max(0, m.start() - SNIPPET_PAD)
                    b = min(len(text), m.end() + SNIPPET_PAD)
                    snippets.append(f"...{text[a:b].strip()}...")
                break
    return hits, snippets


def classify(rec: dict, compiled: dict) -> tuple[str, list[str], list[str], str]:
    """Return (proxy, terms, snippets, reason)."""
    if rec.get("error"):
        return "UNDETERMINED", [], [], rec["error"]
    text = rec.get("text", "")
    if len(text) < MIN_TEXT_CHARS:
        return ("UNDETERMINED", [], [],
                f"insufficient_text:{len(text)}chars "
                f"(likely JavaScript-rendered; determine by hand)")
    hits, snips = match_lexicon(text, compiled)
    return ("TRUE" if hits else "FALSE"), hits, snips, ""


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
OUT_COLUMNS = [
    "org_id", "name", "lexicon_proxy", "lexicon_proxy_terms",
    "lexicon_proxy_snippets", "lexicon_proxy_reason",
    "url_requested", "final_url", "http_status", "fetched_at",
    "text_chars", "text_sha256", "script_version",
]


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Compute the lexicon proxy (a sampling aid, NOT tier).")
    ap.add_argument("--in", dest="infile", help="input CSV of enumerated records")
    ap.add_argument("--out", dest="outfile", help="output CSV")
    ap.add_argument("--id-col", default="org_id")
    ap.add_argument("--url-col", default="website_url")
    ap.add_argument("--name-col", default="name")
    ap.add_argument("--cache-dir", default=".lexicon_cache")
    ap.add_argument("--delay", type=float, default=1.5,
                    help="seconds between live requests (default 1.5)")
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument("--limit", type=int, default=0, help="process only N rows")
    ap.add_argument("--retry-undetermined", action="store_true",
                    help="clear cached failures and re-fetch those records")
    ap.add_argument("--lexicon", default=str(DEFAULT_LEXICON_PATH),
                    help="path to frozen_lexicon.json "
                         "(default: alongside this script)")
    ap.add_argument("--print-lexicon", action="store_true",
                    help="print the frozen lexicon and patterns, then exit")
    args = ap.parse_args()

    lexicon, lex_provenance = load_lexicon(Path(args.lexicon))
    compiled = compile_lexicon(lexicon)

    if args.print_lexicon:
        print(f"{lex_provenance['lexicon_file']}  "
              f"version {lex_provenance['lexicon_version'] or '(unversioned)'}  "
              f"sha256 {lex_provenance['lexicon_sha256'][:16]}…  "
              f"{lex_provenance['lexicon_term_count']} terms\n")
        for term, pats in lexicon.items():
            print(f"{term}\n    " + "\n    ".join(pats))
        return

    if not args.infile or not args.outfile:
        ap.error("--in and --out are required")

    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(exist_ok=True)

    with open(args.infile, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if args.limit:
        rows = rows[: args.limit]

    for col in (args.id_col, args.url_col):
        if rows and col not in rows[0]:
            sys.exit(f"column {col!r} not in input; found: {list(rows[0])}")

    if args.retry_undetermined:
        cleared = 0
        for r in rows:
            url = normalize_url(r.get(args.url_col, ""))
            if not url:
                continue
            cp = cache_path(cache_dir, url)
            if cp.exists():
                cached = json.loads(cp.read_text())
                if cached.get("error") or len(cached.get("text", "")) < MIN_TEXT_CHARS:
                    cp.unlink()
                    cleared += 1
        print(f"cleared {cleared} cached failures for retry", file=sys.stderr)

    robots_cache: dict = {}
    counts = {"TRUE": 0, "FALSE": 0, "UNDETERMINED": 0}
    out_rows = []

    for i, r in enumerate(rows, 1):
        oid = r.get(args.id_col, "")
        name = r.get(args.name_col, "")
        url = normalize_url(r.get(args.url_col, ""))

        if url is None:
            proxy, terms, snips, reason = "UNDETERMINED", [], [], "no_usable_url"
            rec = {"url_requested": r.get(args.url_col, ""), "final_url": "",
                   "http_status": "", "fetched_at": "", "text": ""}
        else:
            rec = fetch(url, cache_dir, robots_cache, args.delay, args.timeout)
            proxy, terms, snips, reason = classify(rec, compiled)

        counts[proxy] += 1
        text = rec.get("text", "")
        out_rows.append({
            "org_id": oid,
            "name": name,
            "lexicon_proxy": proxy,
            "lexicon_proxy_terms": "; ".join(terms),
            "lexicon_proxy_snippets": " || ".join(snips),
            "lexicon_proxy_reason": reason,
            "url_requested": rec.get("url_requested", ""),
            "final_url": rec.get("final_url", ""),
            "http_status": rec.get("http_status", ""),
            "fetched_at": rec.get("fetched_at", ""),
            "text_chars": len(text),
            "text_sha256": hashlib.sha256(text.encode()).hexdigest() if text else "",
            "script_version": SCRIPT_VERSION,
        })

        if i % 25 == 0:
            print(f"  {i}/{len(rows)} …", file=sys.stderr)

    with open(args.outfile, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=OUT_COLUMNS)
        w.writeheader()
        w.writerows(out_rows)

    sidecar = Path(args.outfile).with_suffix(".run.json")
    sidecar.write_text(json.dumps({
        "script_version": SCRIPT_VERSION,
        "run_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "input_file": args.infile,
        "records": len(rows),
        "counts": counts,
        "min_text_chars": MIN_TEXT_CHARS,
        **lex_provenance,
        "lexicon": lexicon,
    }, indent=2))

    n = len(rows) or 1
    print(f"\nwrote {args.outfile}  ({len(rows)} records)")
    for k in ("TRUE", "FALSE", "UNDETERMINED"):
        print(f"  {k:<13} {counts[k]:>5}  ({counts[k]/n:5.1%})")
    print(f"\nrun manifest: {sidecar}")
    if counts["UNDETERMINED"]:
        print(f"\n{counts['UNDETERMINED']} records need manual determination "
              f"before the queue is built.\n"
              f"  Filter on lexicon_proxy == UNDETERMINED and read "
              f"lexicon_proxy_reason.\n"
              f"  Re-run with --retry-undetermined first; transient failures "
              f"often clear.")
    print("\nREMINDER: lexicon_proxy is a sampling aid. It is not tier, and "
          "must not prefill the tier field.")


if __name__ == "__main__":
    main()
