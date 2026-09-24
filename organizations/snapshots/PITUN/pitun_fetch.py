#!/usr/bin/env python3
"""
pitun_fetch.py — capture the PIT-UN member directory, including entity pages.

    fetch     save the directory pages, then every member's entity page
    parse     turn the saved HTML into one CSV, plus a capture summary

WHY THE ENTITY PAGES ARE NOT OPTIONAL
    PIT-UN lists universities, so Rule 1 applies to every record: it resolves
    to the unit the FRAME ITSELF NAMES, and the parent institution does not
    enter the sample. The directory listing names no unit — it gives a
    university name, a link, and a regional hub, nothing more. Capturing only
    the three directory pages would send every record to O3 with nothing for
    Rule 1 to resolve against, and the whole of Block A would log as
    unit_unresolved.

    The entity pages carry what the rule needs: a Designee with their stated
    Positions, often a Co-Designee with theirs, and a Website field that
    frequently gives a PIT-specific address alongside the university's. For
    Arizona State, for instance, the positions name the School for the Future
    of Innovation in Society and the Julie Ann Wrigley Global Futures
    Laboratory, and the website field gives pit.asu.edu next to asu.edu.

    Those fields ARE the frame's naming of a unit. They are captured verbatim
    into listing_text, and a human resolves them at O3.

WHAT THIS SCRIPT DOES NOT DO
    Resolve the unit. It captures what the frame says; Rule 1 is a human
    judgment made at O3 against exactly this text and nothing else. A coder who
    knows of a qualifying unit the frame does not name may not add it — that
    case is logged as unit_known_not_surfaced and counted.

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
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("needs requests and beautifulsoup4:  pip install requests beautifulsoup4")

SCRIPT_VERSION = "2.0.0"

# Output defaults to the directory this script lives in, so it can sit inside
# snapshots/PITUN/ and be run from anywhere without writing a nested
# snapshots/PITUN/snapshots/PITUN tree.
HERE = Path(__file__).resolve().parent

DIRECTORY = "https://pit-un.org/directory/"
UA = ("PICANTE/0.0 (https://github.com/jkropko/PICANTE; jkropko@virginia.edu) "
      "python-requests")

# Fields as the entity page labels them. Order matters: each label's value is
# the text between it and the next label.
ENTITY_LABELS = ["Designee", "Positions", "Co-Designee", "Co-Positions",
                 "Website", "Region"]


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    return s


def get(s: requests.Session, url: str, timeout: int = 45) -> str:
    r = s.get(url, timeout=timeout)
    r.raise_for_status()
    return r.text


def entity_links(html: str) -> list[tuple[str, str]]:
    """(url, name as the DIRECTORY lists it).

    The directory-listed name is kept because it is the only name available
    when a member's entity page does not resolve. Without it those records
    come out named after whatever page the server returned instead.
    """
    soup = BeautifulSoup(html, "html.parser")
    seen, out = set(), []
    for a in soup.find_all("a", href=True):
        href = urljoin(DIRECTORY, a["href"])
        if "/entity/" not in href:
            continue
        href = href.split("?")[0].rstrip("/") + "/"
        if href in seen:
            continue
        label = a.get_text(" ", strip=True)
        if label.lower().startswith("read more"):
            continue  # the duplicate "Read More »: X" link on each card
        seen.add(href)
        out.append((href, label))
    return out


def page_url(n: int) -> str:
    return DIRECTORY if n == 1 else f"{DIRECTORY}?query-7-page={n}"


def cmd_fetch(args) -> int:
    out = Path(args.out).resolve()
    print(f"writing to {out}\n")
    (out / "directory").mkdir(parents=True, exist_ok=True)
    (out / "entities").mkdir(parents=True, exist_ok=True)
    s = session()

    all_links: list[tuple[str, str]] = []
    known: set = set()
    for n in range(1, args.pages + 1):
        url = page_url(n)
        html = get(s, url)
        (out / "directory" / f"page_{n}.html").write_text(html, encoding="utf-8")
        links = entity_links(html)
        new = [l for l in links if l[0] not in known]
        known.update(l[0] for l in new)
        if n > 1 and not new:
            print(f"  page {n}: no members not already seen — pagination is not advancing. "
                  f"Stopping rather than saving duplicates.")
            return 4
        all_links.extend(new)
        print(f"  directory page {n}: {len(links)} members ({len(new)} new)")
        time.sleep(args.delay)

    print(f"\n{len(all_links)} distinct members across {args.pages} directory pages\n")

    index = {}
    for i, (url, listed_name) in enumerate(all_links, start=1):
        slug = url.rstrip("/").rsplit("/", 1)[-1]
        dest = out / "entities" / f"{slug}.html"
        entry = {"listed_name": listed_name, "entity_url": url}
        if dest.exists() and not args.refetch:
            index[slug] = entry
            continue
        try:
            r = s.get(url, timeout=45)
            r.raise_for_status()
            dest.write_text(r.text, encoding="utf-8")
            # A member whose entity page does not resolve is served something
            # else — usually the directory. Recording the final URL is what
            # makes that visible instead of silently parsing the wrong page.
            entry["final_url"] = r.url
            entry["redirected"] = r.url.rstrip("/") != url.rstrip("/")
        except requests.RequestException as e:
            print(f"\n  FAILED {slug}: {e}")
            entry["fetch_error"] = str(e)
        index[slug] = entry
        print(f"\r  entity {i}/{len(all_links)}  {slug[:48]:<48}", end="", flush=True)
        time.sleep(args.delay)

    (out / "entity_index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    redirected = [k for k, v in index.items() if v.get("redirected")]
    if redirected:
        print(f"\n\n  {len(redirected)} entity page(s) redirected — the member is listed in "
              f"the directory but has no entity page of its own. Recorded in "
              f"entity_index.json and flagged per record at parse.")

    print(f"\n\nsaved to {out}/")
    (out / "fetch_manifest.json").write_text(json.dumps({
        "script": "pitun_fetch.py", "script_version": SCRIPT_VERSION,
        "captured_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "directory_url": DIRECTORY,
        "directory_pages": args.pages,
        "members_listed": len(all_links),
        "entity_pages_saved": len(list((out / "entities").glob("*.html"))),
        "_why_entity_pages": "PIT-UN lists universities. The directory names no unit; the "
                             "entity pages carry Designee, Positions, Co-Designee, "
                             "Co-Positions and Website, which is what Rule 1 resolves "
                             "against. Capturing the directory alone would make every record "
                             "unit_unresolved.",
    }, indent=2), encoding="utf-8")
    return 0


URL_RE = re.compile(r"https?://[^\s\"'<>]+")


def parse_entity(html: str) -> dict:
    """Pull the labelled fields out of an entity page.

    Driven by the page's own classes — pit__entity-info--row wraps a
    pit__entity-info--label and its value — rather than by walking text, which
    breaks whenever the markup shifts.

    Two traps in this source:

      The Website value is an anchor whose HREF is frequently an unsaved
      WordPress placeholder while the anchor TEXT holds the real URL:
          <a href=".../_wp_link_placeholder">https://direitosp.fgv.br/...</a>
      Reading the href and ignoring the text throws away a working address and
      records the member as having no website.

      A member listed in the directory may have no entity page. The server
      answers with the directory instead, which parses perfectly and yields a
      record named "PIT-UN Member Directory". Detected here by the absence of
      any entity-info row.
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select(".pit__entity-info--row")
    if not rows:
        return {"_is_entity_page": False}

    vals: dict[str, str] = {}
    links: dict[str, list[str]] = {}
    for row in rows:
        lab_el = row.select_one(".pit__entity-info--label")
        if not lab_el:
            continue
        label = lab_el.get_text(" ", strip=True)
        value_el = None
        for child in row.find_all("div", recursive=False):
            if child is not lab_el:
                value_el = child
                break
        if value_el is None:
            continue
        vals[label] = value_el.get_text(" ", strip=True)
        urls = []
        for a in value_el.find_all("a", href=True):
            # Prefer a URL in the anchor text; fall back to the href.
            m = URL_RE.search(a.get_text(" ", strip=True))
            cand = m.group(0) if m else a["href"]
            if cand.startswith("http") and cand not in urls:
                urls.append(cand)
        if not urls:
            urls = [u for u in URL_RE.findall(vals[label])]
        links[label] = urls

    h = soup.select_one(".pit__entity-info") or soup
    title = soup.find(["h1", "h2"])

    raw_sites = links.get("Website", [])
    sites, internal, broken = [], [], []
    for u in raw_sites:
        if "_wp_link_placeholder" in u:
            broken.append(u)
        elif "pit-un.org" in u:
            internal.append(u)
        else:
            sites.append(u)

    return {
        "_is_entity_page": True,
        "name": title.get_text(" ", strip=True) if title else "",
        "designee": vals.get("Designee", ""),
        "positions": vals.get("Positions", ""),
        "co_designee": vals.get("Co-Designee", ""),
        "co_positions": vals.get("Co-Positions", ""),
        "region": vals.get("Region", ""),
        "websites": "; ".join(sites),
        "pitun_internal_links": "; ".join(internal),
        "broken_links": "; ".join(broken),
        "designee_profiles": "; ".join(links.get("Designee", []) +
                                       links.get("Co-Designee", [])),
    }


FIELDS = ["name", "entity_url", "website_url", "all_websites", "region",
          "designee", "positions", "co_designee", "co_positions",
          "designee_profiles", "pitun_internal_links", "broken_links",
          "entity_page_missing", "listing_text", "international_flag"]


def cmd_parse(args) -> int:
    out = Path(args.out).resolve()
    pages = sorted((out / "entities").glob("*.html"))
    if not pages:
        print(f"no entity pages in {out / 'entities'} — run `fetch` first", file=sys.stderr)
        return 2

    idx = {}
    idx_path = out / "entity_index.json"
    if idx_path.exists():
        idx = json.loads(idx_path.read_text(encoding="utf-8"))

    rows, no_unit, intl, missing = [], 0, 0, 0
    for p in pages:
        d = parse_entity(p.read_text(encoding="utf-8"))
        meta = idx.get(p.stem, {})
        if not d.get("_is_entity_page"):
            # Listed in the directory, no entity page of its own. The record is
            # kept — it is a real member and dropping it would understate the
            # frame — with every field the entity page would have supplied left
            # empty, and the name taken from the directory listing.
            missing += 1
            rows.append({
                "name": meta.get("listed_name", "") or f"[UNRESOLVED: {p.stem}]",
                "entity_url": meta.get("entity_url", f"https://pit-un.org/entity/{p.stem}/"),
                "website_url": "", "all_websites": "", "region": "",
                "designee": "", "positions": "", "co_designee": "", "co_positions": "",
                "designee_profiles": "", "pitun_internal_links": "", "broken_links": "",
                "entity_page_missing": "TRUE",
                "listing_text": "[the member is listed in the directory but its entity page "
                                "does not resolve; the frame names no designee, position, "
                                "unit or website for it]",
                "international_flag": "",
            })
            no_unit += 1
            continue

        sites = [s for s in d["websites"].split("; ") if s]
        listing = " | ".join(x for x in [
            f"Designee: {d['designee']}" if d["designee"] else "",
            f"Positions: {d['positions']}" if d["positions"] else "",
            f"Co-Designee: {d['co_designee']}" if d["co_designee"] else "",
            f"Co-Positions: {d['co_positions']}" if d["co_positions"] else "",
            f"Websites: {d['websites']}" if d["websites"] else "",
            f"[frame gives only a pit-un.org link: {d['pitun_internal_links']}]"
            if d["pitun_internal_links"] and not d["websites"] else "",
            "[frame's website field is an unsaved editor placeholder]"
            if d["broken_links"] and not d["websites"] else "",
        ] if x)
        if not (d["positions"] or d["co_positions"]):
            no_unit += 1
        is_intl = "international" in d["region"].lower()
        if is_intl:
            intl += 1
        rows.append({
            "name": d["name"] or meta.get("listed_name", ""),
            "entity_url": meta.get("entity_url", f"https://pit-un.org/entity/{p.stem}/"),
            "website_url": sites[0] if sites else "",
            "all_websites": d["websites"],
            "region": d["region"],
            "designee": d["designee"],
            "positions": d["positions"],
            "co_designee": d["co_designee"],
            "co_positions": d["co_positions"],
            "designee_profiles": d["designee_profiles"],
            "pitun_internal_links": d["pitun_internal_links"],
            "broken_links": d["broken_links"],
            "entity_page_missing": "",
            "listing_text": listing,
            "international_flag": "TRUE" if is_intl else "",
        })

    rows.sort(key=lambda r: r["name"].lower())
    dest = out / "pitun_members.csv"
    with dest.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    (out / "primary.txt").write_text("pitun_members.csv\n", encoding="utf-8")

    print(f"{len(rows)} members -> {dest}")
    print(f"primary.txt written: capture_log.py finds both pitun_members.csv and "
          f"fetch_manifest.json in this directory and would otherwise refuse to guess "
          f"which is the frame of record.\n")
    if missing:
        print(f"  {missing} member(s) have NO ENTITY PAGE — listed in the directory but the "
              f"page does not resolve, so the frame names no designee, unit or website for "
              f"them. Kept with entity_page_missing = TRUE and every such field empty. They "
              f"will log as unit_unresolved at O3; that is the frame's gap, not a coding "
              f"failure.")
    print(f"  {len(rows) - no_unit} name at least one unit in Positions or Co-Positions")
    print(f"  {no_unit} name NO unit — these will log as unit_unresolved at O3 unless the "
          f"website field resolves them")
    print(f"  {intl} carry the International region — C2 candidates, but C2 is a human "
          f"determination at O4 from the organization's own materials, not from this field")
    no_site = sum(1 for r in rows if not r["website_url"])
    internal_n = sum(1 for r in rows if r["pitun_internal_links"])
    broken_n = sum(1 for r in rows if r["broken_links"])
    if no_site:
        print(f"  {no_site} have NO usable website from the frame — website_url is blank "
              f"rather than wrong ({internal_n} gave only a pit-un.org link, {broken_n} an "
              f"unsaved editor placeholder). Find the site from the organization's own "
              f"materials at O4; do not point the O5 lexicon proxy at a blank or a "
              f"pit-un.org page.")
    multi = sum(1 for r in rows if ";" in r["all_websites"])
    print(f"  {multi} give more than one website, often a PIT-specific address alongside the "
          f"university's — frequently the clearest unit the frame names")
    print("\nlisting_text carries every unit the frame names, verbatim. Rule 1 is resolved "
          "by a human at O3 against that text and nothing else.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--delay", type=float, default=1.5)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("fetch", help="save directory pages and every entity page")
    p.add_argument("--out", default=str(HERE),
                   help="defaults to this script's own directory")
    p.add_argument("--pages", type=int, default=3)
    p.add_argument("--refetch", action="store_true")
    p.set_defaults(fn=cmd_fetch)

    p = sub.add_parser("parse", help="saved HTML -> one CSV")
    p.add_argument("--out", default=str(HERE),
                   help="defaults to this script's own directory")
    p.set_defaults(fn=cmd_parse)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
