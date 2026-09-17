# O3 — enumeration and deduplication

Turns the frozen frame snapshots into a deduplicated candidate pool of organization-level units, with the provenance the later stages depend on. No third-party dependencies.

| File | What it is |
| --- | --- |
| `capture_log.py` | O2 close-out: hashes the snapshots, logs the capture, writes `sources.json` |
| `enumerate_o3.py` | CLI: inspect, enumerate, dedupe-candidates, apply-merges, prisma |
| `frames_io.py` | One reader per frame shape; applies each registered boundary |
| `dedupe.py` | Cross-frame candidate generation, merge application, org_id assignment |
| `normalize.py` | Name, domain and location normalization |
| `config/frames.json` | Frame codes, blocks, boundaries (registered) and column mappings (not) |
| `config/operators.json` | Rule 2 operator list, with the six contested entries marked UNDECIDED |
| `test_enumerate_o3.py` | 56 tests, each named for the failure it guards against |

```
python test_enumerate_o3.py
python capture_log.py log --snapshots snapshots --as-of 2026-10-01
python enumerate_o3.py inspect --frame CFA --file snapshots/CFA/organizations.json
python enumerate_o3.py enumerate --sources sources.json --out run
python enumerate_o3.py dedupe-candidates
python enumerate_o3.py apply-merges
python enumerate_o3.py prisma
```

## O2 — closing out the capture

Lay the snapshots out one directory per frame code. A directory holding one data file needs nothing else; a directory holding several needs a `primary.txt` naming the file `enumerate` should read, because guessing which export is the frame of record is not a decision a script should make. Drop the archive URL in `wayback.txt`, one per line. For CFA, clone the repo into the directory — the commit SHA is read from the working tree rather than typed.

`log` hashes every file, reads the CFA commit, counts rows, checks each frame against the register's size estimate, and writes `capture_log.json` plus a `sources.json` already pointed at the right files. It exits non-zero on a missing frame, an ambiguous primary, or a CFA capture with no commit SHA.

The size check is a warning, never a refusal — a count outside the estimate may mean the frame moved since the register was written, which is a finding, or that the wrong file was saved, which is a mistake, and the script cannot tell which. The one it is most worth heeding is CTFG: a count in the low thousands almost always means the boundary filter was applied at capture, which leaves the two O8 audit pools with nothing to draw from.

`verify` re-hashes against the log later, so before O3 you can confirm nothing moved between the freeze and the enumeration. `enumerate` hashes its inputs again into `run_manifest.json`, so the two can be compared after the fact as well.

## The three things the script will not do

**It will not decide.** Unit resolution, fiscal-sponsor routing and every merge are registered human judgments. Where the script can tell one is needed it sets `PENDING`, writes the frame's own listing text onto the record, and queues it — `unit_resolution_worksheet.csv` and `dedupe_candidates.csv` are worksheets for a coder, not outputs.

**It will not run with the operator list open.** Rule 2 operators enter the pool by construction at this stage, so `enumerate` exits 3 while any entry in `operators.json` reads UNDECIDED. Six do: Schmidt, Knight, DSSG, DataKind, NDIA and NetGain all operate frames that were considered and rejected. On the registration's own wording — operators of frames *used in this study* — all six are out, but that is your call and it needs a date.

**It will not treat an unreviewed pair as a non-duplicate.** `apply-merges` exits 3 if any proposed pair has a blank decision. A blank is not evidence of anything, and letting it default to SEPARATE would put an unexamined judgment into the dataset while looking like a coder had made it.

## Before the first real run

Column names and the CFA tag vocabulary are placeholders. Every one reading `CONFIRM` must be mapped against the actual frozen file, and any reader hitting one refuses rather than guessing. `inspect` prints each snapshot's columns with non-empty counts and a sample value, and for CFA the full tag inventory with counts, which is what you set `include_any` and `exclude_any` from.

**One boundary decision is yours and is flagged in `frames.json`.** For CFA, `location_rule` defaults to `drop_clearly_non_us`: records whose location reads US *or cannot be determined* stay in, and only positively non-US records leave. That mirrors CTFG, whose registered boundary deliberately retains country-missing records so C2 — a human determination at O4 — decides them rather than a string match at enumeration. The alternative, `keep_us_only`, drops the undeterminable ones too and matches the register's "~125 US (of 221)" estimate more literally. It changes the enumerated count and cannot be revisited without re-enumerating, so set it before the first run.

`us_location_guess` is asymmetric on purpose: an unrecognized location returns UNKNOWN, never NON_US. Nothing leaves a frame because the function failed to recognize a string. It is a boundary aid and is never wired to C2.

## What `enumerate` writes

- `enumerated_pool.csv` — the candidate pool before cross-frame dedup
- `dropped_at_boundary.csv` — every record a boundary excluded, with the reason, so the PRISMA accounting can show what the boundary cost
- `ctfg_audit_stratum_a.csv` / `ctfg_audit_stratum_b.csv` — the two O8 audit pools, which sit *outside* the CTFG boundary and therefore only exist if the full export was captured at freeze. Stratum (a) is type-present-and-not-Organization, per workbook v4; read as merely "not typed Organization" it would contain stratum (b) entirely and the two samples would not be independent. A test asserts they are disjoint.
- `unit_resolution_worksheet.csv` — every PENDING record with the frame's listing text
- `run_manifest.json` — SHA-256 of every input and config file, the CFA commit SHA, script versions, the freeze date, and per-frame counts

## Frame-specific behaviour worth knowing

**GORG** rejects any row whose cohort is not one of the four named cohorts. This is what keeps the six organizations listed under "Previously funded recipients" on the AI for Science page out of the frame — they belong to the earlier inaugural AI for Science fund, not to a named cohort, and enumerating them would silently widen the frame. Checked 2026-09-16: AI for Government Innovation published its 15 recipients on 15 September and is capturable; AI for Science has not published and is recorded as pending.

**FORD** refuses to run without a `source_route` column, because it is a two-source frame — the live topic-filtered database plus 990-PF filings from 2011 — and which source a grantee came from has to be on the record.

**FORD and MCGV** collapse grants to organizations within the frame and keep `grant_count`. Any row naming a fiscal sponsor is flagged PENDING with the Rule 1 clause quoted, including the instruction never to enter both the sponsor and the project.

**PITUN** emits every record PENDING, since the frame lists universities, and carries the frame's own listing text — which is what Rule 1 resolves against, and the only thing it may resolve against.

## Deduplication

Candidates are blocked on registrable domain and on name tokens, scored, and written with the reason in words a coder can check against the sources. Within-frame pairs are not proposed; that is the reader's job. Cross-block pairs are marked `cross_block = YES`, because those records are the multi-frame subset that sensitivity check (f) depends on — a wrong merge there destroys the analysis, so they deserve the closest look.

Merging preserves everything. The survivor carries every originating frame in register order, every source key, and any PENDING flag from any member of the group. Merges are transitive. `org_id`s are assigned after dedup, deterministically, so a re-run of the same pool with the same decisions produces the same IDs.

## What this does not touch

C1 and C2 (O4). The lexicon proxy and the coding queue (O5) — `lexicon_proxy.py` runs against the passing pool after screening, not here. Every count the `prisma` command prints is over the enumerated pool, before any screening, and describes no population.
