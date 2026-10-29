"""Offline tests for tpg_search.py. Run:  python3 test_tpg_search.py

A synthetic citation network stands in for OpenAlex, so the expected results
(link counts, statuses, validation outcomes, leave-one-out) are known exactly.

  Seeds S1, S2.  S1 refs A,B.  S2 refs B,C.  D cites S1 and refs A.  E cites S1,S2 and refs F.
  Gen-1 includes: B, D, E.
  Gen 2 from B,D,E:  B refs G.  H cites B and E.  I cites B.
  -> H has two links (to_screen); G, F, I have one (below_threshold).
"""
import contextlib, csv, io, json, os, sys, tempfile, urllib.parse
from openpyxl import Workbook
import tpg_search as T

W = {
    "S1": dict(doi="10.1/s1", refs=["A", "B"]),
    "S2": dict(doi="10.1/s2", refs=["B", "C"]),
    "A": dict(doi="10.1/a", refs=[]),
    "B": dict(doi="10.1/b", refs=["G"], type="report", publisher="Ford Foundation"),
    "C": dict(doi="10.1/c", refs=[]),
    "D": dict(doi="10.1/d", refs=["S1", "A"]),
    "E": dict(doi="10.1/e", refs=["S1", "S2", "F"]),
    "F": dict(doi="10.1/f", refs=[]),
    "G": dict(doi="10.1/g", refs=[]),
    "H": dict(doi="10.1/h", refs=["B", "E"]),
    "I": dict(doi="10.1/i", refs=["B"]),
    "X": dict(doi="10.1/x", refs=[]),          # in the index, unreachable
    "K": dict(doi="10.1/k", refs=[]),          # keyword-only hit
}
ALIAS = {"10.48550/arxiv.s1": "S1", "10.48550/arxiv.c": "C"}   # preprint DOIs merged into records


def rec(k):
    w = W[k]
    return {"id": "https://openalex.org/" + k, "doi": "https://doi.org/" + w["doi"],
            "display_name": "Title " + k, "publication_year": 2020, "type": w.get("type", "article"),
            "primary_location": {"source": {"display_name": "Venue " + k,
                                            "host_organization_name": w.get("publisher")}},
            "locations": [], "authorships": [{"author": {"display_name": "Author " + k}}],
            "referenced_works": ["https://openalex.org/" + r for r in w["refs"]],
            "cited_by_count": sum(k in v["refs"] for v in W.values()),
            "abstract_inverted_index": {"Abstract": [0], k: [1]}, "ids": {}}


def transport(url):
    u = urllib.parse.urlparse(url)
    q = urllib.parse.parse_qs(u.query)
    path = urllib.parse.unquote(u.path)
    if path.startswith("/works/"):
        key = path[len("/works/"):]
        if key.startswith("doi:"):
            d = key[4:].lower()
            k = ALIAS.get(d) or next((k for k, v in W.items() if v["doi"] == d), None)
        else:
            k = key if key in W else None
        return (200, rec(k)) if k else (404, None)
    flt = q["filter"][0]
    if flt.startswith("cites:"):
        tgt = flt[6:]
        res = [rec(k) for k, v in W.items() if tgt in v["refs"]]
    elif flt.startswith("ids.openalex:"):
        res = [rec(k) for k in flt[13:].split("|") if k in W]
    elif flt.startswith("title_and_abstract.search:"):
        res = [rec("A"), rec("K")] if "civic technology" in flt else []
    else:
        raise AssertionError(flt)
    return 200, {"meta": {"count": len(res), "next_cursor": None}, "results": res}


def make_inputs(d, seed_exp=("DOI (as recorded)", "DOI (as recorded)")):
    wb = Workbook(); ws = wb.active; ws.title = "Seed set (23)"
    ws.append(["Seed #", "DOI / stable ID", "Expansion identifier"])
    ws.append([1, "10.1/s1", seed_exp[0]]); ws.append([2, "10.1/s2", seed_exp[1]])
    wb.save(os.path.join(d, "seeds.xlsx"))
    wb = Workbook(); ws = wb.active; ws.title = "Validation set (8)"
    ws.append(["V #", "DOI / stable ID", "Arm tested", "Counts toward expansion criterion"])
    exp = "Citation-network expansion"
    ws.append([1, "10.1/a", exp, "Yes"])         # recovered, gen 1
    ws.append([2, "10.1/x", exp, "Yes"])         # cause (c)
    ws.append([3, "10.1/missing", exp, "Yes"])   # cause (a)
    ws.append([4, "10.1/nope", exp, "Yes"])      # recovered via alternate (merged preprint -> C)
    ws.append([5, "10.1/h", exp, "Yes"])         # recovered, gen 2
    ws.append([6, "https://example.org/report (no DOI)", "Targeted hand-searching", "No"])
    ws.append([8, "10.1/b", exp, "NO"])          # Arnstein analogue
    wb.save(os.path.join(d, "validation.xlsx"))
    cfg = {"database": os.path.join(d, "t.sqlite"), "seed_file": os.path.join(d, "seeds.xlsx"),
           "validation_file": os.path.join(d, "validation.xlsx"),
           "merge_checks": {"seed 1": ["10.1/s1", "10.48550/arXiv.s1"]},
           "validation_alternates": {"V4": ["10.48550/arXiv.c"]}}
    json.dump(cfg, open(os.path.join(d, "cfg.json"), "w"))
    return cfg


def run(cfg, fn, *args):
    db = T.connect(cfg["database"])
    oa = T.OpenAlex(db, transport=transport, sleep=0)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(db, cfg, oa, *args) if fn not in (T.cmd_init, T.cmd_status, T.cmd_load_includes,
                                             T.cmd_handsearch_list, T.cmd_loo) else fn(db, cfg, *args)
    db.commit()
    return db, buf.getvalue()


def statuses(db, g):
    return dict(db.execute("SELECT work_id, status FROM pool WHERE generation=? AND arm='expansion'", (g,)))


def test_all():
    d = tempfile.mkdtemp()
    cfg = make_inputs(d)
    run(cfg, T.cmd_init)
    db, out = run(cfg, T.cmd_resolve)
    assert "SAME record" in out, out

    db, out = run(cfg, T.cmd_gen1)
    s1 = statuses(db, 1)
    assert s1 == {"A": "to_screen", "B": "to_screen", "C": "to_screen", "D": "to_screen", "E": "to_screen"}, s1
    prov = set(db.execute("SELECT work_id, parent_id, direction FROM provenance WHERE generation=1"))
    assert ("B", "S1", "backward") in prov and ("B", "S2", "backward") in prov   # every parent kept
    assert ("E", "S1", "forward") in prov and ("E", "S2", "forward") in prov
    y = dict((r[0], r[1:3]) for r in db.execute("SELECT * FROM seed_yields"))
    assert y == {1: (2, 2), 2: (2, 1)}, y

    try:
        run(cfg, T.cmd_gen1); raise AssertionError("gen1 re-run should be refused")
    except SystemExit:
        pass

    db, out = run(cfg, T.cmd_keyword)
    kw = dict(db.execute("SELECT work_id, status FROM pool WHERE arm='keyword'"))
    assert kw == {"A": "to_screen", "K": "to_screen"}, kw

    db, out = run(cfg, T.cmd_handsearch_list, os.path.join(d, "hs.csv"))
    assert "Ford Foundation" in out, out

    db, out = run(cfg, T.cmd_validate, 1)
    vr = {r[0]: (r[1], r[2]) for r in db.execute(
        "SELECT v_no, outcome, cause FROM validation_results WHERE generation=1")}
    assert vr[1] == ("recovered", None)
    assert vr[2][1].startswith("c")
    assert vr[3][1].startswith("a")
    assert vr[4] == ("recovered", None)            # via alternate identifier
    assert 5 not in vr                             # V5 waits for generation 2
    assert "Trigger not met" in out and "counted toward the trigger: 1" in out, out

    inc = os.path.join(d, "inc1.csv")
    with open(inc, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["openalex_id", "arm", "generation"])
        for k in ("B", "D", "E"): w.writerow([k, "expansion", 1])
        w.writerow(["K", "keyword", ""])
    run(cfg, T.cmd_load_includes, inc)

    db, out = run(cfg, T.cmd_gen, 2)
    s2 = statuses(db, 2)
    assert s2["H"] == "to_screen", s2
    assert s2["G"] == s2["F"] == s2["I"] == "below_threshold", s2
    assert s2["S1"] == s2["S2"] == "seed", s2
    assert s2["A"] == "previously_screened" and "B" not in s2, s2
    lc = dict(db.execute("SELECT work_id, link_count FROM pool WHERE generation=2"))
    assert lc["H"] == 2 and lc["I"] == 1 and lc["F"] == 1, lc

    db, out = run(cfg, T.cmd_validate, 2)
    v5 = db.execute("SELECT outcome, first_generation FROM validation_results WHERE v_no=5").fetchone()
    assert v5 == ("recovered", 2), v5

    inc2 = os.path.join(d, "inc2.csv")
    with open(inc2, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["openalex_id", "arm", "generation"]); w.writerow(["H", "expansion", 2])
    run(cfg, T.cmd_load_includes, inc2)
    stop, msg = T.stopping_rule(db, 2)               # 1 new / 5 non-seed = 20% -> continue
    assert not stop and "20.0%" in msg, msg

    bad = os.path.join(d, "bad.csv")
    with open(bad, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["openalex_id", "arm", "generation"]); w.writerow(["G", "expansion", 2])
    try:
        run(cfg, T.cmd_load_includes, bad); raise AssertionError("below-threshold include accepted")
    except SystemExit:
        pass

    db, out = run(cfg, T.cmd_loo, os.path.join(d, "loo.csv"))
    loo = {int(r["seed_no"]): r for r in csv.DictReader(open(os.path.join(d, "loo.csv")))}
    assert loo[1]["gen1_works_only_via_seed"] == "2"      # A, D
    assert loo[1]["gen1_includes_only_via_seed"] == "1"   # D
    assert loo[1]["includes_all_paths_via_seed"] == "1"   # D (B, E, H also reachable from S2)
    assert loo[2]["includes_all_paths_via_seed"] == "0"

    try:
        run(cfg, T.cmd_gen, 4); raise AssertionError("generation 4 should be refused")
    except SystemExit:
        pass

    # Deterministic sampling, and extension by offset continues the same draw.
    pool = os.path.join(d, "pool.csv")
    with open(pool, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["key", "title"])
        for i in range(300): w.writerow([f"W{i}", f"t{i}"])
    with contextlib.redirect_stdout(io.StringIO()):
        T.cmd_sample(pool, 100, 7, 0, os.path.join(d, "a.csv"))
        T.cmd_sample(pool, 150, 7, 100, os.path.join(d, "b.csv"))
        T.cmd_sample(pool, 250, 7, 0, os.path.join(d, "c.csv"))
    ka = [r["key"] for r in csv.DictReader(open(os.path.join(d, "a.csv")))]
    kb = [r["key"] for r in csv.DictReader(open(os.path.join(d, "b.csv")))]
    kc = [r["key"] for r in csv.DictReader(open(os.path.join(d, "c.csv")))]
    assert ka + kb == kc and len(set(ka) & set(kb)) == 0

    # API key never written to the request log.
    db2 = T.connect(os.path.join(d, "k.sqlite"))
    T.OpenAlex(db2, api_key="SECRET", transport=transport, sleep=0).work("10.1/a")
    assert "SECRET" not in db2.execute("SELECT url FROM requests").fetchone()[0]


def test_seed20_guard():
    d = tempfile.mkdtemp()
    cfg = make_inputs(d, seed_exp=("DOI (as recorded)", "TO BE RECORDED — no DOI."))
    run(cfg, T.cmd_init)
    try:
        run(cfg, T.cmd_resolve); raise AssertionError("unrecorded seed identifier accepted")
    except SystemExit as e:
        assert "Seed 2" in str(e)
    assert T.connect(cfg["database"]).execute("SELECT COUNT(*) FROM requests").fetchone()[0] == 0
    cfg["seed_identifier_overrides"] = {"2": "none"}
    db, out = run(cfg, T.cmd_resolve)
    assert "no_identifier" in out


def test_relative_config_paths_follow_config_not_cwd():
    d = tempfile.mkdtemp()
    cfg = make_inputs(d)
    rel = {k: os.path.basename(cfg[k]) for k in T.PATH_KEYS}
    path = os.path.join(d, "rel.json")
    json.dump(dict(cfg, **rel), open(path, "w"))
    here = os.getcwd()
    os.chdir(tempfile.mkdtemp())
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            T.main(["--config", path, "init"])
    finally:
        os.chdir(here)
    assert T.connect(cfg["database"]).execute("SELECT COUNT(*) FROM seeds").fetchone()[0] > 0


if __name__ == "__main__":
    test_all(); test_seed20_guard(); test_relative_config_paths_follow_config_not_cwd()
    print("All tests passed.")
