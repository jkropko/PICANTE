# AI validation harness — organizational strand

Enforces the guardrails in sheet 1 item 4.3 of the protocol workbook, and computes the statistics the registration commits you to reporting. No third-party dependencies except openpyxl, which is used only by `check-codebook`.

| File | What it is |
| --- | --- |
| `ai_harness.py` | Validation, verbatim fidelity, Role 3 sealing, per-field logging |
| `ai_metrics.py` | Role 1 gate, Role 2 recall, human-to-AI agreement, RA-to-RA agreement |
| `fields.json` | Field names, controlled values, thresholds — the harness's only source of truth |
| `test_harness.py` | 59 tests, each named for the failure it guards against |

```
python test_harness.py
python ai_harness.py check-codebook --workbook ../TPG_org_strand_protocol_v3.xlsx
python ai_harness.py ingest --role 1 --record rec.json --response resp.json
python ai_metrics.py role1-gate --truth handcoded.jsonl
```

## What it enforces

**Verbatim fidelity, programmatically.** Every quote must be an exact substring of the source it cites, at the offsets claimed. Three verdicts, and the distinction matters: `offset_mismatch` (quote is on the page but not where claimed) is usually a re-extraction artifact; `not_found` is the model having written text that was never on the page. The second is counted and reported separately, because it is the number a reader assessing an AI-assisted workflow actually wants.

**Rejection means routing, never retrying.** A field that fails validation is coded by a human unaided and the routing is logged. The harness never re-requests a field. A retry loop would select for well-formed output rather than accurate output, and the accuracy figure computed afterwards would be measuring the loop.

**Role boundaries.** Role 1 responses containing a Group 3 field reject the record. Role 2 candidates carrying anything that looks like a proposed value — a lexicon term, a tier, a placement, a speaker, a confidence score — reject the record, because the point of Role 2 is that the coder's judgment is unprompted. Role 3 responses touching the self-label block reject the record.

**Blinding, with a commitment.** Role 3 output is written to a sealed directory the coding interface never reads; only a SHA-256 commitment goes into the open log at production time. Release requires an adjudicated human value in the decisions log and re-verifies the commitment. Tampering with a sealed file after the fact is detected and the record refused. A second blind coding of the same record is refused outright, since allowing one would let the first be discarded after the humans' values were known.

The commitment is worth the twenty lines it costs. Without it, "the AI coded this blind" is a claim a reader has to take on trust; with it, the timestamped hash shows the output existed before the human value was recorded.

## Two things the checker found in your workbook

`check-codebook` compares `fields.json` against sheet 4 using subset semantics: a role may propose *fewer* values than the codebook allows, never a value it doesn't contain. Running it against v3 produces one of each.

**Restricted, and deliberate.** Role 1 may not propose `unit_known_not_surfaced` on `unit_resolution_flag`. That code means a unit exists that the frame did not name — which requires knowing about a unit from outside the supplied text, exactly what the model is forbidden to do. Humans keep the code; the model doesn't get it.

**A real conflict, needing your decision.** Sheet 3's C1 rule says that where a listing cannot be resolved to any organization, code `unresolvable` rather than fail. Sheet 4's controlled list for `screening_C1_unit` is `pass / fail`, and puts `unresolvable` on `screening_decision` instead. Both cannot be right. Either add `unresolvable` to the C1 list in sheet 4, or amend sheet 3's rule text to say the code is recorded at `screening_decision`. It is a one-cell edit either way, but it decides where a reported count comes from, and it needs making before collection rather than after.

`fields.json` currently follows sheet 3, so the check exits non-zero until you settle it.

## Inputs you supply

**`run/logs/decisions.jsonl`** — appended by your coding interface, not by the harness:

```json
{"ts_utc": "...", "org_id": "CTFG-0417", "stage": "independent", "coder": "RA1", "fields": {"screening_C3_constitutive": "pass"}}
{"ts_utc": "...", "org_id": "CTFG-0417", "stage": "adjudicated", "fields": {"screening_C3_constitutive": "pass"}}
```

`independent` lines drive RA-to-RA agreement; `adjudicated` lines gate Role 3 release and drive human-to-AI agreement.

**Truth files** for the two validation commands: `{"org_id": ..., "fields": {...}}` for the Role 1 gate, `{"org_id": ..., "selected_phrases": [...]}` for Role 2 recall.

## On the agreement statistics

`ra-agreement` and `role3-agreement` are the same arithmetic and mean opposite things, which is why they are separate commands with separate output. RA-to-RA kappa is a property of the instrument and carries the 0.60 benchmark. Human-to-AI kappa is descriptive and carries none — Role 3 never contributes to a coded value, so a low figure says something about the model, not about the codebook's reliability. Printing them in one table would invite exactly the comparison that isn't meaningful.

Where one category takes more than 85% of codings, kappa is unstable and the field is judged on percentage agreement at 90% instead, per the registered rule. Where a category is used for every record by both coders, kappa is undefined rather than zero, and the harness says so instead of printing a number.

`role3-agreement` warns when it is computing on a subset of sealed records, since a figure computed over whichever records happened to get released is not the reportable figure.

## Still to wire up

The API adapter is deliberately absent: the harness takes a response from anywhere, which is what makes it testable offline and what lets you re-run validation over archived responses without re-billing the calls. A thin `call_model` wrapper that writes its raw output to a file is all that's needed between the prompt files and `ingest`.
