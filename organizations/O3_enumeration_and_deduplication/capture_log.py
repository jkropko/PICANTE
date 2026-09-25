#!/usr/bin/env python3
"""
capture_log.py — close out O2: hash the snapshots, log the capture, write sources.json.

    log      walk the snapshot tree, hash every file, pull the CFA commit SHA,
             check each frame against its registered size estimate, and emit
             capture_log.json + sources.json
    verify   re-hash against an existing capture_log.json and report any file
             that has moved, changed or vanished since the freeze

WHY HASH AT ALL
    The freeze is the one step in this strand that cannot be repeated. A hash
    taken on the freeze date is what lets you demonstrate, later, that the file
    O3 enumerated is the file O2 captured — not a re-download that quietly
    picked up a newer roster. `enumerate` hashes its inputs again into
    run_manifest.json, so a mismatch between the two is a real signal.

EXPECTED LAYOUT
    snapshots/
      CTFG/  civic_tech_field_guide_full_export.csv
             wayback.txt          <- one archive URL per line, optional but checked
      CFA/   brigade-information/ <- a git clone; the commit SHA is read from it
             organizations.json
      FORD/  ford_live_grants.csv
             ford_990pf_2011_2025.csv
             primary.txt          <- names which file enumerate should read
      ...

    A directory holding one data file needs no primary.txt. A directory holding
    several needs one, because guessing which export is the frame of record is
    exactly the kind of silent decision this stage exists to prevent.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_VERSION = "1.2.0"
HERE = Path(__file__).resolve().parent

# Python caps a single CSV field at 128 KB. The Civic Tech Field Guide export
# carries long free-text fields across its 86 columns and exceeds that, which
# surfaces as "_csv.Error: field larger than field limit (131072)" rather than
# as anything describing the data. Raise the cap as far as the platform allows.
def _raise_csv_field_limit() -> None:
    limit = sys.maxsize
    while True:
        try:
            csv.field_size_limit(limit)
            return
        except OverflowError:
            limit //= 10


_raise_csv_field_limit()

# .yml/.yaml matter: the ACT frame of record is act_members.yml, copied from
# the pinned Jekyll repo. Omitting the suffix made that frame read as EMPTY —
# a captured frame reported as missing, which is the wrong kind of wrong.
DATA_SUFFIXES = {".csv", ".json", ".tsv", ".xlsx", ".xls", ".yml", ".yaml"}
SIDECAR_NAMES = {"primary.txt", "wayback.txt", "notes.txt", "notes.md", "commit.txt"}

# Frames whose rows legitimately arrive in more than one file. For these, ALL
# data files are the frame and enumerate reads them together; primary.txt does
# not apply, because there is no single file of record to name.
# Frames whose rows legitimately arrive in more than one file, so that ALL
# data files are the frame and primary.txt does not apply.
#
# EMPTY as of 2026-09-24. FORD was the only entry: the register defined it as
# the live database plus a 990-PF tail. That second source was dropped once
# the capture showed the live database already reaches back to 2011, so FORD
# is single-source and its primary.txt governs. Leaving it here would have
# handed the enumerator the grants CSV plus all 44 raw API pages as one frame.
MULTI_SOURCE: dict[str, str] = {}

# Register estimates, sheet 2. Warnings only — never a refusal. A count outside
# the estimate may mean the frame moved since the register was written, which
# is a finding, or it may mean the wrong file was saved, which is a mistake.
# The script cannot tell which, so it says so and leaves it to you.
EXPECTED = {
    "CTFG": (8000, None, "the FULL export is ~12,114 records across 86 columns. A count in "
                         "the low thousands usually means the boundary filter was applied at "
                         "capture — which would leave the two O8 audit pools with nothing to "
                         "draw from, since both sit OUTSIDE the boundary."),
    "CFA":  (150, 400, "organizations.json held 221 records when the register was written, "
                       "181 of them tagged Brigade."),
    "PITUN": (30, 120, "roughly 48-59 US members expected; New America reported 64 member "
                       "institutions in 2023, so a lower count may be real attrition and a "
                       "finding for the field-dynamics analysis."),
    "ACT":  (10, 60, "~18-25 members; first official list published February 2025."),
    "FF":   (40, 250, "~100 portfolio organizations."),
    "MCGV": (200, 2000, "the unit here is GRANTS, not organizations — ~795 grants expected, "
                        "collapsing to well under 100 after dedup and screening."),
    "GORG": (10, 200, "~20 participants per cohort, globally recruited, across the three "
                      "capturable cohorts."),
    "FORD": (50, 3000, "100-300 grantees expected across the live database and the 990-PF tail."),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit(path: Path) -> str | None:
    """Commit SHA of a git working tree, or None. CFA is pinned to a commit
    rather than a date, which makes it the most reproducible frame here."""
    for cand in [path] + [p for p in path.iterdir() if p.is_dir()] if path.is_dir() else []:
        if (cand / ".git").exists():
            try:
                out = subprocess.run(["git", "-C", str(cand), "rev-parse", "HEAD"],
                                     capture_output=True, text=True, timeout=20)
                if out.returncode == 0 and out.stdout.strip():
                    return out.stdout.strip()
            except (OSError, subprocess.SubprocessError):
                return None
    return None


def read_sidecar(d: Path, name: str) -> list[str]:
    """Non-empty, non-comment lines from a sidecar file.

    The wayback.txt files carry substantial commentary — which page each
    snapshot covers, what it does and does not prove, why a save failed. An
    earlier version counted every non-empty line, so a frame with five
    archived pages reported ninety-three archive URLs. A count that inflates
    with the quality of the notes is worse than no count.
    """
    p = d / name
    if not p.exists():
        return []
    return [l.strip() for l in p.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.lstrip().startswith("#")]


def data_files(d: Path) -> list[Path]:
    return sorted(p for p in d.rglob("*")
                  if p.is_file()
                  and p.suffix.lower() in DATA_SUFFIXES
                  and p.name not in SIDECAR_NAMES
                  and ".git" not in p.parts)


def count_rows(p: Path) -> int | None:
    """Row count for the size checks. None where the file cannot be read.

    Deliberately self-contained: this script imports nothing from the rest of
    the toolkit, so an import path problem cannot stop the capture log being
    written on the freeze day. It still READS config/frames.json for the
    register's frame list, so run it from the toolkit directory — or pass
    --config.
    """
    try:
        suf = p.suffix.lower()
        if suf in (".yml", ".yaml"):
            import yaml
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        elif suf == ".json":
            data = json.loads(p.read_text(encoding="utf-8"))
        elif suf in (".csv", ".tsv"):
            delim = "\t" if suf == ".tsv" else ","
            with p.open(newline="", encoding="utf-8-sig", errors="replace") as fh:
                return sum(1 for _ in csv.reader(fh, delimiter=delim)) - 1
        else:
            return None

        if isinstance(data, dict):
            for key in ("organizations", "records", "data", "items", "members", "grants"):
                if isinstance(data.get(key), list):
                    return len(data[key])
            return None
        return len(data) if isinstance(data, list) else None
    except Exception:  # noqa: BLE001
        return None


def cmd_log(args) -> int:
    root = Path(args.snapshots)
    if not root.is_dir():
        print(f"snapshot directory not found: {root}", file=sys.stderr)
        return 2
    cfg = json.loads((Path(args.config)).read_text(encoding="utf-8"))
    as_of = args.as_of or cfg.get("as_of")
    if not as_of:
        print("REFUSED: no freeze date. Set `as_of` in frames.json or pass --as-of.\n"
              "It is the single register freeze date and belongs on every record.",
              file=sys.stderr)
        return 3

    frames_cfg = cfg["frames"]
    entries: dict = {}
    sources: dict = {}
    warnings: list[str] = []
    problems: list[str] = []

    for fc in frames_cfg:
        d = root / fc
        if not d.is_dir():
            problems.append(f"{fc}: no directory at {d} — frame not captured")
            entries[fc] = {"status": "not captured"}
            continue

        files = data_files(d)
        if not files:
            problems.append(f"{fc}: directory exists but holds no data file")
            entries[fc] = {"status": "empty"}
            continue

        primary_names = read_sidecar(d, "primary.txt")
        multi = fc in MULTI_SOURCE
        if multi:
            primary = files[0]
            if len(files) < 2:
                warnings.append(f"{fc}: only one data file captured. {MULTI_SOURCE[fc]}")
        elif len(files) == 1:
            primary = files[0]
        elif primary_names:
            match = [p for p in files if p.name == primary_names[0]]
            if not match:
                problems.append(f"{fc}: primary.txt names {primary_names[0]!r}, which is not "
                                f"among the captured files")
                entries[fc] = {"status": "primary not found"}
                continue
            primary = match[0]
        else:
            problems.append(
                f"{fc}: {len(files)} data files and no primary.txt. Name the file enumerate "
                f"should read — guessing which export is the frame of record is not this "
                f"script's decision to make.")
            entries[fc] = {"status": "primary ambiguous",
                           "files": [p.name for p in files]}
            continue

        wayback = read_sidecar(d, "wayback.txt")
        if not wayback:
            warnings.append(f"{fc}: no wayback.txt. The register requires an archived capture "
                            f"of every frame source page on the freeze date.")

        commit = git_commit(d) or (read_sidecar(d, "commit.txt") or [None])[0]
        if fc == "CFA" and not commit:
            problems.append("CFA: no commit SHA. This frame is pinned to a COMMIT, not a date "
                            "— it is the only exactly reproducible frame in the register, and "
                            "a dated copy gives that up.")

        n = sum(x for x in (count_rows(p) for p in files) if x is not None) if multi \
            else count_rows(primary)
        if n is not None and fc in EXPECTED:
            lo, hi, why = EXPECTED[fc]
            if lo is not None and n < lo:
                warnings.append(f"{fc}: {n} rows, below the register's estimate. {why}")
            elif hi is not None and n > hi:
                warnings.append(f"{fc}: {n} rows, above the register's estimate. {why}")

        entries[fc] = {
            "status": "captured",
            "primary_file": (", ".join(str(p.relative_to(root)) for p in files) if multi
                             else str(primary.relative_to(root))),
            "primary_sha256": sha256(primary),
            "primary_rows": n,
            "multi_source": multi,
            "all_files": [
                {"path": str(p.relative_to(root)), "sha256": sha256(p),
                 "bytes": p.stat().st_size, "rows": count_rows(p)}
                for p in files
            ],
            "pinned_commit": commit,
            "wayback": wayback,
            "notes": read_sidecar(d, "notes.txt") + read_sidecar(d, "notes.md"),
        }
        sources[fc] = ({"paths": [str(p) for p in files], "pinned_commit": commit} if multi
                       else {"path": str(primary), "pinned_commit": commit})

    # Cohorts recorded as pending are a registered state, not an omission.
    pending = (frames_cfg.get("GORG", {}).get("cohorts", {}) or {}).get("pending", [])
    if pending:
        warnings.append(
            "GORG pending cohorts: " + "; ".join(pending) + ". Enumerate each when its list "
            "publishes and record THAT date separately from the freeze date. Keep the dated "
            "capture of the page as it stood at freeze, with no list on it — that capture is "
            "the evidence the cohort was unpublished rather than overlooked.")

    log = {
        "script": "capture_log.py",
        "script_version": SCRIPT_VERSION,
        "logged_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "register_freeze_date": as_of,
        "snapshot_root": str(root.resolve()),
        "config_sha256": sha256(Path(args.config)),
        "frames": entries,
        "pending_cohorts": pending,
        "warnings": warnings,
        "problems": problems,
        "_note": "Hashes are of the files as captured on the freeze date. enumerate_o3.py "
                 "re-hashes its inputs into run_manifest.json; a mismatch means a file changed "
                 "between capture and enumeration.",
    }

    Path(args.out).write_text(json.dumps(log, indent=2), encoding="utf-8")
    Path(args.sources).write_text(json.dumps(sources, indent=2), encoding="utf-8")

    captured = sum(1 for e in entries.values() if e.get("status") == "captured")
    print(f"freeze date {as_of} — {captured}/{len(frames_cfg)} frames captured\n")
    for fc, e in entries.items():
        if e.get("status") != "captured":
            print(f"  {fc:<6} {e['status'].upper()}")
            continue
        bits = [f"{e['primary_rows']} rows" if e["primary_rows"] is not None else "rows n/a"]
        if e["pinned_commit"]:
            bits.append(f"commit {e['pinned_commit'][:10]}")
        if len(e["all_files"]) > 1:
            bits.append(f"{len(e['all_files'])} files")
        bits.append(f"{len(e['wayback'])} archive URL(s)")
        print(f"  {fc:<6} {e['primary_file']:<46} {', '.join(bits)}")

    for w in warnings:
        print(f"\n  WARNING  {w}")
    for p in problems:
        print(f"\n  PROBLEM  {p}")

    print(f"\n  capture log -> {args.out}")
    print(f"  sources     -> {args.sources}")
    if problems:
        print("\nProblems above must be fixed before O3. Several can only be fixed by going "
              "back to the source, which is why this runs on the freeze day rather than after.")
        return 1
    return 0


def cmd_verify(args) -> int:
    log = json.loads(Path(args.log).read_text(encoding="utf-8"))
    root = Path(log["snapshot_root"])
    bad = 0
    for fc, e in log["frames"].items():
        if e.get("status") != "captured":
            continue
        for f in e["all_files"]:
            p = root / f["path"]
            if not p.exists():
                print(f"  MISSING  {fc}  {f['path']}")
                bad += 1
                continue
            now = sha256(p)
            if now != f["sha256"]:
                print(f"  CHANGED  {fc}  {f['path']}")
                print(f"           captured {f['sha256'][:16]}…  now {now[:16]}…")
                bad += 1
    if bad:
        print(f"\n{bad} file(s) differ from the freeze-date capture. The frozen snapshot is "
              f"the frame; a file that has changed since capture is not the frame that was "
              f"frozen, and enumerating it would silently move the boundary.")
        return 1
    print(f"all files match the capture of {log['register_freeze_date']}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("log", help="hash the snapshots and write the capture log")
    p.add_argument("--snapshots", required=True)
    p.add_argument("--out", default="capture_log.json")
    p.add_argument("--sources", default="sources.json")
    p.add_argument("--as-of", default=None)
    p.add_argument("--config", default=str(HERE / "config" / "frames.json"))
    p.set_defaults(fn=cmd_log)

    p = sub.add_parser("verify", help="re-hash against an existing capture log")
    p.add_argument("--log", default="capture_log.json")
    p.set_defaults(fn=cmd_verify)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
