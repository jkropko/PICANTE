"""
resolutions.py — O3: consume the reviewed Rule 1 worksheet.

Rule 1 (unit resolution) and the fiscal-sponsor clause are registered human
judgments. `enumerate` queues them in unit_resolution_worksheet.csv; this
module reads the reviewed worksheet back and applies it to the pool BEFORE
cross-frame deduplication, because dedup has to compare the units that will
be coded, not the institutions the frames happened to list.

One worksheet row per resulting unit. The `decision` column takes:

    AS_LISTED        the listing is already an organization-level unit;
                     nothing changes. (Most FORD grantees; a fiscally
                     sponsored project that meets C1 on its own.)
    RESOLVED         resolves to a unit THE FRAME ITSELF names. Name and URL
                     are replaced by the unit's; the frame's own listing is
                     kept on the record. Requires resolved_unit_name and
                     resolution_basis (where in the frame the unit is named).
                     Several RESOLVED rows for one source_key split the
                     listing into several units.
    UNIT_UNRESOLVED  an institution is identified but the frame names no
                     unit within it. Logged, counted, excluded from full
                     coding; written to its own file, not to the pool.

`known_not_surfaced` (any decision): a unit the coder knows of that the frame
does not name. Never added to the pool; logged and counted for the
unit-resolution bound (sensitivity check h). Several may be given, separated
by semicolons.

`sponsor_routing` is REQUIRED where the frame names a fiscal sponsor:
PROJECT (the sponsored project, if the frame names it and it meets C1 on its
own) or SPONSOR (the sponsor). Never both: one source_key cannot produce a
PROJECT row and a SPONSOR row.

Refuses, rather than defaulting, on: a pending record with no row; a blank
decision or coder; an unknown decision; RESOLVED without a unit name or
basis; a split that mixes RESOLVED with anything else; a sponsor record with
no routing; a row for a source_key not in the pool; a row for a Rule 2
operator. Each of these would otherwise put an unexamined judgment into the
data looking like a coder had made it.

What this does NOT decide: `unresolvable` (a listing that is not an
organization at all — dead link, a page on another site) is coded under C1
at O4, not here.
"""
from __future__ import annotations

import csv
from dataclasses import replace
from pathlib import Path

import normalize as nz
from frames_io import Record, PENDING

SCRIPT_VERSION = "1.0.0"

AS_LISTED, RESOLVED, UNIT_UNRESOLVED = "AS_LISTED", "RESOLVED", "UNIT_UNRESOLVED"
DECISIONS = (AS_LISTED, RESOLVED, UNIT_UNRESOLVED)
FINAL_FLAG = {AS_LISTED: "as_listed", RESOLVED: "resolved", UNIT_UNRESOLVED: "unit_unresolved"}
ROUTINGS = ("PROJECT", "SPONSOR")

WORKSHEET_FIELDS = [
    # context, written by enumerate — do not edit
    "source_key", "originating_frame", "name", "website_url", "frame_listing_text",
    "fiscal_sponsor_named", "unit_resolution_note",
    # the coder's columns
    "decision", "resolved_unit_name", "resolved_unit_url", "resolution_basis",
    "sponsor_routing", "known_not_surfaced", "coder", "note",
]


class ResolutionError(RuntimeError):
    pass


def read_worksheet(path: str | Path) -> list[dict]:
    with Path(path).open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        cols = reader.fieldnames or []
        if "decision" not in cols:
            raise ResolutionError(
                f"{path} has no `decision` column — it was written by enumerate_o3.py "
                f"before 1.1.0. Re-run `enumerate` to regenerate the worksheet in the "
                f"current format (the pool and source_keys are unchanged by a re-run), "
                f"and copy across anything already entered."
            )
        return list(reader)


def _clean(v) -> str:
    return (v or "").strip()


def validate(records: list[Record], rows: list[dict]) -> dict[str, list[dict]]:
    """Check the reviewed worksheet against the pool; return rows grouped by
    source_key in worksheet order. Raises ResolutionError on the first
    problem, naming the worksheet row (row 2 = first data row)."""
    by_key = {r.source_key: r for r in records}
    grouped: dict[str, list[dict]] = {}
    for n, row in enumerate(rows, start=2):
        key = _clean(row.get("source_key"))
        where = f"worksheet row {n} ({key or 'no source_key'})"
        if key not in by_key:
            raise ResolutionError(f"{where}: source_key is not in the pool")
        rec = by_key[key]
        if rec.frame_operator == "TRUE":
            raise ResolutionError(
                f"{where}: {rec.name} is a Rule 2 operator. Operators enter by construction "
                f"as named in config/operators.json and are not resolved here.")
        dec = _clean(row.get("decision")).upper()
        if not dec:
            raise ResolutionError(
                f"{where}: no decision. Every row needs AS_LISTED, RESOLVED or "
                f"UNIT_UNRESOLVED — an unreviewed row is not an AS_LISTED one.")
        if dec not in DECISIONS:
            raise ResolutionError(f"{where}: decision must be one of {', '.join(DECISIONS)}, got {dec!r}")
        if not _clean(row.get("coder")):
            raise ResolutionError(f"{where}: no coder. Every resolution is attributed.")
        if dec == RESOLVED:
            if not _clean(row.get("resolved_unit_name")):
                raise ResolutionError(f"{where}: RESOLVED without resolved_unit_name")
            if not _clean(row.get("resolution_basis")):
                raise ResolutionError(
                    f"{where}: RESOLVED without resolution_basis. Rule 1 resolves only to a "
                    f"unit the frame itself names; record where it names it (designee's "
                    f"stated affiliation, a center in the listing, a funded project).")
        routing = _clean(row.get("sponsor_routing")).upper()
        if rec.fiscal_sponsor_named:
            if routing not in ROUTINGS:
                raise ResolutionError(
                    f"{where}: the frame names a fiscal sponsor ({rec.fiscal_sponsor_named}); "
                    f"sponsor_routing must be PROJECT or SPONSOR.")
            if routing == "SPONSOR" and dec != RESOLVED:
                raise ResolutionError(
                    f"{where}: routed to the SPONSOR, so the decision must be RESOLVED with "
                    f"the sponsor as resolved_unit_name.")
        elif routing:
            raise ResolutionError(f"{where}: sponsor_routing given but the frame names no sponsor")
        row["_decision"], row["_routing"], row["_n"] = dec, routing, n
        grouped.setdefault(key, []).append(row)

    for key, grp in grouped.items():
        decs = {r["_decision"] for r in grp}
        if len(grp) > 1 and decs != {RESOLVED}:
            raise ResolutionError(
                f"{key}: {len(grp)} rows with decisions {sorted(decs)}. Several rows for one "
                f"listing is a SPLIT into several units, and every row of a split must be "
                f"RESOLVED.")
        routes = {r["_routing"] for r in grp if r["_routing"]}
        if len(routes) > 1:
            raise ResolutionError(
                f"{key}: routed to both PROJECT and SPONSOR. The fiscal-sponsor clause never "
                f"enters both as separate records.")

    missing = [r.source_key for r in records
               if r.unit_resolution_flag == PENDING and r.source_key not in grouped]
    if missing:
        more = f" and {len(missing) - 10} more" if len(missing) > 10 else ""
        raise ResolutionError(
            f"{len(missing)} pending records have no worksheet row: "
            f"{', '.join(missing[:10])}{more}")
    return grouped


def apply(records: list[Record], rows: list[dict]) -> tuple[list[Record], list[Record], list[dict], list[dict]]:
    """Returns (pool, unit_unresolved, known_not_surfaced, log).

    `pool` holds organization-level units only and goes on to dedup.
    `unit_unresolved` holds the institutions the frames named no unit for.
    """
    grouped = validate(records, rows)
    pool: list[Record] = []
    unresolved: list[Record] = []
    known: list[dict] = []
    log: list[dict] = []

    for rec in records:
        grp = grouped.get(rec.source_key)
        if not grp:
            pool.append(rec)
            continue

        for row in grp:
            for unit in _clean(row.get("known_not_surfaced")).split(";"):
                if unit.strip():
                    known.append({"source_key": rec.source_key,
                                  "originating_frame": rec.originating_frame,
                                  "listed_name": rec.name, "known_unit": unit.strip(),
                                  "coder": _clean(row.get("coder")), "note": _clean(row.get("note"))})

        dec = grp[0]["_decision"]
        base = replace(rec, frame_listed_name=rec.name, frame_listed_url=rec.website_url,
                       unit_resolution_flag=FINAL_FLAG[dec],
                       unit_resolution_coder=_clean(grp[0].get("coder")),
                       sponsor_routing=grp[0]["_routing"])

        if dec == AS_LISTED:
            base.unit_resolution_basis = _clean(grp[0].get("resolution_basis"))
            _append_note(base, grp[0])
            pool.append(base)
            log.append(_log(rec, grp[0], rec.source_key, rec.name, rec.website_url))
            continue

        if dec == UNIT_UNRESOLVED:
            base.unit_resolution_basis = _clean(grp[0].get("resolution_basis"))
            _append_note(base, grp[0])
            unresolved.append(base)
            log.append(_log(rec, grp[0], "", "", ""))
            continue

        # RESOLVED: one unit, or a split into several. Split keys are ordered
        # by normalized unit name so a re-run with the same decisions gives
        # the same keys whatever order the rows were typed in.
        ordered = sorted(grp, key=lambda r: (nz.normalize_name(r["resolved_unit_name"]), r["_n"]))
        for i, row in enumerate(ordered, start=1):
            unit = replace(base)
            if len(ordered) > 1:
                unit.source_key = f"{rec.source_key}.{i}"
                unit.parent_source_key = rec.source_key
            unit.name = _clean(row["resolved_unit_name"])
            unit.website_url = _clean(row.get("resolved_unit_url"))
            unit.unit_resolution_basis = _clean(row["resolution_basis"])
            unit.unit_resolution_coder = _clean(row.get("coder"))
            # Keys recomputed for the unit. location_guess is deliberately
            # left alone: finalize_keys() would re-derive it from raw_location
            # and overwrite what the boundary recorded.
            unit.name_key = nz.normalize_name(unit.name)
            unit.domain_key = nz.registrable_domain(unit.website_url)
            _append_note(unit, row)
            pool.append(unit)
            log.append(_log(rec, row, unit.source_key, unit.name, unit.website_url))

    return pool, unresolved, known, log


def _append_note(rec: Record, row: dict) -> None:
    n = _clean(row.get("note"))
    if n:
        rec.notes = (rec.notes + " | " if rec.notes else "") + f"Rule 1: {n}"


def _log(rec: Record, row: dict, out_key: str, out_name: str, out_url: str) -> dict:
    return {"source_key": rec.source_key, "originating_frame": rec.originating_frame,
            "listed_name": rec.name, "decision": row["_decision"],
            "sponsor_routing": row["_routing"], "out_source_key": out_key,
            "out_name": out_name, "out_url": out_url,
            "resolution_basis": _clean(row.get("resolution_basis")),
            "coder": _clean(row.get("coder")), "note": _clean(row.get("note"))}


LOG_FIELDS = ["source_key", "originating_frame", "listed_name", "decision", "sponsor_routing",
              "out_source_key", "out_name", "out_url", "resolution_basis", "coder", "note"]
KNOWN_FIELDS = ["source_key", "originating_frame", "listed_name", "known_unit", "coder", "note"]
