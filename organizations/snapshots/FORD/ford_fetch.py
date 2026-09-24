#!/usr/bin/env python3
"""
ford_fetch.py — capture the Ford Foundation grants database via its JSON API.

    fetch-html  page the rendered documents and pull the JSON out of each;
                the route that works when the API is gated
    probe     one request: confirm the endpoint answers and find the largest
              per_page it honours
    terms     list the program and subject slugs, for writing the boundary
    fetch     page through the whole database, saving each raw response
    flatten   turn the raw pages into one CSV, plus an inventory of the
              program and subject values present

WHY CAPTURE THE WHOLE DATABASE
    The register describes FORD as the topic-filtered view, but the site
    exposes no working topic filter and the program appears only as a field on
    each grant. Capturing everything and applying the program boundary at
    enumeration puts the narrowing in frames.json, where it is deterministic,
    inspectable and reproducible, instead of in a UI state nobody can
    reconstruct later. It also makes the boundary's cost measurable: the
    inventory shows how many technology-subject grants sit under a program
    label that the boundary would exclude.

    4,319 grants is small. There is no reason to filter at capture.

THE PRE-2018 PROBLEM, WHICH THE INVENTORY IS THERE TO SIZE
    Ford's program structure dates from 2018. Grants made before then that did
    not map onto it carry the label "Other Grantmaking" instead, whatever they
    funded. So `program = Technology and Society` will miss Ford's earlier
    technology grantmaking, which is exactly the historical depth this frame
    was meant to supply. `subjects[] = technology` is the likelier route to
    those records. Run `flatten` and read the inventory BEFORE fixing the
    boundary in frames.json.

IDENTIFYING THE CLIENT
    Requests are sent with a User-Agent naming the project, its repository and
    a contact address, so Ford can see who is fetching and get in touch rather
    than having to guess at anonymous traffic. With a one-second delay over 44
    pages this is a trivial load, but the courtesy is the point.

    One caveat that will otherwise cost an hour: Cloudflare binds a
    cf_clearance cookie to the User-Agent that earned it. A cookie copied from
    a browser and replayed under a different UA can be rejected. If the run
    403s on a cookie that plainly works in the browser, pass --browser-ua.

ON THE VERIFICATION GATE
    The database sits behind Cloudflare Turnstile. An unauthenticated request
    returns 401 rest_authorization_required, which reads like a login wall and
    is not one: /ford/v1/turnstile-verify sets a clearance cookie once a human
    passes the check. There is no account to create.

    Open the database in a browser, pass the check, copy the whole Cookie
    request header from any XHR in the network tab, and pass it with --cookie.
    The cookie expires; a long run that starts failing partway just needs a
    fresh one, and `fetch` resumes from the pages already saved.

    If a response comes back as HTML, the script stops rather than saving a
    challenge page as data.

NO FILTER EXISTS AT THE API LEVEL
    The grants route accepts page, per_page (max 100), search, orderby, order,
    after, before, amount_min and amount_max — and nothing else. There is no
    program, subject or location parameter. Filtering at capture is therefore
    not available even in principle, which settles the question: capture all
    4,319 grants and apply the boundary in frames.json.

Needs `requests`.
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
except ImportError:  # noqa: BLE001
    sys.exit("ford_fetch.py needs requests:  pip install requests")

SCRIPT_VERSION = "1.0.0"
# DEFAULT ONLY — override with --endpoint. The page's own embedded payload
# names "https://www.fordfoundation.org/grant-api" as its api, while the
# ford/v1 namespace index lists /wp-json/ford/v1/grants as the collection
# route. Those need not be the same thing: WordPress sites routinely lock
# /wp-json to logged-in users while exposing one proxy route publicly, which
# is exactly what "rest_authorization_required" on wp-json alongside a working
# front end looks like. Read the real request out of the browser's network tab
# and pass it with --endpoint rather than trusting this default.
ENDPOINT = "https://www.fordfoundation.org/grant-api"
TERMS_ENDPOINT = "https://www.fordfoundation.org/wp-json/ford/v1/term-search"
MAX_PER_PAGE = 100  # the route declares this maximum; larger values are rejected
UA = (f"PICANTE/0.0 (https://github.com/jkropko/PICANTE; jkropko@virginia.edu) "
      f"python-requests:{requests.__version__}")

# Fallback only. cf_clearance cookies are bound to the User-Agent that earned
# them, so if the run 403s with a cookie that works in the browser, the UA
# mismatch is the first thing to suspect — see --browser-ua.
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:156.0) "
              "Gecko/20100101 Firefox/156.0")

# The grants database renders server-side: every page is a real URL whose HTML
# embeds the same JSON the API would return, inside <div class="grants-db">.
# This is the sturdier capture route, because it is the document the browser
# itself renders — no endpoint to guess, no nonce.
PAGE_1 = "https://www.fordfoundation.org/work/our-grants/awarded-grants/grants-database/"
PAGE_N = PAGE_1 + "page/{n}/"

# Matches the payload block inside the grants-db container.
_JSON_BLOCK = re.compile(
    r'<div[^>]*class="[^"]*grants-db[^"]*"[^>]*>\s*'
    r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)
_GATE_MARK = "ford-ts-gate"


class GateError(RuntimeError):
    pass


def make_session(cookie: str | None, browser_ua: bool = False,
                 nonce: str | None = None,
                 extra_headers: list[str] | None = None,
                 ua: str | None = None,
                 document_mode: bool = False) -> requests.Session:
    """One session for the whole run.

    A session matters here beyond tidiness: the Turnstile clearance lives in a
    cookie, and the server may refresh or add cookies as the run proceeds. A
    session carries those forward; independent requests would discard them and
    the run would fail partway through for no visible reason.
    """
    s = requests.Session()
    s.headers.update({
        "User-Agent": ua or (BROWSER_UA if browser_ua else UA),
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.fordfoundation.org/work/our-grants/awarded-grants/grants-database/",
    })
    if document_mode:
        # A clearance cookie is issued against a particular navigation
        # fingerprint. Sending an XHR-shaped request with it invites a
        # challenge that has nothing to do with whether the cookie is valid.
        s.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
        })
        s.headers.pop("Referer", None)
    if nonce:
        # WordPress REST routes called from a page usually require this, and its
        # absence is a common cause of a 401 that a valid cookie does not fix.
        s.headers["X-WP-Nonce"] = nonce
    for h in (extra_headers or []):
        if ":" in h:
            k, v = h.split(":", 1)
            s.headers[k.strip()] = v.strip()
    if cookie:
        # A Cookie header copied wholesale from the browser's network tab.
        for part in cookie.split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                s.cookies.set(k.strip(), v.strip())
    return s


def request(params: dict, session: requests.Session, timeout: int = 60,
            endpoint: str | None = None) -> dict:
    endpoint = endpoint or ENDPOINT
    try:
        r = session.get(endpoint, params=params, timeout=timeout)
    except requests.RequestException as e:
        raise GateError(f"request failed: {type(e).__name__}: {e}") from e

    if r.status_code in (401, 403):
        raise GateError(
            f"HTTP {r.status_code} at {endpoint}\n\n"
            "TWO DIFFERENT CAUSES LOOK LIKE THIS. Check the endpoint before blaming the "
            "cookie.\n\n"
            "1. WRONG ENDPOINT. If /wp-json/... returns rest_authorization_required while "
            "the database works in your browser, that route is locked to logged-in users and "
            "is simply not the one the page calls. Open the database, pass the check, open "
            "the network tab filtered to Fetch/XHR, click 'Load More', and read off the URL, "
            "its query parameters, and whether an X-WP-Nonce header is sent. Then pass "
            "--endpoint (and --nonce if present). No amount of cookie-fiddling fixes a route "
            "that was never public.\n\n"
            "2. THE TURNSTILE GATE. The route /ford/v1/turnstile-verify sets the clearance; there "
            "is no account to create. Copy the whole Cookie request "
            "header from any XHR and pass it with --cookie \"...\". The clearance expires, "
            "so if a long run starts failing partway, re-copy it and re-run — saved pages "
            "are kept and the fetch resumes. Cloudflare also binds cf_clearance to the "
            "User-Agent that earned it, so try --browser-ua.\n\n"
            f"URL: {r.url}"
        )
    if r.status_code != 200:
        raise GateError(f"HTTP {r.status_code} from the API. {r.url}")

    ctype = r.headers.get("Content-Type", "")
    if r.text.lstrip().startswith("<") or "text/html" in ctype:
        raise GateError(
            "the API returned HTML, not JSON — almost certainly the Turnstile challenge "
            "page.\n"
            "Pass the check in a browser and supply a fresh --cookie.\n"
            f"URL: {r.url}"
        )
    try:
        return r.json()
    except ValueError as e:
        raise GateError(f"response was neither HTML nor valid JSON: {e}") from e


def payload(d: dict) -> dict:
    """The page object, whether or not it is wrapped in `response`."""
    return d.get("response", d)


def cmd_probe(args) -> int:
    global ENDPOINT
    if args.endpoint:
        ENDPOINT = args.endpoint
    session = make_session(args.cookie, args.browser_ua, args.nonce, args.header, args.ua)
    print(f"endpoint: {ENDPOINT}\n")
    base = payload(request({"page": 1, "per_page": 10}, session))
    total = base.get("total_grants")
    print(f"  total_grants   {total}")
    print(f"  total_grantees {base.get('total_grantees')}")
    print(f"  year range     {base.get('min_year')} to {base.get('max_year')}")
    print(f"  per_page 10 -> {len(base.get('grants', []))} grants, "
          f"{base.get('total_pages')} pages")

    best = 10
    for n in (50, 100):
        try:
            p = payload(request({"page": 1, "per_page": n}, session))
            got = len(p.get("grants", []))
            print(f"  per_page {n:<4} -> {got} grants, {p.get('total_pages')} pages")
            if got > best:
                best = got
            if got < n:
                print("     (capped; larger values will not help)")
                break
        except GateError as e:
            print(f"  per_page {n:<4} -> failed: {e}")
            break
        time.sleep(args.delay)

    facets = base.get("facets")
    print(f"\n  facets in the payload: {facets if facets else 'none (they load separately)'}")
    attrs = (base if "attributes" not in base else base)["attributes"] \
        if "attributes" in base else {}
    if not attrs:
        attrs = request({"page": 1, "per_page": 1}, session).get("attributes", {})
    if attrs:
        labels = {k: v for k, v in attrs.items() if k.endswith("Label")}
        print("  facet labels the UI declares:")
        for k, v in sorted(labels.items()):
            print(f"      {k:<26} {v}")

    print(f"\nLargest usable per_page: {best}. "
          f"That is {-(-int(total or 0) // best)} pages for {total} grants.")
    print("\nIf a Program facet is offered, a filtered URL may work directly — the payload's "
          "location links use ?grant_location[]=<slug>, so ?program[]=<slug> is worth trying. "
          "Capturing everything and narrowing at enumeration is still the better route.")
    return 0


def cmd_fetch(args) -> int:
    global ENDPOINT
    if args.endpoint:
        ENDPOINT = args.endpoint
    session = make_session(args.cookie, args.browser_ua, args.nonce, args.header, args.ua)
    out = Path(args.out)
    (out / "raw").mkdir(parents=True, exist_ok=True)

    first = payload(request({"page": 1, "per_page": args.per_page}, session))
    total_pages = int(first.get("total_pages") or 0)
    total_grants = int(first.get("total_grants") or 0)
    if not total_pages:
        print("the API reported no pages; nothing to fetch", file=sys.stderr)
        return 2
    print(f"{total_grants} grants across {total_pages} pages at per_page={args.per_page}\n")

    collected = 0
    for page in range(1, total_pages + 1):
        dest = out / "raw" / f"page_{page:04d}.json"
        if dest.exists() and not args.refetch:
            collected += len(payload(json.loads(dest.read_text(encoding="utf-8")))
                             .get("grants", []))
            continue
        for attempt in range(1, args.retries + 1):
            try:
                d = request({"page": page, "per_page": args.per_page}, session)
                break
            except GateError as e:
                if attempt == args.retries:
                    print(f"\npage {page} failed after {attempt} attempts:\n  {e}",
                          file=sys.stderr)
                    print("Pages already saved are kept; re-run to resume.", file=sys.stderr)
                    return 3
                time.sleep(args.delay * attempt * 2)
        dest.write_text(json.dumps(d, indent=None), encoding="utf-8")
        n = len(payload(d).get("grants", []))
        collected += n
        print(f"\r  page {page}/{total_pages}  ({collected}/{total_grants} grants)",
              end="", flush=True)
        time.sleep(args.delay)

    print(f"\n\nsaved {total_pages} raw pages to {out / 'raw'}")
    if collected != total_grants:
        print(f"WARNING: collected {collected} grants but the API reported {total_grants}. "
              f"A mismatch usually means the database changed mid-capture. Re-run with "
              f"--refetch and note it in notes.txt.")
    manifest = {
        "script": "ford_fetch.py",
        "script_version": SCRIPT_VERSION,
        "captured_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "endpoint": ENDPOINT,
        "params": {"per_page": args.per_page, "order": first.get("order"),
                   "orderby": first.get("orderby"), "search": first.get("search", "")},
        "filters_applied": "NONE — full database captured; the program boundary is applied "
                           "at enumeration, per frames.json",
        "total_grants_reported": total_grants,
        "total_grantees_reported": first.get("total_grantees"),
        "grants_collected": collected,
        "total_pages": total_pages,
        "year_range": [first.get("min_year"), first.get("max_year")],
    }
    (out / "ford_api_manifest.json").write_text(json.dumps(manifest, indent=2),
                                                encoding="utf-8")
    print(f"manifest: {out / 'ford_api_manifest.json'}")
    return 0


def fetch_page_html(session: requests.Session, n: int, per_page: int | None,
                    mode: str = "path", timeout: int = 60) -> dict:
    """One rendered page; returns the JSON payload embedded in its HTML.

    Two pagination shapes exist and they do not compose. The path form,
    /page/N/, is what the document's own rel=next link uses. The query form,
    ?page=N, is what a per_page parameter appears to want. Mixing them —
    /page/N/?per_page=100 — silently returns page 1 every time, which looks
    like a successful capture and is not.
    """
    if mode == "query":
        url, params = PAGE_1, {"page": n}
        if per_page:
            params["per_page"] = per_page
    else:
        url = PAGE_1 if n == 1 else PAGE_N.format(n=n)
        params = {"per_page": per_page} if per_page else None

    try:
        r = session.get(url, params=params, timeout=timeout)
    except requests.RequestException as e:
        raise GateError(f"request failed: {type(e).__name__}: {e}") from e

    if r.status_code != 200:
        raise GateError(f"HTTP {r.status_code} at {r.url}")

    if _GATE_MARK in r.text:
        raise GateError(
            f"the Turnstile gate answered instead of the page ({r.url}).\n"
            "The clearance has expired or is not being accepted. Reload the grants database "
            "in the SAME browser, pass the check, copy the Cookie header again, and re-run — "
            "pages already saved are kept and the fetch resumes from where it stopped.\n"
            "Two cookies matter and both must be present: cf_clearance and "
            "ford_gd_ts_verified.\n"
            "The clearance is also bound to the User-Agent that earned it, so send the same "
            "one the browser sent (--ua \"...\")."
        )

    m = _JSON_BLOCK.search(r.text)
    if not m:
        raise GateError(
            f"no grants payload found in the HTML at {r.url}.\n"
            "Expected a <script type=\"application/json\"> block inside "
            "<div class=\"grants-db\">. Either the page markup changed, or this is not the "
            "database page. Save the response and look at it before re-running."
        )
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError as e:
        raise GateError(f"the embedded payload at {r.url} is not valid JSON: {e}") from e


def first_ids(d: dict) -> list:
    return [g.get("grant_id") for g in payload(d).get("grants", [])[:3]]


def choose_pagination(session: requests.Session, per_page: int | None) -> tuple[str, int | None]:
    """Find a pagination shape that actually advances.

    Verified against page 2, not assumed. A capture whose pages all return the
    same records is the worst kind of failure: it completes, it writes a
    plausible number of files, and only a uniqueness check downstream reveals
    that every page is page 1.
    """
    attempts = []
    if per_page:
        attempts.append(("query", per_page, f"?page=N&per_page={per_page}"))
        attempts.append(("path", per_page, f"/page/N/?per_page={per_page}"))
    attempts.append(("path", None, "/page/N/ at the site's own page size"))

    base_ids = None
    for mode, pp, label in attempts:
        try:
            p1 = fetch_page_html(session, 1, pp, mode=mode)
            p2 = fetch_page_html(session, 2, pp, mode=mode)
        except GateError as e:
            print(f"  {label}: failed ({e.args[0].splitlines()[0]})")
            continue
        ids1, ids2 = first_ids(p1), first_ids(p2)
        reported = payload(p2).get("page")
        if ids1 and ids2 and ids1 != ids2:
            n = len(payload(p1).get("grants", []))
            print(f"  {label}: advances correctly ({n} per page)")
            return mode, pp
        print(f"  {label}: page 2 returned the SAME records as page 1 "
              f"(payload says page={reported}) — rejected")
        base_ids = ids1

    raise GateError(
        "no pagination shape advances past page 1. Every variant returned the same records, "
        "so a capture would silently duplicate page 1 across every file. Open "
        f"{PAGE_N.format(n=2)} in the browser and check what URL the 'Load More' control or "
        "the rel=next link actually uses, then adjust PAGE_N."
    )


def cmd_fetch_html(args) -> int:
    """Capture by paging the rendered document, not the API.

    Reuses a clearance a human obtained by passing the check; it does not
    circumvent one. Expect to re-copy the cookie partway through a long run —
    clearances are short-lived, and the fetch resumes.
    """
    session = make_session(args.cookie, args.browser_ua, None, args.header,
                           args.ua, document_mode=True)
    out = Path(args.out)
    (out / "raw").mkdir(parents=True, exist_ok=True)

    print("checking which pagination shape advances:")
    mode, per_page = choose_pagination(session, args.per_page)
    print()

    first = payload(fetch_page_html(session, 1, per_page, mode=mode))
    total_pages = int(first.get("total_pages") or 0)
    total_grants = int(first.get("total_grants") or 0)
    got_per_page = len(first.get("grants", []))
    if got_per_page:
        total_pages = -(-total_grants // got_per_page)
    print(f"{total_grants} grants across {total_pages} pages "
          f"({got_per_page} per page, {mode} pagination)\n")
    if total_pages > 200 and args.delay < 2:
        print(f"{total_pages} requests at {args.delay}s apart. Ford put a bot check in front "
              f"of this database, which is a signal about automated access; consider "
              f"--delay 3 and do not re-run casually.\n")

    seen: set = set()
    for page in range(1, total_pages + 1):
        dest = out / "raw" / f"page_{page:04d}.json"
        if dest.exists() and not args.refetch:
            seen.update(g.get("grant_id") for g in
                        payload(json.loads(dest.read_text(encoding="utf-8"))).get("grants", []))
            continue
        try:
            d = fetch_page_html(session, page, per_page, mode=mode)
        except GateError as e:
            print(f"\n\npage {page} of {total_pages} stopped:\n  {e}\n", file=sys.stderr)
            print(f"{len(seen)} unique grants saved so far. Re-run with a fresh cookie to "
                  f"resume.", file=sys.stderr)
            return 3

        ids = [g.get("grant_id") for g in payload(d).get("grants", [])]
        new_ids = [i for i in ids if i not in seen]
        if ids and not new_ids:
            # Fail here rather than writing 400 more copies of the same page.
            print(f"\n\nSTOPPED at page {page}: every record on it was already captured.\n"
                  f"The site has stopped advancing, so continuing would write duplicates that "
                  f"look like a complete capture. {len(seen)} unique grants saved.\n"
                  f"Check what {PAGE_N.format(n=page)} returns in the browser.",
                  file=sys.stderr)
            return 4
        seen.update(ids)
        dest.write_text(json.dumps(d), encoding="utf-8")
        print(f"\r  page {page}/{total_pages}  ({len(seen)}/{total_grants} unique grants)",
              end="", flush=True)
        time.sleep(args.delay)

    print(f"\n\nsaved {total_pages} raw pages to {out / 'raw'}")
    print(f"{len(seen)} unique grants captured, {total_grants} reported by the site")
    if len(seen) != total_grants:
        print("WARNING: those numbers differ. Either the database changed mid-capture or the "
              "paging missed records; note it in notes.txt before enumerating.")
    (out / "ford_capture_manifest.json").write_text(json.dumps({
        "script": "ford_fetch.py", "script_version": SCRIPT_VERSION,
        "captured_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "route": "rendered HTML documents, payload extracted from div.grants-db",
        "reason": "the registered route (manual export of a topic-filtered view) does not "
                  "exist: the UI exposes only Approval date and Amount facets, search matches "
                  "grantee names only, and the program appears solely as a field on each grant",
        "page_1_url": PAGE_1, "page_n_pattern": PAGE_N, "pagination_mode": mode,
        "per_page": got_per_page, "total_pages": total_pages,
        "filters_applied": "NONE — full database; the program boundary is applied at "
                           "enumeration, per frames.json",
        "total_grants_reported": total_grants, "unique_grants_captured": len(seen),
        "year_range": [first.get("min_year"), first.get("max_year")],
        "user_agent": session.headers.get("User-Agent"),
        "gate": "Cloudflare Turnstile; clearance obtained manually in a browser and reused",
    }, indent=2), encoding="utf-8")
    print(f"manifest: {out / 'ford_capture_manifest.json'}")
    return 0


def join(items, key) -> str:
    return "; ".join(str(i.get(key, "")) for i in (items or []) if i.get(key))


FIELDS = [
    "grant_id", "grantee_id", "grantee_name", "grantee_website_url", "grantee_url",
    "grant_amount", "total_amount", "description", "approval_date", "start_date",
    "end_date", "fiscal_year_of_approval", "link", "locations", "programs",
    "program_slugs", "subjects", "subject_slugs", "regions", "grant_types",
    "source_route",
]


def cmd_flatten(args) -> int:
    out = Path(args.out)
    pages = sorted((out / "raw").glob("page_*.json"))
    if not pages:
        print(f"no raw pages in {out / 'raw'} — run `fetch` first", file=sys.stderr)
        return 2

    rows, seen = [], set()
    prog_counts: dict[str, int] = {}
    subj_counts: dict[str, int] = {}
    prog_by_subject_tech: dict[str, int] = {}
    year_by_prog: dict[str, list] = {}

    for p in pages:
        for g in payload(json.loads(p.read_text(encoding="utf-8"))).get("grants", []):
            gid = g.get("grant_id")
            if gid in seen:
                continue
            seen.add(gid)
            progs = g.get("programs") or []
            subjs = g.get("subjects") or []
            rows.append({
                "grant_id": gid,
                "grantee_id": g.get("grantee_id"),
                "grantee_name": g.get("grantee_name", ""),
                "grantee_website_url": g.get("grantee_website_url", ""),
                "grantee_url": g.get("grantee_url", ""),
                "grant_amount": g.get("grant_amount"),
                "total_amount": g.get("total_amount"),
                "description": g.get("description", ""),
                "approval_date": g.get("approval_date", ""),
                "start_date": g.get("start_date", ""),
                "end_date": g.get("end_date", ""),
                "fiscal_year_of_approval": g.get("fiscal_year_of_approval", ""),
                "link": g.get("link", ""),
                "locations": join(g.get("locations"), "location_name"),
                "programs": join(progs, "program_name"),
                "program_slugs": join(progs, "program_slug"),
                "subjects": join(subjs, "subject_name"),
                "subject_slugs": join(subjs, "subject_slug"),
                "regions": join(g.get("regions"), "region_name"),
                "grant_types": join(g.get("types"), "type_name"),
                "source_route": args.source_route,
            })
            for pr in progs:
                name = pr.get("program_name", "")
                prog_counts[name] = prog_counts.get(name, 0) + 1
                yr = g.get("fiscal_year_of_approval")
                if yr:
                    year_by_prog.setdefault(name, []).append(str(yr))
            for sb in subjs:
                subj_counts[sb.get("subject_name", "")] = \
                    subj_counts.get(sb.get("subject_name", ""), 0) + 1
            if any("technolog" in (sb.get("subject_slug") or "") for sb in subjs):
                for pr in progs:
                    nm = pr.get("program_name", "")
                    prog_by_subject_tech[nm] = prog_by_subject_tech.get(nm, 0) + 1

    csv_path = out / "ford_grants_live_database.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} unique grants -> {csv_path}\n")

    print("PROGRAM values present (this is the boundary you are choosing):")
    for name, n in sorted(prog_counts.items(), key=lambda kv: -kv[1]):
        yrs = year_by_prog.get(name, [])
        span = f"  {min(yrs)}-{max(yrs)}" if yrs else ""
        print(f"  {n:>6}  {name}{span}")

    print("\nTOPIC (subject) values present:")
    for name, n in sorted(subj_counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:>6}  {name}")

    if prog_by_subject_tech:
        print("\nGrants carrying a TECHNOLOGY subject, by program label:")
        for name, n in sorted(prog_by_subject_tech.items(), key=lambda kv: -kv[1]):
            print(f"  {n:>6}  {name}")
        print("\nThis is the number that matters. Technology-subject grants sitting under "
              "'Other Grantmaking' are pre-2018 records that a program-only boundary will "
              "MISS — and pre-2018 technology grantmaking is the historical depth this frame "
              "was meant to supply. If that count is large, define the FORD boundary as "
              "program OR technology-subject, and record the choice and this count in the "
              "register as a measured bound on frame completeness.")

    inv = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "unique_grants": len(rows),
        "programs": prog_counts,
        "program_year_range": {k: [min(v), max(v)] for k, v in year_by_prog.items() if v},
        "subjects": subj_counts,
        "technology_subject_by_program": prog_by_subject_tech,
    }
    (out / "ford_inventory.json").write_text(json.dumps(inv, indent=2), encoding="utf-8")
    print(f"\ninventory: {out / 'ford_inventory.json'}")
    print("\nNothing here is frame contents in the sense the freeze protects: these are "
          "counts of metadata values, which is what the register needs to fix a boundary. "
          "Do not read the grantee list.")
    return 0


def cmd_terms(args) -> int:
    """Taxonomy slugs for the boundary definition.

    The grants route accepts no program or subject parameter, so the boundary
    is written in frames.json against these slugs. Term names and counts are
    metadata, not frame contents.
    """
    session = make_session(args.cookie, args.browser_ua, args.nonce, args.header, args.ua)
    for subtype in ("program_tax", "grant_subject"):
        print(f"\n{subtype}:")
        try:
            d = request({"type": "term", "subtype": subtype, "search": ""},
                        session, endpoint=TERMS_ENDPOINT)
        except GateError as e:
            print(f"  failed: {e}")
            continue
        items = d if isinstance(d, list) else d.get("results", d.get("terms", []))
        if not items:
            print(f"  no terms returned; raw: {json.dumps(d)[:300]}")
            continue
        for it in items:
            if isinstance(it, dict):
                print(f"  {it.get('slug', ''):<44} {it.get('name', it.get('title', ''))}")
            else:
                print(f"  {it}")
    print("\nUse the technology-and-society program slug, and the technology subject slug, "
          "in the FORD boundary in frames.json.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cookie", default=None,
                    help="Cookie header copied from a browser that passed the check")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    ap.add_argument("--ua", default=None,
                    help="exact User-Agent to send. A Turnstile clearance is bound to the "
                         "User-Agent that earned it, so pass the one your browser sent.")
    ap.add_argument("--endpoint", default=None,
                    help="the grants endpoint, as read from the browser's network tab. "
                         f"Default: {ENDPOINT}")
    ap.add_argument("--nonce", default=None,
                    help="value of the X-WP-Nonce request header, if the page sends one")
    ap.add_argument("--header", action="append", default=[],
                    help="extra request header, 'Name: value'; repeatable")
    ap.add_argument("--browser-ua", action="store_true", dest="browser_ua",
                    help="send a browser User-Agent instead of the identifying one. "
                         "Cloudflare binds a cf_clearance cookie to the User-Agent that "
                         "obtained it, so a cookie copied from a browser may be rejected "
                         "when sent with any other UA. Try this if the run 403s on a cookie "
                         "that plainly works in the browser.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("probe", help="check the endpoint and find the best per_page")
    p.set_defaults(fn=cmd_probe)

    p = sub.add_parser("fetch", help="page through the database, saving raw JSON")
    p.add_argument("--out", default="snapshots/FORD")
    p.add_argument("--per-page", type=int, default=MAX_PER_PAGE, dest="per_page",
                   help=f"max {MAX_PER_PAGE}, declared by the route")
    p.add_argument("--retries", type=int, default=4)
    p.add_argument("--refetch", action="store_true", help="re-fetch pages already saved")
    p.set_defaults(fn=cmd_fetch)

    p = sub.add_parser("fetch-html",
                       help="page the rendered documents (works when the API does not)")
    p.add_argument("--out", default="snapshots/FORD")
    p.add_argument("--per-page", type=int, default=100, dest="per_page",
                   help="page size to request (default 100). The rendered page may ignore it "
                        "and stay at 10, which the script detects and reports; 100 turns 432 "
                        "requests into 44, so it is worth asking for.")
    p.add_argument("--refetch", action="store_true")
    p.set_defaults(fn=cmd_fetch_html)

    p = sub.add_parser("terms", help="list program and subject slugs for the boundary")
    p.set_defaults(fn=cmd_terms)

    p = sub.add_parser("flatten", help="raw pages -> one CSV plus a value inventory")
    p.add_argument("--out", default="snapshots/FORD")
    p.add_argument("--source-route", default="live_database", dest="source_route")
    p.set_defaults(fn=cmd_flatten)

    args = ap.parse_args()
    try:
        return args.fn(args)
    except GateError as e:
        print(f"\nSTOPPED: {e}\n", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())