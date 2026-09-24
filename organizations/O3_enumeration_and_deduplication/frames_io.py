#!/usr/bin/env python3
"""
frames_io.py — read each frozen frame snapshot into the common record schema.

One reader per frame shape. Each reader does three things and no more:
    1. applies the frame's REGISTERED boundary definition,
    2. carries every value it used through to the record verbatim,
    3. flags, for a human, anything the boundary does not settle.

A reader never decides C1, C2, unit resolution, fiscal-sponsor routing, or a
merge. Those are registered human judgments. Where a reader can tell that one
is needed it sets a PENDING flag and writes the frame's own listing text onto
the record so the coder has what the frame said in front of them.

Records dropped at the boundary are not discarded silently: every reader
returns them with a drop reason, and the enumerator writes them to
dropped_at_boundary.csv so the PRISMA accounting can show what the boundary
cost.
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

import normalize as nz

PENDING = "PENDING"


@dataclass
class Record:
    """One enumerated candidate, before screening and before dedup."""
    source_key: str = ""            # stable within-frame key: "<FRAME>:<row>"
    originating_frame: str = ""     # single frame here; multi after dedup
    block: str = ""
    admission_mechanism: str = ""
    frame_type: str = ""
    date_identified: str = ""
    name: str = ""                  # verbatim, as the frame gave it
    website_url: str = ""           # verbatim
    raw_location: str = ""          # verbatim
    location_guess: str = nz.UNKNOWN
    frame_listing_text: str = ""    # the frame's own entry, verbatim
    unit_resolution_flag: str = ""  # "" | PENDING (human sets the final value)
    unit_resolution_note: str = ""
    fiscal_sponsor_named: str = ""  # verbatim; presence routes to a human
    frame_operator: str = "FALSE"
    frame_operated: str = ""
    operator_status: str = ""
    grant_count: str = ""           # grants frames only
    source_route: str = ""          # FORD: live database vs 990-PF
    cohort: str = ""                # GORG only
    ctfg_networks: str = ""         # CTFG only, verbatim, ~9% populated
    cfa_independence_tag: str = ""  # CFA only
    previous_names: str = ""        # CFA only
    name_key: str = ""
    domain_key: str = ""
    org_id: str = ""                # assigned after dedup, at O3 close
    merged_into_org_id: str = ""
    notes: str = ""

    def finalize_keys(self) -> "Record":
        self.name_key = nz.normalize_name(self.name)
        self.domain_key = nz.registrable_domain(self.website_url)
        self.location_guess = nz.us_location_guess(self.raw_location)
        return self


@dataclass
class FrameResult:
    frame_code: str
    kept: list[Record] = field(default_factory=list)
    dropped: list[dict] = field(default_factory=list)
    stats: dict = field(default_factory=dict)
    extra_pools: dict = field(default_factory=dict)  # CTFG audit strata


class ConfigError(RuntimeError):
    pass


# ----------------------------------------------------------------- utilities

def read_rows(path) -> list[dict]:
    """CSV or JSON array of objects. Anything else is an error, loudly.

    Accepts a list of paths as well as one. Ford is a two-source frame — the
    live topic-filtered database plus the 990-PF tail — and its rows arrive in
    two files that have to be read as one frame.
    """
    if isinstance(path, (list, tuple)):
        rows: list[dict] = []
        for p in path:
            rows.extend(read_rows(p))
        return rows
    p = Path(path)
    if not p.exists():
        raise ConfigError(f"snapshot not found: {p}")
    if p.suffix.lower() in (".yml", ".yaml"):
        try:
            import yaml
        except ImportError as e:
            raise ConfigError(
                f"{p} is YAML and PyYAML is not installed. Either `pip install pyyaml` or "
                f"convert the file to CSV/JSON at capture. Do not rename it: the reader "
                f"chooses by suffix, and a YAML file named .csv parses as one long broken "
                f"row."
            ) from e
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for key in ("organizations", "records", "data", "items", "members"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break
        if not isinstance(data, list):
            raise ConfigError(f"{p}: expected a YAML list of mappings")
        return [r for r in data if isinstance(r, dict)]
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            for key in ("organizations", "records", "data", "items"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break
        if not isinstance(data, list):
            raise ConfigError(f"{p}: expected a JSON array of objects")
        return [r for r in data if isinstance(r, dict)]
    with p.open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def _col(cols: dict, key: str, required: bool = True) -> str | None:
    name = cols.get(key)
    if name in (None, "", "CONFIRM"):
        if required:
            raise ConfigError(
                f"column mapping for '{key}' is unset or still CONFIRM. "
                f"Run `inspect` against the frozen snapshot and set it in frames.json."
            )
        return None
    return name


def _get(row: dict, colname: str | None) -> str:
    if not colname:
        return ""
    v = row.get(colname, "")
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return "; ".join(str(x) for x in v)
    return str(v).strip()


def _base(rec: Record, fc: str, cfg: dict, as_of: str) -> Record:
    rec.originating_frame = fc
    rec.block = cfg["block"]
    rec.admission_mechanism = cfg["admission_mechanism"]
    rec.frame_type = cfg["frame_type"]
    rec.date_identified = as_of
    return rec


# -------------------------------------------------------------- generic list

def read_generic(fc: str, cfg: dict, path, as_of: str) -> FrameResult:
    """A published list of organizations: PITUN, ACT, FF, GORG."""
    cols = cfg.get("columns", {})
    c_name = _col(cols, "name")
    c_url = _col(cols, "website_url", required=False)
    c_loc = _col(cols, "location", required=False)
    c_txt = _col(cols, "listing_text", required=False)
    cohort_cfg = cfg.get("cohorts")
    c_cohort = _col(cols, "cohort", required=False) if cohort_cfg else None
    if cohort_cfg and not c_cohort:
        raise ConfigError(f"{fc}: a cohort column is required for a cohort-defined frame")

    res = FrameResult(frame_code=fc)
    for i, row in enumerate(read_rows(path), start=1):
        name = _get(row, c_name)
        if nz.is_blank(name):
            res.dropped.append({"frame": fc, "row": i, "reason": "no name in listing",
                                "raw": json.dumps(row, default=str)[:500]})
            continue

        if cohort_cfg:
            cohort = _get(row, c_cohort)
            allowed = cohort_cfg["allowed"]
            if cohort not in allowed:
                # This is the guard that keeps the AI for Science page's
                # "previously funded recipients" — an earlier, different fund —
                # out of the frame.
                res.dropped.append({
                    "frame": fc, "row": i, "name": name,
                    "reason": f"cohort '{cohort}' is not one of the four named cohorts",
                })
                continue

        rec = _base(Record(source_key=f"{fc}:{i:05d}"), fc, cfg, as_of)
        rec.name = name
        rec.website_url = _get(row, c_url)
        rec.raw_location = _get(row, c_loc)
        rec.frame_listing_text = _get(row, c_txt)
        if cohort_cfg:
            rec.cohort = _get(row, c_cohort)
        if cfg.get("lists_institutions"):
            rec.unit_resolution_flag = PENDING
            rec.unit_resolution_note = (
                "Rule 1: frame lists institutions. Resolve to the unit the FRAME names, "
                "or log unit_unresolved. Never add a unit the frame did not name."
            )
        res.kept.append(rec.finalize_keys())

    res.stats = {"rows_read": len(res.kept) + len(res.dropped), "kept": len(res.kept),
                 "dropped": len(res.dropped)}
    return res


# --------------------------------------------------------------------- CTFG

def read_ctfg(fc: str, cfg: dict, path, as_of: str) -> FrameResult:
    """Civic Tech Field Guide, under its registered boundary definition.

    Also writes the two O8 audit pools, which live OUTSIDE the boundary and
    therefore only exist if the full export was captured at freeze.
    """
    cols = cfg.get("columns", {})
    c_name = _col(cols, "name")
    c_url = _col(cols, "website_url", required=False)
    c_type = _col(cols, "type")
    c_country = _col(cols, "country")
    c_net = _col(cols, "networks", required=False)

    b = cfg["boundary"]
    type_needle = b["type_contains"].lower()
    country_ok = {c.lower() for c in b["country_in"]}
    allow_missing_country = bool(b.get("country_missing_included", True))

    res = FrameResult(frame_code=fc)
    stratum_a, stratum_b = [], []
    n_us_confirmed = n_country_missing = 0

    for i, row in enumerate(read_rows(path), start=1):
        name = _get(row, c_name)
        rtype = _get(row, c_type)
        country = nz.normalize_country(_get(row, c_country))
        type_present = not nz.is_blank(rtype)
        is_org_type = type_present and type_needle in rtype.lower()
        country_is_us = country in country_ok
        country_missing = country == ""

        in_boundary = is_org_type and (country_is_us or (allow_missing_country and country_missing))

        if in_boundary:
            if nz.is_blank(name):
                res.dropped.append({"frame": fc, "row": i, "reason": "in boundary but no name"})
                continue
            rec = _base(Record(source_key=f"{fc}:{i:05d}"), fc, cfg, as_of)
            rec.name = name
            rec.website_url = _get(row, c_url)
            rec.raw_location = _get(row, c_country)
            rec.ctfg_networks = _get(row, c_net)
            if country_missing:
                n_country_missing += 1
                rec.notes = "country missing in export; C2 requires a manual determination at O4"
            else:
                n_us_confirmed += 1
            res.kept.append(rec.finalize_keys())
            continue

        # Outside the boundary. Two of these become the O8 audit pools.
        if country_is_us and type_present and not is_org_type:
            stratum_a.append({"row": i, "name": name, "type": rtype,
                              "country": _get(row, c_country), "website": _get(row, c_url)})
        elif country_is_us and not type_present:
            stratum_b.append({"row": i, "name": name, "type": "",
                              "country": _get(row, c_country), "website": _get(row, c_url)})
        res.dropped.append({
            "frame": fc, "row": i, "name": name,
            "reason": ("type is not Organization" if not is_org_type else "country is not US"),
        })

    res.extra_pools = {"ctfg_audit_stratum_a": stratum_a, "ctfg_audit_stratum_b": stratum_b}
    res.stats = {
        "rows_read": len(res.kept) + len(res.dropped),
        "kept": len(res.kept),
        "kept_us_confirmed": n_us_confirmed,
        "kept_country_missing": n_country_missing,
        "dropped": len(res.dropped),
        "audit_stratum_a_pool": len(stratum_a),
        "audit_stratum_b_pool": len(stratum_b),
    }
    return res


# ---------------------------------------------------------------------- CFA

def read_cfa(fc: str, cfg: dict, path, as_of: str) -> FrameResult:
    """Code for America brigade roster, pinned to a commit SHA.

    The file is not brigades only: it carries 18F, Code for All members, OK
    Labs, Code for Poland and government entities. Tag filtering is what
    separates them, and the tag vocabulary must be confirmed against the
    pinned file before the first real run.
    """
    cols = cfg.get("columns", {})
    tags_cfg = cfg.get("tags", {})
    include_any = [t.lower() for t in tags_cfg.get("include_any", [])]
    exclude_any = [t.lower() for t in tags_cfg.get("exclude_any", [])]
    independence = [t.lower() for t in tags_cfg.get("independence_tags", [])]
    if not include_any:
        raise ConfigError("CFA: tags.include_any is empty. Run `inspect --frame CFA` first.")

    c_name = _col(cols, "name")
    c_url = _col(cols, "website_url", required=False)
    c_loc = _col(cols, "location", required=False)
    c_tags = _col(cols, "tags")
    c_prev = _col(cols, "previous_names", required=False)

    rule = cfg.get("boundary", {}).get("location_rule", "drop_clearly_non_us")
    if rule not in ("drop_clearly_non_us", "keep_us_only"):
        raise ConfigError(f"CFA: unknown location_rule '{rule}'")

    res = FrameResult(frame_code=fc)
    n_unknown_loc = 0
    for i, row in enumerate(read_rows(path), start=1):
        name = _get(row, c_name)
        raw_tags = row.get(c_tags, "")
        if isinstance(raw_tags, (list, tuple)):
            tags = [str(t).strip() for t in raw_tags if str(t).strip()]
        else:
            tags = [t.strip() for t in str(raw_tags or "").split(",") if t.strip()]
        low = [t.lower() for t in tags]

        if nz.is_blank(name):
            res.dropped.append({"frame": fc, "row": i, "reason": "no name in listing"})
            continue
        if any(x in low for x in exclude_any):
            res.dropped.append({"frame": fc, "row": i, "name": name,
                                "reason": f"excluded tag: {tags}"})
            continue
        if not any(x in low for x in include_any):
            res.dropped.append({"frame": fc, "row": i, "name": name,
                                "reason": f"no include tag: {tags}"})
            continue

        loc = _get(row, c_loc)
        guess = nz.us_location_guess(loc)
        if guess == nz.NON_US:
            res.dropped.append({"frame": fc, "row": i, "name": name,
                                "reason": f"location reads non-US: {loc!r}"})
            continue
        if guess == nz.UNKNOWN:
            n_unknown_loc += 1
            if rule == "keep_us_only":
                res.dropped.append({"frame": fc, "row": i, "name": name,
                                    "reason": f"location not determinable: {loc!r} (keep_us_only)"})
                continue

        rec = _base(Record(source_key=f"{fc}:{i:05d}"), fc, cfg, as_of)
        rec.name = name
        rec.website_url = _get(row, c_url)
        rec.raw_location = loc
        rec.previous_names = _get(row, c_prev)
        rec.cfa_independence_tag = "; ".join(
            t for t in tags if t.lower() in independence
        )
        if guess == nz.UNKNOWN:
            rec.notes = "location string not determinable; retained for C2 at O4"
        res.kept.append(rec.finalize_keys())

    res.stats = {"rows_read": len(res.kept) + len(res.dropped), "kept": len(res.kept),
                 "dropped": len(res.dropped), "location_unknown_retained": n_unknown_loc,
                 "location_rule": rule}
    return res


# ------------------------------------------------------------------- grants

def read_grants(fc: str, cfg: dict, path, as_of: str) -> FrameResult:
    """FORD and MCGV: the unit in the source is a GRANT, not an organization.

    Grants are collapsed to organizations within the frame, keeping a grant
    count. Where a row names a fiscal sponsor, the record is flagged for the
    Rule 1 fiscal-sponsor clause — a human decides whether it resolves to the
    sponsored project or to the sponsor, and both are never entered.
    """
    cols = cfg.get("columns", {})
    c_name = _col(cols, "grantee_name")
    c_url = _col(cols, "website_url", required=False)
    c_loc = _col(cols, "location", required=False)
    c_route = _col(cols, "source_route", required=False)
    c_sponsor = _col(cols, "fiscal_sponsor", required=False)
    c_txt = _col(cols, "listing_text", required=False)
    c_prog = _col(cols, "program_slugs", required=False)
    c_subj = _col(cols, "subject_slugs", required=False)

    b = cfg.get("boundary") or {}
    want_prog = b.get("program_slug")
    want_subj = b.get("subject_slug") if b.get("include_technology_subject") else None
    if want_prog and not c_prog:
        raise ConfigError(
            f"{fc}: the boundary selects on program '{want_prog}' but no program_slugs column "
            f"is mapped. Without it every grant would pass and the frame would be the funder's "
            f"whole portfolio."
        )
    if b.get("include_technology_subject") and not c_subj:
        raise ConfigError(
            f"{fc}: the boundary includes grants by subject but no subject_slugs column is "
            f"mapped."
        )

    if fc == "FORD" and not c_route:
        raise ConfigError(
            "FORD is a two-source frame (live topic-filtered database plus 990-PF filings "
            "from 2011). A source_route column is required so each grantee records which "
            "source it came from."
        )

    res = FrameResult(frame_code=fc)
    by_key: dict[str, Record] = {}
    counts: dict[str, int] = {}
    routes: dict[str, set] = {}
    rows_read = 0
    boundary_program_only = boundary_subject_only = boundary_both = 0

    for i, row in enumerate(read_rows(path), start=1):
        rows_read += 1
        name = _get(row, c_name)
        if nz.is_blank(name):
            res.dropped.append({"frame": fc, "row": i, "reason": "grant row names no grantee"})
            continue
        # Frame boundary, applied here rather than at capture: the source
        # offers no filter, so the narrowing lives in config where it is
        # deterministic and its cost is measurable.
        if want_prog:
            progs = {s.strip().lower() for s in _get(row, c_prog).split(";") if s.strip()}
            subjs = {s.strip().lower() for s in _get(row, c_subj).split(";") if s.strip()} \
                if c_subj else set()
            in_program = want_prog.lower() in progs
            in_subject = bool(want_subj) and want_subj.lower() in subjs
            if not (in_program or in_subject):
                res.dropped.append({
                    "frame": fc, "row": i, "name": name,
                    "reason": f"outside the frame boundary (programs={sorted(progs)}, "
                              f"subjects={sorted(subjs)})",
                })
                continue
            if in_program and in_subject:
                boundary_both += 1
            elif in_program:
                boundary_program_only += 1
            else:
                boundary_subject_only += 1

        url = _get(row, c_url)
        key = nz.normalize_name(name) or f"row{i}"
        dom = nz.registrable_domain(url)
        if dom:
            key = f"{key}|{dom}"

        counts[key] = counts.get(key, 0) + 1
        routes.setdefault(key, set()).add(_get(row, c_route))

        if key in by_key:
            rec = by_key[key]
            if not rec.website_url and url:
                rec.website_url = url
            sponsor = _get(row, c_sponsor)
            if sponsor and sponsor not in rec.fiscal_sponsor_named:
                rec.fiscal_sponsor_named = "; ".join(
                    x for x in [rec.fiscal_sponsor_named, sponsor] if x)
            continue

        rec = _base(Record(source_key=f"{fc}:{i:05d}"), fc, cfg, as_of)
        rec.name = name
        rec.website_url = url
        rec.raw_location = _get(row, c_loc)
        rec.frame_listing_text = _get(row, c_txt)
        rec.fiscal_sponsor_named = _get(row, c_sponsor)
        if cfg.get("lists_institutions"):
            rec.unit_resolution_flag = PENDING
            rec.unit_resolution_note = (
                "Rule 1: frame may list an institution. Resolve to the unit the FRAME names, "
                "or log unit_unresolved."
            )
        by_key[key] = rec

    n_sponsored = 0
    for key, rec in by_key.items():
        rec.grant_count = str(counts.get(key, 1))
        rt = {r for r in routes.get(key, set()) if r}
        rec.source_route = "; ".join(sorted(rt))
        if rec.fiscal_sponsor_named:
            n_sponsored += 1
            rec.unit_resolution_flag = PENDING
            rec.unit_resolution_note = (
                (rec.unit_resolution_note + " ") if rec.unit_resolution_note else ""
            ) + (
                "FISCAL SPONSOR NAMED. Rule 1 fiscal-sponsor clause: resolve to the SPONSORED "
                "PROJECT if the frame names it and it meets C1 independently, otherwise to the "
                "sponsor. Record the routing. Never enter both as separate records."
            )
        res.kept.append(rec.finalize_keys())

    res.stats = {
        "grant_rows_read": rows_read,
        "organizations_after_within_frame_dedup": len(res.kept),
        "dropped": len(res.dropped),
        "fiscal_sponsor_flagged": n_sponsored,
    }
    if want_prog:
        grants_in = boundary_program_only + boundary_subject_only + boundary_both
        res.stats.update({
            "boundary_rule": b.get("rule", ""),
            "grants_inside_boundary": grants_in,
            "grants_in_program": boundary_program_only + boundary_both,
            "grants_by_subject_only": boundary_subject_only,
            "_narrower_boundary_would_have_held": boundary_program_only + boundary_both,
            "_note": "grants_in_program is what a program-only boundary would have captured; "
                     "grants_by_subject_only is what the chosen wider boundary adds. Report "
                     "both as a measured bound on frame completeness.",
        })
    return res


READERS = {
    "generic": read_generic,
    "ctfg": read_ctfg,
    "cfa": read_cfa,
    "grants": read_grants,
}


def read_frame(frame_code: str, cfg: dict, path, as_of: str) -> FrameResult:
    reader = READERS.get(cfg.get("reader", "generic"))
    if reader is None:
        raise ConfigError(f"{frame_code}: unknown reader '{cfg.get('reader')}'")
    res = reader(frame_code, cfg, path, as_of)
    if not res.kept and not res.dropped:
        # Zero in and zero out is not an empty frame; it is a file the reader
        # could not read. An empty frame still produces boundary drops. Failing
        # here stops a frame silently contributing nothing to the pool.
        raise ConfigError(
            f"{frame_code}: the reader found NO ROWS AT ALL in {path} — neither kept nor "
            f"dropped at the boundary. A genuinely empty frame is not possible here: every "
            f"frame in the register was captured with records in it. Almost always this is "
            f"the file format (is it YAML, CSV or JSON, and does the suffix say so?) or a "
            f"column mapping pointing at a field name the file does not have. Run `inspect` "
            f"against this file."
        )
    return res


def record_fields() -> list[str]:
    return list(asdict(Record()).keys())
