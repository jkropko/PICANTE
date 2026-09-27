#!/usr/bin/env python3
"""
gorg_fetch.py — capture the four named Google.org cohorts.

    fetch     save each cohort's source page
    inspect   dump candidate records from a saved page, to confirm parsing
              before trusting it
    parse     produce one CSV across all cohorts, with a cohort column

THE FRAME IS FOUR NAMED COHORTS AND NOTHING ELSE
    Google.org runs no standing portfolio, so the register defines this frame
    as the union of four cohorts, named explicitly:

        2019 AI Impact Challenge
        2025 Google.org Accelerator: Generative AI
        2026 Impact Challenge: AI for Government Innovation
        2026 Impact Challenge: AI for Science

    Cohorts announced after the freeze date do not enter the frame regardless
    of when they are announced. Earlier or adjacent Google.org programmes do
    not enter it either.

TWO WAYS TO CAPTURE THE WRONG ORGANIZATIONS, BOTH GUARDED
    1. The AI for Science page carries six organizations under "Previously
       funded recipients". They belong to an EARLIER, separate fund — the
       inaugural AI for Science fund — not to the named 2026 cohort. This
       script extracts NO organizations from that page. Its recipient list was
       unpublished on the capture date, and the page is captured as dated
       evidence of that fact, not as a source of records.

    2. The Generative AI Accelerator ran twice: 21 organizations in 2024 and
       20 in 2025. The register names only the 2025 cohort. The cohort page
       lists the 2025 participants and merely mentions 2024 in prose, so
       capturing the page is correct — but a blog post about "the Generative
       AI Accelerator" may list the 2024 cohort, and those must not be added.

WHY EVERY COHORT HAS AN EXPECTED COUNT
    Each cohort's size is known from Google's own announcements. `parse`
    refuses a cohort whose record count does not match. Three of the four
    failures met so far in this project were silent — a page returning the
    wrong records, or none, while the output looked ordinary. A declared count
    turns that class of failure into an error.

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

SCRIPT_VERSION = "1.4.0"
HERE = Path(__file__).resolve().parent
UA = ("PICANTE/0.0 (https://github.com/jkropko/PICANTE; jkropko@virginia.edu) "
      "python-requests")

# Cohort names MUST match frames.json GORG.cohorts.allowed exactly: the
# enumerator rejects any row whose cohort is not in that list, and that
# rejection is what keeps out-of-frame organizations out of the pool.
COHORTS = {
    "ai2018": {
        "cohort": "2019 AI Impact Challenge",
        "url": "https://impactchallenge.withgoogle.com/ai2018",
        "expected": 20,
        "note": "Launched 2018, grantees announced May 2019. Google's own URL and page "
                "title say 2018; the register calls it the 2019 AI Impact Challenge. Same "
                "cohort. Still live despite its age, but the most likely of the four to "
                "disappear, so archive it.",
    },
    "genaiaccelerator": {
        "cohort": "2025 Google.org Accelerator: Generative AI",
        "url": "https://impactchallenge.withgoogle.com/genaiaccelerator",
        "expected": 20,
        "note": "The 2025 cohort. A 2024 cohort of 21 exists and is mentioned in prose on "
                "this page but not listed; it is NOT in the frame.",
    },
    "ai-government-innovation": {
        "cohort": "2026 Impact Challenge: AI for Government Innovation",
        "url": "https://www.google.org/impact-challenges/ai-government-innovation/",
        "expected": 15,
        "note": "Recipients announced 2026-09-15, selected from more than 2,600 proposals.",
    },
    "ai-science": {
        "cohort": "2026 Impact Challenge: AI for Science",
        "url": "https://www.google.org/impact-challenges/ai-science/",
        "expected": 0,
        "pending": True,
        "note": "PENDING. Applications closed 2026-05-01; no recipient list published as of "
                "the capture date. The page is captured as dated evidence of "
                "non-publication. Its 'Previously funded recipients' belong to the earlier "
                "inaugural AI for Science fund and are NOT this cohort; no organization is "
                "extracted from this page.",
    },
}

# Matched as HOSTS, never as substrings. A substring test for "x.com" once
# deleted a Mexican organization from the Fast Forward frame because its
# domain was muevetex.com.mx.
CHROME_HOSTS = {
    "google.com", "google.org", "blog.google", "ai.google", "edu.google.com",
    "grow.google", "sustainability.google", "crisisresponse.google",
    "withgoogle.com", "googletagmanager.com", "googleblog.com",
    "youtube.com", "facebook.com", "twitter.com", "x.com", "linkedin.com",
    "instagram.com", "policies.google.com", "support.google.com",
    "services.google.com", "submittable.com", "g.co", "goo.gle",
}

# Google owns the .google top-level domain outright, so any host under it is
# the funder's own property: research.google, deepmind.google, about.google,
# publicpolicy.google, crisisresilience.google. Listing them one by one would
# miss the next one.
GOOGLE_TLD = ".google"


def host_of(url: str) -> str:
    try:
        h = url.split("://", 1)[1].split("/", 1)[0]
    except IndexError:
        return ""
    h = h.split("@")[-1].split(":")[0].strip().lower().rstrip(".")
    return h[4:] if h.startswith("www.") else h


def is_chrome(url: str) -> bool:
    h = host_of(url)
    if not h:
        return True
    if h == GOOGLE_TLD.lstrip(".") or h.endswith(GOOGLE_TLD):
        return True
    return any(h == d or h.endswith("." + d) for d in CHROME_HOSTS)


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    return s


def cmd_fetch(args) -> int:
    out = Path(args.out).resolve()
    (out / "pages").mkdir(parents=True, exist_ok=True)
    print(f"writing to {out}\n")
    s = session()
    for key, c in COHORTS.items():
        dest = out / "pages" / f"{key}.html"
        if dest.exists() and not args.refetch:
            print(f"  {key:<26} already saved")
            continue
        r = s.get(c["url"], timeout=45)
        r.raise_for_status()
        dest.write_text(r.text, encoding="utf-8")
        flag = "  [PENDING — captured as evidence of non-publication]" if c.get("pending") else ""
        print(f"  {key:<26} saved{flag}")
        time.sleep(args.delay)
    print(f"\nsaved to {out / 'pages'}")
    return 0


def candidates(html: str) -> list[dict]:
    """Outbound links that look like a recipient's own site, with their text.

    Every one of these pages is a list of organizations, each linking out to
    its own site. Rather than guess at per-page class names — which has failed
    three times in this project — this takes every non-Google outbound link
    and the text of the block around it, then `inspect` lets a human confirm
    the result before `parse` is trusted.
    """
    soup = BeautifulSoup(html, "html.parser")
    seen, out = set(), []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href.startswith("http") or is_chrome(href):
            continue
        key = href.rstrip("/")
        if key in seen:
            continue
        seen.add(key)

        block, text = a, ""
        for _ in range(4):
            if block is None:
                break
            tx = block.get_text(" ", strip=True)
            if len(tx) > 40:
                text = tx
                break
            block = block.parent
        text = re.sub(r"\s+", " ", text or a.get_text(" ", strip=True)).strip()
        text = re.sub(r"\s*Learn more\s*$", "", text, flags=re.I)

        # Read the card's own elements rather than splitting a run-together
        # string. The 2019 cohort renders each grantee in Google's "glue" card
        # components — glue-label for the country, glue-headline for the name,
        # glue-body for the description — and an earlier version looked only
        # for h2-h5 headings, found none, fell back to a verb-list split, and
        # produced names like "American University of Beirut Millions of
        # people in the Middle East...". Names that long break deduplication
        # at O3, which is where cross-frame records are matched.
        name_hint = country_hint = desc_hint = ""
        if block is not None:
            el = block.select_one(".glue-headline")
            if el:
                name_hint = el.get_text(" ", strip=True)
            el = block.select_one(".glue-label")
            if el:
                country_hint = el.get_text(" ", strip=True)
            el = block.select_one(".glue-body")
            if el:
                desc_hint = el.get_text(" ", strip=True)
            if not name_hint:
                for h in block.find_all(["h2", "h3", "h4", "h5", "strong"]):
                    cand = h.get_text(" ", strip=True)
                    if 2 <= len(cand) <= 90:
                        name_hint = cand
                        break
        out.append({"url": href, "text": text, "name_hint": name_hint,
                    "country_hint": country_hint, "desc_hint": desc_hint})
    return out


FOCUS = ["Knowledge, Skills, & Learning", "Scientific Progress", "Stronger Communities",
         "Health", "Resilience", "Economy", "Economic Opportunity", "Education",
         "Environment", "Crisis Response", "Misinformation", "Empowerment"]
REGIONS = ["Americas", "Asia Pacific", "Europe, Middle East, & Africa", "Global"]


# A description opens with a verb phrase describing what the organization
# does. An earlier version also allowed any capitalised word to start the
# description, which truncated "SkillUp Coalition" to "SkillUp" — organization
# names routinely contain capitalised words (Coalition, Foundation, Institute,
# University, Health), so that rule cut names in half.
# The 2019 cohort page prefixes each grantee with its COUNTRY in capitals:
# "LEBANON American University of Beirut ...". That is the best C2 material in
# this frame — better than the other cohorts' regional groupings — so it is
# captured into its own column rather than stripped away.
#
# Matched against a list rather than by "leading capitals", because
# organization names are capitalised too: a generic rule would read TOJIL and
# CIV:LAB as countries.
COUNTRIES = [
    "UNITED STATES", "UNITED KINGDOM", "SOUTH AFRICA", "NEW ZEALAND",
    "SOUTH KOREA", "SAUDI ARABIA", "SRI LANKA", "COSTA RICA", "SIERRA LEONE",
    "LEBANON", "UGANDA", "COLOMBIA", "INDONESIA", "INDIA", "SWITZERLAND",
    "BRAZIL", "FRANCE", "AUSTRALIA", "NETHERLANDS", "GERMANY", "CANADA",
    "KENYA", "NIGERIA", "GHANA", "ETHIOPIA", "TANZANIA", "RWANDA", "SENEGAL",
    "MEXICO", "ARGENTINA", "CHILE", "PERU", "JAPAN", "CHINA", "SINGAPORE",
    "PAKISTAN", "BANGLADESH", "PHILIPPINES", "VIETNAM", "THAILAND", "NEPAL",
    "SPAIN", "ITALY", "PORTUGAL", "IRELAND", "BELGIUM", "AUSTRIA", "POLAND",
    "SWEDEN", "NORWAY", "DENMARK", "FINLAND", "ISRAEL", "JORDAN", "EGYPT",
    "MOROCCO", "TUNISIA", "TURKEY", "GREECE", "UKRAINE", "ROMANIA",
]
COUNTRY_RE = re.compile(r"^(" + "|".join(sorted(COUNTRIES, key=len, reverse=True)) + r")\s+")

DESC_START = re.compile(
    r"\b(?:Uses|Use|Provides|Provide|Enables|Enable|Improves|Improve|Advances|Advance|"
    r"Streamlines|Streamline|Automates|Automate|Creates|Create|Supports|Support|"
    r"Translates|Translate|Enhances|Enhance|Addresses|Addressing|Democratizes|"
    r"Democratize|Delivers|Deliver|Builds|Build|Helps|Help|Develops|Develop|Scales|"
    r"Scale|Reduces|Reduce|Expands|Expand|Empowers|Empower|Connects|Connect|In "
    r"partnership|Is |Will )")


def split_record(text: str, name_hint: str = "", country_hint: str = "",
                 desc_hint: str = "") -> tuple[str, str, str, str, str]:
    """(focus, region, country, name, description) from a card's text.

    `name_hint` is the card's own heading where the page provides one, and is
    trusted over any split of the flattened text.

    The flattened text repeats whatever the heading holds, and the labels may
    come in any order — heading, then country, then the heading again — so
    prefixes are stripped in a loop until nothing more matches, rather than
    once in a fixed order.
    """
    # Where the card states the fields outright, take them and stop guessing.
    if name_hint and desc_hint:
        return ("", "", country_hint.title() if country_hint else "",
                name_hint.strip(), desc_hint.strip())

    focus = region = country = ""
    if country_hint:
        country = country_hint.title()
    rest = text.strip()
    hint = COUNTRY_RE.sub("", name_hint).strip() if name_hint else ""

    changed = True
    while changed:
        changed = False
        for f in FOCUS:
            if not focus and rest.startswith(f):
                focus, rest, changed = f, rest[len(f):].strip(), True
        for r in REGIONS:
            if not region and rest.startswith(r):
                region, rest, changed = r, rest[len(r):].strip(), True
        m_c = COUNTRY_RE.match(rest)
        if not country and m_c:
            country, rest, changed = m_c.group(1).title(), rest[m_c.end():].strip(), True
        if hint and rest.lower().startswith(hint.lower()):
            rest, changed = rest[len(hint):].strip(), True

    if hint:
        return focus, region, country, hint, rest

    m = DESC_START.search(rest)
    if m and m.start() > 1:
        return focus, region, country, rest[:m.start()].strip(), rest[m.start():].strip()
    # No heading and no recognisable verb: keep the whole string as the name
    # rather than guessing a cut point. A wrong name is worse than a missing
    # description.
    return focus, region, country, rest.strip(), ""


FIELDS = ["name", "website_url", "cohort", "focus_area", "region", "country",
          "description", "listing_text"]


def cmd_inspect(args) -> int:
    out = Path(args.out).resolve()
    key = args.cohort
    if key not in COHORTS:
        print(f"unknown cohort {key}; known: {', '.join(COHORTS)}", file=sys.stderr)
        return 2
    p = out / "pages" / f"{key}.html"
    if not p.exists():
        print(f"{p} not saved — run `fetch` first", file=sys.stderr)
        return 2
    cands = candidates(p.read_text(encoding="utf-8"))
    exp = COHORTS[key]["expected"]
    print(f"{key}: {len(cands)} outbound links found, {exp} expected\n")
    kept = 0
    for c in cands:
        focus, region, country, name, desc = split_record(c["text"], c.get("name_hint", ""), c.get("country_hint", ""), c.get("desc_hint", ""))
        if not name:
            print(f"  [DROPPED: no name] {'':<26} {c['url'][:44]}")
            continue
        kept += 1
        print(f"  {name[:44]:<44} {c['url'][:44]}")
        if args.verbose:
            print(f"      focus={focus!r} region={region!r} country={country!r}")
            print(f"      desc={desc[:100]!r}")
    print(f"\n  {kept} with a name, {len(cands) - kept} dropped for having none")
    return 0


def cmd_parse(args) -> int:
    out = Path(args.out).resolve()
    rows, problems = [], []

    for key, c in COHORTS.items():
        p = out / "pages" / f"{key}.html"
        if not p.exists():
            problems.append(f"{key}: page not saved — run `fetch`")
            continue

        if c.get("pending"):
            # Deliberately extracts nothing. The page's "Previously funded
            # recipients" belong to an earlier fund, and admitting them would
            # silently widen the frame beyond its registered definition.
            print(f"  {c['cohort']}")
            print(f"    PENDING — no recipient list published; 0 records extracted by "
                  f"design. The page is captured as dated evidence of non-publication.")
            continue

        cands = candidates(p.read_text(encoding="utf-8"))
        named_n = sum(1 for cd in cands if split_record(cd["text"], cd.get("name_hint", ""), cd.get("country_hint", ""), cd.get("desc_hint", ""))[3])
        got, exp = named_n, c["expected"]
        if got != exp:
            problems.append(
                f"{key}: parsed {got} organizations, expected {exp}. Run "
                f"`inspect --cohort {key} --verbose` and look at what was and was not "
                f"picked up before trusting this."
            )
            print(f"  {c['cohort']}\n    {got} parsed, {exp} expected — MISMATCH")
            continue

        named = []
        for cand in cands:
            focus, region, country, name, desc = split_record(cand["text"], cand.get("name_hint", ""), cand.get("country_hint", ""), cand.get("desc_hint", ""))
            if not name:
                # A link with no accompanying text is page furniture — a
                # partner logo or a collaborator credit — not a recipient.
                continue
            named.append((focus, region, country, name, desc, cand["url"]))

        for focus, region, country, name, desc, url in named:
            rows.append({
                "name": name,
                "website_url": url,
                "cohort": c["cohort"],
                "focus_area": focus,
                "region": region,
                "country": country,
                "description": desc,
                "listing_text": " | ".join(x for x in [
                    desc,
                    f"Focus area: {focus}" if focus else "",
                    f"Region (as the cohort page reports it, NOT headquarters): {region}"
                    if region else "",
                    f"Country (as the cohort page reports it): {country}" if country else "",
                ] if x),
            })
        print(f"  {c['cohort']}\n    {got} organizations")

    if problems:
        print("\nREFUSED — nothing written:\n", file=sys.stderr)
        for p_ in problems:
            print(f"  {p_}\n", file=sys.stderr)
        return 4

    dest = out / "gorg_cohorts.csv"
    with dest.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    (out / "primary.txt").write_text("gorg_cohorts.csv\n", encoding="utf-8")

    (out / "gorg_capture_manifest.json").write_text(json.dumps({
        "script": "gorg_fetch.py", "script_version": SCRIPT_VERSION,
        "captured_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "cohorts": {k: {"cohort": c["cohort"], "url": c["url"],
                        "expected": c["expected"], "pending": bool(c.get("pending")),
                        "note": c["note"]} for k, c in COHORTS.items()},
        "organizations": len(rows),
        "_frame": "The union of four NAMED cohorts. Cohorts announced after the freeze date "
                  "do not enter the frame regardless of when they are announced.",
        "_pending": "2026 Impact Challenge: AI for Science had published no recipient list "
                    "on the capture date. Record it as pending, enumerate it if and when its "
                    "list publishes, recording THAT date separately from the freeze date, "
                    "and report it as unenumerated if it never publishes.",
        "_not_captured": "The six organizations under 'Previously funded recipients' on the "
                         "AI for Science page belong to the earlier inaugural AI for Science "
                         "fund and are not one of the four named cohorts. No record was "
                         "extracted from that page.",
    }, indent=2), encoding="utf-8")

    print(f"\n{len(rows)} organizations across {len(set(r['cohort'] for r in rows))} "
          f"published cohorts -> {dest}")
    print(f"primary.txt written naming gorg_cohorts.csv")
    print("\nThe region field is the cohort page's own grouping, not headquarters. C2 is "
          "determined at O4 from each organization's own materials. Expect the heaviest C2 "
          "attrition in the register: these are global open calls.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--delay", type=float, default=1.5)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("fetch", help="save each cohort's source page")
    p.add_argument("--out", default=str(HERE))
    p.add_argument("--refetch", action="store_true")
    p.set_defaults(fn=cmd_fetch)

    p = sub.add_parser("inspect", help="dump candidate records from one saved page")
    p.add_argument("--out", default=str(HERE))
    p.add_argument("--cohort", required=True, help=", ".join(COHORTS))
    p.add_argument("--verbose", action="store_true")
    p.set_defaults(fn=cmd_inspect)

    p = sub.add_parser("parse", help="saved pages -> one CSV")
    p.add_argument("--out", default=str(HERE))
    p.set_defaults(fn=cmd_parse)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
