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

    Responses are cached on disk, so re-running is cheap and does not re-hit
    sites. Delete the cache directory to force a clean re-fetch.

REPRODUCIBILITY
    Every row records the URL requested, the final URL after redirects, the
    HTTP status, the fetch timestamp (UTC), the length of extracted text, and
    the SHA-256 of that text. The run writes a sidecar JSON with the lexicon,
    the pattern set, and the script version, so a reader can tell exactly what
    was matched against.
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

SCRIPT_VERSION = "1.0.0"

# --------------------------------------------------------------------------
# FROZEN LEXICON
# --------------------------------------------------------------------------
# These terms are frozen at registration and must match the codebook exactly.
# Do not add terms here. A term surfaced during the review that is absent from
# this list is a FINDING, recorded in nonlexicon_self_description and reported
# as a result — not added to the lexicon mid-collection.
#
# Each canonical term maps to the surface variants counted as that term.
# Variants exist only to absorb spelling and spacing differences, never to
# broaden the concept.

LEXICON: dict[str, list[str]] = {
    "civic tech": [
        r"civic[\s\-]tech\b",
        r"civic[\s\-]technolog(?:y|ies|ist|ists)\b",
    ],
    "public interest technology": [
        r"public[\s\-]interest[\s\-]tech\b",
        r"public[\s\-]interest[\s\-]technolog(?:y|ies|ist|ists)\b",
    ],
    "tech for good": [
        r"tech(?:nology)?[\s\-]for[\s\-]good\b",
    ],
    "data for good": [
        r"data[\s\-]for[\s\-]good\b",
    ],
    "data science / AI for social good": [
        r"data[\s\-]science[\s\-]for[\s\-]social[\s\-]good\b",
        r"\bAI[\s\-]for[\s\-]social[\s\-]good\b",
        r"artificial[\s\-]intelligence[\s\-]for[\s\-]social[\s\-]good\b",
        r"\bAI[\s\-]for[\s\-]good\b",
    ],
    "e-government": [
        r"\be[\s\-]?government\b",
    ],
    "e-democracy": [
        r"\be[\s\-]?democracy\b",
    ],
    "govtech": [
        r"\bgov[\s\-]?tech\b",
    ],
    "open government": [
        r"open[\s\-]government\b",
    ],
    "digital civics": [
        r"digital[\s\-]civics\b",
    ],
    "crowd-civic systems": [
        r"crowd[\s\-]civic[\s\-]systems?\b",
    ],
    "data activism": [
        r"data[\s\-]activis(?:m|t|ts)\b",
    ],
}

COMPILED = {
    term: [re.compile(p, re.IGNORECASE) for p in pats]
    for term, pats in LEXICON.items()
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
def match_lexicon(text: str) -> tuple[list[str], list[str]]:
    """Return (canonical terms matched, verifying snippets)."""
    hits, snippets = [], []
    for term, pats in COMPILED.items():
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


def classify(rec: dict) -> tuple[str, list[str], list[str], str]:
    """Return (proxy, terms, snippets, reason)."""
    if rec.get("error"):
        return "UNDETERMINED", [], [], rec["error"]
    text = rec.get("text", "")
    if len(text) < MIN_TEXT_CHARS:
        return ("UNDETERMINED", [], [],
                f"insufficient_text:{len(text)}chars "
                f"(likely JavaScript-rendered; determine by hand)")
    hits, snips = match_lexicon(text)
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
    ap.add_argument("--print-lexicon", action="store_true",
                    help="print the frozen lexicon and patterns, then exit")
    args = ap.parse_args()

    if args.print_lexicon:
        for term, pats in LEXICON.items():
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
            proxy, terms, snips, reason = classify(rec)

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
        "lexicon": LEXICON,
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
