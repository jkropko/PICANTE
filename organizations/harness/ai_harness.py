#!/usr/bin/env python3
"""
ai_harness.py — validation and logging harness for the three AI roles in the
TPG organizational strand.

WHAT THIS ENFORCES
    Sheet 1, item 4.3 of the protocol workbook requires that verbatim fidelity
    be enforced PROGRAMMATICALLY: any phrase returned as extracted text must
    appear as an exact substring of the fetched page text, or the extraction is
    rejected automatically and the field routed to a human. That is this file's
    main job. It also enforces the controlled values, the evidence
    requirements, the role boundaries (Role 1 must not touch Group 3 fields;
    Role 2 must not propose values), and the blinding of Role 3.

WHAT IT DELIBERATELY DOES NOT DO
    It does not decide anything. A field that fails validation is not corrected
    and not re-requested: it is routed to a human, who codes it unaided, and
    the routing is recorded. Silently retrying until the model returns
    something well-formed would select for well-formed output rather than
    accurate output, and the accuracy figure computed later would be measuring
    the retry loop.

BLINDING
    Role 3 output is written to a sealed directory that the coding interface
    never reads, and only a SHA-256 commitment is written to the open log at
    production time. Releasing it requires a recorded adjudicated human value
    for that record, and re-verifies the commitment. The commitment is what
    lets a reader confirm the blind coding existed before the human value was
    recorded rather than after — which is the thing a skeptical reader of a
    human-AI agreement statistic would otherwise have to take on trust.

USAGE
    python ai_harness.py ingest --role 1 --record rec.json --response resp.json
    python ai_harness.py ingest --role 3 --record rec.json --response resp.json
    python ai_harness.py release-role3 --org-id CTFG-0417
    python ai_harness.py check-codebook --workbook ../TPG_org_strand_protocol_v3.xlsx
    python ai_harness.py status

    --run-dir defaults to ./run. Layout:
        run/logs/proposals.jsonl    one line per field proposal, open to coders
        run/logs/raw/               raw responses for roles 1 and 2
        run/logs/decisions.jsonl    human decisions, appended by the coding app
        run/sealed/                 Role 3 output, withheld until release
        run/logs/released/          Role 3 output after release

No third-party dependencies. openpyxl is imported only by check-codebook.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HARNESS_VERSION = "0.1.0"

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        sys.exit(f"cannot read {path}: {exc}")
    except json.JSONDecodeError as exc:
        sys.exit(f"{path} is not valid JSON: {exc}")


def load_fields(path: Path) -> dict:
    spec = load_json(path)
    for key in ("role1", "role2", "role3", "gates", "quote_max_words"):
        if key not in spec:
            sys.exit(f"{path} is missing '{key}'")
    return spec


def append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as exc:
            sys.exit(f"{path} line {i} is not valid JSON: {exc}")
    return out


# ---------------------------------------------------------------------------
# response parsing
# ---------------------------------------------------------------------------

FENCE = re.compile(r"^\s*```(?:json)?\s*|\s*```\s*$")


def parse_response(raw: str) -> tuple[dict | None, str]:
    """Parse a model response into an object.

    The prompts forbid code fences and preamble. We strip a fence if we find
    one rather than failing the record, but we say so, because a model that
    starts adding fences has drifted from the frozen prompt and that is worth
    seeing in the log.
    """
    text = raw.strip()
    note = ""
    if text.startswith("```"):
        text = FENCE.sub("", text).strip()
        note = "code fence stripped; response did not follow the frozen output format"
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, f"response is not valid JSON: {exc}"
    if not isinstance(obj, dict):
        return None, "response is not a JSON object"
    return obj, note


# ---------------------------------------------------------------------------
# verbatim fidelity — the check sheet 4.3 requires
# ---------------------------------------------------------------------------

def check_quote(quote, start, end, source_text: str) -> tuple[str, str]:
    """Return (verdict, detail).

    Verdicts, from benign to serious:
      ok               quote is an exact substring AND the offsets point at it
      offset_mismatch  quote is present in the source but not where claimed
      not_found        quote is not in the source at all
      malformed        quote or offsets are not usable

    offset_mismatch and not_found are distinguished on purpose. Offsets drift
    for dull reasons (a re-extraction, an off-by-one). A quote absent from the
    page is the model having written text that was never there, which is the
    failure mode this whole harness exists to catch, and it is reported
    separately in the metrics.
    """
    if not isinstance(quote, str) or not quote:
        return "malformed", "quote missing or not a string"
    if not isinstance(start, int) or not isinstance(end, int):
        return "malformed", "start/end missing or not integers"
    if start < 0 or end > len(source_text) or start >= end:
        return "malformed", f"offsets {start}:{end} outside source of length {len(source_text)}"

    if source_text[start:end] == quote:
        return "ok", ""
    if quote in source_text:
        found = source_text.find(quote)
        return "offset_mismatch", f"quote present at {found} but claimed at {start}"
    return "not_found", "quote does not appear in the cited source"


def quote_too_long(quote: str, max_words: int) -> bool:
    return len(quote.split()) > max_words


# ---------------------------------------------------------------------------
# validation result
# ---------------------------------------------------------------------------

class FieldResult:
    def __init__(self, field: str, value=None):
        self.field = field
        self.value = value
        self.errors: list[str] = []
        self.evidence: list[dict] = []
        self.fidelity: list[dict] = []

    @property
    def accepted(self) -> bool:
        return not self.errors

    def to_log(self) -> dict:
        return {
            "field": self.field,
            "proposed_value": self.value,
            "accepted": self.accepted,
            "routed_to_human_unaided": not self.accepted,
            "errors": self.errors,
            "evidence": self.evidence,
            "fidelity": self.fidelity,
        }


class RecordResult:
    def __init__(self, org_id: str, role: int):
        self.org_id = org_id
        self.role = role
        self.record_errors: list[str] = []
        self.fields: list[FieldResult] = []
        self.notes: list[str] = []
        self.injection_flag = False
        self.candidates: list[dict] = []   # role 2 only
        self.truncated = False             # role 2 only

    @property
    def usable(self) -> bool:
        return not self.record_errors


# ---------------------------------------------------------------------------
# shared field-level validation for roles 1 and 3
# ---------------------------------------------------------------------------

def _sources_index(record: dict) -> dict[str, str]:
    idx = {}
    for src in record.get("sources", []):
        sid, text = src.get("source_id"), src.get("text")
        if isinstance(sid, str) and isinstance(text, str):
            idx[sid] = text
    return idx


def _validate_evidence(entry, sources, max_words, fr: FieldResult) -> None:
    if not isinstance(entry, dict):
        fr.errors.append("evidence entry is not an object")
        return
    sid = entry.get("source_id")
    if sid not in sources:
        fr.errors.append(f"evidence cites unknown source_id {sid!r}")
        return
    verdict, detail = check_quote(entry.get("quote"), entry.get("start"),
                                 entry.get("end"), sources[sid])
    fr.fidelity.append({"source_id": sid, "verdict": verdict, "detail": detail})
    if verdict != "ok":
        fr.errors.append(f"verbatim fidelity failed ({verdict}): {detail}")
        return
    if quote_too_long(entry.get("quote", ""), max_words):
        fr.errors.append(f"quote exceeds {max_words} words")
    fr.evidence.append({
        "source_id": sid,
        "start": entry.get("start"),
        "end": entry.get("end"),
        "quote": entry.get("quote"),
        "for": entry.get("for"),
    })


def validate_fields(payload: dict, spec: dict, record: dict,
                    max_words: int, res: RecordResult) -> None:
    """Validate the 'fields' object of a Role 1 or Role 3 response."""
    sources = _sources_index(record)
    defs = spec["fields"]
    exempt = set(spec.get("evidence_exempt_values", []))
    reasoning_required = spec.get("reasoning_required", False)

    for bad in spec.get("forbidden_fields", []):
        if bad in payload:
            res.record_errors.append(
                f"response contains {bad!r}, which this role must not touch")

    for name, fdef in defs.items():
        fr = FieldResult(name)
        entry = payload.get(name)
        if entry is None:
            fr.errors.append("field missing from response")
            res.fields.append(fr)
            continue
        if not isinstance(entry, dict) or "value" not in entry:
            fr.errors.append("field is not an object with a 'value'")
            res.fields.append(fr)
            continue

        value = entry.get("value")
        fr.value = value
        kind = fdef["kind"]
        allowed = fdef.get("values")

        # ---- value shape and controlled values
        if kind in ("single", "date", "text", "rubric_pending"):
            if not isinstance(value, str):
                fr.errors.append("value is not a string")
            elif kind == "single" and allowed and value not in allowed:
                fr.errors.append(f"value {value!r} not in controlled list {allowed}")
            elif kind == "date" and value != "undetermined" and not ISO_DATE.match(value):
                fr.errors.append(f"value {value!r} is not an ISO date")
        elif kind == "multi":
            if value == "undetermined":
                pass
            elif not isinstance(value, list) or not value:
                fr.errors.append("multi-valued field is not a non-empty list")
            else:
                if allowed:
                    for v in value:
                        if v not in allowed:
                            fr.errors.append(f"value {v!r} not in controlled list {allowed}")
                if len(set(map(str, value))) != len(value):
                    fr.errors.append("multi-valued field repeats a value")

        # ---- evidence
        raw_ev = entry.get("evidence", [])
        if not isinstance(raw_ev, list):
            fr.errors.append("evidence is not a list")
            raw_ev = []
        for ev in raw_ev:
            _validate_evidence(ev, sources, max_words, fr)

        is_exempt = isinstance(value, str) and value in exempt
        needs_ev = fdef.get("evidence_required", True) and not is_exempt
        if needs_ev and not fr.evidence and not fr.errors:
            fr.errors.append("value proposed with no usable evidence")
        elif needs_ev and not fr.evidence and fr.errors:
            pass  # already failed for a more specific reason

        # every member of a multi-valued field needs its own evidence
        if kind == "multi" and isinstance(value, list) and fr.evidence:
            covered = {e.get("for") for e in fr.evidence}
            missing = [v for v in value if v not in covered]
            if missing:
                fr.errors.append(f"no evidence attached to {missing}")

        # ---- reasoning (role 3)
        if reasoning_required:
            reasoning = entry.get("reasoning")
            if not isinstance(reasoning, str) or not reasoning.strip():
                fr.errors.append("reasoning missing")

        res.fields.append(fr)

    unknown = set(payload) - set(defs) - set(spec.get("forbidden_fields", []))
    if unknown:
        res.notes.append(f"response carried unrequested fields, ignored: {sorted(unknown)}")


# ---------------------------------------------------------------------------
# role 2 — passages only, no values
# ---------------------------------------------------------------------------

def validate_role2(obj: dict, spec: dict, record: dict, res: RecordResult) -> None:
    sources = _sources_index(record)
    required = spec["candidate_keys_required"]
    allowed = set(required) | set(spec.get("candidate_keys_allowed_extra", []))
    forbidden_bits = [b.lower() for b in spec.get("forbidden_key_substrings", [])]

    cands = obj.get("candidates")
    if not isinstance(cands, list):
        res.record_errors.append("'candidates' missing or not a list")
        return

    res.truncated = bool(obj.get("truncated", False))
    if len(cands) > spec["max_candidates"]:
        res.record_errors.append(
            f"{len(cands)} candidates exceeds the cap of {spec['max_candidates']}")

    last_key = None
    for i, c in enumerate(cands):
        fr = FieldResult(f"candidate[{i}]")
        if not isinstance(c, dict):
            fr.errors.append("candidate is not an object")
            res.fields.append(fr)
            continue

        for k in required:
            if k not in c:
                fr.errors.append(f"missing {k!r}")

        # Role 2 proposes NO values. A key the model invented to label,
        # classify or rank a passage is a role violation, not a stray field:
        # it puts a suggested value in front of a coder whose judgment is
        # supposed to be unprompted.
        for k in c:
            if k in allowed:
                continue
            if any(bit in k.lower() for bit in forbidden_bits):
                res.record_errors.append(
                    f"candidate[{i}] carries {k!r}: Role 2 must propose no values")
            else:
                fr.errors.append(f"unexpected key {k!r}")

        sid = c.get("source_id")
        if sid not in sources:
            fr.errors.append(f"unknown source_id {sid!r}")
            res.fields.append(fr)
            continue
        text = sources[sid]

        verdict, detail = check_quote(c.get("text_verbatim"), c.get("start"),
                                      c.get("end"), text)
        fr.fidelity.append({"source_id": sid, "verdict": verdict, "detail": detail})
        if verdict != "ok":
            fr.errors.append(f"verbatim fidelity failed ({verdict}): {detail}")

        sent = c.get("sentence_verbatim")
        if isinstance(sent, str) and sent:
            if sent not in text:
                fr.errors.append("sentence_verbatim is not a substring of the source")
            elif isinstance(c.get("text_verbatim"), str) and c["text_verbatim"] not in sent:
                fr.errors.append("sentence_verbatim does not contain text_verbatim")

        head = c.get("heading_context_verbatim")
        if isinstance(head, str) and head and head not in text:
            fr.errors.append("heading_context_verbatim is not a substring of the source")

        if fr.accepted:
            key = (str(sid), c.get("start"))
            if last_key is not None and key < last_key:
                res.notes.append(f"candidate[{i}] out of document order")
            last_key = key
            res.candidates.append(c)

        res.fields.append(fr)


# ---------------------------------------------------------------------------
# top-level validation
# ---------------------------------------------------------------------------

def validate(role: int, raw_response: str, record: dict, spec: dict) -> RecordResult:
    org_id = record.get("org_id", "")
    res = RecordResult(org_id, role)

    if not org_id:
        res.record_errors.append("record has no org_id")
    if not _sources_index(record):
        res.record_errors.append("record has no usable sources")

    obj, note = parse_response(raw_response)
    if note:
        res.notes.append(note)
    if obj is None:
        res.record_errors.append(note or "unparseable response")
        return res

    if obj.get("org_id") != org_id:
        res.record_errors.append(
            f"response org_id {obj.get('org_id')!r} does not match record {org_id!r}")

    res.injection_flag = bool(obj.get("injection_flag", False))
    if res.injection_flag:
        res.notes.append("model reported instruction-like text in the source; "
                         "review the page before accepting any field")

    if role == 2:
        validate_role2(obj, spec["role2"], record, res)
    else:
        key = "role1" if role == 1 else "role3"
        payload = obj.get("fields")
        if not isinstance(payload, dict):
            res.record_errors.append("'fields' missing or not an object")
            return res
        validate_fields(payload, spec[key], record, spec["quote_max_words"], res)

    return res


# ---------------------------------------------------------------------------
# logging and sealing
# ---------------------------------------------------------------------------

class Run:
    def __init__(self, run_dir: Path):
        self.dir = run_dir
        self.logs = run_dir / "logs"
        self.raw = self.logs / "raw"
        self.sealed = run_dir / "sealed"
        self.released = self.logs / "released"
        self.proposals = self.logs / "proposals.jsonl"
        self.decisions = self.logs / "decisions.jsonl"
        for d in (self.logs, self.raw, self.sealed, self.released):
            d.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self.sealed, 0o700)
        except OSError:
            pass


def ingest(role: int, record: dict, raw_response: str, run: Run,
           spec: dict, prompt_version: str, model: str) -> RecordResult:
    res = validate(role, raw_response, record, spec)
    ts = now_utc()
    raw_sha = sha256_text(raw_response)

    if role == 3:
        # Sealed: the coding interface reads proposals.jsonl and never the
        # sealed directory. Only the commitment goes in the open log.
        sealed_path = run.sealed / f"{res.org_id}.role3.json"
        if sealed_path.exists():
            sys.exit(f"refusing to overwrite existing sealed output for {res.org_id}. "
                     f"A second blind coding of the same record would let the first "
                     f"be discarded after the fact.")
        sealed_path.write_text(json.dumps({
            "org_id": res.org_id,
            "sealed_at_utc": ts,
            "prompt_version": prompt_version,
            "model": model,
            "raw_response": raw_response,
            "fields": [f.to_log() for f in res.fields],
            "record_errors": res.record_errors,
            "notes": res.notes,
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        try:
            os.chmod(sealed_path, 0o600)
        except OSError:
            pass
        append_jsonl(run.proposals, {
            "ts_utc": ts, "org_id": res.org_id, "role": 3,
            "prompt_version": prompt_version, "model": model,
            "harness_version": HARNESS_VERSION,
            "status": "sealed",
            "commitment_sha256": sha256_text(raw_response),
            "sealed_file": str(sealed_path.name),
            "fields_proposed": len([f for f in res.fields if f.accepted]),
            "fields_routed_to_human": len([f for f in res.fields if not f.accepted]),
            "injection_flag": res.injection_flag,
            "note": "content withheld until the adjudicated human value is recorded",
        })
        return res

    (run.raw / f"{res.org_id}.role{role}.json").write_text(raw_response, encoding="utf-8")

    base = {
        "ts_utc": ts, "org_id": res.org_id, "role": role,
        "prompt_version": prompt_version, "model": model,
        "harness_version": HARNESS_VERSION,
        "raw_response_sha256": raw_sha,
        "injection_flag": res.injection_flag,
    }

    if role == 2:
        append_jsonl(run.proposals, {
            **base,
            "status": "ok" if res.usable else "record_rejected",
            "record_errors": res.record_errors,
            "candidates_returned": len(res.candidates),
            "candidates_rejected": len([f for f in res.fields if not f.accepted]),
            "truncated": res.truncated,
            "candidates": res.candidates,
            "notes": res.notes,
        })
        return res

    for fr in res.fields:
        append_jsonl(run.proposals, {**base, **fr.to_log(),
                                     "record_errors": res.record_errors,
                                     "notes": res.notes})
    return res


def release_role3(org_id: str, run: Run) -> dict:
    """Release a sealed blind coding, once the human value exists."""
    sealed_path = run.sealed / f"{org_id}.role3.json"
    if not sealed_path.exists():
        sys.exit(f"no sealed Role 3 output for {org_id}")

    decisions = [d for d in read_jsonl(run.decisions)
                 if d.get("org_id") == org_id and d.get("stage") == "adjudicated"]
    if not decisions:
        sys.exit(f"refusing to release: no adjudicated human values recorded for "
                 f"{org_id}. Role 3 is withheld until the humans have committed "
                 f"to their value.")

    raw = json.loads(sealed_path.read_text(encoding="utf-8"))
    commitments = [p for p in read_jsonl(run.proposals)
                   if p.get("org_id") == org_id and p.get("role") == 3]
    if not commitments:
        sys.exit(f"no commitment logged for {org_id}; cannot verify the seal")
    recomputed = sha256_text(raw["raw_response"])
    if recomputed != commitments[-1].get("commitment_sha256"):
        sys.exit(f"SEAL BROKEN for {org_id}: the sealed file does not match the "
                 f"commitment recorded when it was produced. Do not use this "
                 f"record's blind coding; report the discrepancy.")

    out = run.released / f"{org_id}.role3.json"
    raw["released_at_utc"] = now_utc()
    raw["commitment_verified"] = True
    raw["adjudicated_at_utc"] = decisions[-1].get("ts_utc")
    out.write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")
    append_jsonl(run.proposals, {
        "ts_utc": now_utc(), "org_id": org_id, "role": 3,
        "status": "released", "commitment_sha256": recomputed,
        "harness_version": HARNESS_VERSION,
    })
    return raw


# ---------------------------------------------------------------------------
# codebook drift check
# ---------------------------------------------------------------------------

def check_codebook(workbook: Path, spec: dict) -> int:
    try:
        import openpyxl
    except ImportError:
        sys.exit("check-codebook needs openpyxl: pip install openpyxl")

    wb = openpyxl.load_workbook(workbook, read_only=True)
    if "4. Codebook" not in wb.sheetnames:
        sys.exit(f"{workbook} has no '4. Codebook' sheet")

    book: dict[str, list[str]] = {}
    for row in wb["4. Codebook"].iter_rows(values_only=True):
        cells = [c for c in row if c is not None]
        if len(cells) < 2:
            continue
        field = str(cells[0]).strip()
        controlled = str(cells[-1]).strip()
        if "/" not in controlled or len(controlled) > 200:
            continue
        vals = [v.strip() for v in controlled.split("/") if v.strip()]
        if vals:
            book[field] = vals

    # Subset semantics. A role may legitimately be allowed FEWER values than
    # the codebook permits — Role 1 is barred from unit_known_not_surfaced
    # because that code requires knowing of a unit the frame did not name,
    # which is exactly the judgment the model is forbidden to make. A role
    # offering a value the codebook does not contain is never legitimate: it
    # means the harness and the coders are applying different lists.
    problems = restricted = 0
    for role in ("role1", "role3"):
        for name, fdef in spec[role]["fields"].items():
            allowed = fdef.get("values")
            if not allowed or name not in book:
                continue
            here = {v for v in allowed if v != "undetermined"}
            there = set(book[name])
            extra = here - there
            missing = there - here
            if extra:
                problems += 1
                print(f"NOT IN CODEBOOK  {name}: {sorted(extra)}")
                print(f"  {role} may propose it, but the codebook's controlled "
                      f"list is {sorted(there)}.")
                print("  Reconcile before collection: either the value belongs in "
                      "the codebook's list or the role must stop proposing it.")
            elif missing:
                restricted += 1
                print(f"restricted       {name}: {role} may not propose "
                      f"{sorted(missing)} (codebook allows it for humans)")

    checked = sum(1 for r in ("role1", "role3")
                  for n, f in spec[r]["fields"].items()
                  if f.get("values") and n in book)
    print(f"\n{checked} controlled-value fields compared: {problems} not in the "
          f"codebook, {restricted} deliberately restricted.")
    if problems:
        print("The harness follows fields.json, so anything listed above as NOT IN "
              "CODEBOOK means the model and the coders are working from different "
              "controlled lists.")
    return 1 if problems else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_ingest(args, spec) -> int:
    run = Run(Path(args.run_dir))
    record = load_json(Path(args.record))
    raw = Path(args.response).read_text(encoding="utf-8")
    res = ingest(args.role, record, raw, run, spec, args.prompt_version, args.model)

    print(f"org_id {res.org_id or '(none)'}   role {args.role}")
    if res.record_errors:
        print("  RECORD REJECTED — every field routed to a human unaided")
        for e in res.record_errors:
            print(f"    - {e}")
    for n in res.notes:
        print(f"  note: {n}")
    if args.role == 2:
        ok = len(res.candidates)
        bad = len([f for f in res.fields if not f.accepted])
        print(f"  {ok} candidate passages accepted, {bad} rejected"
              + (", list truncated" if res.truncated else ""))
    else:
        ok = [f for f in res.fields if f.accepted]
        bad = [f for f in res.fields if not f.accepted]
        print(f"  {len(ok)} fields proposed, {len(bad)} routed to a human")
        for f in bad:
            print(f"    - {f.field}: {'; '.join(f.errors)}")
    if args.role == 3:
        print("  sealed; withheld until the adjudicated human value is recorded")
    return 0 if res.usable else 2


def cmd_release(args, spec) -> int:
    run = Run(Path(args.run_dir))
    raw = release_role3(args.org_id, run)
    print(f"released {args.org_id}: commitment verified, sealed "
          f"{raw['sealed_at_utc']}, adjudicated {raw.get('adjudicated_at_utc')}")
    return 0


def cmd_status(args, spec) -> int:
    run = Run(Path(args.run_dir))
    props = read_jsonl(run.proposals)
    sealed = list(run.sealed.glob("*.role3.json"))
    released = list(run.released.glob("*.role3.json"))
    by_role = {}
    for p in props:
        by_role.setdefault(p.get("role"), []).append(p)
    print(f"run dir: {run.dir}")
    for role in sorted(k for k in by_role if k is not None):
        rows = by_role[role]
        orgs = {r["org_id"] for r in rows}
        routed = sum(1 for r in rows if r.get("routed_to_human_unaided"))
        flagged = {r["org_id"] for r in rows if r.get("injection_flag")}
        print(f"  role {role}: {len(orgs)} records, {len(rows)} log lines, "
              f"{routed} fields routed to a human")
        if flagged:
            print(f"    injection_flag set on: {sorted(flagged)}")
    print(f"  role 3 sealed: {len(sealed)}, released: {len(released)}, "
          f"still withheld: {len(sealed) - len(released)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-dir", default="run")
    ap.add_argument("--fields", default=str(Path(__file__).resolve().parent / "fields.json"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("ingest", help="validate and log one model response")
    p.add_argument("--role", type=int, choices=[1, 2, 3], required=True)
    p.add_argument("--record", required=True, help="input envelope JSON")
    p.add_argument("--response", required=True, help="raw model response")
    p.add_argument("--prompt-version", default="draft-0.1")
    p.add_argument("--model", default="claude-opus-5")
    p.set_defaults(func=cmd_ingest)

    p = sub.add_parser("release-role3", help="release a sealed blind coding")
    p.add_argument("--org-id", required=True)
    p.set_defaults(func=cmd_release)

    p = sub.add_parser("check-codebook", help="compare fields.json to the workbook")
    p.add_argument("--workbook", required=True)
    p.set_defaults(func=lambda a, s: check_codebook(Path(a.workbook), s))

    p = sub.add_parser("status", help="summarize the run")
    p.set_defaults(func=cmd_status)

    args = ap.parse_args()
    spec = load_fields(Path(args.fields))
    return args.func(args, spec)


if __name__ == "__main__":
    sys.exit(main())
