# TPG Organizational Strand — Responsibility Table

Every step of the organizational strand, showing who does what.

**Coders:** Jon Kropko (lead reviewer / PI), Akshita and Carmen (research assistants).

---

## Key to the AI column

The model has exactly three registered roles, and one governing constraint: **AI never precedes independent human judgment on a Group 3 field.** If both RAs saw the same recommendation before coding, their codings would be correlated through it, and the human-to-human agreement statistic would measure the model's persuasiveness rather than the instrument's reliability.

| Role | What it does | Constraint |
| --- | --- | --- |
| **Role 1** | Proposes a value plus the supporting passage on Group 1 mechanical fields, including C1 and C2 | Every proposal verified against the source by an RA before it is accepted. Gated at 95% field-level accuracy. |
| **Role 2** | Returns candidate passages with exact character spans on the self-label fields | Proposes **no values**. The model locates; the human judges. |
| **Role 3** | Codes the Group 3 judgment fields blind | Output withheld from all three humans until the adjudicated value is recorded. Never contributes to a coded value. |

**The AI never:** assigns tier, adjudicates a disagreement, codes the inductive categories, or makes any synthesis decision. The lexicon proxy is deterministic pattern matching, not a model.

**Group definitions:** Group 1 = mechanical fields (enumeration, dedup, C1, C2, status, ecosystem role, partners, descriptive fields). Group 2 = self-label and non-lexicon description fields, including tier. Group 3 = judgment fields (C3, C4, C5, and the five framework dimensions).

**Splitting Group 1 and Group 2:** the protocol says "one RA" decides these, without fixing which. Agree an assignment convention before O4 — per record or per frame — and record it, so the division is documented rather than ad hoc.

---

## Stage 0 — Fixes before anything starts

None of these needs a new filing; they are corrections and specifications of rules already registered. Date each one so the record shows it was settled before data was seen.

| Step | Jon (PI) | Akshita & Carmen | AI |
| --- | --- | --- | --- |
| Confirm both RAs are available and hours are budgeted | Decides and confirms | Confirm availability; one RA needed from O4, all three coders from O6 | None |
| Agree the Group 1 / Group 2 assignment convention | Sets the convention | Follow it; record it in the log | None |
| **Framework dimensions — RESOLVED.** Preregistration update 2 separates them into five: `who_participates`, `who_benefits`, `what_counts_as_social_good`, `who_decides`, `what_counts_as_relevant_technology`. Codebook v3 and the literature charting form both conform | Files the update before O2; confirms the charting form matches | — | None |
| Confirm `technologies` (six-way select) stays a descriptive field, and add a Group 3 field if "relevant technology" is adopted as a dimension | Decides | — | None |
| **Settle the Rule 2 operator list.** Registration scope is operators of frames *used*: PIT-UN, Ford, CTFG, ACT, Code for America, Fast Forward, McGovern, Google.org, plus New America. Workbook also lists Schmidt, Knight, DSSG, DataKind, NDIA, NetGain — all rejected frames | Decides in or out for each of the six | — | None |
| **Fix the lexicon proxy: `civic tech` must match the closed compound.** `govtech` matches with or without a separator; `civic tech` does not, so "civictech" and "CivicTech" miss entirely | Approves as a spelling variant, not a broadening | Either RA can make the edit | None — deterministic pattern matching |
| **Fix the proxy script to read `frozen_lexicon.json`** instead of its hardcoded copy. The JSON claims it is read at runtime and is not | Approves | Either RA can make the edit; bump the script version | None |
| **Write the saturation rule for `undetermined` values.** Nothing currently addresses this. Six organizations in a row whose sites do not address who benefits or who decides would stop a block without saturation occurring | Decides and writes it into the codebook | — | None |
| Correct probe size to **50** (not 200) and status to **not optional** | Corrects the workbook | — | None |
| Correct unit-resolution sensitivity to a **reported bound**, not a recomputation | Corrects the workbook | — | None |
| Correct inductive-coding agreement to the **full set** of pooled phrases, not a subsample | Corrects the workbook and the registration text | — | None |
| Define CTFG audit stratum (a) as "type present and not Organization," so the two audit samples do not overlap | Decides | — | None |
| Move the Role 1 validation to before O4 (see O4 row) | Decides | — | None |
| Write out what SE, DS, OD, UX, POL, HW mean in `technologies` | Approves | Either RA can draft | None |
| Clean `originating_frame` allowed values — drop NAPIT, KNIGHT, SCHM unless retained as operators | Decides | Either RA can edit | None |
| Decide how the ~40 calibration organizations are spread across blocks | Decides | — | None |

---

## O2 — Freeze the register

| Step | Jon (PI) | Akshita & Carmen | AI |
| --- | --- | --- | --- |
| Pick one freeze date without looking at any frame's contents | Decides | — | None |
| Between filing and freeze, do not inspect frames beyond confirming listings load | Enforces | Observe | None |
| **CTFG: capture the FULL export**, not the filtered subset — the O8 audits draw from records outside the frame boundary | Confirms scope | Capture and verify record count | None |
| CFA: pin `organizations.json` to a commit SHA | — | Capture and record the SHA | None |
| Ford: manual export of the topic-filtered active-grant view (human-verification gate), plus 990-PF filings from 2011 | Decides topic assignment method | Capture both sources; record which source each grantee came from | None |
| PIT-UN: confirm the 2026–27 cohort is in the directory; capture the full institution list | — | Capture list, not just count | None |
| ACT: capture the exact member list | — | Capture | None |
| Fast Forward and McGovern: capture portfolio and grants listings | — | Capture | None |
| Google.org: capture the four named cohorts only; 2019 from an archive; mark unpublished cohorts pending | Decides pending handling | Capture; record enumeration dates separately | None |
| Archive a web capture of every frame source page on the freeze date | — | Capture and verify | None |
| Record as-of dates in the register; deposit snapshots on OSF | Confirms | Deposit | None |

---

## O3 — Enumerate and deduplicate

| Step | Jon (PI) | Akshita & Carmen | AI |
| --- | --- | --- | --- |
| Enumerate each frame in full from its snapshot under its recorded boundary definition | Spot-checks | Enumerate | None at this step |
| CTFG boundary: type contains Organization AND (US or country missing) — roughly 1,099 candidates | — | Apply and record the count | None |
| CFA: tag-filter out non-brigades (18F, Code for All, OK Labs, Code for Poland, government); normalize city strings before the US filter | Resolves ambiguous cases | Filter and normalize | None |
| McGovern: unit is grants, not organizations — dedupe to organizations before counting | — | Dedupe | None |
| Apply Rule 1 unit resolution; log `resolved` / `unit_unresolved` / `unit_known_not_surfaced` | Resolves ambiguous cases | Apply and log | None |
| Apply the fiscal-sponsor clause; never enter sponsor and project as separate records | Resolves ambiguous cases | Apply and log the routing | None |
| Add every frame operator to the pool by construction, flagged, with frames operated | Confirms against the Stage 0 list | Add and flag | None |
| Dedupe to organization-level units; record merges with parent IDs; retain multi-frame provenance | Spot-checks | Dedupe and record | Role 1 may propose dedup candidates; RA verifies each |

---

## O4 — First screening pass

| Step | Jon (PI) | Akshita & Carmen | AI |
| --- | --- | --- | --- |
| **Validate Role 1 first.** The registered gate refers to calibration values that do not exist until O6, so validate against a small hand-coded set before this stage | Approves the hand-coded reference set; confirms the gate is cleared | Hand-code the reference set | Role 1 runs against it; must reach 95% field-level accuracy per Group 1 field |
| Revise prompts where a field falls short; drop AI from any field still short and report it | Decides | Recode those fields unassisted | Role 1 excluded from failing fields |
| Run Role 1 over the pool on Group 1 fields including C1 and C2 | — | Receive proposals | **Role 1:** proposes value + supporting passage |
| Verify every proposal against the source — no proposal accepted without opening the source | — | One RA verifies every record | Proposal only; never authoritative |
| Determine C2 by hand where frame location data is missing (~476 CTFG records — the largest manual cost in the strand) | Resolves ambiguous cases | One RA determines from the organization's own materials | May propose; RA determines |
| Code unresolvable listings as `unresolvable`; keep the count | — | Code and count | May flag candidates |
| Record the first criterion failed for every exclusion | — | Record | None |
| Re-check a random 10% of records per block against recorded evidence; report the error rate and the RA override rate | **Jon does this check** | — | None |

---

## O5 — Build the coding queue

| Step | Jon (PI) | Akshita & Carmen | AI |
| --- | --- | --- | --- |
| Run the corrected proxy script over the passing pool | — | Run | None — deterministic matching |
| Re-run with `--retry-undetermined` to clear transient failures | — | Run | None |
| Resolve every remaining `UNDETERMINED` by hand before building the queue | Resolves hard cases | Resolve by hand | None |
| Stratify each block by originating frame and by proxy value | — | Build strata | None |
| Assign multi-frame records to the first-listed frame's stratum, keeping provenance | — | Assign | None |
| Fix the draw order: round-robin across strata, random within, recorded seed | Approves the seed | Generate and record | None |
| Deposit the seed and queue order on OSF | Confirms | Deposit | None |
| Never report the proxy as tier or use it to prefill tier | Enforces | Observe | None |

---

## O6 — Calibrate

| Step | Jon (PI) | Akshita & Carmen | AI |
| --- | --- | --- | --- |
| Draw ~20 organizations spanning all three blocks | Draws per the Stage 0 distribution decision | — | None |
| Code the calibration set independently on the full instrument | **Codes independently** | **Both code independently** | Withheld |
| Discuss disagreements; revise codebook and field wording where the instrument is at fault — especially the five dimensions, all of which arrive marked PILOT with no rubrics | Leads revision, decides final wording | Contribute | None |
| Repeat on a fresh set of ~20 | Codes | Both code | Withheld |
| Compute and report agreement; kappa ≥ 0.60 per judgment field is the **benchmark, not a gate** | Computes and reports | — | None |
| Keep double coding regardless of agreement; a below-benchmark field is reported with its statistic, used descriptively, excluded from cross-block claims | Decides and documents | — | None |
| Calibrate status coding (dormant vs closed is genuinely ambiguous for small volunteer orgs) | Adjudicates | Both code | None |
| Validate Role 2 (report passage recall, no gate) and Role 3 (no gate) against adjudicated values | Reviews and reports | — | Roles 2 and 3 run against the calibration set |
| Discard all calibration records from the analytic dataset | Confirms | Remove | None |
| File a preregistration update recording revised wording and agreement results; carry dimension changes to the literature strand | **Jon files** | — | May draft prose (non-decisional, disclosed) |

---

## O7 — Screen and code

| Step | Jon (PI) | Akshita & Carmen | AI |
| --- | --- | --- | --- |
| Draw the next record from the fixed queue | — | Draw in order | None |
| Apply C3, C4, C5 | **Adjudicates every disagreement** | **Both code independently, every record** | **Role 3:** codes blind, withheld until adjudication is recorded |
| Code the self-label fields: verbatim phrase, lexicon term matched, URL, access date, placement, speaker, and **tier** | Re-derives tier from phrase + placement + speaker for every record | One RA decides every field | **Role 2:** returns candidate passages with exact spans; proposes no values, never assigns tier |
| Record any categorial self-description matching no lexicon term, verbatim, with full evidence. Do not normalize toward a lexicon term | Spot-checks | One RA records | Role 2 may locate; RA decides |
| Code status (active / dormant / closed) with a date and a dated evidence artifact | Spot-checks in the 10% | One RA decides, verifying every proposal | Role 1 may propose |
| Code the five framework dimensions | **Adjudicates every disagreement** | **Both code independently, every record** | **Role 3:** blind, withheld |
| Archive a capture of every page supporting a self-label, non-lexicon description, or status determination | — | Capture | None |
| Record anything undeterminable as `undetermined` with a note; route to adjudication rather than guessing | Adjudicates; reports what stays undetermined | Record, do not guess | Instructed to return undetermined where evidence is absent |
| Verify a random 10% per block against recorded evidence | **Jon does this check** | — | None |
| **Conflicts: ACT and Code for Charlottesville** | **Jon recuses entirely — no screening, coding, adjudication, or review** | **Both code independently; disagreements reported unadjudicated** | Role 3 as normal |
| Flag author-conflicted records in the dataset; log every recusal | Logs | Flag in the dataset | None |
| Track saturation per block: six consecutively coded organizations with no new code on the five framework dimensions. `ecosystem_role` is coded but is **not** part of the criterion | Confirms the count; only **adjudicated** new codes reset it | Track and report new codes | None |
| An `undetermined` value neither resets the counter nor counts toward the six | Enforces; reports undetermined counts per dimension | Record `undetermined` with a note rather than guessing | Instructed to return undetermined where evidence is absent |
| Exclude second-pass exclusions and frame-operator records from the six | Enforces | Apply | None |
| Apply the Stage 0 rule for `undetermined` values in the counter | Enforces | Apply | None |
| If a block exhausts before six: report as exhausted with the count and counter state; do **not** add frames | Decides and documents as a finding | — | None |
| Recompute human-to-human agreement at the midpoint so drift is visible | Computes and records | — | None |

---

## O8 — Boundary audits and partner probe

| Step | Jon (PI) | Akshita & Carmen | AI |
| --- | --- | --- | --- |
| Draw 100 CTFG US records with type present but not Organization; screen against C1 | Approves the seed | Draw and screen | Role 1 may propose C1; RA verifies |
| Draw 100 CTFG US records with no type recorded; screen against C1 | Approves the seed | Draw and screen | Role 1 may propose C1; RA verifies |
| Run both audits to full sample size regardless of interim results | Enforces | Complete both | None |
| Report pass rates with confidence intervals as a bound on frame completeness | Computes and reports | — | None |
| Assemble partner organizations named on included records that are not in the pool | — | Assemble and dedupe | May propose extraction; RA verifies |
| Draw 50 at random with a recorded seed; code on label fields only. If fewer than 50 exist, code all and report the number | Approves the seed | Draw and code | Role 2 may locate passages |
| Report the probe as exploratory — no denominator, no rate over any population | Enforces in the write-up | — | None |

---

## O9 — Validate and report

| Step | Jon (PI) | Akshita & Carmen | AI |
| --- | --- | --- | --- |
| Compute human-to-human kappa per judgment field at calibration, midpoint, and end | Computes and reports | — | None |
| Compute human-to-AI agreement separately and label it clearly | Computes and reports | — | Supplies the blind Role 3 output |
| Review records where the model disagreed with both humans, or all three diverged — **only after** adjudication is recorded. Log changes with reasons; report the count | Leads the review; logs | Participate | Role 3 output released at this point |
| Report the proportion of undetermined values per field as a finding about what organizations disclose | Reports | — | None |
| Report unique-organization yield per frame and per block | Computes and reports | Supply counts | None |
| Report unit-resolution rates, comparing **Blocks B and C only** (Block A excluded — PIT-UN lists universities) | Computes and reports | — | None |
| Report frame redundancy per block as description only; never compare across blocks as evidence of population size | Reports with the structural caveats | — | None |
| **Inductive category coding of non-lexicon phrases** | **Adjudicates** | **Both code independently over the full pooled set** | **No AI at this step** — a model would impose the vocabulary the step exists to escape |
| Report categories recurring across organizations, cutting across blocks, and used by operators. Do not add any to the frozen lexicon | Reports | — | May organize already-coded excerpts afterwards (non-decisional, disclosed) |
| State the limit: absence of categories cannot be distinguished from frames admitting only organizations whose vocabulary already fits | Writes | — | None |
| Compare organizational findings to literature findings on the five dimensions — structural, not distributional | **Jon's judgment throughout** | — | None |
| Activity sensitivity: re-run main results excluding dormant and closed organizations | Runs and reports | Supply data | None |
| Leave-one-frame-out: re-run block results dropping each frame | Runs and reports | — | None |
| Multi-frame subset: analyze only if ≥ 10 organizations; below that, report as not conducted with the count and the list | Decides and reports | — | None |
| Unit-resolution bound: report counts of `unresolvable`, `unit_unresolved`, `unit_known_not_surfaced` per frame | Reports | Supply counts | None |
| Report every result per frame before any pooled figure | Enforces | — | None |
| Attach a population statement to every figure (frames, block, operators in or out, which denominator) | Enforces | — | None |
| Report pass rates and tier rates per frame only, with what that frame selects for. Never aggregate or compare across blocks | Enforces | — | None |
| Report no population proportion, coverage estimate, or rate beyond the frame set | Enforces | — | None |
| Report operators and probe records separately, excluded from within-block rates and saturation counts | Enforces | — | None |
| Produce PRISMA-style accounting: candidates per frame, duplicates removed, screened, excluded by criterion, included, by tier and block | Reports | Supply the screening log | None |
| Deposit on OSF under CC-BY 4.0, no embargo: register, snapshots, screening log, dataset, codebook, every seed, queue order, proxy script, frozen lexicon, model version, frozen prompts, and the per-field log of every AI proposal against the human decision including blind Role 3 output | Confirms completeness | Prepare and deposit | Supplies its own logs |
| Resolve the CTFG license discrepancy with the curator before redistributing derived data (site states CC BY 4.0 in one place, CC BY-NC-SA in another) | **Jon contacts the curator** | — | None |
| Report contributor roles for all three coders using CRediT | Assigns and reports | Confirm their own | None |

---

## Where the load falls

The execution protocol estimates roughly **480 combined RA hours** and **135 lead-reviewer hours** — about 1.5 to 1.7 semesters for two assistants at ten hours a week. O4 (the first screening pass, including ~476 manual country determinations) and O7 (coding to saturation) together are about 60% of that.

Jon's 135 hours concentrate in four places: adjudicating every Group 3 disagreement across the whole sample, the 10% verification passes, calibration, and the analysis and write-up. Of these, adjudication is the one that cannot be deferred or batched far — it sits on the critical path for every record, and the saturation counter only advances on adjudicated codes.
