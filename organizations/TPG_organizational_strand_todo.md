# TPG Organizational Strand — To-Do List

Every step needed to run the organizational strand, in the order it has to happen.

Where the registration and the protocol workbook disagree, the registration governs — the execution protocol says so explicitly. Several items below are corrections to bring the workbook into line.

---

## Stage 0 — Fixes and staffing (before anything else)

These are the things that get harder or impossible to decide later. None of them requires a new registration filing; they are corrections and specifications of rules already registered. Write each one down with a date so the record shows it was settled before data was seen.

### People

- [ ] Confirm both research assistants are hired and available. One is needed from O4 onward; all three coders are needed from O6 onward. Nothing after O3 can run without them.
- [ ] Confirm who plays which role: the lead reviewer adjudicates and spot-checks, the two assistants do the double coding.

### Framework dimensions — RESOLVED by preregistration update 2

- [x] The dimensions are now five: `who_participates`, `who_benefits`, `what_counts_as_social_good`, `who_decides`, `what_counts_as_relevant_technology`. Decision authority is separated from the definition of the good, because the ladder these derive from is ordered on decision authority and because participation without it — tokenism — is only observable when the two are coded separately.
- [ ] **File update 2 before O2.** The assurance that no data have been observed is what gives the change standing, and it expires at the register freeze.
- [ ] Decide which set of four you are actually coding, and make the literature strand's charting form match. This is the shared axis both strands are compared on — if they differ, RQ6 has nothing to compare across.
- [ ] Note that the existing `technologies` field (the six-way select) is a descriptive field, not this dimension. If you adopt "relevant technology" as a dimension, it needs its own Group 3 field.

### Decide who counts as a frame operator

- [ ] Settle the Rule 2 operator list before enumeration, because operators enter the pool by construction at O3. Under the registration — operators of frames *used in this study* — the list is: PIT-UN, Ford Foundation, Civic Tech Field Guide, ACT, Code for America, Fast Forward, McGovern Foundation, Google.org, plus New America as a PIT-UN co-convener.
- [ ] Decide explicitly whether Schmidt, Knight, DSSG, DataKind, NDIA, and NetGain are in or out. The workbook lists them as operators, but all six operate frames that were considered and rejected. Schmidt was dropped for being the wrong tradition, so coding it as a TPG organization would be odd.

### Fix the lexicon proxy script (must be before any page is fetched)

- [ ] Make `civic tech` match the closed compound. Right now `govtech` matches with or without a space or hyphen, but `civic tech` requires a separator, so "civictech" and "CivicTech" do not match at all. The frame is literally called civictech.guide, so this rendering will appear. This is a spelling variant, which the lexicon file's own rules allow patterns to absorb — it does not broaden the concept.
- [ ] Make the script read `frozen_lexicon.json` instead of keeping its own hardcoded copy. The JSON file claims it is read at runtime and it is not. The two copies agree today; there is nothing to stop them drifting.
- [ ] Re-record the script version after either change.

### Write down the saturation rule for undetermined values

- [ ] Decide what an `undetermined` value does to the six-record saturation counter, and write it into the codebook. Nothing currently addresses this. The dimensions went unanswered across the entire prior exploratory collection, and `who_decides` is expected to be the most frequently undetermined of the five, so six organizations in a row whose sites simply do not address it is a live possibility. **Resolved in update 2:** an undetermined value neither resets the counter nor counts toward the six.
- [ ] The natural reading is that an undetermined value neither resets the counter nor counts toward the six. Whatever you choose, choose it now: once you have coded enough organizations to see how their pages read, any rule you write is informed by that.

### Correct the workbook to match the registration

- [ ] Partner probe size: **50** organizations, not "all if 200 or fewer, otherwise 200" (workbook sheet 1, item 2.4).
- [ ] Partner probe status: **not optional**. The registration registers it as a required supplementary probe; sheet 2 labels it an optional robustness check.
- [ ] Unit-resolution sensitivity: it is a **reported bound**, not a recomputation. Sheet 6 says to report what changes if `unit_known_not_surfaced` records were included, which cannot be done — those records are deliberately never coded. O9 in the execution protocol has this right.
- [ ] Inductive coding agreement: computed over the **full set** of pooled phrases, not a subsample. Sheet 6 and the registration's Synthesis Plan say subsample; the registration's Extraction Reliability section says the full set. Pick the full set and make all three documents say so.

### Settle two definitions that affect sampling

- [ ] Define CTFG audit stratum (a) as "record type is present and is not Organization." If "not typed Organization" is read as including records with no type at all, then audit sample (a) contains audit sample (b) and the two are not independent, which undermines the confidence intervals.
- [ ] Move the AI Role 1 validation to before O4. The gate says Role 1 runs on analytic records only after reaching 95% field-level accuracy against adjudicated calibration values — but calibration is O6 and O4 processes every enumerated record. Validate Role 1 against a small hand-coded set before O4 instead. (Practical risk here is low, since an assistant verifies every Role 1 proposal against the source anyway, but the gate is registered and should be satisfied rather than explained.)

### Housekeeping

- [ ] Write out what the `technologies` codes mean (SE, DS, OD, UX, POL, HW). They are not defined anywhere.
- [ ] Clean the `originating_frame` allowed values. NAPIT, KNIGHT, and SCHM are dropped frames; keep a code only if that organization enters as an operator record.
- [ ] Decide how the roughly 40 calibration organizations will be spread across blocks. They are discarded from the analytic dataset, and in Block A and the Google.org frame — both thin after unit resolution and the US criterion — that is a meaningful share of the pool.

---

## O2 — Freeze the register

Fix the contents of every frame on a single stated date.

- [ ] Pick one freeze date without looking at what is inside any frame. The clear window is August 2026 to January 2027, which avoids the PIT-UN intake.
- [ ] Between now and that date, do not inspect any frame beyond confirming its listing still loads.
- [ ] **Civic Tech Field Guide:** capture the **full data export**, not just the records inside the frame boundary. The two boundary audits at O8 draw from records *outside* the boundary — US records not typed as organizations, and US records with no type — and those pools will not exist in the frozen state if you only save the filtered subset.
- [ ] **Code for America brigades:** pin `organizations.json` to a specific commit SHA rather than a date. This is the most reproducible frame in the register.
- [ ] **Ford Foundation:** export the topic-filtered active-grant view by hand (the database sits behind a human-verification gate), and pull the historical tail from 990-PF filings from 2011 onward. Record which source each grantee came from.
- [ ] **PIT-UN:** confirm the 2026–27 member cohort appears in the directory, and capture the full institution list, not just a count.
- [ ] **ACT:** capture the exact member list on the freeze date.
- [ ] **Fast Forward and McGovern:** capture the portfolio and grants listings.
- [ ] **Google.org:** capture participant lists for the four named cohorts only (2019 AI Impact Challenge, 2025 Accelerator: Generative AI, 2026 AI for Government Innovation, 2026 AI for Science). The 2019 cohort needs an archived snapshot, not the live page. If a cohort's list is not yet published, record it as pending and enumerate it later, recording that date separately.
- [ ] Take an archived web capture of every frame source page on the freeze date.
- [ ] Record each frame's as-of date in the frame register and deposit the snapshots on OSF.

---

## O3 — Enumerate and deduplicate

Turn the frozen snapshots into a candidate pool of roughly 1,800 organizations.

- [ ] Enumerate each frame in full from its snapshot, using the boundary definition recorded in the register.
- [ ] CTFG boundary: record type contains "Organization" AND (country is United States OR country is missing). Expect roughly 1,099 candidates.
- [ ] CFA: filter by tag to exclude non-brigade entries (18F, Code for All, OK Labs, Code for Poland, government entities), and normalize the inconsistent city strings before applying the US filter.
- [ ] McGovern: the unit is grants, not organizations — deduplicate to organizations before counting.
- [ ] Apply Rule 1 wherever a frame lists an institution rather than an organization. Resolve to the unit the frame itself names. Log each record as `resolved`, `unit_unresolved`, or `unit_known_not_surfaced`.
- [ ] Apply the fiscal-sponsor clause where a frame names a sponsor instead of the sponsored project. Never enter both as separate records.
- [ ] Add every frame operator to the pool by construction, flagged as an operator, with the frames it operates and whether those are current or historical.
- [ ] Deduplicate to organization-level units. Record every merge with its parent ID, and keep the multi-frame provenance on records surfaced by more than one frame.

---

## O4 — First screening pass

Apply the two cheap criteria to every enumerated record.

- [ ] **First:** run the Role 1 validation described in Stage 0 and confirm 95% field-level accuracy per Group 1 field. Revise prompts and re-check where a field falls short; any field still short is coded by an assistant with no AI help, and that is reported.
- [ ] Run AI Role 1 over the pool. For each Group 1 field, including C1 and C2, the model proposes a value and the passage supporting it.
- [ ] One assistant verifies every proposal against the source. No proposal is accepted without opening the source.
- [ ] Where a frame has no location data, determine C2 from the organization's own materials. For CTFG this applies to roughly 476 records and is the single largest manual cost in the strand.
- [ ] Code any listing that cannot be resolved to an organization at all as `unresolvable`, and keep the count.
- [ ] Record the first criterion failed for every exclusion.
- [ ] Lead reviewer: re-check a random 10% of records per block against the recorded evidence. Report the error rate found, and separately the rate at which assistants corrected or overrode the model.

---

## O5 — Compute the proxy and build the coding queue

Fix the coding order in advance so the stopping point does not depend on who opens which record first.

- [ ] Run the corrected lexicon proxy script over the records that passed the first screening pass.
- [ ] Re-run with `--retry-undetermined` to clear transient fetch failures.
- [ ] Resolve every remaining `UNDETERMINED` record by hand before building the queue. Undetermined is not the same as false — a page that failed to load has not told you the vocabulary is absent.
- [ ] Stratify each block two ways: by originating frame, and by the proxy value.
- [ ] Assign records surfaced by more than one frame to the stratum of whichever frame is listed first in the register, keeping the multi-frame provenance in the data.
- [ ] Fix the draw order: round-robin rotation across a block's strata, random within each stratum, using a recorded seed. Where a stratum runs out, the rotation continues over the rest.
- [ ] Deposit the seed and the resulting queue order on OSF.
- [ ] Remember the proxy is a sampling aid only. It is never reported as tier and never prefills the tier field.

---

## O6 — Calibrate

Establish that the instrument is codable before touching any analytic record.

- [ ] Draw about 20 organizations spanning all three blocks.
- [ ] All three coders code them independently on the full instrument.
- [ ] Discuss the disagreements. Revise the codebook and field wording where the disagreement traces to the instrument rather than the coder — especially the five framework dimensions, all of which arrive marked PILOT with no rubrics and which went unanswered across the whole prior exploratory collection.
- [ ] Repeat on a fresh set of about 20.
- [ ] Compute and report agreement on the final round. Cohen's kappa of 0.60 or above per judgment-dependent field is the benchmark.
- [ ] Note that failing the benchmark does **not** change who codes the field. Double coding is kept regardless. A field still below benchmark after revision is reported with its statistic, used descriptively only, and excluded from comparisons across blocks or frames.
- [ ] Calibrate organizational status on the same set — dormant versus closed is genuinely ambiguous for small volunteer organizations.
- [ ] Validate AI Role 2 against the adjudicated values (report passage recall; there is no gate) and Role 3 (no gate — it never touches a coded value).
- [ ] Discard all calibration records from the analytic dataset.
- [ ] File a preregistration update recording the revised codebook wording and the agreement results, and carry any change to the five dimensions across to the literature strand's charting form.

---

## O7 — Screen and code

Produce the coded sample, one record at a time from the fixed queue.

### For each record

- [ ] Draw the next record from the queue.
- [ ] Apply C3 (constitutive technology), C4 (public benefit), and C5 (funder program). Both assistants code these independently; the lead reviewer adjudicates every disagreement.
- [ ] For records passing all criteria, code the self-label fields. AI Role 2 returns candidate passages with exact character spans and proposes no values. One assistant decides every field: the verbatim phrase, which lexicon term it matched, placement, speaker, any non-lexicon self-description, and tier.
- [ ] Record any categorial self-description that matches no lexicon term, verbatim, with the same evidence as a lexicon hit. Do not normalize it toward a lexicon term. This field carries the third part of RQ5.
- [ ] Code status as active, dormant, or closed, with a date and a dated evidence artifact.
- [ ] Both assistants code the five framework dimensions independently; the lead reviewer adjudicates.
- [ ] Run AI Role 3 blind on C3, C4, C5 and the five dimensions. Withhold its output from all three humans until the adjudicated human value is recorded.
- [ ] Archive a web capture of every page supporting a self-label, a non-lexicon description, or a status determination.
- [ ] Record anything that cannot be determined as `undetermined` with a note, and send it to adjudication rather than guessing a value.

### Conflicts of interest

- [ ] Route records for ACT (entering as a frame operator) and Code for Charlottesville away from the conflicted author entirely — no screening, coding, adjudication, or review.
- [ ] Have both assistants code those records independently, and report any disagreement unadjudicated rather than resolving it.
- [ ] Flag every such record as author-conflicted in the dataset, and log every recusal.

### Stopping

- [ ] Track, per block, how many consecutively coded organizations produce no new code on the five framework dimensions. `ecosystem_role` is coded but is no longer part of the criterion (update 2).
- [ ] Stop sampling in a block at six. Reset the count whenever a new code appears, counting only adjudicated new codes.
- [ ] Do not count records excluded at this pass, or frame-operator records, toward the six.
- [ ] Apply the undetermined rule you wrote at Stage 0.
- [ ] If a block runs out of records before reaching six, report it as exhausted with the number coded and the state of the counter, and treat that as a finding about the tradition's organizational density. Do not add frames to compensate.
- [ ] Recompute and record human-to-human agreement at the midpoint of coding, so drift is visible rather than assumed absent.

---

## O8 — Boundary audits and partner probe

- [ ] Draw 100 CTFG records at random, with a recorded seed, from US records whose type is present and is not Organization. Screen against C1.
- [ ] Draw 100 CTFG records at random, with a recorded seed, from US records with no type recorded. Screen against C1.
- [ ] Run both audits to their full sample size regardless of what interim results look like.
- [ ] Report both as pass rates with confidence intervals, stated as a bound on how complete the frame is.
- [ ] Assemble every organization named in `partner_orgs_named` on included records that is not already in the candidate pool.
- [ ] Draw 50 at random with a recorded seed and code them on the label fields only. If fewer than 50 exist, code all of them and report the number.
- [ ] Report the probe as exploratory. It has no denominator and estimates no population; it only checks whether organizations no frame reached use the same non-lexicon vocabulary.

---

## O9 — Validate and report

### Reliability

- [ ] Compute human-to-human kappa over all coded records for each judgment-dependent field, at calibration, midpoint, and end.
- [ ] Compute human-to-AI agreement separately and label it clearly, so neither statistic is mistaken for the other.
- [ ] Review records where the model disagreed with both humans, or where all three diverged, only after the adjudicated value is recorded. Log any resulting change with its reason and report the count.
- [ ] Report the proportion of undetermined values per field as a finding about what organizations disclose.

### Analysis

- [ ] Report unique-organization yield per frame and per block.
- [ ] Report unit-resolution rates, comparing Blocks B and C only. Block A is excluded because PIT-UN lists universities, so its rate reflects a listing convention rather than organizational form.
- [ ] Report frame redundancy per block as description only. Do not compare it across blocks as evidence of population size — Ford helped create the network PIT-UN enumerates, and ACT succeeded the sunset brigade network.
- [ ] Pool every non-lexicon self-description and code them into emergent categories: both assistants independently over the full set, lead reviewer adjudicating, **no AI at this step**. A phrase used by one organization is noise, not a category.
- [ ] Report which categories recur across organizations, which cut across blocks, and which appear among frame operators as well as members. Do not add any of them to the frozen lexicon.
- [ ] State the limit: an absence of emergent categories cannot be distinguished from the frames having admitted only organizations whose vocabulary already fits.
- [ ] Compare the organizational findings against the literature findings on the five framework dimensions — which configurations appear in practice, which in the literature, which in only one. Structural, not distributional.

### Sensitivity checks

- [ ] Activity sensitivity: re-run the main descriptive results excluding dormant and closed organizations, to show what an activity gate would have done.
- [ ] Leave-one-frame-out: re-run block-level results dropping each frame in turn.
- [ ] Multi-frame subset: analyze organizations claimed by frames from two or more blocks — but only if there are at least ten. Below that, report it as not conducted, give the count, and list the organizations.
- [ ] Unit-resolution bound: report counts of `unresolvable`, `unit_unresolved`, and `unit_known_not_surfaced` per frame. This is a reported bound, not a recomputation.
- [ ] Report anything that changes materially under any of these checks.

### Reporting rules

- [ ] Report every result per frame before any pooled figure.
- [ ] Attach a population statement to every figure: which frames, which block, whether operators are included, and whether the denominator is the enumerated pool, the screened pool, or the coded sample.
- [ ] Report screening pass rates and tier rates per frame only, alongside a statement of what that frame selects for. Never aggregate them to block level or compare across blocks.
- [ ] Report no population-level proportion, coverage estimate, or rate over any population beyond the frame set.
- [ ] Report operators and probe records separately, excluded from every within-block rate and saturation count.
- [ ] Produce the PRISMA-style accounting: candidates per frame, duplicates removed, screened, excluded by criterion, included, split by tier and block.

### Deposit and disclosure

- [ ] Deposit on OSF under CC-BY 4.0 with no embargo: the frozen frame register with enumeration routes, boundary definitions, and snapshot references; the screening log with the first criterion failed for every exclusion; the final dataset with its codebook; every random seed and the resulting queue order; the proxy script and frozen lexicon; and the model, version, frozen prompts, and per-field log of every AI proposal against the human decision, including the blind Role 3 output.
- [ ] Resolve the CTFG license discrepancy with the curator before redistributing any derived data. The site states CC BY 4.0 in one place and CC BY-NC-SA in another. If it is incompatible, cite the frame rather than redistributing it.
- [ ] Report contributor roles for all three coders using the CRediT taxonomy.

---

## Timing note

The execution protocol estimates this strand at roughly 480 combined research-assistant hours and 135 lead-reviewer hours — about 1.5 to 1.7 semesters for two assistants at ten hours a week. The registration's End date field budgets four to six weeks for the same work. The 480-hour figure is the realistic one, and the first screening pass plus the coding together account for about 60% of it. Nothing in the protocol is time-boxed, so extending across two semesters requires no registration change, but the planned end date of 30 June 2027 will need to move in one of the updates you are already planning.
