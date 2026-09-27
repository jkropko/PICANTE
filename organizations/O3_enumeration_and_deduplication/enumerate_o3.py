#!/usr/bin/env python3
"""
enumerate_o3.py — O3: enumerate the frozen frames into a candidate pool.

    inspect             read a snapshot and print its columns / tag inventory,
                        so frames.json can be mapped to the real files
    enumerate           apply each frame's registered boundary; write the pool,
                        the boundary drops, the CTFG audit pools, the unit
                        resolution worksheet and a run manifest
    apply-resolutions   consume the reviewed Rule 1 worksheet: replace listed
                        institutions with the units the frames name, split
                        multi-unit listings, set aside unit_unresolved records
    dedupe-candidates   propose cross-frame duplicate pairs for human review
    apply-merges        consume the reviewed worksheet, merge, assign org_ids
    prisma              PRISMA-style accounting from the run manifest

ORDER MATTERS AND THE SCRIPT ENFORCES IT. `enumerate` refuses to run while the
operator list has an UNDECIDED entry or the freeze date is unset. `apply-merges`
refuses to run while any proposed pair is unreviewed. `apply-resolutions`
refuses while any Rule 1 row is unreviewed, and both dedup commands refuse a
pool that still carries a PENDING resolution, because dedup must compare the
units that will be coded, not the institutions the frames listed. Both refusals exist
because the alternative is a default that looks like a decision in the data
afterwards.

WHAT THIS SCRIPT DOES NOT DO
    C1, C2 (O4). The lexicon proxy and the queue (O5). Unit resolution,
    fiscal-sponsor routing and merges are human judgments: the script flags,
    queues and then consumes what a human decided.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import normalize as nz
import dedupe as dd
import frames_io
import resolutions as rs
from frames_io import (ConfigError, Record, FrameResult, read_frame, read_rows,
                       record_fields, PENDING)

SCRIPT_VERSION = "1.1.0"
HERE = Path(__file__).resolve().parent


# ------------------------------------------------------------------- helpers

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def read_records(path: Path) -> list[Record]:
    out = []
    with path.open(newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            r = Record()
            for k, v in row.items():
                if k in asdict(r):
                    setattr(r, k, v or "")
            out.append(r)
    return out


def check_operators(cfg: dict) -> list[dict]:
    """Rule 2 list must be closed before enumeration, because operators enter
    the pool by construction at this stage."""
    undecided = [e for e in cfg.get("undecided", [])
                 if (e.get("decision") or "UNDECIDED").upper() == "UNDECIDED"]
    if undecided:
        names = ", ".join(e["name"] for e in undecided)
        raise ConfigError(
            "the Rule 2 frame-operator list is still open: " + names + ".\n"
            "Operators enter the candidate pool by construction at O3, so the list must be "
            "closed before enumeration rather than during it. Set decision to IN or OUT for "
            "each entry in config/operators.json, with a dated note, and move any IN entry "
            "into `settled`."
        )
    return cfg.get("settled", [])


# ------------------------------------------------------------------- inspect

def cmd_inspect(args) -> int:
    frames = load_json(Path(args.config))["frames"]
    fc = args.frame.upper()
    if fc not in frames:
        print(f"unknown frame {fc}; known: {', '.join(frames)}", file=sys.stderr)
        return 2
    rows = read_rows(args.file)
    print(f"{fc}: {len(rows)} rows in {args.file}")
    if not rows:
        return 0
    keys: list[str] = []
    for r in rows[:2000]:
        for k in r:
            if k not in keys:
                keys.append(k)
    print(f"\n{len(keys)} columns. Non-empty counts over {min(len(rows), 2000)} rows:\n")
    for k in keys:
        n = sum(1 for r in rows[:2000] if str(r.get(k, "") or "").strip())
        sample = next((str(r.get(k)) for r in rows[:2000] if str(r.get(k, "") or "").strip()), "")
        print(f"  {k:<34} {n:>6}  e.g. {sample[:58]}")

    cfgf = frames[fc]
    tag_col = (cfgf.get("columns") or {}).get("tags")
    if tag_col and tag_col not in ("CONFIRM", None):
        counts: dict[str, int] = {}
        for r in rows:
            v = r.get(tag_col, "")
            vals = v if isinstance(v, (list, tuple)) else str(v or "").split(",")
            for t in vals:
                t = str(t).strip()
                if t:
                    counts[t] = counts.get(t, 0) + 1
        print(f"\nTag inventory from '{tag_col}' ({len(counts)} distinct):\n")
        for t, n in sorted(counts.items(), key=lambda kv: -kv[1]):
            print(f"  {n:>5}  {t}")
        print("\nSet tags.include_any / tags.exclude_any in frames.json from this list.")

    unset = [k for k, v in (cfgf.get("columns") or {}).items() if v == "CONFIRM"]
    if unset:
        print(f"\nStill CONFIRM in frames.json for {fc}: {', '.join(unset)}")
    return 0


# ----------------------------------------------------------------- enumerate

def cmd_enumerate(args) -> int:
    cfg = load_json(Path(args.config))
    ops_cfg = load_json(Path(args.operators))
    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    as_of = args.as_of or cfg.get("as_of")
    if not as_of:
        raise ConfigError(
            "no freeze date. Set `as_of` in frames.json (or pass --as-of). It is the single "
            "register freeze date, chosen without reference to any frame's contents, and it "
            "is written to date_identified on every record."
        )
    operators = check_operators(ops_cfg)

    sources = load_json(Path(args.sources))
    all_records: list[Record] = []
    dropped: list[dict] = []
    per_frame: dict = {}
    inputs: dict = {}

    for fc, fcfg in cfg["frames"].items():
        src = sources.get(fc)
        if not src:
            print(f"  {fc:<6} SKIPPED — no snapshot in sources.json")
            per_frame[fc] = {"status": "not enumerated", "reason": "no snapshot path given"}
            continue
        path = Path(src["path"])
        res: FrameResult = read_frame(fc, fcfg, path, as_of)
        all_records.extend(res.kept)
        dropped.extend(res.dropped)
        inputs[fc] = {"path": str(path), "sha256": sha256(path),
                      "pinned_commit": src.get("pinned_commit")}
        per_frame[fc] = {"status": "enumerated", **res.stats}
        print(f"  {fc:<6} kept {len(res.kept):>5}   dropped at boundary {len(res.dropped):>5}")
        if "name_labels_stripped" in res.stats:
            print(f"         name labels stripped: {res.stats['name_labels_stripped']}"
                  + (f"; in-scope names WITHOUT a label: {res.stats['in_scope_names_without_label']}"
                     if res.stats["in_scope_names_without_label"] else ""))

        for pool_name, pool_rows in (res.extra_pools or {}).items():
            if pool_rows:
                write_csv(outdir / f"{pool_name}.csv",
                          ["row", "name", "type", "country", "website"], pool_rows)
                print(f"         + {pool_name}.csv ({len(pool_rows)} records) for the O8 audit")

    # Rule 1, case by case. Frames flagged `lists_institutions` arrive PENDING
    # from their readers; elsewhere an institution arrives unflagged. Flag any
    # record whose name signals one, for a human to decide. AS_LISTED on the
    # worksheet disposes of a false positive.
    flagged_by_name: dict[str, int] = {}
    for r in all_records:
        if r.unit_resolution_flag == PENDING:
            continue
        sig = nz.institution_signal(r.name)
        if sig:
            r.unit_resolution_flag = PENDING
            r.unit_resolution_note = (
                f"POSSIBLE INSTITUTION (name signal: {sig}). Flagged by name, not by frame "
                f"configuration. If the listing is already an organization-level unit, "
                f"decide AS_LISTED. Otherwise Rule 1 applies: resolve only to a unit this "
                f"frame itself names, or UNIT_UNRESOLVED.")
            flagged_by_name[r.originating_frame] = flagged_by_name.get(r.originating_frame, 0) + 1
    if flagged_by_name:
        print("  flagged as possible institutions by name: " +
              ", ".join(f"{k} {v}" for k, v in flagged_by_name.items()))

    # Rule 2: operators enter by construction.
    for n, op in enumerate(operators, start=1):
        rec = Record(
            source_key=f"OPER:{n:03d}",
            originating_frame="OPERATOR",
            block="operator",
            admission_mechanism="none",
            frame_type="operator",
            date_identified=as_of,
            name=op["name"],
            website_url=op.get("website_url", ""),
            frame_operator="TRUE",
            frame_operated=op.get("frame_operated", ""),
            operator_status=op.get("operator_status", ""),
            notes=("AUTHOR-CONFLICTED. " if op.get("author_conflict") else "") +
                  "Rule 2 operator: enters by construction; excluded from every within-block "
                  "rate and from the saturation count. " + (op.get("note") or ""),
        )
        all_records.append(rec.finalize_keys())
    print(f"  {'OPER':<6} added {len(operators):>5}   (Rule 2, by construction)")

    write_csv(outdir / "enumerated_pool.csv", record_fields(),
              [asdict(r) for r in all_records])
    write_csv(outdir / "dropped_at_boundary.csv",
              ["frame", "row", "name", "reason", "type", "country", "raw"], dropped)

    pending = [asdict(r) for r in all_records if r.unit_resolution_flag == "PENDING"]
    write_csv(outdir / "unit_resolution_worksheet.csv", rs.WORKSHEET_FIELDS, pending)

    manifest = {
        "script": "enumerate_o3.py",
        "script_version": SCRIPT_VERSION,
        "normalize_version": nz.SCRIPT_VERSION,
        "frames_io_version": frames_io.SCRIPT_VERSION,
        "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "register_freeze_date": as_of,
        "inputs": inputs,
        "config_sha256": sha256(Path(args.config)),
        "operators_sha256": sha256(Path(args.operators)),
        "per_frame": per_frame,
        "operators_added": len(operators),
        "pool_before_cross_frame_dedup": len(all_records),
        "boundary_drops": len(dropped),
        "unit_resolution_pending": len(pending),
        "unit_resolution_pending_by_frame": {
            fc: sum(1 for r in pending if r["originating_frame"] == fc)
            for fc in dict.fromkeys(r["originating_frame"] for r in pending)},
        "flagged_as_possible_institution_by_name": flagged_by_name,
        "_note": "Counts here are pre-dedup and pre-screening. Nothing in this run applied "
                 "C1-C5, resolved a unit, routed a fiscal sponsor, or merged anything.",
    }
    (outdir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"\n  pool before cross-frame dedup: {len(all_records)}")
    print(f"  unit resolutions awaiting a human: {len(pending)}")
    print(f"  written to {outdir}/")
    return 0


# ---------------------------------------------------------- apply-resolutions

def cmd_apply_resolutions(args) -> int:
    records = read_records(Path(args.pool))
    rows = rs.read_worksheet(args.worksheet)
    pool, unresolved, known, log = rs.apply(records, rows)

    outdir = Path(args.out).parent
    outdir.mkdir(parents=True, exist_ok=True)
    write_csv(Path(args.out), record_fields(), [asdict(r) for r in pool])
    write_csv(outdir / "unit_unresolved.csv", record_fields(), [asdict(r) for r in unresolved])
    write_csv(outdir / "unit_known_not_surfaced.csv", rs.KNOWN_FIELDS, known)
    write_csv(outdir / "resolution_log.csv", rs.LOG_FIELDS, log)

    def by_frame(items, key):
        out: dict[str, dict[str, int]] = {}
        for it in items:
            fc, k = it["originating_frame"], it[key]
            out.setdefault(fc, {}).setdefault(k, 0)
            out[fc][k] += 1
        return out

    splits = sorted({r.parent_source_key for r in pool if r.parent_source_key})
    no_url = [r.source_key for r in pool if r.unit_resolution_flag == "resolved" and not r.website_url]
    manifest = {
        "script": "enumerate_o3.py apply-resolutions",
        "script_version": SCRIPT_VERSION,
        "resolutions_version": rs.SCRIPT_VERSION,
        "run_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "inputs": {"pool": {"path": args.pool, "sha256": sha256(Path(args.pool))},
                   "worksheet": {"path": args.worksheet, "sha256": sha256(Path(args.worksheet))}},
        "records_in": len(records),
        "pool_out": len(pool),
        "unit_unresolved": len(unresolved),
        "units_created_by_splits": sum(1 for r in pool if r.parent_source_key),
        "listings_split": len(splits),
        "known_not_surfaced": len(known),
        "decisions_by_frame": by_frame(log, "decision"),
        "sponsor_routing_by_frame": by_frame([l for l in log if l["sponsor_routing"]],
                                             "sponsor_routing"),
        "resolved_units_without_url": no_url,
        "_note": "unit_unresolved records are counted and excluded from full coding; they are "
                 "not in the pool that goes to dedup. known_not_surfaced units are never added "
                 "to the pool; they bound the frame for sensitivity check (h). Nothing here "
                 "applied C1-C5.",
    }
    (outdir / "resolution_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"{len(records)} records in -> {len(pool)} in the pool, "
          f"{len(unresolved)} unit_unresolved (set aside, counted)")
    if splits:
        print(f"  {len(splits)} listings split into {manifest['units_created_by_splits']} units")
    print(f"  {len(known)} known-but-not-surfaced units logged (never added)")
    if no_url:
        print(f"  WARNING: {len(no_url)} resolved units have no URL; the O5 lexicon proxy "
              f"cannot fetch them (see resolution_manifest.json)")
    for fc, d in manifest["decisions_by_frame"].items():
        print(f"  {fc:<6} " + ", ".join(f"{k} {v}" for k, v in sorted(d.items())))
    print(f"  -> {args.out}; next: dedupe-candidates --pool {args.out}")
    return 0


# ----------------------------------------------------------------- dedupe

def refuse_if_pending(records: list[Record], pool_path: str) -> None:
    n = sum(1 for r in records if r.unit_resolution_flag == PENDING)
    if n:
        raise ConfigError(
            f"{pool_path} still carries {n} PENDING unit resolutions. Dedup has to compare "
            f"the units that will be coded, not the institutions the frames listed, so Rule 1 "
            f"comes first: complete run/unit_resolution_worksheet.csv, run "
            f"`apply-resolutions`, and dedupe the pool it writes (run/resolved_pool.csv).")


def cmd_dedupe_candidates(args) -> int:
    records = read_records(Path(args.pool))
    refuse_if_pending(records, args.pool)
    rows = dd.propose_candidates(records, threshold=args.threshold)
    dd.write_candidates(args.out, rows)
    cross = sum(1 for r in rows if r["cross_block"] == "YES")
    print(f"{len(rows)} candidate pairs proposed ({cross} cross-block) -> {args.out}")
    print("Every pair needs MERGE or SEPARATE in the `decision` column, with a coder.")
    print("Cross-block pairs matter twice over: they are the multi-frame subset (sensitivity")
    print("check f), so a wrong merge there destroys the record that analysis depends on.")
    return 0


def cmd_apply_merges(args) -> int:
    records = read_records(Path(args.pool))
    refuse_if_pending(records, args.pool)
    with Path(args.decisions).open(newline="", encoding="utf-8-sig") as fh:
        decisions = list(csv.DictReader(fh))
    survivors, log = dd.apply_merges(records, decisions)
    survivors = dd.assign_org_ids(survivors, prefix=args.prefix)

    merged = sum(1 for d in log if d["decision"] == "MERGE")
    multi = sum(1 for r in survivors if ";" in r.originating_frame)
    outdir = Path(args.out).parent
    outdir.mkdir(parents=True, exist_ok=True)
    write_csv(Path(args.out), record_fields(), [asdict(r) for r in survivors])
    write_csv(outdir / "merge_log.csv", ["a", "b", "decision", "coder", "note"], log)

    print(f"{len(records)} records in, {len(survivors)} organizations out")
    print(f"  {merged} merges applied, {len(log) - merged} pairs kept separate")
    print(f"  {multi} organizations carry more than one originating frame")
    print(f"  org_ids assigned {args.prefix}-00001 upward -> {args.out}")
    return 0


# ------------------------------------------------------------------- prisma

def cmd_prisma(args) -> int:
    m = load_json(Path(args.manifest))
    print(f"PRISMA-style accounting — O3, register frozen {m['register_freeze_date']}\n")
    print(f"{'frame':<8}{'read':>9}{'kept':>9}{'dropped':>9}")
    total = 0
    for fc, st in m["per_frame"].items():
        if st.get("status") != "enumerated":
            print(f"{fc:<8}{'—':>9}{'—':>9}{'—':>9}   {st.get('reason','')}")
            continue
        read = st.get("rows_read") or st.get("grant_rows_read") or ""
        kept = st.get("kept") or st.get("organizations_after_within_frame_dedup") or 0
        total += kept
        print(f"{fc:<8}{read:>9}{kept:>9}{st.get('dropped', 0):>9}")
    print(f"\n{'sum':<8}{'':>9}{total:>9}")
    print(f"operators added by construction: {m['operators_added']}")
    print(f"pool before cross-frame dedup:   {m['pool_before_cross_frame_dedup']}")
    print(f"unit resolutions pending:        {m['unit_resolution_pending']}")
    rpath = Path(args.manifest).parent / "resolution_manifest.json"
    if rpath.exists():
        r = load_json(rpath)
        print(f"\nafter Rule 1 (apply-resolutions):")
        print(f"  pool going to dedup:            {r['pool_out']}")
        print(f"  unit_unresolved (set aside):    {r['unit_unresolved']}")
        print(f"  listings split / units created: {r['listings_split']} / {r['units_created_by_splits']}")
        print(f"  known, not surfaced (logged):   {r['known_not_surfaced']}")
    print("\nEvery figure above is a count over the ENUMERATED POOL. No screening has been "
          "applied, so none of it describes a population.")
    return 0


# ---------------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("inspect", help="print a snapshot's columns and tag inventory")
    p.add_argument("--frame", required=True)
    p.add_argument("--file", required=True)
    p.add_argument("--config", default=str(HERE / "config" / "frames.json"))
    p.set_defaults(fn=cmd_inspect)

    p = sub.add_parser("enumerate", help="apply boundaries and build the candidate pool")
    p.add_argument("--sources", required=True, help='JSON: {"CTFG": {"path": "..."} , ...}')
    p.add_argument("--out", default="run")
    p.add_argument("--as-of", default=None)
    p.add_argument("--config", default=str(HERE / "config" / "frames.json"))
    p.add_argument("--operators", default=str(HERE / "config" / "operators.json"))
    p.set_defaults(fn=cmd_enumerate)

    p = sub.add_parser("apply-resolutions", help="consume the reviewed Rule 1 worksheet")
    p.add_argument("--pool", default="run/enumerated_pool.csv")
    p.add_argument("--worksheet", default="run/unit_resolution_worksheet.csv")
    p.add_argument("--out", default="run/resolved_pool.csv")
    p.set_defaults(fn=cmd_apply_resolutions)

    p = sub.add_parser("dedupe-candidates", help="propose cross-frame duplicate pairs")
    p.add_argument("--pool", default="run/resolved_pool.csv")
    p.add_argument("--out", default="run/dedupe_candidates.csv")
    p.add_argument("--threshold", type=float, default=0.45)
    p.set_defaults(fn=cmd_dedupe_candidates)

    p = sub.add_parser("apply-merges", help="consume reviewed decisions, assign org_ids")
    p.add_argument("--pool", default="run/resolved_pool.csv")
    p.add_argument("--decisions", default="run/dedupe_candidates.csv")
    p.add_argument("--out", default="run/candidate_pool.csv")
    p.add_argument("--prefix", default="TPG")
    p.set_defaults(fn=cmd_apply_merges)

    p = sub.add_parser("prisma", help="accounting from the run manifest")
    p.add_argument("--manifest", default="run/run_manifest.json")
    p.set_defaults(fn=cmd_prisma)

    args = ap.parse_args()
    try:
        return args.fn(args)
    except (ConfigError, dd.MergeError, rs.ResolutionError) as e:
        print(f"\nREFUSED: {e}\n", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
