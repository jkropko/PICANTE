# TPG Organizational Strand — Glossary

Reference for anyone coding on this project. Where the study uses a term more narrowly than the field does, that is flagged.

---

## Contents

1. [The object of study](#1-the-object-of-study) — TPG, the three traditions, Arnstein's ladder, the five framework dimensions
2. [Review methodology](#2-review-methodology) — scoping review, meta-narrative synthesis, charting, saturation, reflexivity
3. [Standards and frameworks cited](#3-standards-and-frameworks-cited) — PCC, JBI, PRISMA-ScR, RAMESES, RAISE, CRediT
4. [Sampling: frames and the register](#4-sampling-frames-and-the-register) — frames, blocks, boundary definitions, freeze dates, admission mechanism, the eight frames
5. [The two standing rules](#5-the-two-standing-rules) — unit resolution, fiscal sponsors, frame operators
6. [Screening criteria](#6-screening-criteria) — C1–C5, constitutive technology, public benefit, status as a variable
7. [The lexicon and tiers](#7-the-lexicon-and-tiers) — frozen lexicon, lexicon proxy, Tier 1 and Tier 2, non-lexicon self-descriptions
8. [Sampling to saturation](#8-sampling-to-saturation) — draw rule, stratification, recorded seeds, the stopping rule
9. [Measures and what they can support](#9-measures-and-what-they-can-support) — yield, redundancy, boundary audits, denominators, what is out of scope
10. [Reliability](#10-reliability) — double coding, adjudication, kappa, gate vs benchmark, undetermined
11. [AI roles and constraints](#11-ai-roles-and-constraints) — the governing constraint, field groups, Roles 1–3, verbatim fidelity
12. [Conflicts of interest](#12-conflicts-of-interest) — recusal, author-conflicted records, unadjudicated disagreement

**Most often confused:** [`unresolvable` vs `unit_unresolved` vs `unit_known_not_surfaced`](#5-the-two-standing-rules) · [lexicon proxy vs tier](#7-the-lexicon-and-tiers) · [`UNDETERMINED` vs `FALSE`](#7-the-lexicon-and-tiers) · [kappa vs percentage agreement](#10-reliability) · [human-to-human vs human-to-AI agreement](#11-ai-roles-and-constraints) · [gate vs benchmark](#10-reliability)

---

## 1. The object of study

**TPG (technology for the public good)** — The umbrella field this review maps. Not a term any organization is required to use about itself; it is the reviewers' label for the territory the three traditions share.

**The three traditions** — The scholarly and practitioner communities the study compares:
- **PIT (public interest technology)** — Foundation-derived and field-building. Organizes through university networks and funder portfolios.
- **Civic technology** — Participation-oriented, grounded in HCI/CSCW research. Organizes through volunteer brigades and membership networks.
- **"For good"** — Data science, technology, and AI for social good. Computational and method-first. Organizes through accelerators, funder portfolios, and corporate cohorts rather than membership.

**Arnstein's ladder (1969)** — A classic eight-rung scale of citizen participation, from manipulation up to citizen control. This study borrows it as a **common analytic axis, not an evaluative scale**: the five framework dimensions derive from it, but the review is not ranking the traditions against each other. The ladder is ordered on one quantity — decision authority — which is why `who_decides` is a dimension in its own right rather than a clause attached to another.

**The five framework dimensions** — The axes on which both strands are compared: `who_participates`, `who_benefits`, `what_counts_as_social_good`, `who_decides`, and `what_counts_as_relevant_technology`. All five are Group 3 fields, double-coded in full and adjudicated, and all five are marked PILOT: their rubrics are built at calibration rather than fixed in advance.

**Tokenism** — Arnstein's term for participation without decision authority: consultation, placation, and information are rungs on her ladder precisely because people take part without deciding. This is the configuration `who_participates` and `who_decides` exist to make visible, and it is only observable when the two are coded as separate fields. *Separated by preregistration update 2, filed before any record was coded; previously `what counts as social good and who decides` was a single dimension.*

---

## 2. Review methodology

**Scoping review** — A review that maps the extent, range, and distribution of a literature rather than estimating an effect. Deliberately does not appraise study quality.

**Meta-narrative synthesis** — A method for reconstructing how separate research traditions have told different stories about the same topic: each tradition's origins, its exemplars, its methods, and its definition of the good. Reported per RAMESES.

**Charting** — The scoping-review word for data extraction. Filling in a structured form for each included source or organization.

**Critical appraisal** — Formal assessment of a study's methodological quality (Cochrane RoB, GRADE). **Deliberately not done here**, and documented as a choice: the aim is to map how a field conceptualizes itself, not to estimate an effect whose credibility depends on study quality.

**Grey literature** — Work published outside commercial or academic channels: foundation reports, white papers, theses, preprints. Central to the PIT tradition, so actively sought rather than excluded.

**Saturation** — The point at which additional records stop producing anything new. Here it is operationalized precisely as the stopping rule (below), not left as a judgment call.

**Reflexivity** — Documenting how the research team's prior exposure and disciplinary vantage may shape interpretation. Required by RAMESES.

**Peer debriefing** — Discussing interpretive decisions with a colleague not involved in coding. Substitutes for inter-synthesist reconciliation, since there is a single synthesist.

**Preregistration update** — A dated amendment filed on OSF before the affected work is executed. The point is that changes are on the record *before* they could have been informed by results.

---

## 3. Standards and frameworks cited

| Abbreviation | What it is |
| --- | --- |
| **PCC** | Population–Concept–Context. The JBI framework for writing scoping-review eligibility criteria. |
| **JBI** | Joanna Briggs Institute. Source of the scoping-review guidance this protocol follows. |
| **PRISMA-ScR** | Reporting standard for scoping reviews. Governs the search-and-selection write-up and the flow diagram. |
| **RAMESES** | Publication standards for meta-narrative reviews. Governs the synthesis write-up. |
| **RAISE** | Responsible AI in Evidence Synthesis (2025). Governs disclosure and validation of AI tools — model, version, exact prompts, and validation against blind human coding. |
| **CRediT** | Contributor Roles Taxonomy. How each coder's contribution is reported. |

---

## 4. Sampling: frames and the register

**Sampling frame (or just "frame")** — A published list from which candidate organizations are drawn. Organizations enter this study **only** through a frame; there is no keyword searching for organizations, and organizations encountered incidentally during the literature search do not enter the pool.

**Frame register** — The frozen document naming every frame, its enumeration route, its boundary definition, and its as-of date. Also records which candidate frames were considered and rejected, and why.

**Block** — A group of frames belonging to one tradition. Block A = PIT, Block B = civic tech, Block C = "for good". **Blocks are the unit of balance**; frames within a block are not assumed equivalent.

**Boundary definition** — The written rule stating exactly which records in a source count as part of the frame. For the Civic Tech Field Guide: record type contains "Organization" AND (country is United States OR country is missing).

**Enumeration** — Listing every record inside a frame's boundary, exhaustively, from the frozen snapshot. Distinct from sampling, which happens afterward.

**Freeze date** — The single date on which every frame's contents are captured. Chosen *without reference to what is inside any frame*.

**Snapshot** — An archived capture of a frame's source page on the freeze date, so the frame's contents are reproducible later.

**Commit SHA pinning** — For version-controlled sources, freezing to a specific Git commit rather than a date. Exactly reproducible. Used for the Code for America brigade roster.

**Candidate pool** — Everything enumerated from all frames, deduplicated to organization-level units, before screening.

**Admission mechanism** — *How* an organization got into its frame. Recorded per record, because it is a confound the analysis must hold rather than ignore:
- **Self-declaration** — the organization joined an identity roster.
- **Selection** — a funder or accelerator admitted it.
- **Affiliation** — it joined a coalition.

**Frame type** — What kind of frame surfaced the record: identity, coalition, funder portfolio, accelerator, or corporate philanthropy.

### The eight frames

| Code | Frame | Block | Admission |
| --- | --- | --- | --- |
| PITUN | PIT University Network roster | A | Self-declaration |
| FORD | Ford Foundation Technology & Society grantees | A | Selection |
| CTFG | Civic Tech Field Guide (US organizations) | B | Self-declaration |
| ACT | Alliance of Civic Technologists members | B | Self-declaration |
| CFA | Code for America brigades (archived) | B | Self-declaration |
| FF | Fast Forward portfolio | C | Selection |
| MCGV | Patrick J. McGovern Foundation grantees | C | Selection |
| GORG | Google.org — four named cohorts | C | Selection |

---

## 5. The two standing rules

**Rule 1 — Unit resolution** — Where a frame lists an *institution* (a university, an agency, a corporate parent) rather than an organization, the record resolves to whichever unit **the frame itself names**. The parent institution does not enter the sample. This keeps the frame boundary fixed rather than letting a coder's own knowledge move it.

Three outcomes to distinguish:
- **`unresolvable`** — the listing cannot be resolved to any organization at all. A dead link, a project name with nothing behind it, an entry that turns out to be a page on someone else's site. This is a **C1 coding**, not a Rule 1 outcome.
- **`unit_unresolved`** — an institution is clearly identified, but the frame names no unit inside it. Logged, counted, excluded from coding.
- **`unit_known_not_surfaced`** — the coder personally knows of a qualifying unit the frame does not name. **Do not add it.** Log it, count it, move on. A high count here is evidence that the frame under-represents its institutions' activity.

**Fiscal sponsor** — An established nonprofit that receives and administers funds on behalf of a project without its own 501(c)(3) status. Where a frame names the sponsor instead of the project, resolve to the sponsored project if the frame names it and it independently meets C1; otherwise to the sponsor. Record the routing. **Never enter both.**

**Rule 2 — Frame operators** — Any organization that operates, convenes, or publishes a frame used in the study enters the candidate pool **by construction**, whether or not it appears in any frame's listings. Operators are coded on the full instrument like any other record, but are **excluded from every within-block rate and saturation count**, because their inclusion is guaranteed rather than sampled. The rationale: conveners are the layer that defines who counts as part of a tradition, and sampling members while never coding conveners would omit the infrastructure of the object of study.

---

## 6. Screening criteria

Applied in order. On exclusion, record the **first** criterion failed.

| ID | Test | When | Who codes |
| --- | --- | --- | --- |
| **C1 — unit** | Organization-level unit: own name, own web presence, evidence of staffing or governance | Pass A | One RA (AI proposes) |
| **C2 — US** | Headquarters or principal operations in the United States | Pass A | One RA (AI proposes) |
| **C3 — constitutive** | Remove the technology: does the core activity survive? | Pass B | Both RAs, adjudicated |
| **C4 — public benefit** | Beneficiary is the public, not members or industry | Pass B | Both RAs, adjudicated |
| **C5 — funder program** | Funders only: a named technology program or portfolio as a primary activity | Pass B | Both RAs, adjudicated |

**Constitutive technology (C3)** — The test that separates organizations *doing* technology work from organizations that merely *use* technology or *receive* it from others. A nonprofit that adopts AI to run its housing program fails; a nonprofit that builds the tool does not. This is the criterion most exposed to judgment drift and carries the largest share of the screening workload, which is why it is never coded by one person.

**Public benefit (C4)** — For for-profits, only **structural commitment** counts: public-benefit corporation status, B-Corp certification, or an equivalent commitment recorded in articles or bylaws. A mission statement, values page, or impact-marketing claim is not sufficient on its own.

**PBC (public-benefit corporation)** — A for-profit whose charter obliges it to pursue a stated public benefit alongside profit.

**B-Corp** — A third-party certification (B Lab) of social and environmental performance. Distinct from PBC status, which is a legal form.

**Activity is not a criterion** — Deliberately. Gating on whether an organization is still running would remove dormant and closed organizations, biasing every result toward survivors.

**Status** — Coded as a variable, not a gate: `active` / `dormant` / `closed`, with a date and a **dated evidence artifact** (a specific dated thing — a filing, a post, a closure notice — with URL and access date). The dormant/closed distinction is genuinely ambiguous for small volunteer organizations, so it is calibrated.

**Survivorship bias** — The distortion that results from studying only what still exists. Coding status instead of gating on it converts survivorship from an invisible exclusion into a reportable sensitivity analysis.

---

## 7. The lexicon and tiers

**Frozen lexicon** — The finite list of 12 self-identification terms (civic tech, public interest technology, tech for good, data for good, data science / AI for social good, e-government, e-democracy, govtech, open government, digital civics, crowd-civic systems, data activism). Every term derives from the manuscript's own taxonomy. **Frozen means frozen**: a term encountered during the review that is not on the list is a *finding*, recorded and reported, never added mid-collection.

**Lexicon proxy** — An automated pattern match checking whether any lexicon term appears on an organization's homepage. **A sampling aid only.** Its sole function is to stratify the coding queue. Three values:
- `TRUE` — at least one term found
- `FALSE` — page fetched and read, no term found
- `UNDETERMINED` — could not be established: fetch failed, no usable URL, or too little text (often a JavaScript-rendered site)

`UNDETERMINED` is **not** `FALSE`. A site that failed to load has not told you the vocabulary is absent. These are resolved by hand before the queue is built.

**Tier** — A human judgment, made later, about how an organization describes itself:
- **Tier 1** — self-applies a lexicon label.
- **Tier 2** — nominated by a frame and doing recognizably the same work **without** the vocabulary. **Tier 2 organizations stay in.** Excluding them would reproduce the exclusion the manuscript critiques.

**The proxy is not the tier.** Tier requires knowing the phrase's placement and who is speaking, which a text match cannot establish. The proxy is never reported as tier and never prefills the tier field.

**Placement** — Where on the site the phrase appears: homepage, about, mission, annual report, other. Guards against false positives from blog posts and job listings.

**Speaker** — Whether the organization is describing *itself* or quoting a funder, partner, or news source. A grantee page quoting its funder's language is not self-identification.

**Non-lexicon self-description** — A categorial phrase an organization uses about itself that matches no frozen lexicon term, recorded **verbatim**, with the same evidence requirements as a lexicon hit. Do not normalize it toward a lexicon term or toward another organization's wording. This field carries the third clause of RQ5.

**Inductive category coding** — After charting is complete, all non-lexicon phrases are pooled and coded into emergent categories. **No AI at this step** — a model grouping the phrases would impose the prior vocabulary the step exists to escape. A phrase used by one organization is noise; a category used by many, across blocks, is the finding. Categories are reported as results and are **not** added to the lexicon.

**Ecosystem role** — What the organization does in the field: practices / funds / studies / trains / convenes. Distinct from legal form (`org_form`: nonprofit, for-profit, government, university, public-private partnership).

---

## 8. Sampling to saturation

**Draw rule** — The coding queue order is fixed **in advance**, so the point at which sampling stops does not depend on the order coders happen to open records.

**Stratification** — Within each block, records are grouped two ways: by originating frame, and by lexicon proxy value.

**Round-robin rotation** — Drawing across a block's strata in turn rather than working through one at a time. This guarantees the six-record saturation window spans strata rather than sitting inside a single frame or a single side of the proxy — and guarantees that organizations whose homepages carry no field vocabulary are reached before sampling can stop, since those are where blur across traditions is most likely visible.

**Recorded seed** — The random-number seed used for a draw, written down and deposited, so anyone can reproduce the same queue order or audit sample.

**Stopping rule** — Sampling in a block ends when **six consecutively coded organizations produce no new code** on any of the five framework dimensions. The counter resets whenever a new code appears — but **only an adjudicated new code**, not a novel code in one coder's judgment alone. Assessed **per block**, not globally. Records excluded at the second pass and frame-operator records do not count toward the six.

An **`undetermined` value neither resets the counter nor counts toward the six.** Undetermined records that the available evidence does not reach the question, which is not evidence that the dimension has stopped yielding new answers; counting it would let a block terminate on absence of disclosure rather than exhaustion of variety.

**`ecosystem_role` is not part of the criterion.** It is still coded on every record, but it is a closed controlled list rather than a rubric built at calibration, so it can only register the first appearance of a fixed value in a block — which happens early and then never again, while still being able to reset the counter on a record whose dimension answers are already familiar. *Removed from the criterion by preregistration update 2.*

**Exhaustion** — When a block runs out of records before reaching six. Reported as a finding about that tradition's organizational density, with the count and the state of the counter. **Frames are not added to compensate.**

---

## 9. Measures and what they can support

**Unique-organization yield** — Distinct organizations produced per frame and per block. Requires no population denominator, which is why it can carry the cross-tradition comparison.

**Frame redundancy** — How much frames overlap within a block. **Description only.** It cannot compare population sizes across blocks, because two blocks contain frames with structural relationships that manufacture overlap independently of field size: Ford co-created the infrastructure PIT-UN enumerates, and ACT succeeded the sunset Code for America brigade network.

**Multi-frame subset** — Organizations claimed by frames from two or more *blocks*. Blur measured here is immune to recruitment bias, since these organizations were recruited by every tradition that claims them. Analyzed only if the subset reaches **ten**; below that it is reported as not conducted, with the count and the organizations listed.

**Boundary audit** — Measuring what a frame's boundary definition excludes rather than assuming it excludes nothing. Two samples of 100 CTFG records each, drawn from *outside* the boundary and screened against C1, reported as rates with confidence intervals. Run to full sample size regardless of interim results.

**Non-frame probe (partner snowball)** — 50 organizations named as partners by included records but reached by no frame, coded on label fields only. Checks whether organizations outside the frame set use the same non-lexicon vocabulary. **Carries no denominator and estimates no population.**

**Denominator** — The population a rate is computed over. The recurring problem in this design: frame composition sets the denominator for every count the instrument produces, so most rates would not describe any nameable population.

**Population statement** — Attached to every reported figure: which frames, which block, whether operators are included, and whether the denominator is the enumerated pool, the screened pool, or the coded sample.

**Out of scope, explicitly** — Population-level proportions, coverage estimates, and any rate over a population beyond the frame set. Also: cross-block comparison of screening pass rates or tier rates, since selection-based frames pre-vet for exactly what C1 and C3 test.

---

## 10. Reliability

**Double coding** — Both RAs code the same field independently, for **every** record, not a sample. Applied to all Group 3 fields.

**Adjudication** — The lead reviewer resolves disagreements and sets the recorded value. The exception is author-conflicted records, where the disagreement is **reported unadjudicated** because the person who would adjudicate is the conflicted party.

**Blind coding** — Coding without seeing another coder's or the model's output. What makes an agreement statistic mean anything.

**Calibration** — Coding a shared practice set (~20 organizations, twice) before any analytic record, revising the instrument where disagreement traces to the *instrument* rather than the coder. Calibration records are discarded from the analytic dataset.

**Drift** — Coders' judgments shifting over time. Made visible by recomputing agreement at calibration, midpoint, and end rather than assuming it is absent.

**Cohen's kappa (κ)** — Agreement between two coders, corrected for the agreement you would expect by chance alone. Ranges roughly 0 (chance) to 1 (perfect). 0.60 is conventionally "substantial."

**Percentage agreement** — Raw proportion of records two coders coded identically. **Not interchangeable with kappa.** On a field with skewed marginals, raw agreement can be high while kappa is near zero.

**Skewed marginals** — When one category dominates a field (say, 95% of records pass C4). Kappa becomes unstable and hard to interpret, so percentage agreement is reported alongside it.

**Field-level accuracy** — Proportion of records where an extracted value matches the verified value. Used for mechanical fields, where there is a right answer, rather than kappa.

**Recall (sensitivity)** — Of the records that should have been kept, the proportion actually kept. The literature strand gates on recall rather than accuracy because screening errors are asymmetric: a wrongly excluded record is lost permanently and invisibly, while a wrongly retained one is caught at full text.

**Specificity** — Of the records that should have been excluded, the proportion actually excluded.

**Gate vs benchmark** — A crucial distinction between the strands:
- In the **literature** strand, κ ≥ 0.60 is a **gate**: a field failing it reverts to human-only charting.
- In the **organizational** strand, κ ≥ 0.60 is a **benchmark**: failing it does not change who codes the field. Double coding is kept regardless, because withdrawing it would remove the only mechanism that reveals the problem and leave the least reliable field the least checked. A below-benchmark field is reported with its statistic, restricted to descriptive use, and excluded from comparative claims.

**Undetermined** — A value a coder cannot establish from the available evidence. Recorded with a note and routed to adjudication, never guessed. The proportion of undetermined values per field is **reported as a finding** about what organizations disclose, not treated as a gap to be filled.

---

## 11. AI roles and constraints

**The governing constraint** — AI never precedes independent human judgment on a Group 3 field. If both RAs saw the same recommendation before coding, their codings would be correlated through it, and the human-to-human agreement statistic would measure the model's persuasiveness rather than the instrument's reliability.

**Field groups**
- **Group 1 (mechanical)** — enumeration, dedup candidates, C1, C2, status, ecosystem role, partners, descriptive fields. AI proposes, one RA verifies against the source.
- **Group 2 (self-label)** — verbatim phrase, lexicon term, URL, access date, placement, speaker, non-lexicon description, tier. AI locates passages only; one RA decides every value.
- **Group 3 (judgment)** — C3, C4, C5, and the five framework dimensions. Both RAs code independently; lead adjudicates; AI codes blind.

**Role 1 — first-pass extraction** — Proposes a value plus its supporting passage on Group 1 fields. Gated at 95% field-level accuracy. **No proposal is accepted without an RA opening the source.**

**Role 2 — evidence location** — Returns candidate passages with exact character spans, and **proposes no value**. Whether a phrase is categorial, where it appears, who is speaking, and what tier follows are human judgments a text match cannot make. Judged on passage recall, with no gate — a missed passage costs search time, not accuracy, because the human reads the page anyway.

**Role 3 — blind third coder** — Codes Group 3 fields independently, with output **withheld from all three humans until the adjudicated value is recorded**. Never contributes to a coded value. Serves as a separately reported validation of the model, and as a trigger for review where it disagrees with both human coders.

**Verbatim fidelity check** — Any phrase the model returns as extracted text must appear as an **exact substring** of the fetched page text. Failures are rejected automatically and the field routed to a human. A paraphrased self-description would silently destroy the data the strand exists to collect.

**Human-to-human agreement vs human-to-AI agreement** — Two different statistics, computed and reported separately and clearly labelled. The first measures the **instrument's reliability**; the second measures **the model**. Neither substitutes for the other, and every decision about a field's usability rests on the first.

---

## 12. Conflicts of interest

**Recusal** — A conflicted coder does not screen, code, adjudicate, or review a record. Every recusal is logged with the record and the substituting coder, and reported with the review. **Applies to screening and charting only, not synthesis**, which is holistic and thematic rather than record-by-record.

**Author-conflicted record** — A record for an organization in which an author holds a governance or staff role. Here: the Alliance of Civic Technologists (entering as a frame operator) and Code for Charlottesville. These records are **not removed from the pool** — the conflict changes who codes them and how the coding is reported.

**Unadjudicated disagreement** — Where the two RAs differ on an author-conflicted record, the disagreement is **reported as a disagreement** rather than resolved, because the person who would ordinarily adjudicate is the conflicted party.

**Residual limitation** — The RAs are supervised by the conflicted author, so their independence is structural rather than complete. The procedure is designed to make any resulting bias *visible in the shared data*, not to eliminate it.
