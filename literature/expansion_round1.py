"""
PICANTE literature strand -- citation-network expansion, round 1 (seeds only).

Backward (references) and forward (citing works) chasing from the frozen seeds
via the live OpenAlex API. Every request is logged with a UTC timestamp so the
API access dates can be reported, as the preregistration requires.

Usage:
    export OPENALEX_API_KEY=...        # free key from openalex.org/settings/api
    pip install requests openpyxl
    python expansion_round1.py TPG_seed_set_v3.xlsx out/

Outputs (in out/):
    raw/                 raw JSON for every response, untouched
    seeds_resolved.csv   seed # -> DOI -> OpenAlex W-ID
    edges.csv            citing_id, cited_id, direction, seed
    pool_prededup.csv    every retrieved record (seeds included), one row per work
    yields.csv           per-seed backward / forward counts
    access_log.jsonl     one line per API request
"""
import csv, json, os, sys, time
from datetime import datetime, timezone
from pathlib import Path

import openpyxl
import requests
import dotenv
dotenv.load_dotenv()

BASE = "https://api.openalex.org"
KEY = os.environ.get("OPENALEX_API_KEY")
FIELDS = ("id,doi,display_name,publication_year,type,language,authorships,"
          "primary_location,locations,abstract_inverted_index,referenced_works,"
          "cited_by_count,is_retracted")

if not KEY:
    sys.exit("Set OPENALEX_API_KEY first.")

seed_file, out = Path(sys.argv[1]), Path(sys.argv[2])
(out / "raw").mkdir(parents=True, exist_ok=True)
log = open(out / "access_log.jsonl", "a")
n_req = 0


def get(path, params=None):
    """GET with key, retry on 429/5xx, log, and save the raw response."""
    global n_req
    params = dict(params or {}, api_key=KEY)
    for attempt in range(5):
        r = requests.get(BASE + path, params=params, timeout=60)
        if r.status_code in (429, 500, 502, 503):
            time.sleep(2 ** attempt)
            continue
        r.raise_for_status()
        break
    n_req += 1
    stamp = datetime.now(timezone.utc).isoformat()
    safe = {k: v for k, v in params.items() if k != "api_key"}
    log.write(json.dumps({"n": n_req, "utc": stamp, "path": path, "params": safe}) + "\n")
    (out / "raw" / f"{n_req:06d}.json").write_text(r.text)
    return r.json()


def short(wid):
    return wid.rsplit("/", 1)[-1] if wid else None


# 1. Read seeds. Seed 20 has no identifier and is skipped by design (prereg 1.6).
ws = openpyxl.load_workbook(seed_file, data_only=True)["Seed set (23)"]
hdr = [c.value for c in ws[1]]
seeds = []
for row in ws.iter_rows(min_row=2, values_only=True):
    rec = dict(zip(hdr, row))
    doi = str(rec["DOI / stable ID"] or "")
    if doi.startswith("10."):
        seeds.append((int(rec["Seed #"]), doi))
    else:
        print(f"Seed {rec['Seed #']}: no DOI -- contributes no neighbourhood (recorded, not replaced)")

# 2. Resolve each seed DOI to its OpenAlex work (single-entity lookups).
works, seed_ids = {}, {}
with open(out / "seeds_resolved.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["seed", "doi", "openalex_id", "cited_by_count", "n_refs"])
    for n, doi in seeds:
        rec = get(f"/works/doi:{doi}", {"select": FIELDS})
        works[rec["id"]] = rec; seed_ids[n] = rec["id"]
        w.writerow([n, doi, short(rec["id"]), rec["cited_by_count"], len(rec["referenced_works"])])

# 3. Backward + forward chasing per seed.
edges, yields = [], []
for n, sid in seed_ids.items():
    # Backward: referenced_works are already on the seed record; fetch them in
    # batches of 50 so the pool has full metadata and abstracts for screening.
    refs = works[sid]["referenced_works"]
    for i in range(0, len(refs), 50):
        batch = "|".join(short(x) for x in refs[i:i + 50])
        for rec in get("/works", {"filter": f"openalex:{batch}", "per-page": 50, "select": FIELDS})["results"]:
            works.setdefault(rec["id"], rec)
    edges += [(sid, r, "backward", n) for r in refs]

    # Forward: every work that cites the seed, paged with a cursor.
    fwd, cursor = [], "*"
    while cursor:
        page = get("/works", {"filter": f"cites:{short(sid)}", "per-page": 200,
                              "cursor": cursor, "select": FIELDS})
        for rec in page["results"]:
            works.setdefault(rec["id"], rec); fwd.append(rec["id"])
        cursor = page["meta"].get("next_cursor") if page["results"] else None
    edges += [(c, sid, "forward", n) for c in fwd]
    yields.append((n, short(sid), len(refs), len(fwd)))
    print(f"Seed {n}: {len(refs)} backward, {len(fwd)} forward")

# 4. Write outputs. The pool is PRE-deduplication and includes the seeds, so the
#    validation check can be run against it before seeds are removed (prereg 2.4).
with open(out / "edges.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["citing_id", "cited_id", "direction", "seed"])
    w.writerows((short(a), short(b), d, n) for a, b, d, n in edges)

with open(out / "yields.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["seed", "openalex_id", "backward", "forward"])
    w.writerows(yields)

def abstract(inv):
    if not inv: return ""
    pos = {p: word for word, ps in inv.items() for p in ps}
    return " ".join(pos[i] for i in sorted(pos))

with open(out / "pool_prededup.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["openalex_id", "doi", "title", "year", "type", "language", "venue",
                "authors", "abstract", "is_retracted", "is_seed"])
    seed_set = set(seed_ids.values())
    for wid, r in works.items():
        src = ((r.get("primary_location") or {}).get("source") or {}).get("display_name", "")
        w.writerow([short(wid), r.get("doi"), r.get("display_name"), r.get("publication_year"),
                    r.get("type"), r.get("language"), src,
                    "; ".join(a["author"]["display_name"] for a in r.get("authorships", [])),
                    abstract(r.get("abstract_inverted_index")), r.get("is_retracted"),
                    wid in seed_set])

print(f"\n{len(works)} unique works, {len(edges)} edges, {n_req} requests. See {out}/")
