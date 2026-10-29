"""
PICANTE literature strand -- manual reference supplement, step 3 (matching).

Matches references extracted from seed PDFs to OpenAlex records, logs every
decision, and (after human review) writes labelled backward edges in the same
format as round1/edges.csv.

Two modes:

  1. match     python match_references.py match refs/ round1/ manual/
     refs/ holds one file per seed, named with the seed number
     (seed06.tei.xml, seed20.csv, ...). Either format:
       - GROBID TEI XML (processReferences / processFulltextDocument output)
       - CSV with columns: ref_no, raw, first_author, year, title, doi
         (only raw is required; fill what you can)
     Writes manual/match_log.csv and manual/verification_sample.csv.

  2. finalize  python match_references.py finalize manual/match_log.csv round1/ manual/
     Run after review. Refuses to run while any flagged row is unreviewed.
     Writes manual/edges_manual.csv, manual/pool_manual.csv,
     manual/coverage_by_seed.csv.

Review columns in match_log.csv (fill by hand):
  final_decision     blank = accept the automatic match
                     accept | reject | matched_by_hand | not_in_openalex | grey_literature
  manual_openalex_id W-ID, required when final_decision = matched_by_hand
  reviewer, review_date, notes

Matching routes, in order:
  doi         DOI in the reference (or found in its raw text) -> single lookup
  title_auto  title search within +/- YEAR_WINDOW years; accepted only if
              title similarity >= SIM_THRESHOLD AND first-author surname matches
  unmatched   everything else -> needs_review = TRUE
"""
import csv, json, os, random, re, sys, time, unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

import requests

SIM_THRESHOLD = 0.90      # registered acceptance score for automatic title matches
YEAR_WINDOW = 1           # preprint and published years often differ by one
SAMPLE_RATE = 0.10        # share of title_auto matches drawn for second-person check
SAMPLE_SEED = 20261028    # fixed RNG seed so the sample is reproducible; record it

BASE = "https://api.openalex.org"
KEY = os.environ.get("OPENALEX_API_KEY")
FIELDS = ("id,doi,display_name,publication_year,type,language,authorships,"
          "primary_location,abstract_inverted_index,referenced_works,"
          "cited_by_count,is_retracted")
TEI = {"t": "http://www.tei-c.org/ns/1.0"}
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"<>]+", re.I)
ARXIV_RE = re.compile(r"arXiv[:\s]*(\d{4}\.\d{4,5})|arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", re.I)
_log = None


# ---------------------------------------------------------------- API helpers
class StopRun(Exception):
    """OpenAlex keeps refusing requests (rate limit or daily allowance): stop, keep progress."""


PAUSE = 0.15            # seconds between requests, to stay under OpenAlex's per-second limit


def get(path, params=None):
    safe = dict(params or {})                   # what is logged and shown: never the key
    full = dict(safe, api_key=KEY)
    waits = [2, 5, 15, 30, 60, 120]
    for attempt in range(len(waits) + 1):
        time.sleep(PAUSE)
        try:
            r = requests.get(BASE + path, params=full, timeout=60)
        except requests.RequestException as e:
            if attempt == len(waits):
                raise StopRun(f"network error on {path}: {type(e).__name__}")
            time.sleep(waits[attempt]); continue
        if r.status_code in (429, 500, 502, 503) and attempt < len(waits):
            ra = r.headers.get("Retry-After", "")
            time.sleep(min(int(ra), 300) if ra.isdigit() else waits[attempt])
            continue
        break
    _log.write(json.dumps({"utc": datetime.now(timezone.utc).isoformat(), "path": path,
                           "params": safe, "status": r.status_code}) + "\n")
    _log.flush()
    if r.status_code == 404:
        return None
    if r.status_code == 429:
        raise StopRun("OpenAlex returned 429 (too many requests) after waiting about 4 minutes. "
                      "This usually means the daily allowance is used up. Message from OpenAlex: "
                      + r.text[:200].replace(KEY or "\0", "[key]"))
    if r.status_code >= 400:
        raise StopRun(f"OpenAlex returned {r.status_code} for {path} {safe}: "
                      + r.text[:200].replace(KEY or "\0", "[key]"))
    return r.json()


def short(wid):
    return wid.rsplit("/", 1)[-1] if wid else ""


# ---------------------------------------------------------------- text helpers
def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def norm_title(t):
    t = re.sub(r"[\u2019\u2018'`]", "", fold(t))          # isn't -> isnt, not "isn t"
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", t)).strip()


VENUE_TAIL = re.compile(r"\.\s+(?:arXiv\b|In\b|Preprint\b|Proceedings\b|[A-Za-z][\w.&' ]{0,40},\s*\d).*$")
def clean_title(t):
    """Drop venue text the reference parser left on the end of a title."""
    t = re.sub(r"\s*arXiv preprint arXiv:\S+", "", t or "")
    return VENUE_TAIL.sub("", t).strip().rstrip(".")


def surname_ok(surname, rec):
    """First-author surname appears in the candidate's first author name."""
    if not surname or not rec.get("authorships"):
        return False
    a = rec["authorships"][0]
    names = fold(a["author"].get("display_name", "") + " " + (a.get("raw_author_name") or ""))
    return norm_title(surname).split()[-1] in norm_title(names).split()


def clean_doi(d):
    d = (d or "").strip().rstrip(".,;)")
    d = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", d, flags=re.I)
    return d.lower() if d.startswith("10.") else ""


# ---------------------------------------------------------------- reading refs
def seed_number(path):
    m = re.search(r"(\d+)", path.stem)
    if not m:
        sys.exit(f"Cannot read a seed number from file name: {path.name}")
    return int(m.group(1))


def read_tei(path):
    root = ET.parse(path).getroot()
    out = []
    for i, b in enumerate(root.iter("{http://www.tei-c.org/ns/1.0}biblStruct"), 1):
        title = (b.findtext("t:analytic/t:title", namespaces=TEI)
                 or b.findtext("t:monogr/t:title", namespaces=TEI) or "")
        sur = (b.findtext("t:analytic/t:author/t:persName/t:surname", namespaces=TEI)
               or b.findtext("t:monogr/t:author/t:persName/t:surname", namespaces=TEI) or "")
        date = b.find(".//t:imprint/t:date", TEI)
        year = (date.get("when", "")[:4] if date is not None else "")
        doi = b.findtext(".//t:idno[@type='DOI']", namespaces=TEI) or ""
        raw = b.findtext("t:note[@type='raw_reference']", namespaces=TEI) or ""
        out.append({"ref_no": i, "raw": raw.strip(), "first_author": sur.strip(),
                    "year": year, "title": title.strip(), "doi": doi.strip()})
    return out


def read_csv(path):
    rows = list(csv.DictReader(open(path, encoding="utf-8-sig")))
    for i, r in enumerate(rows, 1):
        r.setdefault("ref_no", i)
        for k in ("raw", "first_author", "year", "title", "doi"):
            r[k] = (r.get(k) or "").strip()
    return rows


# ---------------------------------------------------------------- matching
def match_one(ref):
    in_raw = DOI_RE.search(ref["raw"])
    ax = ARXIV_RE.search(ref["raw"] + " " + ref["title"])
    doi = (clean_doi(ref["doi"]) or (clean_doi(in_raw.group(0)) if in_raw else "")
           or (clean_doi("10.48550/arXiv." + (ax.group(1) or ax.group(2))) if ax else ""))
    res = {"route": "unmatched", "openalex_id": "", "matched_title": "",
           "similarity": "", "author_ok": "", "year_diff": "", "doi_used": doi, "note": ""}

    if doi:
        rec = get(f"/works/doi:{doi}", {"select": "id,display_name,publication_year,authorships"})
        if rec:
            res.update(route="doi", openalex_id=short(rec["id"]),
                       matched_title=rec["display_name"], similarity="",
                       author_ok=surname_ok(ref["first_author"], rec))
            return res
        res["note"] = "DOI not found in OpenAlex; tried title"

    title = norm_title(clean_title(ref["title"]))
    if len(title.split()) < 3:
        res["note"] += ("; " if res["note"] else "") + "no usable title parsed"
        return res

    yr = ""
    if ref["year"][:4].isdigit():
        y = int(ref["year"][:4])
        yr = f"publication_year:{y - YEAR_WINDOW}-{y + YEAR_WINDOW}"
    sel = "id,display_name,publication_year,authorships"
    # 1) strict: every title word must appear in the record's title
    page = get("/works", {"filter": f"title.search:{title}" + (f",{yr}" if yr else ""),
                          "per-page": 10, "select": sel}) or {"results": []}
    # 2) fallback: relevance search, used only when the strict search finds nothing
    #    (one stray or garbled word in a parsed title makes the strict search return nothing)
    if not page["results"]:
        page = get("/works", {"search": title, **({"filter": yr} if yr else {}),
                              "per-page": 10, "select": sel}) or {"results": []}
        if page["results"]:
            res["note"] += ("; " if res["note"] else "") + "relevance-search fallback"

    best, best_sim = None, 0.0
    for rec in page["results"]:
        s = SequenceMatcher(None, title, norm_title(rec["display_name"])).ratio()
        if s > best_sim:
            best, best_sim = rec, s
    if best:
        a_ok = surname_ok(ref["first_author"], best)
        yd = (abs(int(ref["year"][:4]) - best["publication_year"])
              if ref["year"][:4].isdigit() and best.get("publication_year") else "")
        res.update(openalex_id=short(best["id"]), matched_title=best["display_name"],
                   similarity=f"{best_sim:.3f}", author_ok=a_ok, year_diff=yd)
        if best_sim >= SIM_THRESHOLD and a_ok:
            res["route"] = "title_auto"
        else:
            res["note"] += ("; " if res["note"] else "") + "best candidate below threshold"
    return res


def cmd_match(refs_dir, round1, outdir):
    seeds = {int(r["seed"]): r["openalex_id"]
             for r in csv.DictReader(open(round1 / "seeds_resolved.csv"))}
    # Progress is saved after every reference, so a stopped run resumes where it left off.
    prog_path = outdir / "match_progress.jsonl"
    done = {}
    if prog_path.exists():
        for line in open(prog_path, encoding="utf-8"):
            if line.strip():
                d = json.loads(line); done[(d["source_file"], str(d["ref_no"]))] = d
        print(f"Resuming: {len(done)} references already matched (from {prog_path.name}).")
    prog = open(prog_path, "a", encoding="utf-8")

    files = [p for p in sorted(refs_dir.iterdir()) if p.suffix.lower() in (".xml", ".csv")]
    rows, total = [], 0
    plan = []
    for path in files:
        refs = read_tei(path) if path.suffix.lower() == ".xml" else read_csv(path)
        plan.append((path, seed_number(path), refs)); total += len(refs)
    count = 0
    try:
        for path, n, refs in plan:
            todo = sum(1 for ref in refs if (path.name, str(ref["ref_no"])) not in done
                       or done[(path.name, str(ref["ref_no"]))]["raw"] != ref["raw"])
            print(f"Seed {n}: {len(refs)} references from {path.name}" + (f" ({todo} to match)" if todo != len(refs) else ""))
            for ref in refs:
                k = (path.name, str(ref["ref_no"]))
                if k in done and done[k]["raw"] == ref["raw"]:
                    rows.append(done[k]); count += 1; continue
                m = match_one(ref)
                needs = m["route"] == "unmatched" or (m["route"] == "doi" and m["author_ok"] is False)
                row = {"seed": n, "seed_openalex_id": seeds.get(n, f"seed:{n}"),
                       "source_file": path.name, **ref, **m,
                       "needs_review": needs, "in_verification_sample": False,
                       "final_decision": "", "manual_openalex_id": "",
                       "reviewer": "", "review_date": "", "notes": ""}
                prog.write(json.dumps(row) + "\n"); prog.flush()
                rows.append(row); count += 1
    except StopRun as e:
        prog.close()
        print(f"\nStopped after {count} of {total} references: {e}")
        print(f"Progress is saved in {prog_path}. Run the same command again to resume "
              f"(after the allowance resets, if it ran out).")
        sys.exit(2)
    prog.close()

    autos = [r for r in rows if r["route"] == "title_auto"]
    rng = random.Random(SAMPLE_SEED)
    for r in rng.sample(autos, max(1, round(len(autos) * SAMPLE_RATE)) if autos else 0):
        r["in_verification_sample"] = True

    cols = list(rows[0].keys()) if rows else []
    with open(outdir / "match_log.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, cols); w.writeheader(); w.writerows(rows)
    with open(outdir / "verification_sample.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, cols); w.writeheader()
        w.writerows(r for r in rows if r["in_verification_sample"])

    by = defaultdict(lambda: defaultdict(int))
    for r in rows:
        by[r["seed"]][r["route"]] += 1
    print("\nseed  doi  title_auto  unmatched")
    for n in sorted(by):
        print(f"{n:>4}  {by[n]['doi']:>3}  {by[n]['title_auto']:>10}  {by[n]['unmatched']:>9}")
    print(f"\nFlagged for review: {sum(r['needs_review'] for r in rows)}; "
          f"verification sample: {sum(r['in_verification_sample'] for r in rows)} "
          f"(RNG seed {SAMPLE_SEED}). Wrote {outdir / 'match_log.csv'}")


# ---------------------------------------------------------------- finalize
def abstract(inv):
    if not inv:
        return ""
    pos = {p: w for w, ps in inv.items() for p in ps}
    return " ".join(pos[i] for i in sorted(pos))


def cmd_finalize(log_path, round1, outdir):
    rows = list(csv.DictReader(open(log_path, encoding="utf-8-sig")))
    allowed = {"", "accept", "reject", "matched_by_hand", "not_in_openalex", "grey_literature"}
    problems = []
    for r in rows:
        d = r["final_decision"].strip().lower()
        if d not in allowed:
            problems.append(f"seed {r['seed']} ref {r['ref_no']}: unknown decision '{d}'")
        flagged = r["needs_review"] == "True" or r["in_verification_sample"] == "True"
        if flagged and (not d or not r["reviewer"].strip()):
            problems.append(f"seed {r['seed']} ref {r['ref_no']}: flagged but not reviewed")
        if d == "accept" and not r["openalex_id"].strip():
            problems.append(f"seed {r['seed']} ref {r['ref_no']}: 'accept' but the row has no candidate")
        if d == "matched_by_hand" and not r["manual_openalex_id"].strip():
            problems.append(f"seed {r['seed']} ref {r['ref_no']}: matched_by_hand without an ID")
    if problems:
        sys.exit("Not finalized:\n  " + "\n  ".join(problems[:40]))

    # Final ID per reference.
    for r in rows:
        d = r["final_decision"].strip().lower()
        if d == "matched_by_hand":
            r["final_id"] = r["manual_openalex_id"].strip()
        elif d == "accept" and r["openalex_id"]:
            r["final_id"] = r["openalex_id"]          # reviewer accepted the candidate shown
        elif r["route"] in ("doi", "title_auto") and d == "":
            r["final_id"] = r["openalex_id"]
        else:
            r["final_id"] = ""

    # Which links OpenAlex already had (so only genuinely new links are added).
    oa_back = defaultdict(set)
    for e in csv.DictReader(open(round1 / "edges.csv")):
        if e["direction"] == "backward":
            oa_back[int(e["seed"])].add(e["cited_id"])
    yields = {int(y["seed"]): int(y["backward"]) for y in csv.DictReader(open(round1 / "yields.csv"))}

    edges, cov = [], defaultdict(lambda: defaultdict(int))
    seen = set()
    for r in rows:
        n, fid = int(r["seed"]), r["final_id"]
        c = cov[n]; c["pdf_refs"] += 1
        d = r["final_decision"].strip().lower()
        if d in ("not_in_openalex", "grey_literature", "reject"):
            c[d] += 1
        elif not fid:
            c["unresolved"] += 1
        if fid:
            c["matched"] += 1
            if fid in oa_back[n]:
                c["already_in_openalex"] += 1
            elif (n, fid) not in seen:
                seen.add((n, fid)); c["new_links"] += 1
                edges.append((r["seed_openalex_id"], fid, "backward", n, "manual_pdf",
                              r["route"] if d != "matched_by_hand" else "by_hand"))

    with open(outdir / "edges_manual.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["citing_id", "cited_id", "direction", "seed", "source", "match_route"])
        w.writerows(edges)

    with open(outdir / "coverage_by_seed.csv", "w", newline="") as f:
        w = csv.writer(f)
        keys = ["pdf_refs", "matched", "already_in_openalex", "new_links",
                "not_in_openalex", "grey_literature", "reject", "unresolved"]
        w.writerow(["seed", "openalex_backward_round1", "openalex_coverage"] + keys)
        for n in sorted(cov):
            ob = yields.get(n, 0)
            share = f"{ob / cov[n]['pdf_refs']:.0%}" if cov[n]["pdf_refs"] else ""
            w.writerow([n, ob, share] + [cov[n][k] for k in keys])

    # Fetch metadata for works not already in the round-1 pool.
    in_pool = {r["openalex_id"] for r in csv.DictReader(open(round1 / "pool_prededup.csv"))}
    new_ids = sorted({e[1] for e in edges} - in_pool)
    recs = []
    for i in range(0, len(new_ids), 50):
        page = get("/works", {"filter": "openalex:" + "|".join(new_ids[i:i + 50]),
                              "per-page": 50, "select": FIELDS})
        recs += page["results"] if page else []
    with open(outdir / "pool_manual.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["openalex_id", "doi", "title", "year", "type", "language", "venue",
                    "authors", "abstract", "is_retracted", "is_seed", "source"])
        for r in recs:
            src = ((r.get("primary_location") or {}).get("source") or {}).get("display_name", "")
            w.writerow([short(r["id"]), r.get("doi"), r.get("display_name"), r.get("publication_year"),
                        r.get("type"), r.get("language"), src,
                        "; ".join(a["author"]["display_name"] for a in r.get("authorships", [])),
                        abstract(r.get("abstract_inverted_index")), r.get("is_retracted"),
                        False, "manual_pdf"])

    agree = [r for r in rows if r["in_verification_sample"] == "True"]
    ok = sum(1 for r in agree if r["final_decision"].strip().lower() in ("", "accept"))
    print(f"{len(edges)} new backward links; {len(recs)} works new to the pool.")
    if agree:
        print(f"Verification sample: {ok}/{len(agree)} automatic title matches confirmed "
              f"({ok / len(agree):.0%}). Report this figure.")
    print(f"Wrote edges_manual.csv, pool_manual.csv, coverage_by_seed.csv to {outdir}")


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    if len(sys.argv) != 5 or sys.argv[1] not in ("match", "finalize"):
        sys.exit(__doc__)
    if not KEY:
        sys.exit("Set OPENALEX_API_KEY first.")
    mode, a, round1, outdir = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    outdir.mkdir(parents=True, exist_ok=True)
    _log = open(outdir / "access_log.jsonl", "a")
    (cmd_match if mode == "match" else cmd_finalize)(a, round1, outdir)
