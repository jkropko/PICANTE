#!/usr/bin/env python3
"""
test_enumerate_o3.py — each test is named for the failure it guards against.

Run: python test_enumerate_o3.py
"""
from __future__ import annotations

import csv
import json
import tempfile
from pathlib import Path

import normalize as nz
import dedupe as dd
from frames_io import ConfigError, Record, read_frame

PASS, FAIL = [], []


def assert_eq(a, b):
    assert a == b, f"expected {b!r}, got {a!r}"
    return True


def assert_true(x):
    assert x, "expected true"
    return True


def assert_in(needle, hay):
    assert needle in hay, f"{needle!r} not in {hay!r}"
    return True


def assert_not_in(needle, hay):
    assert needle not in hay, f"{needle!r} unexpectedly in {hay!r}"
    return True


def assert_raises(exc, fn):
    try:
        fn()
    except exc:
        return True
    except Exception as e:  # noqa: BLE001
        raise AssertionError(f"expected {exc.__name__}, got {type(e).__name__}: {e}")
    raise AssertionError(f"expected {exc.__name__}, nothing raised")


def check(name, fn):
    try:
        fn()
        PASS.append(name)
        print(f"  pass  {name}")
    except AssertionError as e:
        FAIL.append((name, str(e)))
        print(f"  FAIL  {name}: {e}")
    except Exception as e:  # noqa: BLE001
        FAIL.append((name, f"{type(e).__name__}: {e}"))
        print(f"  ERROR {name}: {type(e).__name__}: {e}")


def tmp_json(obj) -> str:
    p = Path(tempfile.mkdtemp()) / "f.json"
    p.write_text(json.dumps(obj), encoding="utf-8")
    return str(p)


def tmp_csv(rows, fields) -> str:
    p = Path(tempfile.mkdtemp()) / "f.csv"
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return str(p)


def rec(**kw) -> Record:
    r = Record(**kw)
    return r.finalize_keys()


# ------------------------------------------------------------- normalization

check("normalize_name strips a legal suffix but never 'foundation'", lambda: (
    assert_eq(nz.normalize_name("Nava, PBC"), "nava"),
    assert_eq(nz.normalize_name("The Ford Foundation"), "ford foundation"),
))

check("normalize_name folds ampersand and leading article", lambda: assert_eq(
    nz.normalize_name("The Smith & Jones Lab"), "smith and jones lab"))

check("registrable_domain strips scheme, www, path and port", lambda: assert_eq(
    nz.registrable_domain("https://www.codeforamerica.org:443/programs/x"),
    "codeforamerica.org"))

check("registrable_domain handles a multi-label public suffix", lambda: assert_eq(
    nz.registrable_domain("https://www.mysociety.co.uk/research"), "mysociety.co.uk"))

check("registrable_domain returns empty rather than guessing on junk", lambda: assert_eq(
    nz.registrable_domain("not a url at all"), ""))

check("us_location_guess accepts a bare state name at the end of a string", lambda: assert_eq(
    nz.us_location_guess("Akron, Ohio"), nz.US))

check("us_location_guess accepts a two-letter state abbreviation", lambda: assert_eq(
    nz.us_location_guess("Oakland, CA"), nz.US))

check("us_location_guess recognizes non-US countries in the frames", lambda: (
    assert_eq(nz.us_location_guess("Warsaw, Poland"), nz.NON_US),
    assert_eq(nz.us_location_guess("Berlin, Germany"), nz.NON_US),
))

check("us_location_guess returns UNKNOWN rather than NON_US on an unrecognized string",
      lambda: assert_eq(nz.us_location_guess("Springfield"), nz.UNKNOWN))

check("us_location_guess returns UNKNOWN on a blank location", lambda: (
    assert_eq(nz.us_location_guess(""), nz.UNKNOWN),
    assert_eq(nz.us_location_guess(None), nz.UNKNOWN),
))

check("normalize_country folds the US spellings and leaves others alone", lambda: (
    assert_eq(nz.normalize_country("U.S.A."), "united states"),
    assert_eq(nz.normalize_country("United States"), "united states"),
    assert_eq(nz.normalize_country("Kenya"), "kenya"),
    assert_eq(nz.normalize_country("  "), ""),
))


# --------------------------------------------------------------------- CTFG

CTFG_CFG = {
    "block": "B", "admission_mechanism": "self_declaration", "frame_type": "identity",
    "reader": "ctfg", "lists_institutions": False,
    "boundary": {"type_contains": "organization", "country_in": ["united states"],
                 "country_missing_included": True},
    "columns": {"name": "Name", "website_url": "Website", "type": "Type",
                "country": "Country", "networks": "Networks"},
}

CTFG_ROWS = [
    {"Name": "Alpha Civic", "Website": "https://alpha.org", "Type": "Organization",
     "Country": "United States", "Networks": "Brigade"},
    {"Name": "Beta Labs", "Website": "https://beta.org", "Type": "Organization, Nonprofit",
     "Country": "", "Networks": ""},
    {"Name": "Gamma UK", "Website": "https://gamma.co.uk", "Type": "Organization",
     "Country": "United Kingdom", "Networks": ""},
    {"Name": "Delta Tool", "Website": "https://delta.org", "Type": "App",
     "Country": "United States", "Networks": ""},
    {"Name": "Eps Untyped", "Website": "https://eps.org", "Type": "",
     "Country": "United States", "Networks": ""},
]


def _ctfg():
    return read_frame("CTFG", CTFG_CFG,
                      tmp_csv(CTFG_ROWS, list(CTFG_ROWS[0].keys())), "2026-10-01")


check("CTFG boundary keeps US organizations", lambda: assert_in(
    "Alpha Civic", [r.name for r in _ctfg().kept]))

check("CTFG boundary keeps country-missing organizations, per the registered rule",
      lambda: assert_in("Beta Labs", [r.name for r in _ctfg().kept]))

check("CTFG boundary drops a non-US organization", lambda: assert_not_in(
    "Gamma UK", [r.name for r in _ctfg().kept]))

check("CTFG boundary drops a US record that is not typed Organization", lambda: assert_not_in(
    "Delta Tool", [r.name for r in _ctfg().kept]))

check("CTFG counts US-confirmed separately from country-missing, because the second "
      "group is the manual C2 cost at O4", lambda: (
    assert_eq(_ctfg().stats["kept_us_confirmed"], 1),
    assert_eq(_ctfg().stats["kept_country_missing"], 1),
))

check("CTFG audit stratum (a) holds the type-present-not-Organization record", lambda: assert_eq(
    [r["name"] for r in _ctfg().extra_pools["ctfg_audit_stratum_a"]], ["Delta Tool"]))

check("CTFG audit stratum (b) holds the type-missing record", lambda: assert_eq(
    [r["name"] for r in _ctfg().extra_pools["ctfg_audit_stratum_b"]], ["Eps Untyped"]))

check("CTFG audit strata are disjoint, or the O8 confidence intervals are wrong", lambda: (
    lambda a, b: assert_eq(set(x["row"] for x in a) & set(x["row"] for x in b), set())
)(_ctfg().extra_pools["ctfg_audit_stratum_a"], _ctfg().extra_pools["ctfg_audit_stratum_b"]))

check("CTFG carries the Networks field verbatim", lambda: assert_eq(
    next(r.ctfg_networks for r in _ctfg().kept if r.name == "Alpha Civic"), "Brigade"))

check("CTFG refuses to run on an unmapped column", lambda: assert_raises(
    ConfigError, lambda: read_frame(
        "CTFG", {**CTFG_CFG, "columns": {**CTFG_CFG["columns"], "type": "CONFIRM"}},
        tmp_csv(CTFG_ROWS, list(CTFG_ROWS[0].keys())), "2026-10-01")))


# ---------------------------------------------------------------------- CFA

CFA_CFG = {
    "block": "B", "admission_mechanism": "self_declaration", "frame_type": "identity",
    "reader": "cfa", "lists_institutions": False,
    "tags": {"include_any": ["Brigade"], "exclude_any": ["Code for All", "Government"],
             "independence_tags": ["Official", "Partner"]},
    "boundary": {"location_rule": "drop_clearly_non_us"},
    "columns": {"name": "name", "website_url": "website", "location": "city",
                "tags": "tags", "previous_names": "previous_names"},
}

CFA_ROWS = [
    {"name": "Open Akron", "website": "https://openakron.org", "city": "Akron, Ohio",
     "tags": ["Brigade", "Official"], "previous_names": ["Code for Akron"]},
    {"name": "Code for Poland", "website": "https://cfp.pl", "city": "Warsaw, Poland",
     "tags": ["Brigade"], "previous_names": []},
    {"name": "18F", "website": "https://18f.gov", "city": "Washington, DC",
     "tags": ["Government"], "previous_names": []},
    {"name": "Code for All", "website": "https://codeforall.org", "city": "",
     "tags": ["Code for All"], "previous_names": []},
    {"name": "Mystery Group", "website": "https://mystery.org", "city": "Springfield",
     "tags": ["Brigade"], "previous_names": []},
]


def _cfa(rule="drop_clearly_non_us"):
    cfg = {**CFA_CFG, "boundary": {"location_rule": rule}}
    return read_frame("CFA", cfg, tmp_json(CFA_ROWS), "2026-10-01")


check("CFA keeps a tagged US brigade", lambda: assert_in(
    "Open Akron", [r.name for r in _cfa().kept]))

check("CFA drops a non-US brigade", lambda: assert_not_in(
    "Code for Poland", [r.name for r in _cfa().kept]))

check("CFA drops government and Code for All entries by tag", lambda: (
    assert_not_in("18F", [r.name for r in _cfa().kept]),
    assert_not_in("Code for All", [r.name for r in _cfa().kept]),
))

check("CFA default rule RETAINS an undeterminable location, leaving C2 to a human at O4",
      lambda: assert_in("Mystery Group", [r.name for r in _cfa().kept]))

check("CFA keep_us_only rule drops it instead — the switch actually switches", lambda: (
    assert_not_in("Mystery Group", [r.name for r in _cfa("keep_us_only").kept])))

check("CFA records how many undeterminable locations it retained, so the boundary's cost "
      "is visible", lambda: assert_eq(_cfa().stats["location_unknown_retained"], 1))

check("CFA carries previous_names, which is how a renamed brigade is later recognized",
      lambda: assert_in("Code for Akron",
                        next(r.previous_names for r in _cfa().kept if r.name == "Open Akron")))

check("CFA records the independence tag", lambda: assert_eq(
    next(r.cfa_independence_tag for r in _cfa().kept if r.name == "Open Akron"), "Official"))

check("CFA refuses to run with an unconfirmed tag vocabulary", lambda: assert_raises(
    ConfigError, lambda: read_frame("CFA", {**CFA_CFG, "tags": {"include_any": []}},
                                    tmp_json(CFA_ROWS), "2026-10-01")))


# ------------------------------------------------------------------- grants

MCGV_CFG = {
    "block": "C", "admission_mechanism": "selection", "frame_type": "funder_portfolio",
    "reader": "grants", "lists_institutions": False,
    "columns": {"grantee_name": "grantee", "website_url": "site", "location": "loc",
                "fiscal_sponsor": "sponsor", "listing_text": "desc"},
}

MCGV_ROWS = [
    {"grantee": "Helpful Org", "site": "https://helpful.org", "loc": "Boston, MA",
     "sponsor": "", "desc": "grant 1"},
    {"grantee": "Helpful Org", "site": "https://helpful.org", "loc": "Boston, MA",
     "sponsor": "", "desc": "grant 2"},
    {"grantee": "Helpful Org", "site": "https://helpful.org", "loc": "Boston, MA",
     "sponsor": "", "desc": "grant 3"},
    {"grantee": "Sponsored Thing", "site": "", "loc": "Oakland, CA",
     "sponsor": "Convergent Research", "desc": "grant 4"},
]


def _mcgv():
    return read_frame("MCGV", MCGV_CFG,
                      tmp_csv(MCGV_ROWS, list(MCGV_ROWS[0].keys())), "2026-10-01")


check("grants reader collapses grants to organizations", lambda: assert_eq(
    len(_mcgv().kept), 2))

check("grants reader keeps the grant count, since the register warns the unit is grants",
      lambda: assert_eq(
          next(r.grant_count for r in _mcgv().kept if r.name == "Helpful Org"), "3"))

check("a named fiscal sponsor routes the record to a human under the Rule 1 clause",
      lambda: assert_eq(
          next(r.unit_resolution_flag for r in _mcgv().kept if r.name == "Sponsored Thing"),
          "PENDING"))

check("the fiscal-sponsor note tells the coder never to enter both records", lambda: assert_in(
    "Never enter both",
    next(r.unit_resolution_note for r in _mcgv().kept if r.name == "Sponsored Thing")))

check("FORD refuses to run without a source_route column, because it is a two-source frame",
      lambda: assert_raises(ConfigError, lambda: read_frame(
          "FORD", {**MCGV_CFG, "lists_institutions": True,
                   "columns": {**MCGV_CFG["columns"], "source_route": None}},
          tmp_csv(MCGV_ROWS, list(MCGV_ROWS[0].keys())), "2026-10-01")))


# ------------------------------------------------------------------ generic

PITUN_CFG = {
    "block": "A", "admission_mechanism": "self_declaration", "frame_type": "identity",
    "reader": "generic", "lists_institutions": True,
    "columns": {"name": "institution", "website_url": "url", "location": "loc",
                "listing_text": "designee"},
}

GORG_CFG = {
    "block": "C", "admission_mechanism": "selection", "frame_type": "corporate_philanthropy",
    "reader": "generic", "lists_institutions": False,
    "cohorts": {"allowed": ["2019 AI Impact Challenge",
                            "2026 Impact Challenge: AI for Science"]},
    "columns": {"name": "org", "website_url": "url", "location": "loc", "cohort": "cohort"},
}

GORG_ROWS = [
    {"org": "Cohort Member", "url": "https://cm.org", "loc": "Chicago, IL",
     "cohort": "2019 AI Impact Challenge"},
    {"org": "Spore.Bio", "url": "https://spore.bio", "loc": "Paris",
     "cohort": "Inaugural AI for Science fund"},
]


def _gorg():
    return read_frame("GORG", GORG_CFG,
                      tmp_csv(GORG_ROWS, list(GORG_ROWS[0].keys())), "2026-10-01")


check("PIT-UN records all arrive PENDING under Rule 1, since the frame lists universities",
      lambda: assert_eq(
          [r.unit_resolution_flag for r in read_frame(
              "PITUN", PITUN_CFG,
              tmp_csv([{"institution": "State U", "url": "https://su.edu", "loc": "TX",
                        "designee": "Policy Lab"}],
                      ["institution", "url", "loc", "designee"]), "2026-10-01").kept],
          ["PENDING"]))

check("PIT-UN carries the frame's own listing text, which is what Rule 1 resolves against",
      lambda: assert_eq(
          read_frame("PITUN", PITUN_CFG,
                     tmp_csv([{"institution": "State U", "url": "https://su.edu", "loc": "TX",
                               "designee": "Policy Lab"}],
                             ["institution", "url", "loc", "designee"]),
                     "2026-10-01").kept[0].frame_listing_text, "Policy Lab"))

check("GORG keeps a record from a named cohort", lambda: assert_in(
    "Cohort Member", [r.name for r in _gorg().kept]))

check("GORG rejects the AI for Science page's 'previously funded recipients', which belong "
      "to an earlier fund and are not one of the four named cohorts", lambda: assert_not_in(
          "Spore.Bio", [r.name for r in _gorg().kept]))

check("GORG says in the drop log WHY the out-of-cohort record was dropped", lambda: assert_in(
    "not one of the four named cohorts", _gorg().dropped[0]["reason"]))

check("a cohort-defined frame refuses to run without a cohort column", lambda: assert_raises(
    ConfigError, lambda: read_frame(
        "GORG", {**GORG_CFG, "columns": {**GORG_CFG["columns"], "cohort": None}},
        tmp_csv(GORG_ROWS, list(GORG_ROWS[0].keys())), "2026-10-01")))


# -------------------------------------------------------------------- dedupe

A = rec(source_key="CTFG:00001", originating_frame="CTFG", block="B",
        name="Open Akron", website_url="https://openakron.org")
B = rec(source_key="CFA:00002", originating_frame="CFA", block="B",
        name="Open Akron", website_url="https://openakron.org")
C = rec(source_key="FORD:00003", originating_frame="FORD", block="A",
        name="Open Akron Inc.", website_url="https://openakron.org")
D = rec(source_key="FF:00004", originating_frame="FF", block="C",
        name="Totally Different", website_url="https://different.org")


check("dedupe proposes a cross-frame pair sharing a domain and a name", lambda: assert_true(
    any(p["a_source_key"] == "CTFG:00001" and p["b_source_key"] == "CFA:00002"
        for p in dd.propose_candidates([A, B, D]))))

check("dedupe does not propose an unrelated pair", lambda: assert_true(
    all("FF:00004" not in (p["a_source_key"], p["b_source_key"])
        for p in dd.propose_candidates([A, B, D]))))

check("dedupe flags a cross-BLOCK pair, which is the multi-frame subset the sensitivity "
      "check depends on", lambda: assert_eq(
          [p["cross_block"] for p in dd.propose_candidates([A, C])], ["YES"]))

check("dedupe gives a reason a coder can check against the sources", lambda: assert_in(
    "same registrable domain", dd.propose_candidates([A, B])[0]["why"]))

check("dedupe does not propose a within-frame pair — that is the reader's job", lambda: assert_eq(
    dd.propose_candidates([A, rec(source_key="CTFG:00009", originating_frame="CTFG",
                                  block="B", name="Open Akron",
                                  website_url="https://openakron.org")]), []))


def _apply(decisions, records=(A, B, C, D)):
    return dd.apply_merges(list(records), decisions)


check("apply_merges REFUSES an unreviewed pair rather than defaulting to separate",
      lambda: assert_raises(dd.MergeError, lambda: _apply(
          [{"decision": "", "a_source_key": "CTFG:00001", "b_source_key": "CFA:00002"}])))

check("apply_merges rejects a decision value that is neither MERGE nor SEPARATE",
      lambda: assert_raises(dd.MergeError, lambda: _apply(
          [{"decision": "maybe", "a_source_key": "CTFG:00001", "b_source_key": "CFA:00002"}])))

check("apply_merges collapses an accepted pair into one organization", lambda: assert_eq(
    len(_apply([{"decision": "MERGE", "a_source_key": "CTFG:00001",
                 "b_source_key": "CFA:00002"}])[0]), 3))

check("a merged organization keeps EVERY originating frame — the multi-frame record is the "
      "point, not a duplicate to discard", lambda: assert_eq(
          next(r.originating_frame for r in _apply(
              [{"decision": "MERGE", "a_source_key": "CTFG:00001", "b_source_key": "CFA:00002"}]
          )[0] if "CTFG" in r.originating_frame), "CTFG;CFA"))

check("merges are transitive: A~B and B~C collapse all three", lambda: assert_eq(
    len(_apply([{"decision": "MERGE", "a_source_key": "CTFG:00001", "b_source_key": "CFA:00002"},
                {"decision": "MERGE", "a_source_key": "CFA:00002", "b_source_key": "FORD:00003"}]
               )[0]), 2))

check("a transitive merge orders frames by the register, not by discovery", lambda: assert_eq(
    next(r.originating_frame for r in _apply(
        [{"decision": "MERGE", "a_source_key": "CTFG:00001", "b_source_key": "CFA:00002"},
         {"decision": "MERGE", "a_source_key": "CFA:00002", "b_source_key": "FORD:00003"}]
    )[0] if ";" in r.originating_frame), "FORD;CTFG;CFA"))

check("SEPARATE is recorded rather than silently dropped, so the judgment is on file",
      lambda: assert_eq(
          _apply([{"decision": "SEPARATE", "a_source_key": "CTFG:00001",
                   "b_source_key": "CFA:00002", "coder": "RA1"}])[1][0]["decision"],
          "SEPARATE"))

check("a PENDING unit resolution survives a merge rather than being lost to the survivor",
      lambda: assert_eq(
          next(r.unit_resolution_flag for r in dd.apply_merges(
              [A, rec(source_key="FORD:00007", originating_frame="FORD", block="A",
                      name="Open Akron", website_url="https://openakron.org",
                      unit_resolution_flag="PENDING", unit_resolution_note="Rule 1")],
              [{"decision": "MERGE", "a_source_key": "CTFG:00001",
                "b_source_key": "FORD:00007"}])[0]), "PENDING"))

check("org_ids are assigned after dedup and are stable across runs", lambda: (
    assert_eq([r.org_id for r in dd.assign_org_ids([A, B, C, D])],
              [r.org_id for r in dd.assign_org_ids([D, C, B, A])])))

check("org_ids follow register order, so FORD sorts ahead of CTFG", lambda: assert_eq(
    dd.assign_org_ids([A, C])[0].org_id, "TPG-00001") or assert_eq(
    dd.assign_org_ids([A, C])[0].originating_frame, "FORD"))


if __name__ == "__main__":
    print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
    for n, why in FAIL:
        print(f"  FAILED {n}: {why}")
    raise SystemExit(1 if FAIL else 0)
