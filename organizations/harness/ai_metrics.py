#!/usr/bin/env python3
"""
ai_metrics.py — the reportable statistics for the organizational strand.

    role1-gate     field-level accuracy per Group 1 field against hand-coded
                   values. Registered gate: 95%. Any field below it after
                   prompt revision is coded by an RA with no AI help, and that
                   is reported.
    role2-recall   whether the passages Role 2 returned contained the phrase
                   the human coder actually selected. Reported, no gate.
    role3-agreement  human-to-AI agreement per Group 3 field, computed only on
                   released records.
    ra-agreement   RA-to-RA agreement per Group 3 field — the reliability
                   figure the study reports at calibration, midpoint and end.
                   Benchmark 0.60.

WHY THE TWO AGREEMENT COMMANDS ARE SEPARATE
    They are the same arithmetic and they mean opposite things. RA-to-RA kappa
    is a property of the instrument and carries a benchmark. Human-to-AI kappa
    is descriptive and carries none: Role 3 never contributes to a coded value,
    so a low figure is a finding about the model, not a failure of the codebook.
    Keeping them in one table invites the reader to compare them.

KAPPA
    Cohen's kappa on the adjudicated values. Where one category takes more than
    the threshold share of codings, kappa is unstable and percentage agreement
    is reported alongside it, per the registered rule.

USAGE
    python ai_metrics.py role1-gate --truth handcoded.jsonl
    python ai_metrics.py role2-recall --truth selected_phrases.jsonl
    python ai_metrics.py role3-agreement
    python ai_metrics.py ra-agreement
    python ai_metrics.py role1-gate --truth handcoded.jsonl --json out.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from ai_harness import Run, load_fields, read_jsonl

WS = re.compile(r"\s+")


def norm(v):
    """Normalize a value for comparison.

    Whitespace and case only. We do not stem, strip punctuation, or map
    synonyms: on free-text fields the extraction is supposed to be verbatim,
    and a comparison that forgives near-misses would report an accuracy the
    verbatim requirement does not support.
    """
    if isinstance(v, list):
        return tuple(sorted(norm(x) for x in v))
    if isinstance(v, str):
        return WS.sub(" ", v).strip().casefold()
    return v


# ---------------------------------------------------------------------------
# agreement statistics
# ---------------------------------------------------------------------------

def cohens_kappa(pairs: list[tuple]) -> tuple[float | None, str]:
    """Cohen's kappa. Returns (kappa, note); kappa is None where undefined."""
    n = len(pairs)
    if n == 0:
        return None, "no paired codings"
    cats = sorted({c for p in pairs for c in p}, key=str)
    po = sum(1 for a, b in pairs if a == b) / n
    pe = 0.0
    for c in cats:
        pa = sum(1 for a, _ in pairs if a == c) / n
        pb = sum(1 for _, b in pairs if b == c) / n
        pe += pa * pb
    if abs(1 - pe) < 1e-12:
        return None, ("kappa undefined: both coders used a single category for "
                      "every record, so chance agreement is 1")
    return (po - pe) / (1 - pe), ""


def marginal_skew(pairs: list[tuple]) -> float:
    """Share held by the most common category across both coders."""
    if not pairs:
        return 0.0
    flat = [c for p in pairs for c in p]
    return max(flat.count(c) for c in set(flat)) / len(flat)


def agreement_table(pairs_by_field: dict[str, list[tuple]], gates: dict,
                    benchmark: float | None) -> list[dict]:
    rows = []
    for field, pairs in sorted(pairs_by_field.items()):
        k, note = cohens_kappa(pairs)
        po = sum(1 for a, b in pairs if a == b) / len(pairs) if pairs else 0.0
        skew = marginal_skew(pairs)
        skewed = skew > gates["skewed_marginal_threshold"]
        row = {
            "field": field, "n": len(pairs), "percent_agreement": round(po, 4),
            "kappa": None if k is None else round(k, 4),
            "kappa_note": note,
            "marginal_skew": round(skew, 4),
            "skewed": skewed,
        }
        if benchmark is not None:
            if skewed or k is None:
                row["meets_benchmark"] = po >= gates["skewed_percent_agreement_benchmark"]
                row["judged_on"] = "percent agreement (marginals too skewed for kappa)"
            else:
                row["meets_benchmark"] = k >= benchmark
                row["judged_on"] = "kappa"
        rows.append(row)
    return rows


def print_agreement(rows: list[dict], benchmark: float | None, title: str) -> None:
    print(f"\n{title}")
    print(f"{'field':38} {'n':>5} {'% agr':>7} {'kappa':>7}  verdict")
    print("-" * 78)
    for r in rows:
        k = "n/a" if r["kappa"] is None else f"{r['kappa']:.3f}"
        verdict = ""
        if benchmark is not None:
            verdict = "meets" if r.get("meets_benchmark") else "BELOW"
            if r["skewed"] or r["kappa"] is None:
                verdict += " (on % agreement)"
        print(f"{r['field'][:38]:38} {r['n']:>5} {r['percent_agreement']*100:>6.1f}% "
              f"{k:>7}  {verdict}")
        if r["kappa_note"]:
            print(f"{'':38}       {r['kappa_note']}")


# ---------------------------------------------------------------------------
# role 1 gate
# ---------------------------------------------------------------------------

def cmd_role1_gate(args, spec, run) -> int:
    """Field-level accuracy against hand-coded values.

    Truth file: JSONL, one object per record:
        {"org_id": "...", "fields": {"screening_C2_us": "pass", ...}}
    """
    truth = {t["org_id"]: t.get("fields", {}) for t in read_jsonl(Path(args.truth))}
    if not truth:
        sys.exit(f"no records in {args.truth}")

    props = [p for p in read_jsonl(run.proposals) if p.get("role") == 1]
    if not props:
        sys.exit("no Role 1 proposals logged")

    per_field: dict[str, dict] = {}
    for p in props:
        org, field = p.get("org_id"), p.get("field")
        if org not in truth or field not in truth[org]:
            continue
        s = per_field.setdefault(field, {"n": 0, "correct": 0, "routed": 0,
                                         "wrong": [], "fabricated": 0})
        s["n"] += 1
        if p.get("routed_to_human_unaided"):
            # A field the harness rejected is not a correct proposal. Counting
            # only what survived validation would report the accuracy of the
            # model's well-formed output rather than of the model.
            s["routed"] += 1
            if any(f.get("verdict") == "not_found" for f in p.get("fidelity", [])):
                s["fabricated"] += 1
            continue
        if norm(p.get("proposed_value")) == norm(truth[org][field]):
            s["correct"] += 1
        else:
            s["wrong"].append((org, p.get("proposed_value"), truth[org][field]))

    gate = spec["gates"]["role1_field_accuracy"]
    print(f"\nRole 1 gate: field-level accuracy against hand-coded values "
          f"(threshold {gate:.0%})")
    print(f"{'field':30} {'n':>5} {'correct':>8} {'routed':>7} {'accuracy':>9}  verdict")
    print("-" * 78)
    rows, failing = [], []
    for field, s in sorted(per_field.items()):
        acc = s["correct"] / s["n"] if s["n"] else 0.0
        ok = acc >= gate
        if not ok:
            failing.append(field)
        rows.append({"field": field, **{k: s[k] for k in ("n", "correct", "routed", "fabricated")},
                     "accuracy": round(acc, 4), "meets_gate": ok,
                     "disagreements": [{"org_id": o, "proposed": pv, "hand_coded": tv}
                                       for o, pv, tv in s["wrong"]]})
        print(f"{field[:30]:30} {s['n']:>5} {s['correct']:>8} {s['routed']:>7} "
              f"{acc:>8.1%}  {'meets' if ok else 'BELOW GATE'}")

    fab = sum(s["fabricated"] for s in per_field.values())
    print(f"\nquotes not found in the cited source: {fab}")
    if fab:
        print("  Each is the model returning text that was not on the page. Report "
              "this count; it is the number that matters to a reader assessing the "
              "AI-assisted workflow.")
    if failing:
        print(f"\n{len(failing)} field(s) below the gate: {', '.join(failing)}")
        print("Revise the prompt and re-validate. Any field still below the gate "
              "after revision is coded by an RA with no AI assistance, and that is "
              "reported.")
    else:
        print("\nAll fields meet the gate. Record this result and the prompt version "
              "before running Role 1 over any analytic record.")

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"gate": gate, "fields": rows, "quotes_not_found": fab}, indent=2))
    return 1 if failing else 0


# ---------------------------------------------------------------------------
# role 2 recall
# ---------------------------------------------------------------------------

def cmd_role2_recall(args, spec, run) -> int:
    """Did the returned passages contain the phrase the coder selected?

    Truth file: JSONL, one object per record:
        {"org_id": "...", "selected_phrases": ["...", "..."]}
    """
    truth = {t["org_id"]: t.get("selected_phrases", [])
             for t in read_jsonl(Path(args.truth))}
    props = {p["org_id"]: p for p in read_jsonl(run.proposals) if p.get("role") == 2}

    total = found = 0
    missed: list[tuple[str, str]] = []
    no_output: list[str] = []

    for org, phrases in truth.items():
        p = props.get(org)
        if p is None:
            no_output.append(org)
            continue
        hay = [norm(c.get("text_verbatim", "")) for c in p.get("candidates", [])]
        hay += [norm(c.get("sentence_verbatim", "")) for c in p.get("candidates", [])]
        for phrase in phrases:
            total += 1
            n = norm(phrase)
            if any(n in h for h in hay):
                found += 1
            else:
                missed.append((org, phrase))

    recall = found / total if total else 0.0
    print(f"\nRole 2 passage recall: {found}/{total} = {recall:.1%}")
    print("Reported, not gated: a missed passage costs the coder search time, "
          "and they read the page regardless.")
    if no_output:
        print(f"\n{len(no_output)} record(s) with coded phrases but no Role 2 output: "
              f"{', '.join(sorted(no_output)[:8])}"
              + (" …" if len(no_output) > 8 else ""))
    if missed:
        print(f"\n{len(missed)} phrase(s) the coder found and Role 2 did not:")
        for org, phrase in missed[:20]:
            print(f"  {org}: {phrase[:70]}")
        print("Read these before revising the prompt. A pattern here — non-lexicon "
              "phrasing, footer text, third-party descriptions — is more useful than "
              "the headline figure.")
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"recall": recall, "found": found, "total": total,
             "missed": [{"org_id": o, "phrase": p} for o, p in missed],
             "records_without_output": no_output}, indent=2))
    return 0


# ---------------------------------------------------------------------------
# agreement commands
# ---------------------------------------------------------------------------

def _released_values(run: Run) -> dict[str, dict]:
    out = {}
    for path in run.released.glob("*.role3.json"):
        doc = json.loads(path.read_text(encoding="utf-8"))
        vals = {f["field"]: f["proposed_value"] for f in doc.get("fields", [])
                if f.get("accepted")}
        out[doc["org_id"]] = vals
    return out


def cmd_role3_agreement(args, spec, run) -> int:
    ai = _released_values(run)
    sealed = len(list(run.sealed.glob("*.role3.json")))
    if not ai:
        sys.exit(f"no released Role 3 records. {sealed} are sealed; release them "
                 f"with ai_harness.py release-role3 once the adjudicated human "
                 f"values are recorded.")
    if len(ai) < sealed:
        print(f"note: computing on {len(ai)} released of {sealed} sealed records. "
              f"A figure computed on a subset chosen by which records happened to "
              f"be released is not the reportable figure.")

    human = {d["org_id"]: d.get("fields", {}) for d in read_jsonl(run.decisions)
             if d.get("stage") == "adjudicated"}
    fields = list(spec["role3"]["fields"])
    pairs = {f: [] for f in fields}
    for org, vals in ai.items():
        h = human.get(org, {})
        for f in fields:
            if f in vals and f in h:
                pairs[f].append((norm(h[f]), norm(vals[f])))
    pairs = {f: p for f, p in pairs.items() if p}

    rows = agreement_table(pairs, spec["gates"], benchmark=None)
    print_agreement(rows, None, f"Human-to-AI agreement, Role 3 "
                                f"({len(ai)} released records)")
    print("\nDescriptive only. Role 3 has no gate and never contributes to a coded "
          "value; a low figure here says something about the model, not about the "
          "instrument's reliability.")
    if args.json:
        Path(args.json).write_text(json.dumps({"records": len(ai), "fields": rows}, indent=2))
    return 0


def cmd_ra_agreement(args, spec, run) -> int:
    """RA-to-RA agreement from the decisions log.

    Decisions file: JSONL, with independent codings recorded before adjudication:
        {"org_id": "...", "stage": "independent", "coder": "RA1",
         "fields": {"screening_C3_constitutive": "pass", ...}}
    """
    by_org: dict[str, dict[str, dict]] = {}
    for d in read_jsonl(run.decisions):
        if d.get("stage") != "independent":
            continue
        by_org.setdefault(d["org_id"], {})[d.get("coder", "?")] = d.get("fields", {})

    usable = {o: c for o, c in by_org.items() if len(c) >= 2}
    if not usable:
        sys.exit("no records with two independent codings in the decisions log")

    fields = list(spec["role3"]["fields"])
    pairs = {f: [] for f in fields}
    for org, coders in usable.items():
        names = sorted(coders)[:2]
        a, b = coders[names[0]], coders[names[1]]
        for f in fields:
            if f in a and f in b:
                pairs[f].append((norm(a[f]), norm(b[f])))
    pairs = {f: p for f, p in pairs.items() if p}

    bench = spec["gates"]["role3_kappa_benchmark"]
    rows = agreement_table(pairs, spec["gates"], benchmark=bench)
    print_agreement(rows, bench, f"RA-to-RA agreement, Group 3 fields "
                                 f"({len(usable)} double-coded records, "
                                 f"benchmark {bench})")
    below = [r["field"] for r in rows if not r.get("meets_benchmark")]
    if below:
        print(f"\nBelow benchmark: {', '.join(below)}")
        print("Double coding is kept regardless. A field still below benchmark "
              "after revision is reported with its statistic, used descriptively, "
              "and excluded from comparisons across blocks or frames.")
    if args.json:
        Path(args.json).write_text(json.dumps(
            {"records": len(usable), "benchmark": bench, "fields": rows}, indent=2))
    return 0


# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-dir", default="run")
    ap.add_argument("--fields", default=str(Path(__file__).resolve().parent / "fields.json"))
    ap.add_argument("--json", help="also write the result to this path")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("role1-gate")
    p.add_argument("--truth", required=True, help="hand-coded values, JSONL")
    p.set_defaults(func=cmd_role1_gate)

    p = sub.add_parser("role2-recall")
    p.add_argument("--truth", required=True, help="coder-selected phrases, JSONL")
    p.set_defaults(func=cmd_role2_recall)

    sub.add_parser("role3-agreement").set_defaults(func=cmd_role3_agreement)
    sub.add_parser("ra-agreement").set_defaults(func=cmd_ra_agreement)

    args = ap.parse_args()
    spec = load_fields(Path(args.fields))
    return args.func(args, spec, Run(Path(args.run_dir)))


if __name__ == "__main__":
    sys.exit(main())
