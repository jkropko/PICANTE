#!/usr/bin/env python3
"""
test_harness.py — tests for ai_harness.py and ai_metrics.py.

Run: python test_harness.py

These are written around the ways the pipeline can fail quietly, because a
harness that only proves the happy path works is the kind that lets a
fabricated quote through in month three. Each test names the failure it guards
against.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ai_harness as H
import ai_metrics as M

HERE = Path(__file__).resolve().parent
SPEC = H.load_fields(HERE / "fields.json")

PAGE = (
    "About Us\n"
    "Open Data Collective is a nonprofit based in Oakland, California. "
    "We build and maintain open civic data infrastructure for local government. "
    "Our 2026 annual report was published on 4 March 2026. "
    "We are a registered 501(c)(3) organization founded in 2014."
)

RECORD = {
    "org_id": "CTFG-0417",
    "sources": [{"source_id": "S1", "url": "https://example.org/about",
                 "access_date": "2026-11-03", "text": PAGE}],
    "frame_listing": {"frame_code": "CTFG", "listing_text": "Open Data Collective"},
}

PASSES = FAILS = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global PASSES, FAILS
    if cond:
        PASSES += 1
        print(f"  pass  {name}")
    else:
        FAILS += 1
        print(f"  FAIL  {name}" + (f"\n          {detail}" if detail else ""))


def span(needle: str) -> tuple[int, int]:
    i = PAGE.index(needle)
    return i, i + len(needle)


def ev(needle: str, **over) -> dict:
    s, e = span(needle)
    d = {"source_id": "S1", "start": s, "end": e, "quote": needle}
    d.update(over)
    return d


def role1_response(**over) -> str:
    fields = {
        "screening_C1_unit": {"value": "pass", "evidence": [ev("Open Data Collective is a nonprofit")], "note": ""},
        "screening_C2_us": {"value": "pass", "evidence": [ev("based in Oakland, California")], "note": ""},
        "unit_resolution_flag": {"value": "resolved", "evidence": [ev("Open Data Collective")], "note": ""},
        "unit_resolution_note": {"value": "undetermined", "evidence": [], "note": ""},
        "status": {"value": "active", "evidence": [ev("published on 4 March 2026")], "note": ""},
        "status_date": {"value": "2026-03-04", "evidence": [], "note": ""},
        "status_evidence": {"value": "2026 annual report", "evidence": [ev("Our 2026 annual report")], "note": ""},
        "ecosystem_role": {"value": ["practices"],
                            "evidence": [ev("We build and maintain open civic data infrastructure", **{"for": "practices"})], "note": ""},
        "org_form": {"value": "nonprofit", "evidence": [ev("registered 501(c)(3) organization")], "note": ""},
        "technologies": {"value": ["OD"], "evidence": [ev("open civic data infrastructure", **{"for": "OD"})], "note": ""},
        "partner_orgs_named": {"value": "undetermined", "evidence": [], "note": ""},
        "name": {"value": "Open Data Collective", "evidence": [ev("Open Data Collective")], "note": ""},
        "hq": {"value": "Oakland, California", "evidence": [ev("Oakland, California")], "note": ""},
        "focus": {"value": "open civic data", "evidence": [ev("open civic data infrastructure")], "note": ""},
        "projects": {"value": "undetermined", "evidence": [], "note": ""},
        "founded": {"value": "2014", "evidence": [ev("founded in 2014")], "note": ""},
        "mission": {"value": "undetermined", "evidence": [], "note": ""},
        "expertise": {"value": "undetermined", "evidence": [], "note": ""},
        "contact": {"value": "undetermined", "evidence": [], "note": ""},
        "funding_sources": {"value": "undetermined", "evidence": [], "note": ""},
    }
    fields.update(over.pop("fields", {}))
    body = {"org_id": "CTFG-0417", "injection_flag": False, "fields": fields}
    body.update(over)
    return json.dumps(body)


def role3_response(**over) -> str:
    fields = {
        "screening_C3_constitutive": {"value": "pass", "evidence": [ev("We build and maintain open civic data infrastructure")], "reasoning": "core activity is the infrastructure itself"},
        "screening_C4_public_benefit": {"value": "pass", "evidence": [ev("registered 501(c)(3) organization")], "reasoning": "nonprofit serving local government and public"},
        "screening_C5_funder_program": {"value": "n_a", "evidence": [], "reasoning": "not a funder"},
        "who_participates": {"value": "undetermined", "evidence": [], "reasoning": "not stated"},
        "who_benefits": {"value": "undetermined", "evidence": [], "reasoning": "not stated"},
        "what_counts_as_social_good": {"value": "undetermined", "evidence": [], "reasoning": "not stated"},
        "who_decides": {"value": "undetermined", "evidence": [], "reasoning": "not stated"},
        "what_counts_as_relevant_technology": {"value": "undetermined", "evidence": [], "reasoning": "not stated"},
    }
    fields.update(over.pop("fields", {}))
    return json.dumps({"org_id": "CTFG-0417", "injection_flag": False, "fields": fields})


def role2_response(cands) -> str:
    return json.dumps({"org_id": "CTFG-0417", "injection_flag": False, "candidates": cands})


def cand(needle: str, **over) -> dict:
    s, e = span(needle)
    sentence = next(x for x in PAGE.split(". ") if needle in x)
    d = {"source_id": "S1", "start": s, "end": e, "text_verbatim": needle,
         "sentence_verbatim": sentence, "heading_context_verbatim": "About Us"}
    d.update(over)
    return d


# ---------------------------------------------------------------------------

def test_fidelity_primitive():
    print("\nverbatim fidelity check")
    s, e = span("nonprofit")
    check("exact quote at correct offsets passes",
          H.check_quote("nonprofit", s, e, PAGE)[0] == "ok")
    check("quote present but at wrong offsets is offset_mismatch",
          H.check_quote("nonprofit", 0, 9, PAGE)[0] == "offset_mismatch")
    check("quote absent from the page is not_found — the fabrication case",
          H.check_quote("a leading civic tech intermediary", s, e, PAGE)[0] == "not_found")
    check("offsets past the end of the source are malformed",
          H.check_quote("nonprofit", 9000, 9009, PAGE)[0] == "malformed")
    check("whitespace-normalized near-miss does not pass",
          H.check_quote("Open  Data  Collective", *span("Open Data Collective"), PAGE)[0] != "ok")


def test_role1():
    print("\nRole 1 validation")
    r = H.validate(1, role1_response(), RECORD, SPEC)
    check("clean response is accepted whole", r.usable and all(f.accepted for f in r.fields),
          "; ".join(f"{f.field}: {f.errors}" for f in r.fields if not f.accepted))

    bad = role1_response(fields={"hq": {"value": "Oakland, California",
        "evidence": [{"source_id": "S1", "start": 10, "end": 40,
                      "quote": "headquartered in Oakland, California"}], "note": ""}})
    r = H.validate(1, bad, RECORD, SPEC)
    hq = next(f for f in r.fields if f.field == "hq")
    check("fabricated quote routes the field to a human",
          not hq.accepted and any("not_found" in e for e in hq.errors))
    check("other fields survive one bad field",
          sum(1 for f in r.fields if f.accepted) >= 18)

    bad = role1_response(fields={"status": {"value": "operational",
        "evidence": [ev("published on 4 March 2026")], "note": ""}})
    r = H.validate(1, bad, RECORD, SPEC)
    st = next(f for f in r.fields if f.field == "status")
    check("value outside the controlled list is rejected",
          not st.accepted and any("controlled list" in e for e in st.errors))

    bad = role1_response(fields={"org_form": {"value": "nonprofit", "evidence": [], "note": ""}})
    r = H.validate(1, bad, RECORD, SPEC)
    of = next(f for f in r.fields if f.field == "org_form")
    check("value with no evidence is rejected", not of.accepted)

    bad = role1_response(fields={"technologies": {"value": ["OD", "DS"],
        "evidence": [ev("open civic data infrastructure", **{"for": "OD"})], "note": ""}})
    r = H.validate(1, bad, RECORD, SPEC)
    t = next(f for f in r.fields if f.field == "technologies")
    check("multi-valued field with an unevidenced member is rejected",
          not t.accepted and any("DS" in e for e in t.errors))

    body = json.loads(role1_response())
    body["fields"]["who_decides"] = {"value": "the board", "evidence": []}
    r = H.validate(1, json.dumps(body), RECORD, SPEC)
    check("Role 1 straying into a Group 3 field rejects the record",
          not r.usable and any("who_decides" in e for e in r.record_errors))

    body = json.loads(role1_response())
    body["org_id"] = "CTFG-9999"
    r = H.validate(1, json.dumps(body), RECORD, SPEC)
    check("mismatched org_id rejects the record", not r.usable)

    body = json.loads(role1_response())
    del body["fields"]["founded"]
    r = H.validate(1, json.dumps(body), RECORD, SPEC)
    f = next(f for f in r.fields if f.field == "founded")
    check("missing field is routed, not silently skipped", not f.accepted)

    r = H.validate(1, "```json\n" + role1_response() + "\n```", RECORD, SPEC)
    check("code fence is stripped but noted as prompt drift",
          r.usable and any("fence" in n for n in r.notes))

    r = H.validate(1, "I'd be happy to help! " + role1_response(), RECORD, SPEC)
    check("preamble makes the response unparseable rather than half-parsed",
          not r.usable)

    body = json.loads(role1_response())
    body["injection_flag"] = True
    r = H.validate(1, json.dumps(body), RECORD, SPEC)
    check("injection flag surfaces as a note", r.injection_flag and any("instruction-like" in n for n in r.notes))

    long_quote = " ".join(["word"] * 30)
    rec2 = json.loads(json.dumps(RECORD))
    rec2["sources"][0]["text"] = PAGE + " " + long_quote
    body = json.loads(role1_response())
    start = len(PAGE) + 1
    body["fields"]["focus"] = {"value": "x", "evidence": [
        {"source_id": "S1", "start": start, "end": start + len(long_quote), "quote": long_quote}], "note": ""}
    r = H.validate(1, json.dumps(body), rec2, SPEC)
    fo = next(f for f in r.fields if f.field == "focus")
    check("over-long quote is rejected", not fo.accepted and any("25 words" in e for e in fo.errors))


def test_role2():
    print("\nRole 2 validation (passages only)")
    r = H.validate(2, role2_response([cand("nonprofit"), cand("open civic data infrastructure")]), RECORD, SPEC)
    check("clean candidates accepted", r.usable and len(r.candidates) == 2,
          "; ".join(f"{f.field}: {f.errors}" for f in r.fields if not f.accepted))

    r = H.validate(2, role2_response([cand("nonprofit", lexicon_term="civic tech")]), RECORD, SPEC)
    check("a candidate carrying a lexicon term rejects the record",
          not r.usable and any("propose no values" in e for e in r.record_errors))

    for key in ("tier", "placement", "speaker", "confidence_score", "category"):
        r = H.validate(2, role2_response([cand("nonprofit", **{key: "x"})]), RECORD, SPEC)
        check(f"candidate key {key!r} rejects the record", not r.usable)

    bad = cand("nonprofit")
    bad["sentence_verbatim"] = "Open Data Collective is a leading civic tech nonprofit."
    r = H.validate(2, role2_response([bad]), RECORD, SPEC)
    check("invented sentence context is caught",
          any(not f.accepted for f in r.fields))

    r = H.validate(2, role2_response([cand("open civic data infrastructure"), cand("nonprofit")]), RECORD, SPEC)
    check("out-of-order candidates are noted, not rejected",
          r.usable and any("out of document order" in n for n in r.notes))

    r = H.validate(2, role2_response([]), RECORD, SPEC)
    check("empty candidate list is a legitimate result", r.usable and not r.candidates)

    r = H.validate(2, role2_response([cand("nonprofit")] * 41), RECORD, SPEC)
    check("more candidates than the cap rejects the record", not r.usable)


def test_role3_and_sealing():
    print("\nRole 3 validation and blinding")
    r = H.validate(3, role3_response(), RECORD, SPEC)
    check("clean response accepted", r.usable and all(f.accepted for f in r.fields),
          "; ".join(f"{f.field}: {f.errors}" for f in r.fields if not f.accepted))

    bad = role3_response(fields={"screening_C3_constitutive": {
        "value": "pass", "evidence": [ev("We build and maintain open civic data infrastructure")], "reasoning": ""}})
    r = H.validate(3, bad, RECORD, SPEC)
    c3 = next(f for f in r.fields if f.field == "screening_C3_constitutive")
    check("missing reasoning is rejected", not c3.accepted)

    r = H.validate(3, role3_response(), RECORD, SPEC)
    c5 = next(f for f in r.fields if f.field == "screening_C5_funder_program")
    check("n_a needs no evidence", c5.accepted)

    body = json.loads(role3_response())
    body["fields"]["tier"] = {"value": "tier1", "evidence": []}
    r = H.validate(3, json.dumps(body), RECORD, SPEC)
    check("Role 3 straying into the self-label block rejects the record", not r.usable)

    tmp = Path(tempfile.mkdtemp())
    try:
        run = H.Run(tmp / "run")
        H.ingest(3, RECORD, role3_response(), run, SPEC, "draft-0.1", "claude-opus-5")

        open_log = run.proposals.read_text()
        check("sealed output does not leak into the open log",
              "screening_C3_constitutive" not in open_log and "commitment_sha256" in open_log)
        check("sealed file written", (run.sealed / "CTFG-0417.role3.json").exists())

        try:
            H.release_role3("CTFG-0417", run)
            released_early = True
        except SystemExit:
            released_early = False
        check("release refused before any adjudicated human value exists", not released_early)

        H.append_jsonl(run.decisions, {"ts_utc": H.now_utc(), "org_id": "CTFG-0417",
                                       "stage": "adjudicated",
                                       "fields": {"screening_C3_constitutive": "pass"}})
        doc = H.release_role3("CTFG-0417", run)
        check("release succeeds once the human value is recorded",
              doc.get("commitment_verified") is True)

        sealed_path = run.sealed / "CTFG-0417.role3.json"
        doc2 = json.loads(sealed_path.read_text())
        doc2["raw_response"] = role3_response(fields={"screening_C3_constitutive": {
            "value": "fail", "evidence": [], "reasoning": "changed after the fact"}})
        sealed_path.write_text(json.dumps(doc2))
        try:
            H.release_role3("CTFG-0417", run)
            tamper_caught = False
        except SystemExit as exc:
            tamper_caught = "SEAL BROKEN" in str(exc)
        check("tampering with sealed output after the fact is detected", tamper_caught)

        try:
            H.ingest(3, RECORD, role3_response(), run, SPEC, "draft-0.1", "claude-opus-5")
            second_allowed = True
        except SystemExit:
            second_allowed = False
        check("a second blind coding of the same record is refused", not second_allowed)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_metrics():
    print("\nmetrics")
    check("kappa on perfect agreement is 1.0",
          M.cohens_kappa([("a", "a"), ("b", "b"), ("a", "a"), ("b", "b")])[0] == 1.0)
    k, _ = M.cohens_kappa([("a", "b"), ("b", "a"), ("a", "b"), ("b", "a")])
    check("kappa on systematic disagreement is negative", k is not None and k < 0)
    k, note = M.cohens_kappa([("a", "a")] * 10)
    check("kappa undefined when one category is used throughout, with a note",
          k is None and "chance agreement is 1" in note)
    check("marginal skew detected", M.marginal_skew([("a", "a")] * 19 + [("b", "b")]) > 0.85)

    rows = M.agreement_table({"f": [("a", "a")] * 19 + [("b", "b")]},
                             SPEC["gates"], benchmark=0.60)
    check("skewed field is judged on percentage agreement",
          rows[0]["skewed"] and "percent agreement" in rows[0]["judged_on"])

    check("normalization folds case and whitespace", M.norm("  Civic  Tech ") == M.norm("civic tech"))
    check("normalization is order-insensitive for lists", M.norm(["b", "a"]) == M.norm(["a", "b"]))
    check("normalization does not forgive different words",
          M.norm("open data") != M.norm("open government data"))


def test_gate_end_to_end():
    print("\nRole 1 gate end to end")
    tmp = Path(tempfile.mkdtemp())
    try:
        run_dir = tmp / "run"
        run = H.Run(run_dir)
        # one clean record, one where the model gets hq wrong
        H.ingest(1, RECORD, role1_response(), run, SPEC, "draft-0.1", "claude-opus-5")
        rec2 = json.loads(json.dumps(RECORD)); rec2["org_id"] = "CTFG-0002"
        body = json.loads(role1_response()); body["org_id"] = "CTFG-0002"
        body["fields"]["hq"]["value"] = "Berkeley, California"
        H.ingest(1, rec2, json.dumps(body), run, SPEC, "draft-0.1", "claude-opus-5")

        truth = tmp / "truth.jsonl"
        with truth.open("w") as fh:
            for org in ("CTFG-0417", "CTFG-0002"):
                fh.write(json.dumps({"org_id": org, "fields": {
                    "hq": "Oakland, California", "screening_C2_us": "pass",
                    "org_form": "nonprofit"}}) + "\n")

        out = subprocess.run(
            [sys.executable, str(HERE / "ai_metrics.py"), "--run-dir", str(run_dir),
             "role1-gate", "--truth", str(truth)],
            capture_output=True, text=True)
        check("gate command runs", out.returncode in (0, 1), out.stderr[-400:])
        check("failing field is reported as below gate", "BELOW GATE" in out.stdout)
        check("hq accuracy computed as 50%", "50.0%" in out.stdout)
        check("nonzero exit when a field is below the gate", out.returncode == 1)

        out = subprocess.run(
            [sys.executable, str(HERE / "ai_harness.py"), "--run-dir", str(run_dir), "status"],
            capture_output=True, text=True)
        check("status command runs", out.returncode == 0 and "role 1:" in out.stdout,
              out.stderr[-400:])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_role2_recall_end_to_end():
    print("\nRole 2 recall end to end")
    tmp = Path(tempfile.mkdtemp())
    try:
        run_dir = tmp / "run"
        run = H.Run(run_dir)
        H.ingest(2, RECORD, role2_response([cand("nonprofit")]), run, SPEC,
                 "draft-0.1", "claude-opus-5")
        truth = tmp / "phrases.jsonl"
        truth.write_text(json.dumps({"org_id": "CTFG-0417", "selected_phrases":
            ["nonprofit", "open civic data infrastructure"]}) + "\n")
        out = subprocess.run(
            [sys.executable, str(HERE / "ai_metrics.py"), "--run-dir", str(run_dir),
             "role2-recall", "--truth", str(truth)],
            capture_output=True, text=True)
        check("recall command runs", out.returncode == 0, out.stderr[-400:])
        check("recall reported as 1/2", "1/2" in out.stdout)
        check("the missed phrase is listed for review",
              "open civic data infrastructure" in out.stdout)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_agreement_end_to_end():
    print("\nagreement commands end to end")
    tmp = Path(tempfile.mkdtemp())
    try:
        run_dir = tmp / "run"
        run = H.Run(run_dir)
        for i, (ai_c3, ra1, ra2) in enumerate([
                ("pass", "pass", "pass"), ("fail", "pass", "fail"),
                ("pass", "pass", "pass"), ("pass", "fail", "fail")]):
            org = f"ORG-{i}"
            rec = json.loads(json.dumps(RECORD)); rec["org_id"] = org
            body = json.loads(role3_response())
            body["org_id"] = org
            body["fields"]["screening_C3_constitutive"]["value"] = ai_c3
            if ai_c3 == "fail":
                body["fields"]["screening_C3_constitutive"]["evidence"] = []
                body["fields"]["screening_C3_constitutive"]["value"] = "undetermined"
            H.ingest(3, rec, json.dumps(body), run, SPEC, "draft-0.1", "claude-opus-5")
            for coder, val in (("RA1", ra1), ("RA2", ra2)):
                H.append_jsonl(run.decisions, {"ts_utc": H.now_utc(), "org_id": org,
                    "stage": "independent", "coder": coder,
                    "fields": {"screening_C3_constitutive": val}})
            H.append_jsonl(run.decisions, {"ts_utc": H.now_utc(), "org_id": org,
                "stage": "adjudicated",
                "fields": {"screening_C3_constitutive": ra2}})
            H.release_role3(org, run)

        out = subprocess.run([sys.executable, str(HERE / "ai_metrics.py"),
                              "--run-dir", str(run_dir), "ra-agreement"],
                             capture_output=True, text=True)
        check("ra-agreement runs", out.returncode == 0, out.stderr[-400:])
        check("ra-agreement reports the benchmark verdict",
              "benchmark 0.6" in out.stdout and "screening_C3_constitutive" in out.stdout)

        out = subprocess.run([sys.executable, str(HERE / "ai_metrics.py"),
                              "--run-dir", str(run_dir), "role3-agreement"],
                             capture_output=True, text=True)
        check("role3-agreement runs on released records only", out.returncode == 0,
              out.stderr[-400:])
        check("role3-agreement states it carries no benchmark",
              "no gate" in out.stdout.lower() or "Descriptive only" in out.stdout)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    print("harness tests")
    test_fidelity_primitive()
    test_role1()
    test_role2()
    test_role3_and_sealing()
    test_metrics()
    test_gate_end_to_end()
    test_role2_recall_end_to_end()
    test_agreement_end_to_end()
    print(f"\n{PASSES} passed, {FAILS} failed")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
