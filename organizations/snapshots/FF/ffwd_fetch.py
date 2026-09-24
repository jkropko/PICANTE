#!/usr/bin/env python3
"""
ffwd_fetch.py — capture the Fast Forward accelerator portfolio.

    fetch     save every page of the portfolio-filtered directory
    parse     turn the saved HTML into one CSV

WHICH LISTING THIS CAPTURES, AND WHY IT MATTERS
    Fast Forward publishes TWO listings from the same directory, and the wrong
    one is seventeen times larger than the right one.

        https://www.ffwd.org/directory                    1,759 results
        https://www.ffwd.org/directory?portfolio=true       102 results

    The register's frame is the ACCELERATOR PORTFOLIO — the ~100 organizations
    Fast Forward selected and ran through its accelerator. The full directory
    is "every tech nonprofit that we know about", and organizations enter it by
    submitting a form.

    That difference is not just size. The register types this frame's admission
    mechanism as SELECTION, and the analysis holds admission mechanism as a
    confound it must not ignore. The open directory is self-declaration.
    Capturing it would silently change what Block C is sampling and would
    corrupt a recorded variable, not merely inflate a count.

    So the boundary is applied by the URL, at capture. `portfolio=true` is not
    a convenience here; it is the frame definition.

THE GEOGRAPHY FIELD IS NOT C2, AND MUST NOT BE USED AS IT
    Each record carries "Regions". Those are the geographies the organization's
    WORK SERVES, not where it is based:

        Bayes Impact            France
        Adalat AI               Ghana, India
        Black Sisters in STEM   Africa, Belgium, Canada, Germany, U.S.
        AccesSOS                U.S.

    Black Sisters in STEM is US-based with international reach; Adalat AI works
    in Indian courts. Filtering the directory's Geographies control to "U.S."
    would drop US organizations working abroad AND admit foreign organizations
    working in the US — wrong in both directions.

    C2 asks about headquarters or principal operations and is a human
    determination made at O4 from the organization's own materials. This script
    captures the regions verbatim as data and applies NO location filter, which
    is the same position taken for CTFG's missing country field, the CFA
    location rule, and PIT-UN's regional hubs.

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

SCRIPT_VERSION = "1.0.0"
HERE = Path(__file__).resolve().parent

BASE = "https://www.ffwd.org/directory"
PORTFOLIO = {"portfolio": "true"}
UA = ("PICANTE/0.0 (https://github.com/jkropko/PICANTE; jkropko@virginia.edu) "
      "python-requests")

COUNT_RE = re.compile(r"([\d,]+)\s+results", re.I)

# Site chrome and social links, matched as HOSTS and never as substrings.
#
# Substring matching silently lost a portfolio member: "x.com" is a social
# domain, and muevetex.com.mx contains it — muevete + x.com + .mx. Any
# organization whose domain ends in "x" before ".com" would have vanished from
# the frame with no error and no gap in the count, because the page still had
# its other nine records.
CHROME_HOSTS = {
    "ffwd.org", "jobs.ffwd.org", "share.hsforms.com", "hsforms.com",
    "linkedin.com", "instagram.com", "youtube.com", "forbes.com",
    "twitter.com", "x.com", "bsky.app", "facebook.com", "medium.com",
}


def host_of(url: str) -> str:
    try:
        h = url.split("://", 1)[1].split("/", 1)[0]
    except IndexError:
        return ""
    return h.split("@")[-1].split(":")[0].strip().lower().rstrip(".")


def is_chrome(url: str) -> bool:
    """True for site navigation and social links, false for a member's own site.

    Compares the HOST, exactly or as a parent domain, so a skip entry can never
    match the middle of an unrelated organization's domain.
    """
    h = host_of(url)
    if not h:
        return True
    if h.startswith("www."):
        h = h[4:]
    return any(h == d or h.endswith("." + d) for d in CHROME_HOSTS)


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    return s


def page_params(n: int) -> dict:
    p = dict(PORTFOLIO)
    if n > 1:
        p["page"] = str(n)
    return p


def reported_count(html: str) -> int | None:
    m = COUNT_RE.search(BeautifulSoup(html, "html.parser").get_text(" ", strip=True))
    return int(m.group(1).replace(",", "")) if m else None


def record_links(html: str) -> list[tuple[str, str]]:
    """(organization name, its own website) for each record on the page.

    Records link OUT to the organization's own site — there are no detail
    pages on ffwd.org — so a record is recognised by an external link that is
    not site chrome.
    """
    soup = BeautifulSoup(html, "html.parser")
    out, seen = [], set()
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href.startswith("http"):
            continue
        if is_chrome(href):
            continue
        name = a.get_text(" ", strip=True)
        if not name or len(name) > 120:
            continue
        key = (name.lower(), href.rstrip("/"))
        if key in seen:
            continue
        seen.add(key)
        out.append((name, href))
    return out


def cmd_fetch(args) -> int:
    out = Path(args.out).resolve()
    (out / "pages").mkdir(parents=True, exist_ok=True)
    print(f"writing to {out}\n")
    s = session()

    r = s.get(BASE, params=page_params(1), timeout=45)
    r.raise_for_status()
    first = r.text
    (out / "pages" / "page_01.html").write_text(first, encoding="utf-8")
    total = reported_count(first)
    per_page = len(record_links(first))
    if not per_page:
        print("no records parsed from page 1 — the markup has changed; inspect the saved "
              "HTML before going further", file=sys.stderr)
        return 2
    pages = -(-total // per_page) if total else args.max_pages
    print(f"  {total} organizations in the portfolio, {per_page} per page -> {pages} pages")
    if total and total > 500:
        # 1,759 is the UNFILTERED directory. Landing there means portfolio=true
        # was not applied, and the frame would be the wrong listing entirely.
        print(f"\nSTOPPED: {total} results is the FULL directory, not the portfolio "
              f"(~102). The portfolio filter did not take effect. Check that the request "
              f"URL carries portfolio=true before re-running.", file=sys.stderr)
        return 4

    seen = set(record_links(first))
    for n in range(2, pages + 1):
        dest = out / "pages" / f"page_{n:02d}.html"
        if dest.exists() and not args.refetch:
            continue
        r = s.get(BASE, params=page_params(n), timeout=45)
        r.raise_for_status()
        recs = set(record_links(r.text))
        if recs and not (recs - seen):
            # Ford's directory silently returned page 1 for every request.
            print(f"\nSTOPPED at page {n}: it holds no record not already captured. The "
                  f"site has stopped advancing; continuing would write duplicates that look "
                  f"like a complete capture.", file=sys.stderr)
            return 4
        seen |= recs
        dest.write_text(r.text, encoding="utf-8")
        print(f"\r  page {n}/{pages}  ({len(seen)}/{total} organizations)", end="", flush=True)
        time.sleep(args.delay)

    print(f"\n\nsaved {pages} pages to {out / 'pages'}")
    print(f"{len(seen)} distinct organizations captured, {total} reported by the site")
    if total and len(seen) != total:
        print("WARNING: those differ. Note it in notes.txt before enumerating.")

    (out / "ffwd_capture_manifest.json").write_text(json.dumps({
        "script": "ffwd_fetch.py", "script_version": SCRIPT_VERSION,
        "captured_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "url": f"{BASE}?portfolio=true",
        "_boundary": "portfolio=true applied AT CAPTURE and is the frame definition, not a "
                     "convenience: the unfiltered directory holds 1,759 organizations that "
                     "enter by submitting a form (self-declaration), where this frame's "
                     "registered admission mechanism is selection.",
        "_no_location_filter": "The directory's Geographies control is beneficiary geography, "
                               "not headquarters. No location filter was applied; C2 is "
                               "determined at O4 from each organization's own materials.",
        "pages": pages, "per_page": per_page,
        "reported_total": total, "organizations_captured": len(seen),
    }, indent=2), encoding="utf-8")
    print(f"manifest: {out / 'ffwd_capture_manifest.json'}")
    return 0


FIELDS = ["name", "website_url", "description", "issue_areas", "regions",
          "technologies", "listing_text"]


def parse_page(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for name, href in record_links(html):
        # Each record's facets sit under headings in its own block; find the
        # anchor and walk up to the container that holds them.
        anchor = soup.find("a", href=href)
        block = anchor
        for _ in range(6):
            if block is None or block.parent is None:
                break
            block = block.parent
            txt = block.get_text(" ", strip=True)
            if "Issue Areas" in txt and "Technology" in txt:
                break
        text = block.get_text("\n", strip=True) if block else ""
        lines = [l.strip() for l in text.split("\n") if l.strip()]

        def section(label: str) -> list[str]:
            vals = []
            try:
                i = lines.index(label)
            except ValueError:
                return vals
            for l in lines[i + 1:]:
                if l in ("Issue Areas", "Regions", "Technology", "FFWD Portfolio"):
                    break
                vals.append(l)
            return vals

        issues = section("Issue Areas")
        regions = section("Regions")
        techs = section("Technology")
        # The description is whatever sits between the organization's name and
        # the first facet label. Positional rather than heuristic: an earlier
        # version took the first line over 60 characters and silently dropped a
        # 59-character description.
        STOP = {"FFWD Portfolio", "Issue Areas", "Regions", "Technology"}
        desc_lines = []
        try:
            i = lines.index(name)
        except ValueError:
            i = -1
        for l in lines[i + 1:]:
            if l in STOP:
                break
            desc_lines.append(l)
        desc = " ".join(desc_lines).strip()

        rows.append({
            "name": name,
            "website_url": href,
            "description": desc,
            "issue_areas": "; ".join(issues),
            "regions": "; ".join(regions),
            "technologies": "; ".join(techs),
            "listing_text": " | ".join(x for x in [
                desc,
                f"Issue areas: {'; '.join(issues)}" if issues else "",
                f"Regions (BENEFICIARY, not HQ): {'; '.join(regions)}" if regions else "",
                f"Technologies: {'; '.join(techs)}" if techs else "",
            ] if x),
        })
    return rows


def cmd_parse(args) -> int:
    out = Path(args.out).resolve()
    pages = sorted((out / "pages").glob("page_*.html"))
    if not pages:
        print(f"no pages in {out / 'pages'} — run `fetch` first", file=sys.stderr)
        return 2

    rows, seen = [], set()
    for p in pages:
        for r in parse_page(p.read_text(encoding="utf-8")):
            key = (r["name"].lower(), r["website_url"].rstrip("/"))
            if key in seen:
                continue
            seen.add(key)
            rows.append(r)

    rows.sort(key=lambda r: r["name"].lower())
    dest = out / "ffwd_portfolio.csv"
    with dest.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    (out / "primary.txt").write_text("ffwd_portfolio.csv\n", encoding="utf-8")

    no_desc = sum(1 for r in rows if not r["description"])
    us_only = sum(1 for r in rows if r["regions"].strip() == "U.S.")
    no_region = sum(1 for r in rows if not r["regions"])
    print(f"{len(rows)} organizations -> {dest}\n")
    print(f"  {len(rows) - no_desc} carry a description; {no_desc} do not")
    print(f"  {us_only} list U.S. as their ONLY region, {no_region} list none")
    print("\nThose region counts are NOT a C2 estimate. Regions are the geographies the work "
          "serves, not where the organization is based: an organization listing only 'U.S.' "
          "may be based elsewhere, and one listing several regions may be US-headquartered. "
          "C2 is determined at O4 from each organization's own materials.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--delay", type=float, default=1.5)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("fetch", help="save every page of the portfolio listing")
    p.add_argument("--out", default=str(HERE))
    p.add_argument("--max-pages", type=int, default=20, dest="max_pages")
    p.add_argument("--refetch", action="store_true")
    p.set_defaults(fn=cmd_fetch)

    p = sub.add_parser("parse", help="saved HTML -> one CSV")
    p.add_argument("--out", default=str(HERE))
    p.set_defaults(fn=cmd_parse)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
