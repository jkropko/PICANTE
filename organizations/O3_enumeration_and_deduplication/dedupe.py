#!/usr/bin/env python3
"""
dedupe.py — propose cross-frame duplicate pairs, then apply human decisions.

THE SCRIPT NEVER MERGES ANYTHING ON ITS OWN. The responsibility table assigns
dedup to the research assistants with the model permitted only to propose
candidates, each verified by a human. So this module has two halves that run
at different times:

    propose_candidates()  before human review — emits a worksheet
    apply_merges()        after human review — consumes the decisions

Between them sits a person. That is not a limitation to be engineered away:
an organization appearing in two frames is, in this design, one of the most
informative records in the pool, and a wrong merge destroys the multi-frame
provenance that the multi-frame subset analysis depends on. A wrong split is
recoverable later; a silent merge is not.

MERGING PRESERVES ALL PROVENANCE. The surviving record carries every
originating frame, in register order, and every source_key. An organization
claimed by Ford and the Field Guide must read as claimed by both.
"""
from __future__ import annotations

import csv
from pathlib import Path

import normalize as nz
from organizations.O3_enumeration_and_deduplication.frames_io import Record

# Register order. Multi-frame records take the block and admission mechanism
# of the frame listed FIRST here, per the draw rule; the rest is retained.
REGISTER_ORDER = ["PITUN", "FORD", "CTFG", "ACT", "CFA", "FF", "MCGV", "GORG"]


def _order_index(fc: str) -> int:
    try:
        return REGISTER_ORDER.index(fc)
    except ValueError:
        return len(REGISTER_ORDER)


def jaccard(a: frozenset, b: frozenset) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def score_pair(r1: Record, r2: Record) -> tuple[float, str]:
    """Similarity plus the reason, in words a coder can check against the sources."""
    reasons = []
    score = 0.0
    if r1.domain_key and r1.domain_key == r2.domain_key:
        score += 0.6
        reasons.append(f"same registrable domain ({r1.domain_key})")
    if r1.name_key and r1.name_key == r2.name_key:
        score += 0.5
        reasons.append("identical normalized name")
    else:
        j = jaccard(nz.name_tokens(r1.name), nz.name_tokens(r2.name))
        if j >= 0.5:
            score += 0.35 * j
            reasons.append(f"name token overlap {j:.2f}")
    # Previous names are how a brigade that renamed itself is recognized.
    for a, b in ((r1, r2), (r2, r1)):
        if a.previous_names and b.name_key:
            for prev in a.previous_names.split(";"):
                if nz.normalize_name(prev) and nz.normalize_name(prev) == b.name_key:
                    score += 0.5
                    reasons.append(f"previous name matches ({prev.strip()})")
                    break
    return min(score, 1.0), "; ".join(reasons)


def propose_candidates(records: list[Record], threshold: float = 0.45) -> list[dict]:
    """Blocked candidate generation. Blocks on domain and on name token, so
    the comparison is linear-ish rather than quadratic over ~1,800 records."""
    by_domain: dict[str, list[int]] = {}
    by_token: dict[str, list[int]] = {}
    for i, r in enumerate(records):
        if r.domain_key:
            by_domain.setdefault(r.domain_key, []).append(i)
        for t in nz.name_tokens(r.name):
            if len(t) > 3:
                by_token.setdefault(t, []).append(i)

    pairs: set[tuple[int, int]] = set()
    for bucket in list(by_domain.values()) + list(by_token.values()):
        if len(bucket) < 2 or len(bucket) > 60:
            # A token shared by sixty records ("civic", "data") is not a
            # signal; skipping the bucket avoids drowning the worksheet.
            continue
        for a_i in range(len(bucket)):
            for b_i in range(a_i + 1, len(bucket)):
                pairs.add((min(bucket[a_i], bucket[b_i]), max(bucket[a_i], bucket[b_i])))

    out = []
    for i, j in sorted(pairs):
        r1, r2 = records[i], records[j]
        if r1.originating_frame == r2.originating_frame:
            continue  # within-frame dedup is the reader's job
        score, why = score_pair(r1, r2)
        if score < threshold:
            continue
        out.append({
            "decision": "",
            "score": f"{score:.2f}",
            "why": why,
            "cross_block": "YES" if r1.block != r2.block else "",
            "a_source_key": r1.source_key, "a_frame": r1.originating_frame,
            "a_name": r1.name, "a_url": r1.website_url, "a_location": r1.raw_location,
            "b_source_key": r2.source_key, "b_frame": r2.originating_frame,
            "b_name": r2.name, "b_url": r2.website_url, "b_location": r2.raw_location,
            "coder": "", "note": "",
        })
    out.sort(key=lambda d: (-float(d["score"]), d["a_name"].lower()))
    return out


CANDIDATE_FIELDS = [
    "decision", "score", "why", "cross_block",
    "a_source_key", "a_frame", "a_name", "a_url", "a_location",
    "b_source_key", "b_frame", "b_name", "b_url", "b_location",
    "coder", "note",
]


def write_candidates(path: str | Path, rows: list[dict]) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CANDIDATE_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow(r)


class MergeError(RuntimeError):
    pass


def apply_merges(records: list[Record], decisions: list[dict]) -> tuple[list[Record], list[dict]]:
    """Consume a reviewed candidate worksheet.

    decision = MERGE  -> the two records are one organization
    decision = SEPARATE -> they are not; recorded so the judgment is on file
    decision = ""     -> not reviewed; refuses to run

    Returns (surviving records, merge log). Merges are transitive: if A~B and
    B~C were both accepted, all three collapse into one organization.
    """
    by_key = {r.source_key: r for r in records}
    parent: dict[str, str] = {r.source_key: r.source_key for r in records}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    log = []
    for n, d in enumerate(decisions, start=2):  # row 2 = first data row
        dec = (d.get("decision") or "").strip().upper()
        a, b = d.get("a_source_key", ""), d.get("b_source_key", "")
        if dec == "":
            raise MergeError(
                f"candidate row {n} ({a} / {b}) has no decision. Every proposed pair "
                f"must be marked MERGE or SEPARATE before merges are applied — an "
                f"unreviewed pair is not a non-duplicate."
            )
        if dec == "SEPARATE":
            log.append({"a": a, "b": b, "decision": "SEPARATE",
                        "coder": d.get("coder", ""), "note": d.get("note", "")})
            continue
        if dec != "MERGE":
            raise MergeError(f"candidate row {n}: decision must be MERGE or SEPARATE, got {dec!r}")
        if a not in by_key or b not in by_key:
            raise MergeError(f"candidate row {n}: unknown source_key ({a} / {b})")
        ra, rb = find(a), find(b)
        if ra != rb:
            # Survivor is the record from the frame listed first in the register.
            keep, drop = (ra, rb) if _order_index(by_key[ra].originating_frame.split(";")[0]) <= \
                                     _order_index(by_key[rb].originating_frame.split(";")[0]) else (rb, ra)
            parent[drop] = keep
        log.append({"a": a, "b": b, "decision": "MERGE",
                    "coder": d.get("coder", ""), "note": d.get("note", "")})

    groups: dict[str, list[Record]] = {}
    for r in records:
        groups.setdefault(find(r.source_key), []).append(r)

    survivors = []
    for root, members in groups.items():
        members.sort(key=lambda r: (_order_index(r.originating_frame), r.source_key))
        keep = members[0]
        frames, keys, notes = [], [], []
        for m in members:
            for fc in m.originating_frame.split(";"):
                if fc and fc not in frames:
                    frames.append(fc)
            keys.append(m.source_key)
            if m.notes:
                notes.append(f"[{m.source_key}] {m.notes}")
            # A pending judgment anywhere in the group survives the merge.
            if m.unit_resolution_flag == "PENDING" and keep.unit_resolution_flag != "PENDING":
                keep.unit_resolution_flag = "PENDING"
                keep.unit_resolution_note = m.unit_resolution_note
            if m.fiscal_sponsor_named and not keep.fiscal_sponsor_named:
                keep.fiscal_sponsor_named = m.fiscal_sponsor_named
            if m.website_url and not keep.website_url:
                keep.website_url = m.website_url
        frames.sort(key=_order_index)
        keep.originating_frame = ";".join(frames)
        keep.notes = " | ".join(notes)
        if len(members) > 1:
            keep.notes = (keep.notes + " | " if keep.notes else "") + \
                f"merged from {len(members)} frame listings: {', '.join(keys)}"
        survivors.append(keep)

    survivors.sort(key=lambda r: (_order_index(r.originating_frame.split(";")[0]), r.source_key))
    return survivors, log


def assign_org_ids(records: list[Record], prefix: str = "TPG") -> list[Record]:
    """Stable IDs assigned AFTER deduplication, to the organization-level unit.

    Deterministic: the same pool and the same merge decisions produce the same
    IDs on a re-run, so an ID in the screening log always means the same
    organization.
    """
    ordered = sorted(records, key=lambda r: (_order_index(r.originating_frame.split(";")[0]),
                                             r.source_key))
    for n, r in enumerate(ordered, start=1):
        r.org_id = f"{prefix}-{n:05d}"
    return ordered
