#!/usr/bin/env python3
"""
tpg_search.py -- Search stage for the PICANTE literature strand.

Implements the search procedure registered in Preregistration Update 3:
  item 3.1  generations, the two-link constraint, the 5% stopping rule, cap at 3,
            and full provenance (every parent of every work)
  item 3.3  validation check per generation (V1-V4 on gen 1, V5 on gen 2) and
            the computed leave-one-out check
  item 3.4  the keyword arm (seven registered queries, OpenAlex title+abstract)
  item 3.5  component 3 of the hand-search list (grey literature cited by >= 2 seeds)
and the random draws for the screening pilot and the per-generation drift check.

Everything is stored in one SQLite database. Every API request is logged with its
timestamp (the API key is redacted), so access dates can be reported as registered.

Typical order of use (see README.md):
  init -> resolve -> gen1 + keyword -> handsearch-list -> validate --generation 1
  -> export -> [dedup, pilot, screening outside this script] -> load-includes
  -> status -> gen 2 -> validate --generation 2 -> ... -> loo
"""
import argparse, csv, json, os, random, re, sqlite3, sys, time
import urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone

BASE = "https://api.openalex.org"
SELECT = ("id,doi,display_name,publication_year,type,primary_location,locations,"
          "authorships,referenced_works,referenced_works_count,cited_by_count,"
          "abstract_inverted_index,ids")

# Registered query strings (Query strings, route 2). Terms unchanged from registration.
QUERIES = [
    '"civic technology"',
    '"public interest technology"',
    '"tech for good" OR "technology for good" OR "data for good" OR "data science for social good"',
    '"AI for social good" OR "artificial intelligence for social good" OR "AI for good" OR "AI for social impact"',
    '"machine learning for social good" OR "NLP for social good" OR "computing for social good"',
    '"AI4SG" OR "AI4SI" OR "DSSG" OR "NLP4SG" OR "D4G"',
    '"generative AI for social good" OR "agentic AI for social good" OR "conversational AI for social good"',
]

# Update 3, item 3.3: generation against which each validation work is assessed.
VALIDATION_GENERATION = {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 8: 1}
COUNTING = {1, 2, 3, 4, 5}          # V8 (Arnstein) is reported separately
DEPENDENT_PAIR = {1, 2}             # V1/V2 dependence rule: a joint miss counts once
LINK_THRESHOLD = 2                  # item 3.1
STOP_FRACTION = 0.05                # item 3.1
MAX_GENERATION = 3                  # item 3.1
GREY_TYPES = {"report", "other", "standard"}   # item 3.5, component 3


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def short_id(x):
    """'https://openalex.org/W123' -> 'W123'."""
    return x.rsplit("/", 1)[-1] if x else x


def norm_doi(d):
    if not d:
        return None
    d = d.strip().lower()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    return d if d.startswith("10.") else None


def abstract_text(inv):
    if not inv:
        return ""
    pos = [(i, w) for w, idxs in inv.items() for i in idxs]
    return " ".join(w for _, w in sorted(pos))


# --------------------------------------------------------------------------- DB

SCHEMA = """
CREATE TABLE IF NOT EXISTS works (
  id TEXT PRIMARY KEY, doi TEXT, title TEXT, year INT, type TEXT,
  venue TEXT, publisher TEXT, refs TEXT, raw TEXT, fetched_at TEXT);
CREATE TABLE IF NOT EXISTS seeds (
  seed_no INT PRIMARY KEY, identifier TEXT, expansion_identifier TEXT,
  id TEXT, status TEXT, resolved_at TEXT);
CREATE TABLE IF NOT EXISTS seed_yields (
  seed_no INT PRIMARY KEY, backward INT, forward INT, cited_by_count INT, retrieved_at TEXT);
CREATE TABLE IF NOT EXISTS merge_checks (
  subject TEXT, primary_id TEXT, alt_identifier TEXT, alt_id TEXT,
  same_record INT, checked_at TEXT);
CREATE TABLE IF NOT EXISTS validation_set (
  v_no INT PRIMARY KEY, identifier TEXT, arm TEXT, counts TEXT);
CREATE TABLE IF NOT EXISTS validation_results (
  v_no INT, generation INT, resolved_id TEXT, first_generation INT,
  outcome TEXT, cause TEXT, assessed_at TEXT, PRIMARY KEY (v_no, generation));
-- direction: 'backward' = parent references work; 'forward' = work cites parent;
--            'keyword'  = work returned by query parent (Q1..Q7)
CREATE TABLE IF NOT EXISTS provenance (
  work_id TEXT, parent_id TEXT, direction TEXT, generation INT, arm TEXT,
  recorded_at TEXT, PRIMARY KEY (work_id, parent_id, direction, generation, arm));
-- status: to_screen | below_threshold | previously_screened | seed
CREATE TABLE IF NOT EXISTS pool (
  work_id TEXT, generation INT, arm TEXT, status TEXT, link_count INT,
  PRIMARY KEY (work_id, generation, arm));
-- arm: seed | expansion | keyword | handsearch; generation = generation screened in
CREATE TABLE IF NOT EXISTS includes (
  work_id TEXT PRIMARY KEY, arm TEXT, generation INT, loaded_at TEXT);
CREATE TABLE IF NOT EXISTS queries (
  q_no INT PRIMARY KEY, query TEXT, url TEXT, run_at TEXT, count INT);
CREATE TABLE IF NOT EXISTS requests (
  n INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, at TEXT, status INT);
"""


def connect(path):
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    return db


# ----------------------------------------------------------------------- client

def urllib_transport(url):
    req = urllib.request.Request(url, headers={"User-Agent": "PICANTE-tpg_search/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, None


class OpenAlex:
    def __init__(self, db, mailto=None, api_key=None, transport=urllib_transport, sleep=0.12):
        self.db, self.mailto, self.api_key = db, mailto, api_key
        self.transport, self.sleep = transport, sleep

    def _get(self, path, params=None):
        params = dict(params or {})
        if self.mailto:
            params["mailto"] = self.mailto
        if self.api_key:
            params["api_key"] = self.api_key
        url = BASE + path + ("?" + urllib.parse.urlencode(params, safe=":|*,") if params else "")
        logged = re.sub(r"api_key=[^&]+", "api_key=REDACTED", url)
        for attempt in range(6):
            status, body = self.transport(url)
            self.db.execute("INSERT INTO requests (url, at, status) VALUES (?,?,?)",
                            (logged, now(), status))
            if status == 200:
                time.sleep(self.sleep)
                return body
            if status == 404:
                return None
            if status in (429, 500, 502, 503, 504):
                time.sleep(min(60, 2 ** attempt))
                continue
            raise RuntimeError(f"OpenAlex returned {status} for {logged}")
        raise RuntimeError(f"OpenAlex kept failing for {logged}")

    def work(self, ident):
        """ident: 'W123', or a DOI ('10.x/y')."""
        key = ident if re.match(r"^W\d+$", ident) else "doi:" + ident
        w = self._get("/works/" + key, {"select": SELECT})
        if w:
            store_work(self.db, w)
        return w

    def works_by_ids(self, ids):
        out = []
        ids = list(ids)
        for i in range(0, len(ids), 50):
            chunk = ids[i:i + 50]
            body = self._get("/works", {"filter": "ids.openalex:" + "|".join(chunk),
                                        "select": SELECT, "per_page": 50})
            for w in (body or {}).get("results", []):
                store_work(self.db, w)
                out.append(w)
        return out

    def iter_filter(self, flt):
        cursor = "*"
        while cursor:
            body = self._get("/works", {"filter": flt, "select": SELECT,
                                        "per_page": 200, "cursor": cursor})
            if not body:
                return
            for w in body.get("results", []):
                store_work(self.db, w)
                yield w
            cursor = body.get("meta", {}).get("next_cursor")
            if not body.get("results"):
                return

    def request_url(self, flt):
        """The exact URL submitted for a filter, as recorded for the keyword arm."""
        params = {"filter": flt}
        return BASE + "/works?" + urllib.parse.urlencode(params, safe=":|*,")


def store_work(db, w):
    src = ((w.get("primary_location") or {}).get("source") or {})
    db.execute("INSERT OR REPLACE INTO works VALUES (?,?,?,?,?,?,?,?,?,?)", (
        short_id(w["id"]), norm_doi(w.get("doi")), w.get("display_name"),
        w.get("publication_year"), w.get("type"), src.get("display_name"),
        src.get("host_organization_name"),
        json.dumps([short_id(r) for r in w.get("referenced_works") or []]),
        json.dumps(w), now()))


def refs_of(db, wid):
    row = db.execute("SELECT refs FROM works WHERE id=?", (wid,)).fetchone()
    return set(json.loads(row[0])) if row and row[0] else set()


def missing(db, ids):
    have = {r[0] for r in db.execute("SELECT id FROM works")}
    return [i for i in ids if i not in have]


# --------------------------------------------------------------------- commands

def cmd_init(db, cfg):
    from openpyxl import load_workbook
    ws = load_workbook(cfg["seed_file"], read_only=True)["Seed set (23)"]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    c_no, c_id, c_exp = head.index("Seed #"), head.index("DOI / stable ID"), head.index("Expansion identifier")
    for r in rows[1:]:
        if r[c_no] is None:
            continue
        db.execute("INSERT OR REPLACE INTO seeds (seed_no, identifier, expansion_identifier) "
                   "VALUES (?,?,?)", (int(r[c_no]), r[c_id], r[c_exp]))
    ws = load_workbook(cfg["validation_file"], read_only=True)["Validation set (8)"]
    rows = list(ws.iter_rows(values_only=True))
    head = rows[0]
    c_no, c_id, c_arm, c_cnt = (head.index("V #"), head.index("DOI / stable ID"),
                                head.index("Arm tested"), head.index("Counts toward expansion criterion"))
    for r in rows[1:]:
        if r[c_no] is None:
            continue
        db.execute("INSERT OR REPLACE INTO validation_set VALUES (?,?,?,?)",
                   (int(r[c_no]), r[c_id], r[c_arm], r[c_cnt]))
    db.commit()
    n_s = db.execute("SELECT COUNT(*) FROM seeds").fetchone()[0]
    n_v = db.execute("SELECT COUNT(*) FROM validation_set").fetchone()[0]
    print(f"Loaded {n_s} seeds and {n_v} validation works.")


def seed_input(row, overrides):
    """Return ('W..'|DOI|None, status) for a seed, per item 1.6 and Update 3 C6."""
    seed_no, ident, exp = row
    ov = overrides.get(str(seed_no))
    if ov:
        if ov.strip().lower() == "none":
            return None, "no_identifier"
        return short_id(ov.strip()), "override"
    exp = (exp or "").strip()
    m = re.search(r"W\d+", exp)
    if m:
        return m.group(0), "expansion_identifier"
    if exp.upper().startswith("DOI"):
        d = norm_doi(ident)
        if d:
            return d, "doi"
    raise SystemExit(
        f"Seed {seed_no} has no usable expansion input ('{exp}'). Record its OpenAlex "
        f"work ID, or 'none', under seed_identifier_overrides in the config (Update 3, C6) "
        f"before running the Search stage.")


def cmd_resolve(db, cfg, oa):
    overrides = cfg.get("seed_identifier_overrides", {})
    rows = db.execute("SELECT seed_no, identifier, expansion_identifier FROM seeds ORDER BY seed_no").fetchall()
    plan = [(r[0], *seed_input(r, overrides)) for r in rows]     # fail before any request
    for seed_no, key, how in plan:
        if key is None:
            db.execute("UPDATE seeds SET status=?, resolved_at=? WHERE seed_no=?",
                       ("no_identifier", now(), seed_no))
            continue
        w = oa.work(key)
        wid = short_id(w["id"]) if w else None
        db.execute("UPDATE seeds SET id=?, status=?, resolved_at=? WHERE seed_no=?",
                   (wid, "resolved:" + how if w else "not_in_index", now(), seed_no))
        if wid:
            db.execute("INSERT OR REPLACE INTO includes VALUES (?,?,?,?)", (wid, "seed", 0, now()))
    # Merge checks for preprint / published pairs (seed 22, V4, and any others listed).
    for subject, alts in cfg.get("merge_checks", {}).items():
        primary = alts[0]
        pw = oa.work(primary if re.match(r"^W\d+$", primary) else norm_doi(primary))
        pid = short_id(pw["id"]) if pw else None
        for alt in alts[1:]:
            aw = oa.work(alt if re.match(r"^W\d+$", alt) else norm_doi(alt))
            aid = short_id(aw["id"]) if aw else None
            db.execute("INSERT INTO merge_checks VALUES (?,?,?,?,?,?)",
                       (subject, pid, alt, aid, int(bool(pid) and pid == aid), now()))
    db.commit()
    for r in db.execute("SELECT seed_no, id, status FROM seeds ORDER BY seed_no"):
        print(f"seed {r[0]:>2}  {r[1] or '-':<14} {r[2]}")
    for r in db.execute("SELECT subject, primary_id, alt_identifier, alt_id, same_record FROM merge_checks"):
        print(f"merge check {r[0]}: {r[1]} vs {r[2]} -> {r[3]}  "
              f"{'SAME record' if r[4] else 'SEPARATE records'}")


def expand(db, oa, sources, generation):
    """Retrieve backward and forward neighbours of each source; record every parent."""
    yields = {}
    for src in sources:
        w = oa.work(src) if not refs_of(db, src) else None
        back = sorted(refs_of(db, src))
        need = missing(db, back)
        if need:
            oa.works_by_ids(need)
        for r in back:
            db.execute("INSERT OR IGNORE INTO provenance VALUES (?,?,?,?,?,?)",
                       (r, src, "backward", generation, "expansion", now()))
        fwd = 0
        for c in oa.iter_filter("cites:" + src):
            db.execute("INSERT OR IGNORE INTO provenance VALUES (?,?,?,?,?,?)",
                       (short_id(c["id"]), src, "forward", generation, "expansion", now()))
            fwd += 1
        raw = db.execute("SELECT raw FROM works WHERE id=?", (src,)).fetchone()
        cbc = json.loads(raw[0]).get("cited_by_count") if raw else None
        yields[src] = (len(back), fwd, cbc)
        db.commit()
    return yields


def counting_includes(db):
    """Works that count toward the linkage threshold: seeds and expansion-arm includes."""
    return {r[0] for r in db.execute("SELECT work_id FROM includes WHERE arm IN ('seed','expansion')")}


def link_counts(db, candidates, incl):
    inc_refs = {i: refs_of(db, i) for i in incl}
    cited_by_inc = {}
    for i, rs in inc_refs.items():
        for r in rs:
            cited_by_inc.setdefault(r, set()).add(i)
    out = {}
    for c in candidates:
        linked = (refs_of(db, c) & incl) | cited_by_inc.get(c, set())
        linked.discard(c)
        out[c] = len(linked)
    return out


def build_pool(db, generation):
    seeds = {r[0] for r in db.execute("SELECT id FROM seeds WHERE id IS NOT NULL")}
    screened = {r[0] for r in db.execute("SELECT work_id FROM pool WHERE status='to_screen'")}
    cands = sorted({r[0] for r in db.execute(
        "SELECT work_id FROM provenance WHERE generation=? AND arm='expansion'", (generation,))})
    lc = link_counts(db, cands, counting_includes(db))
    for c in cands:
        if c in seeds:
            st = "seed"
        elif c in screened:
            st = "previously_screened"
        elif generation == 1 or lc[c] >= LINK_THRESHOLD:
            st = "to_screen"
        else:
            st = "below_threshold"
        db.execute("INSERT OR REPLACE INTO pool VALUES (?,?,?,?,?)", (c, generation, "expansion", st, lc[c]))
    db.commit()


def guard_generation(db, generation):
    if db.execute("SELECT 1 FROM provenance WHERE generation=? AND arm='expansion' LIMIT 1",
                  (generation,)).fetchone():
        raise SystemExit(f"Generation {generation} has already been retrieved; refusing to re-run.")


def cmd_gen1(db, cfg, oa):
    guard_generation(db, 1)
    rows = db.execute("SELECT seed_no, id FROM seeds WHERE id IS NOT NULL ORDER BY seed_no").fetchall()
    if not rows:
        raise SystemExit("No resolved seeds. Run 'resolve' first.")
    y = expand(db, oa, [r[1] for r in rows], 1)
    for seed_no, wid in rows:
        b, f, c = y[wid]
        db.execute("INSERT OR REPLACE INTO seed_yields VALUES (?,?,?,?,?)", (seed_no, b, f, c, now()))
    build_pool(db, 1)
    report_generation(db, 1)


def cmd_gen(db, cfg, oa, generation, override_stop=False):
    if generation < 2 or generation > MAX_GENERATION:
        raise SystemExit(f"Generations 2-{MAX_GENERATION} only (item 3.1 caps expansion at 3).")
    guard_generation(db, generation)
    if not db.execute("SELECT 1 FROM provenance WHERE generation=?", (generation - 1,)).fetchone():
        raise SystemExit(f"Generation {generation - 1} has not been retrieved.")
    stop, msg = stopping_rule(db, generation - 1)
    print(msg)
    if stop and not override_stop:
        raise SystemExit("Stopping rule met: expansion ends here (item 3.1).")
    sources = [r[0] for r in db.execute(
        "SELECT work_id FROM includes WHERE arm='expansion' AND generation=?", (generation - 1,))]
    if not sources:
        raise SystemExit(f"No full-text includes loaded for generation {generation - 1}.")
    expand(db, oa, sources, generation)
    need = missing(db, {r[0] for r in db.execute(
        "SELECT work_id FROM provenance WHERE generation=?", (generation,))})
    if need:
        oa.works_by_ids(need)      # forward citers already carry refs; this is a safety net
    build_pool(db, generation)
    report_generation(db, generation)


def report_generation(db, g):
    print(f"\nGeneration {g}:")
    for st, n in db.execute("SELECT status, COUNT(*) FROM pool WHERE generation=? AND arm='expansion' "
                            "GROUP BY status ORDER BY status", (g,)):
        print(f"  {st:<20} {n}")
    if g == 1:
        print("\n  seed  backward  forward  cited_by_count")
        for r in db.execute("SELECT * FROM seed_yields ORDER BY seed_no"):
            print(f"  {r[0]:>4}  {r[1]:>8}  {r[2]:>7}  {r[3]}")


def cmd_keyword(db, cfg, oa):
    if db.execute("SELECT 1 FROM queries LIMIT 1").fetchone():
        raise SystemExit("The keyword arm has already been run; refusing to re-run.")
    seeds = {r[0] for r in db.execute("SELECT id FROM seeds WHERE id IS NOT NULL")}
    for q_no, q in enumerate(QUERIES, 1):
        flt = "title_and_abstract.search:" + q
        n = 0
        for w in oa.iter_filter(flt):
            wid = short_id(w["id"])
            db.execute("INSERT OR IGNORE INTO provenance VALUES (?,?,?,?,?,?)",
                       (wid, f"Q{q_no}", "keyword", 0, "keyword", now()))
            n += 1
        db.execute("INSERT INTO queries VALUES (?,?,?,?,?)", (q_no, q, oa.request_url(flt), now(), n))
        db.commit()
        print(f"Q{q_no}: {n} records")
    ids = {r[0] for r in db.execute("SELECT work_id FROM provenance WHERE arm='keyword'")}
    for wid in ids:
        db.execute("INSERT OR REPLACE INTO pool VALUES (?,?,?,?,?)",
                   (wid, 0, "keyword", "seed" if wid in seeds else "to_screen", None))
    db.commit()
    pre = sum(1 for w in ids if is_preprint_server(db, w))
    print(f"Keyword arm: {len(ids)} distinct records; {pre} with an arXiv or SSRN location "
          f"({100 * pre / max(1, len(ids)):.1f}%, reported under item 3.4).")


def is_preprint_server(db, wid):
    raw = db.execute("SELECT raw FROM works WHERE id=?", (wid,)).fetchone()
    if not raw:
        return False
    w = json.loads(raw[0])
    names = [((l.get("source") or {}).get("display_name") or "") for l in w.get("locations") or []]
    names += [(w.get("ids") or {}).get("arxiv") or ""]
    return any(re.search(r"arxiv|ssrn", n, re.I) for n in names)


def cmd_handsearch_list(db, cfg, out):
    """Item 3.5, component 3: grey-literature items cited by at least two seeds."""
    seeds = {r[0]: r[1] for r in db.execute("SELECT id, seed_no FROM seeds WHERE id IS NOT NULL")}
    cited = {}
    for work, parent in db.execute("SELECT work_id, parent_id FROM provenance "
                                   "WHERE generation=1 AND direction='backward' AND arm='expansion'"):
        if parent in seeds:
            cited.setdefault(work, set()).add(seeds[parent])
    rows = []
    for wid, by in cited.items():
        if len(by) < 2:
            continue
        r = db.execute("SELECT title, type, venue, publisher FROM works WHERE id=?", (wid,)).fetchone()
        if r and r[1] in GREY_TYPES:
            rows.append([r[3] or r[2] or "(publisher not recorded)", wid, r[0], r[1],
                         ";".join(str(s) for s in sorted(by))])
    rows.sort()
    with open(out, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["organization", "openalex_id", "title", "type", "cited_by_seeds"])
        wr.writerows(rows)
    orgs = sorted({r[0] for r in rows})
    print(f"{len(rows)} grey-literature items cited by >= 2 seeds, from {len(orgs)} organizations "
          f"-> {out}\nRecord the resulting organization list before searching any site (item 3.5).")
    for o in orgs:
        print("  " + o)


def resolve_validation(db, oa, v_no, ident):
    d = norm_doi(ident)
    if not d:
        return None, None
    found = db.execute("SELECT id FROM works WHERE doi=?", (d,)).fetchone()
    if found:
        return found[0], d
    w = oa.work(d)
    return (short_id(w["id"]) if w else None), d


def cmd_validate(db, cfg, oa, generation):
    alts = cfg.get("validation_alternates", {})
    results = {}
    for v_no, ident, arm, counts in db.execute("SELECT * FROM validation_set ORDER BY v_no").fetchall():
        if not (arm or "").lower().startswith("citation"):
            print(f"V{v_no}: assessed against the hand-search log, not here ({arm}).")
            continue
        g = VALIDATION_GENERATION.get(v_no)
        if g is None or g > generation:
            continue
        wid, _ = resolve_validation(db, oa, v_no, ident)
        ids = {wid} if wid else set()
        for a in alts.get(f"V{v_no}", []):
            aid, _ = resolve_validation(db, oa, v_no, a)
            if aid:
                ids.add(aid)
        if not ids:
            outcome, cause, first = "not_recovered", "a: absent from index", None
        else:
            rows = db.execute(
                f"SELECT p.generation, p.status FROM pool p WHERE p.arm='expansion' AND p.generation<=? "
                f"AND p.work_id IN ({','.join('?' * len(ids))}) ORDER BY p.generation",
                (g, *ids)).fetchall()
            entered = [r for r in rows if r[1] in ("to_screen", "previously_screened", "seed")]
            if entered:
                outcome, cause, first = "recovered", None, entered[0][0]
            elif rows:
                outcome, cause, first = "retrieved_below_threshold", None, rows[0][0]
            else:
                outcome, cause, first = "not_recovered", "c: in index, unreachable from seed neighbourhood", None
        db.execute("INSERT OR REPLACE INTO validation_results VALUES (?,?,?,?,?,?,?)",
                   (v_no, generation, ",".join(sorted(ids)) or None, first, outcome, cause, now()))
        results[v_no] = (outcome, cause, first)
        tag = "" if v_no in COUNTING else "  (reported separately; not counted)"
        print(f"V{v_no}: {outcome}{' (' + cause + ')' if cause else ''}"
              f"{' first in generation ' + str(first) if first else ''}{tag}")
    db.commit()
    # Trigger: cause (c) among counting works, cumulatively, with V1/V2 counted once.
    prior = {r[0]: r[1] for r in db.execute(
        "SELECT v_no, cause FROM validation_results WHERE generation<=?", (generation,))}
    c_misses = {v for v, cause in prior.items() if v in COUNTING and cause and cause.startswith("c")}
    n = len(c_misses) - (1 if DEPENDENT_PAIR <= c_misses else 0)
    print(f"\nCause (c) misses counted toward the trigger: {n} {sorted(c_misses)}")
    if n >= 2:
        print("TRIGGER MET: add a targeted query and record it in a preregistration update "
              "before the screening this check precedes (item 3.3).")
    else:
        print("Trigger not met. Cause (b) is determined later, as screening completes.")


def cmd_load_includes(db, cfg, path):
    """CSV with columns openalex_id, arm (expansion|keyword|handsearch), generation."""
    pool = {(r[0], r[1]) for r in db.execute("SELECT work_id, generation FROM pool "
                                             "WHERE arm='expansion' AND status='to_screen'")}
    n = 0
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            wid = short_id(row["openalex_id"].strip())
            arm = row["arm"].strip().lower()
            g = int(row["generation"]) if row.get("generation", "").strip() else None
            if arm == "expansion" and (wid, g) not in pool:
                raise SystemExit(f"{wid} is not in the generation-{g} screening pool; check the file.")
            db.execute("INSERT OR REPLACE INTO includes VALUES (?,?,?,?)", (wid, arm, g, now()))
            n += 1
    db.commit()
    print(f"Loaded {n} full-text includes.")


def stopping_rule(db, g):
    new = db.execute("SELECT COUNT(*) FROM includes WHERE arm='expansion' AND generation=?", (g,)).fetchone()[0]
    cum = db.execute("SELECT COUNT(*) FROM includes WHERE arm!='seed'").fetchone()[0]
    frac = new / cum if cum else 0.0
    stop = frac < STOP_FRACTION or g >= MAX_GENERATION
    why = ("cap at generation 3 reached" if g >= MAX_GENERATION and frac >= STOP_FRACTION
           else f"{'below' if frac < STOP_FRACTION else 'at or above'} the 5% threshold")
    return stop, (f"Generation {g}: {new} new full-text includes / {cum} cumulative non-seed includes "
                  f"= {100 * frac:.1f}% ({why}). " + ("Stop." if stop else f"Run generation {g + 1}."))


def cmd_status(db, cfg):
    gens = [r[0] for r in db.execute("SELECT DISTINCT generation FROM pool WHERE arm='expansion' ORDER BY 1")]
    for g in gens:
        report_generation(db, g)
        print("  " + stopping_rule(db, g)[1])
    print(f"\n{db.execute('SELECT COUNT(*) FROM requests').fetchone()[0]} API requests logged, "
          f"first {db.execute('SELECT MIN(at) FROM requests').fetchone()[0]}, "
          f"last {db.execute('SELECT MAX(at) FROM requests').fetchone()[0]}.")


def cmd_export(db, cfg, generation, arm, out):
    """Records to screen, as a Rayyan-importable CSV."""
    rows = db.execute("SELECT p.work_id, w.raw FROM pool p JOIN works w ON w.id=p.work_id "
                      "WHERE p.generation=? AND p.arm=? AND p.status='to_screen' ORDER BY p.work_id",
                      (generation, arm)).fetchall()
    with open(out, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["key", "title", "authors", "journal", "year", "publisher", "url", "abstract", "doi", "notes"])
        for wid, raw in rows:
            w = json.loads(raw)
            src = ((w.get("primary_location") or {}).get("source") or {})
            authors = "; ".join((a.get("author") or {}).get("display_name", "") for a in w.get("authorships") or [])
            wr.writerow([wid, w.get("display_name"), authors, src.get("display_name"),
                         w.get("publication_year"), src.get("host_organization_name"),
                         w.get("id"), abstract_text(w.get("abstract_inverted_index")),
                         norm_doi(w.get("doi")), f"arm={arm}; generation={generation}; type={w.get('type')}"])
    print(f"{len(rows)} records -> {out}")


def cmd_sample(path, n, seed, offset, out):
    """Deterministic random draw (pilot or drift check). Extensions use --offset with the same seed."""
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    keyf = "key" if rows and "key" in rows[0] else list(rows[0])[0]
    rows.sort(key=lambda r: r[keyf])             # independent of file order
    random.Random(seed).shuffle(rows)
    pick = rows[offset:offset + n]
    with open(out, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(pick)
    print(f"Drew records {offset + 1}-{offset + len(pick)} of a {len(rows)}-record pool "
          f"(seed {seed}) -> {out}")


def cmd_loo(db, cfg, out):
    """Item 3.3: generation-1 dependence and lineage dependence, per seed."""
    seeds = dict(db.execute("SELECT id, seed_no FROM seeds WHERE id IS NOT NULL").fetchall())
    incl_exp = {r[0] for r in db.execute("SELECT work_id FROM includes WHERE arm='expansion'")}
    all_nonseed = db.execute("SELECT COUNT(*) FROM includes WHERE arm!='seed'").fetchone()[0]
    parents1 = {}
    for w, p in db.execute("SELECT work_id, parent_id FROM provenance WHERE generation=1 AND arm='expansion'"):
        parents1.setdefault(w, set()).add(p)
    nodes = set(seeds) | incl_exp
    edges = {}
    for w, p in db.execute("SELECT work_id, parent_id FROM provenance WHERE arm='expansion'"):
        if w in incl_exp and p in nodes and p != w:
            edges.setdefault(p, set()).add(w)

    def reachable(start, removed):
        seen, stack = set(), [s for s in start if s != removed]
        while stack:
            x = stack.pop()
            for y in edges.get(x, ()):
                if y != removed and y not in seen:
                    seen.add(y)
                    stack.append(y)
        return seen

    rows = []
    for sid, sno in sorted(seeds.items(), key=lambda x: x[1]):
        only = {w for w, ps in parents1.items() if ps == {sid} and w not in seeds}
        dep = incl_exp - reachable(seeds, sid)
        rows.append([sno, sid, len(only), len(only & incl_exp), len(dep),
                     f"{100 * len(dep) / all_nonseed:.1f}" if all_nonseed else ""])
    with open(out, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["seed_no", "openalex_id", "gen1_works_only_via_seed", "gen1_includes_only_via_seed",
                     "includes_all_paths_via_seed", "pct_of_nonseed_includes"])
        wr.writerows(rows)
    print(f"Leave-one-out for {len(rows)} seeds -> {out}")


# -------------------------------------------------------------------------- CLI

PATH_KEYS = ("database", "seed_file", "validation_file")


def load_config(path):
    """Read the config, resolving its file paths against the config's own directory,
    so the same seed file and database are used whatever directory the script runs from."""
    cfg = json.load(open(path))
    cfg.setdefault("database", "tpg_search.sqlite")
    base = os.path.dirname(os.path.abspath(path))
    for k in PATH_KEYS:
        if cfg.get(k):
            cfg[k] = os.path.join(base, cfg[k])
    return cfg


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default="search_config.json")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("resolve")
    sub.add_parser("gen1")
    g = sub.add_parser("gen"); g.add_argument("generation", type=int)
    g.add_argument("--override-stop", action="store_true",
                   help="run despite the stopping rule (a deviation that must be reported)")
    sub.add_parser("keyword")
    h = sub.add_parser("handsearch-list"); h.add_argument("--out", default="handsearch_component3.csv")
    v = sub.add_parser("validate"); v.add_argument("--generation", type=int, required=True)
    li = sub.add_parser("load-includes"); li.add_argument("csv")
    sub.add_parser("status")
    e = sub.add_parser("export"); e.add_argument("--generation", type=int, default=1)
    e.add_argument("--arm", default="expansion", choices=["expansion", "keyword"])
    e.add_argument("--out", required=True)
    s = sub.add_parser("sample"); s.add_argument("csv"); s.add_argument("--n", type=int, default=100)
    s.add_argument("--seed", type=int, required=True); s.add_argument("--offset", type=int, default=0)
    s.add_argument("--out", required=True)
    lo = sub.add_parser("loo"); lo.add_argument("--out", default="leave_one_out.csv")
    a = ap.parse_args(argv)

    if a.cmd == "sample":
        return cmd_sample(a.csv, a.n, a.seed, a.offset, a.out)
    cfg = load_config(a.config)
    db = connect(cfg["database"])
    oa = OpenAlex(db, cfg.get("mailto"), os.environ.get("OPENALEX_API_KEY") or cfg.get("api_key"))
    if a.cmd == "init": cmd_init(db, cfg)
    elif a.cmd == "resolve": cmd_resolve(db, cfg, oa)
    elif a.cmd == "gen1": cmd_gen1(db, cfg, oa)
    elif a.cmd == "gen": cmd_gen(db, cfg, oa, a.generation, a.override_stop)
    elif a.cmd == "keyword": cmd_keyword(db, cfg, oa)
    elif a.cmd == "handsearch-list": cmd_handsearch_list(db, cfg, a.out)
    elif a.cmd == "validate": cmd_validate(db, cfg, oa, a.generation)
    elif a.cmd == "load-includes": cmd_load_includes(db, cfg, a.csv)
    elif a.cmd == "status": cmd_status(db, cfg)
    elif a.cmd == "export": cmd_export(db, cfg, a.generation, a.arm, a.out)
    elif a.cmd == "loo": cmd_loo(db, cfg, a.out)
    db.commit()


if __name__ == "__main__":
    main()
