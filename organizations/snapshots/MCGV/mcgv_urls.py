#!/usr/bin/env python3
"""
mcgv_urls.py — recover grantee websites, which the CSV does not carry.

    fetch     save the 89 listing pages
    join      extract each grantee's linked URL and write it beside the CSV

WHY THIS EXISTS
    The "Download as CSV file" export gives Grantee, Fiscal Sponsor, Grant,
    Amount, Focus Area, Location and Date — and no URL. The rendered listing
    pages do carry a link on every grantee name.

    website_url does two jobs downstream, and a blank breaks both. It is where
    C1 and C2 start at O4, on the largest frame in the register. And at O5 the
    lexicon proxy FETCHES website_url and pattern-matches the frozen lexicon
    against the page; with nothing to fetch the proxy returns undetermined and
    every record must be resolved by hand before the coding queue can be built.

THE TWO LINK SHAPES, AND THE TRAP IN THE FIRST
    McGovern links grantee names two ways:

        https://www.mcgovern.org/grants/cworthy.org      <- domain in the path
        https://trekmedics.org                           <- direct

    The first is a McGovern page ABOUT the grantee, not the grantee's own site,
    but it encodes the grantee's domain as the last path segment. Recording it
    as-is would file mcgovern.org as the organization's website — the same
    mistake that put pit-un.org into PIT-UN's website_url, with the same
    consequence at O5: the lexicon proxy would score the FUNDER's vocabulary
    instead of the grantee's, and file the record in the wrong stratum for a
    reason having nothing to do with how the organization describes itself.

    So a /grants/<domain> link has its domain extracted and rebuilt as a URL,
    and is recorded as reconstructed rather than as something the frame stated
    outright.

WHAT THIS DOES NOT DO
    Verify that a recovered URL resolves, or that it is the organization's
    current site. It reports what the frame linked to on the capture date. C1
    and C2 remain human determinations at O4 from the organization's own
    materials.

Needs `requests` and `beautifulsoup4`.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("needs requests and beautifulsoup4:  pip install requests beautifulsoup4")

SCRIPT_VERSION = "2.0.0"
HERE = Path(__file__).resolve().parent

BASE = "https://www.mcgovern.org/grants/"
PAGE_N = BASE + "page/{n}/"
UA = ("PICANTE/0.0 (https://github.com/jkropko/PICANTE; jkropko@virginia.edu) "
      "python-requests")

# Links that are the funder's own navigation, never a grantee's site. Matched
# as HOSTS, never as substrings: a substring test for "x.com" once deleted a
# Mexican organization from the Fast Forward frame because its domain was
# muevetex.com.mx.
CHROME_HOSTS = {
    "mcgovern.org", "learn.mcgovern.org", "gg.mcgovern.org",
    "medium.com", "twitter.com", "x.com", "linkedin.com", "facebook.com",
    "youtube.com", "instagram.com",
}

DOMAIN_RE = re.compile(r"^[a-z0-9][a-z0-9.\-]*\.[a-z]{2,12}(?:/.*)?$", re.I)


def host_of(url: str) -> str:
    try:
        h = url.split("://", 1)[1].split("/", 1)[0]
    except IndexError:
        return ""
    h = h.split("@")[-1].split(":")[0].strip().lower().rstrip(".")
    return h[4:] if h.startswith("www.") else h


def is_chrome(url: str) -> bool:
    h = host_of(url)
    return bool(h) and any(h == d or h.endswith("." + d) for d in CHROME_HOSTS)


def resolve(href: str) -> tuple[str, str]:
    """(grantee's own URL, how it was obtained). ('', reason) when none.

    McGovern writes this href two ways, and the first is a defect on their
    side that happens to be useful here:

        href="cworthy.org"            a BARE DOMAIN with no scheme
        href="https://trekmedics.org" a normal absolute URL

    A scheme-less href resolves relative to the current page, so a browser
    turns "cworthy.org" into mcgovern.org/grants/cworthy.org — a link that
    goes nowhere useful for a visitor. The grantee's actual domain is
    nonetheless sitting in the attribute, so it is read directly from the
    source and given a scheme.

    What is never recorded as the grantee's website is a mcgovern.org URL. It
    is the funder's own page, and at O5 the lexicon proxy fetches website_url
    and would score the FUNDER's vocabulary instead of the grantee's, filing
    the record in the wrong stratum for a reason unrelated to how the
    organization describes itself. Same mistake that put pit-un.org into
    PIT-UN's website_url.
    """
    href = (href or "").strip()
    if not href:
        return "", "no href on the grantee-website link"
    if href.startswith("//"):
        href = "https:" + href
    if href.startswith("http"):
        if is_chrome(href):
            return "", f"funder or social link ({host_of(href)})"
        return href, "absolute URL in the frame"
    if href.startswith(("mailto:", "tel:", "#", "javascript:")):
        return "", f"not a website link ({href[:24]})"
    if DOMAIN_RE.match(href):
        # Scheme-less: the site's own link is broken, the domain is not.
        return "https://" + href.lstrip("/"), "bare domain in a scheme-less href"
    return "", f"href is not a domain ({href[:40]})"


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    return s


def cmd_fetch(args) -> int:
    out = Path(args.out).resolve()
    (out / "pages").mkdir(parents=True, exist_ok=True)
    print(f"writing to {out}\n")
    s = session()
    for n in range(1, args.pages + 1):
        dest = out / "pages" / f"page_{n:03d}.html"
        if dest.exists() and not args.refetch:
            continue
        url = BASE if n == 1 else PAGE_N.format(n=n)
        r = s.get(url, timeout=45)
        r.raise_for_status()
        dest.write_text(r.text, encoding="utf-8")
        print(f"\r  page {n}/{args.pages}", end="", flush=True)
        time.sleep(args.delay)
    print(f"\n\nsaved {args.pages} pages to {out / 'pages'}")
    return 0


def extract(html: str) -> dict[str, tuple[str, str]]:
    """{grantee name: (url, how)} from one listing page.

    Driven by the page's own classes. Each grant is an <article> carrying
    grants-tease, with the name in h2.grantee-name and the link in
    a.grantee-website. An earlier version looked for a link on or near the
    heading and found six names across 89 pages, because the anchor is a
    separate empty element in a different column of the card.
    """
    soup = BeautifulSoup(html, "html.parser")
    found: dict[str, tuple[str, str]] = {}
    for art in soup.select("article.grants-tease, article.tease-grants"):
        h = art.select_one("h2.grantee-name") or art.find(["h2", "h3"])
        if not h:
            continue
        name = h.get_text(" ", strip=True)
        if not name:
            continue
        a = art.select_one("a.grantee-website")
        url, how = resolve(a.get("href") if a else "")
        if name not in found or (not found[name][0] and url):
            found[name] = (url, how)
    return found


def cmd_join(args) -> int:
    out = Path(args.out).resolve()
    pages = sorted((out / "pages").glob("page_*.html"))
    if not pages:
        print(f"no pages in {out / 'pages'} — run `fetch` first", file=sys.stderr)
        return 2

    urls: dict[str, tuple[str, str]] = {}
    for p in pages:
        for name, val in extract(p.read_text(encoding="utf-8")).items():
            if name not in urls or (not urls[name][0] and val[0]):
                urls[name] = val
    print(f"{len(urls)} distinct grantee names linked across {len(pages)} pages")

    csv_path = Path(args.csv) if args.csv else None
    if csv_path is None:
        cands = [p for p in out.glob("*.csv") if p.name != "mcgv_grantee_urls.csv"]
        if len(cands) != 1:
            print(f"name the grants CSV with --csv (found {len(cands)} candidates in {out})",
                  file=sys.stderr)
            return 2
        csv_path = cands[0]

    with csv_path.open(newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    col = next((c for c in (rows[0] if rows else {}) if c.strip().lower() == "grantee"), None)
    if not col:
        print(f"no 'Grantee' column in {csv_path}", file=sys.stderr)
        return 2

    names = []
    seen = set()
    for r in rows:
        n = (r.get(col) or "").strip()
        if n and n not in seen:
            seen.add(n)
            names.append(n)

    matched = [n for n in names if urls.get(n, ("", ""))[0]]
    unmatched = [n for n in names if not urls.get(n, ("", ""))[0]]
    absent = [n for n in names if n not in urls]

    dest = out / "mcgv_grantee_urls.csv"
    with dest.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["Grantee", "website_url", "url_source"])
        w.writeheader()
        for n in names:
            url, how = urls.get(n, ("", "grantee name not found in the listing pages"))
            w.writerow({"Grantee": n, "website_url": url, "url_source": how})

    recon = sum(1 for n in names if urls.get(n, ("", ""))[1].startswith("bare domain"))
    direct = sum(1 for n in names if urls.get(n, ("", ""))[1].startswith("absolute"))
    print(f"\n{len(names)} distinct grantees in {csv_path.name}")
    print(f"  {len(matched)} with a website ({direct} absolute URLs, "
          f"{recon} bare domains given a scheme)")
    print(f"  {len(unmatched)} without — of which {len(absent)} were not found in the "
          f"listing pages at all")
    if unmatched:
        print("\n  first few without a website:")
        for n in unmatched[:8]:
            why = urls.get(n, ("", "name not found in the listing pages"))[1]
            print(f"    {n[:52]:<52} {why}")
    print(f"\nwritten: {dest}")
    print("Join on Grantee. A blank website_url means the frame offered none — leave it "
          "blank rather than guessing; C1 and C2 are determined at O4 from the "
          "organization's own materials.")

    (out / "mcgv_urls_manifest.json").write_text(json.dumps({
        "script": "mcgv_urls.py", "script_version": SCRIPT_VERSION,
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "listing_pages": len(pages),
        "grantees_in_csv": len(names),
        "with_website": len(matched),
        "absolute_url_in_frame": direct,
        "bare_domain_given_scheme": recon,
        "without_website": len(unmatched),
        "not_found_in_listings": len(absent),
        "_note": "McGovern writes many grantee links as a BARE DOMAIN with no scheme "
                 "(href=\"cworthy.org\"), which a browser resolves relative to the page and "
                 "turns into a dead mcgovern.org/grants/... link. That is a defect on their "
                 "site; the domain itself is correct and is read from the source and given a "
                 "scheme. A mcgovern.org URL is never recorded as a grantee website.",
    }, indent=2), encoding="utf-8")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--delay", type=float, default=1.5)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("fetch", help="save the listing pages")
    p.add_argument("--out", default=str(HERE))
    p.add_argument("--pages", type=int, default=89)
    p.add_argument("--refetch", action="store_true")
    p.set_defaults(fn=cmd_fetch)

    p = sub.add_parser("join", help="extract URLs and write them beside the CSV")
    p.add_argument("--out", default=str(HERE))
    p.add_argument("--csv", default=None, help="the downloaded grants CSV")
    p.set_defaults(fn=cmd_join)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
