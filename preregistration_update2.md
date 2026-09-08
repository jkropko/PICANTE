# Preregistration Update 2 — Draft

**Registration:** Technology for the Public Good (TPG) — scoping-informed meta-narrative review with a parallel organizational strand
**Initial registration frozen:** 7/31/2026 · **Update 1 filed:** 8/19/2026 · **This update:** [DATE]

> Draft for review. Bracketed fields need completing before filing. Structure follows Update 1: assurance, then classed changes, then amended field text ready to paste into the OSF form.

---

## Reason for update

### ASSURANCE THAT NO DATA HAVE BEEN OBSERVED

No component of the registered protocol has been executed. The citation-network search from the frozen seed set has not been run; no records have been retrieved, screened, or charted; the pilot screening and pilot charting sets have not been drawn. In the organizational strand, the frame register has not been frozen, no snapshot has been captured, no frame has been enumerated, and no organization has been screened or coded. The calibration rounds registered under Screening Reliability have not been conducted.

None of the revisions below could therefore have been informed by results, because no results exist. This update is filed specifically so that the changes are on the record before execution begins rather than after. It is filed before the organizational register's freeze date is set, so that the freeze date is chosen after these revisions are fixed rather than alongside them, and before the Search stage begins, so that the corrections to the search validation procedure are in place before the procedure is run.

The disclosures of prior exploratory work made in the initial registration and in Update 1 stand unchanged and are not repeated here. Nothing in the preliminary literature corpus or the ad hoc collection of 231 practitioner-organization records informed the revisions below.

Several revisions correct defects identified by re-reading the registration against its own frozen attachments: by checking the named landmark works against the frozen seed list, by checking the seed identifiers against the tool that consumes them, and by verifying every seed record field by field against its own source. That verification retrieved the twenty-three seed works' own bibliographic records only. It retrieved no candidate records, executed no search, ran no citation-network expansion, and produced no pool against which any registered analysis could have been computed.

---

# CLASS 1 — CORRECTIONS

These correct errors, omissions, and internal contradictions. None changes the design.

## 1.1 Model name in the screening AI-use disclosure

Update 1 recorded that the model name was corrected from "Clause Opus 5" to "Claude Opus 5". The correction was not applied to the field it governs: the AI-use disclosure under Miscellaneous screening details still reads "Clause Opus 5". It is corrected here. The AI-use disclosure must name the model correctly to serve its reproducibility function under RAISE.

## 1.2 Agreement statistic for the inductive category coding

Extraction Reliability specifies that agreement on category assignment is computed over all pooled non-lexicon phrases; the Synthesis Plan specifies a subsample. Resolved toward the full set, consistent with every other double-coded field in the organizational strand, where full double coding rather than subsampling is what makes the statistic computable over the analytic dataset.

## 1.3 Completing the RAISE citation

RAISE is a collection of three documents rather than one. The guidelines list is amended to cite RAISE 1 (recommendations for practice across the evidence synthesis ecosystem) and RAISE 3 (selecting and using AI tools, including ethical, legal and regulatory considerations), which are the parts that govern this protocol. RAISE 2 addresses tool development and is not applicable.

## 1.4 Methodological citations for the organizational strand

The guidelines list names the standards governing the literature strand but no source for the organizational strand's sampling and reliability procedures, which were registered in Update 1 without attribution. The list is completed below. No procedure changes; the sources are the ones the registered procedures already follow.

## 1.5 Corrections to the frozen seed file

Every record in the frozen seed set was checked field by field against its source: identifier, authors, year, title and venue. The check involved no retrieval of candidate records, no execution of the citation-network expansion, and no search. It produced twenty-two corrections across the twenty-three records, none of which changes which work a record denotes. **No seed has been added, removed or substituted, and the twenty-three works identified are exactly those registered.** A revised seed file replaces the original as an attachment, carrying a revision-log sheet that records every correction with its before and after, the date, and the fact that no stage of the protocol had been executed.

The corrections fall into two kinds.

**Factual corrections (two records).**

*Seed 22 — venue.* The record gives the venue as *Findings of the Association for Computational Linguistics: EACL 2026* and the identifier as `10.18653/v1/2026.eacl-long.238`. The identifier is correct; the venue label is not. The work is a main-track long paper, published in *Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. 5110–5170, Rabat, Morocco. Verified against the ACL Anthology record and the EACL 2026 accepted-papers listing. The venue field is corrected.

*Seed 13 — author name.* The record gives the third author as Lisa M. Chambers. The author is Lauren M. Chambers, verified against arXiv:2508.07230. The name is corrected.

**Formatting corrections (twenty records).** The seed file had been exported from a BibTeX source with the source's escaping intact. Seed 1's venue contained an escaped ampersand (`PS: Political Science \& Politics`). Five author fields carried BibTeX brace protection around multi-word surnames (`{Le Dantec}`, `{Cachat van der Haert}`, `{de Wever}`, `{De Winne}`, `{Ray Choudhury}`), a device that prevents BibTeX mis-parsing surnames and has no meaning in a spreadsheet. Nineteen of the twenty-three author fields used BibTeX's ` and ` separator. All are normalised: escapes resolved, braces removed, author separators changed to semicolons.

These corrections do not affect the citation-network expansion, which consumes identifiers rather than author strings. They are made because the seed file is a shared attachment under CC-BY 4.0 and the source of the citations in the eventual manuscript, and because leaving markup artifacts in a deposited dataset would propagate them into anything built from it.

**Four columns are added** to the seed file, recording per seed what the registered checks require: the identifier supplied to the expansion; preprint and supersession status; forward-chase viability; and the date on which the record was verified against its source. Their content is registered under 1.6, 2.5 and 2.7 below.

## 1.6 Seed 20 — no DOI, and the registered expansion input is a DOI list

Query strings states that the input to the citation-network expansion is "the DOI list of the 23 frozen seed articles." Seed 20 (Arora & Sarkar, 2023, CEUR-WS Vol-3582) has no DOI. As registered, it cannot be supplied to the expansion.

Corrected by amending Query strings to refer to the identifier list rather than the DOI list, and by adding an *Expansion identifier* column to the seed file in which the identifier actually supplied to the tool is recorded for every seed. Seed 20's cell is marked as outstanding: no identifier has been fabricated, and an OpenAlex work ID must be entered there before the Search stage begins. Where a seed's citation neighbourhood is unavailable or materially incomplete in the index — which is expected for CEUR proceedings — that fact is recorded per seed and reported alongside the leave-one-out sensitivity check, so that a seed contributing no expansion is visible rather than silently inert. If no usable identifier exists at the Search stage, seed 20 is reported as contributing no citation neighbourhood, and it is not replaced.

## 1.7 Retraction screening has no registered consequence

Data validation states that included records are screened against retraction registers and that a retracted item will be "excluded or flagged," leaving it undetermined which. The exclusion criteria list five reasons, none of them retraction, so the PRISMA-ScR flow has no category to log such a record against. This is the same defect Update 1 corrected for the agreement thresholds: a rule with no specified consequence is not a constraint.

Resolved by adding retraction as exclusion criterion 6, applied at full-text screening and at any point thereafter when a retraction notice is identified, with the record logged as excluded for retraction in the PRISMA-ScR flow. Records retracted after charting are removed from the analytic corpus, and the count of such removals is reported. Expressions of concern are not retractions: a record under an expression of concern is retained and flagged in the shared dataset.

---

# CLASS 2 — DESIGN CHANGES

Registered before execution. Each states what was registered, what replaces it, and why.

## 2.1 The framework dimensions become five

**As registered.** Four dimensions: who participates; who benefits; what counts as social good and who decides; what counts as relevant technology.

**As revised.** Five dimensions: who participates; who benefits; what counts as social good; **who decides**; what counts as relevant technology.

The change separates decision authority from the definition of the good, which the registered wording bundled into a single dimension. It applies to the literature charting form and the organizational instrument together, because the dimensions are the shared axis on which RQ3 and RQ6 compare the strands.

**Rationale.** The dimensions are derived from Arnstein's (1969) ladder of citizen participation, and the ladder has one axis: decision power. Its rungs, from manipulation through tokenism to citizen control, are degrees of who holds authority over a decision. Registering that quantity as a subordinate clause attached to a different dimension demotes the ladder's own subject within a framework that claims the ladder as its source.

Separating it also restores a distinction the ladder exists to draw. Arnstein's central move is that participation without decision authority is tokenism: consultation, placation and informing are rungs precisely because people take part without deciding. With participation and decision authority as separate coded fields, a source or an organization that involves a community while reserving determination of the good to itself or its funder is directly observable. Bundled into another dimension, that configuration cannot be recorded as such.

The revision bears on registered expectations. Expectation (b) anticipates that civic technology is the most participation-oriented and the "for good" tradition the most method-first; the place those traditions are most likely to diverge is who has standing to decide what problem is worth solving. Expectation (c) concerns configurations of the dimensions that recur across organizations, and the configurations of interest are exactly those in which participation and decision authority come apart.

**What is not claimed.** The revision does not assert that "what counts as social good" and "who decides" are unrelated, only that they are separately answerable and that sources and organizations frequently answer one and not the other. We anticipate that "who decides" will be undetermined or not reported more often than any other dimension, because neither literature nor organizational self-description reliably states where authority over the definition of the good sits. That rate is reported as a finding about what the field articulates rather than as a deficiency of the instrument.

**Consequences for reliability.** "Who decides" becomes a coded field in its own right in both strands. In the organizational strand it is a Group 3 field, double-coded in full by both research assistants and adjudicated, with its own kappa reported at calibration, midpoint and end. Where its marginal distribution is too skewed for kappa to be interpretable, percentage agreement is additionally reported. If its agreement remains below the 0.60 benchmark after codebook revision and a repeated calibration round, it is reported with its statistic stated, restricted to descriptive use, and excluded from comparative claims across blocks or frames — the treatment registered in Update 1 for any Group 3 field failing the benchmark.

## 2.2 Ecosystem role is removed from the saturation criterion

**As registered.** Sampling within a block continues until six consecutively coded organizations produce no new code on any of the four framework dimensions or on ecosystem role.

**As revised.** Sampling within a block continues until six consecutively coded organizations produce no new code on any of the five framework dimensions.

Ecosystem role remains a coded field on the instrument, with its registered controlled values and its registered coding workflow. It is removed from the saturation criterion only.

**Rationale.** Ecosystem role is a closed five-value list fixed in the codebook rather than a rubric constructed at calibration. It cannot produce a new code in the sense the stopping rule is designed to detect. What it can register is the first appearance of one of its five values within a block, which is a different event: not evidence that a dimension is still yielding conceptual variety, but a categorical fact about organizational function.

Two consequences follow, running in opposite directions. The field will exhaust its values early in every block — funders enter each block by construction under the frame-operator rule, and university programs and research centers surface the *studies* and *trains* values readily — after which it contributes nothing to the counter for the remainder of collection. Before that point, a single record that is a block's first convener resets the counter even where its answers on every framework dimension are already familiar, extending sampling for a reason unrelated to the criterion the rule is meant to apply.

The registered rule was written when the framework dimensions numbered four. With five dimensions, four of which are answered against rubrics constructed at calibration rather than against a fixed list, the criterion does not require a supplementary field to remain demanding.

**What does not change.** The threshold of six is unchanged and remains fixed in advance. The rule remains assessed per block rather than globally. Only an adjudicated new code resets the counter. Records excluded at the second screening pass and frame-operator records continue not to count toward the six. The exhaustion contingency is unchanged.

## 2.3 Undetermined values and the saturation counter

Registered here because it would otherwise be resolved by discretion during collection, and because it cannot be settled honestly once coding has begun: a rule written after coders have seen how these pages read would be informed by that observation.

**As registered.** The registration specifies that a coder who cannot determine a field records it as undetermined with a note, that the record is routed to adjudication, and that the proportion of undetermined values per field is reported. It does not specify what an undetermined value does to the saturation counter.

**As revised.** An undetermined value on a framework dimension neither resets the saturation counter nor counts toward the six. The record is coded, retained and reported as normal; it is transparent to the stopping rule alone. Where every framework dimension on a record is undetermined, the record does not advance the counter at all.

**Rationale.** An undetermined value records that the available evidence does not reach the question. It is not evidence that the dimension has stopped yielding new answers. Counting it toward the six would allow a block to terminate on absence of disclosure rather than exhaustion of conceptual variety, and the two are distinguishable only if the rule treats them differently. This is a live rather than a hypothetical concern: the framework dimensions were unanswered across the whole prior exploratory collection, and the newly separated "who decides" dimension is expected to be the most frequently undetermined of the five.

The cost is a longer coding queue in blocks where organizational disclosure is thin. That cost is accepted in preference to a stopping point that cannot be interpreted.

## 2.4 The search validation set is rebuilt so that it can fail

**As registered.** "We validate the strategy against a pre-specified set of known landmark works that any adequate search must recover (e.g., Arnstein 1969; Schrock 2019; Zhang et al. 2022; Shi et al. 2020; Schank & McGuinness 2021)."

**The defect.** Three of the five named works are themselves frozen seeds: Schrock (2019) is seed 4, Zhang et al. (2022) is seed 6, and Schank & McGuinness (2021) is seed 7. Deduplication removes the 23 seeds from the candidate pool as already included. Those three works therefore cannot appear in the pool, and the check as written would report them as not recovered — a failure produced entirely by the study's own deduplication step and carrying no information about search adequacy.

The registered remedy compounds the problem. The response to a non-recovery is "we revise the seed set or add a targeted query," so a spurious failure would trigger revision of the frozen instrument on the basis of an artifact.

The two remaining works are not equivalent as tests. Arnstein (1969) is the framework's own source and is cited by several civic technology seeds, so backward chasing will recover it almost by construction. That leaves one work, Shi et al. (2020), genuinely testing whether the expansion reaches beyond the seeds' immediate neighbourhood.

**As revised.** The validation set is replaced by works that are not seeds, drawn across the three traditions and across source types, and expanded so that a single miss is interpretable. The check is run against the pre-deduplication pool, so that recovery is assessed before seeds are removed and seed-derived hits are distinguishable from genuine recoveries.

The revised set comprises [8–10 works, to be listed here by full citation and DOI, none of them among the 23 seeds, distributed across public interest technology, civic technology and the "for good" tradition, and including at least two grey-literature items and at least one pre-2000 foundational work]. The set is recorded in an attachment to this update and frozen before the Search stage begins.

Arnstein (1969) is retained in the set but reported separately, and its recovery is not counted toward the pass criterion, because it is the framework's own source and its recovery is close to guaranteed by backward chasing from the civic technology seeds.

**Consequence of a miss.** Non-recovery of a validation work is recorded and reported with the review in every case. Revision of the seed set is not automatic: we first establish whether the work is absent from the pool, present but excluded at screening, or present in the index but unreachable from any seed's citation neighbourhood, and we report which. Only the third case bears on search adequacy. Where two or more validation works are unreachable from the seed neighbourhood, we add a targeted query rather than alter the seed set, because the seed set is the frozen input to the expansion and altering it changes the corpus definition; any addition is documented in a preregistration update before the full run.

## 2.5 Superseded seeds

**The gap.** Three seeds are arXiv preprints (6, 13, 23) and one is CEUR proceedings (20). Exclusion criterion 5 removes preprints superseded by a published version, and deduplication removes the preprint in favour of the published version — but seeds are removed from the candidate pool before either rule applies, and the seed set is frozen and is the sole input to the expansion. Nothing registers what happens when a seed is published during the review. Over an eleven-month review with two seeds dated 2025 and 2026, this is likely rather than hypothetical. The question is not only bookkeeping: citation indices sometimes merge preprint and published records and sometimes do not, so the two identifiers can return different citation neighbourhoods.

**Already realised for seed 22.** This is not a prospective concern only. Seed 22 exists in both forms as of filing: an arXiv preprint (2505.22327, v1 May 2025, v2 January 2026) and the published EACL 2026 record cited in the seed file. Whether the index merges the two is checked at the Search stage and reported, and the forward-citation set is read against that result.

**As revised.** The frozen identifier remains the input to the citation-network expansion for the duration of the review, regardless of subsequent publication. The seed file carries a *Preprint / superseded* column in which each seed's status is recorded, flagging the three arXiv seeds and noting seed 22's dual existence. Where a seed is published during the review, the publication is recorded in that column with its date and identifier, the published version is treated as the citable form in the write-up, and whether the index merges the two records is checked and reported. Where the index does not merge them, the forward-citation set retrieved from the frozen identifier is reported as incomplete for that seed, and the seed's leave-one-out result is read against that fact. The seed set is not re-frozen and no seed is substituted.

## 2.6 Pilot sizes and the literature-strand charting gate

**As registered.** The charting pilot is ten included sources. The AI-recommendation workflow proceeds to the full run only if Cohen's kappa reaches 0.60 per categorical interpretive field, with fields failing after revision reverting to unassisted human charting.

**The defect.** Cohen's kappa computed on ten observations for a multi-category interpretive field is unstable in both directions: it will fail fields whose agreement is adequate and pass fields whose agreement is not. The registration attaches a binary consequence — removing AI assistance from a field for the whole corpus — to an estimate that cannot support one. The organizational strand, by contrast, calibrates on approximately twenty organizations twice and treats 0.60 as a benchmark governing how a field is reported rather than who codes it. The stricter consequence currently rests on the weaker estimate.

**As revised.** The charting pilot is increased from ten to twenty-five included sources, drawn to span the three traditions and the source types recorded in the charting form. Kappa, its confidence interval, and percentage agreement are reported per field.

The threshold is retained at 0.60 but is applied as a benchmark rather than a gate, matching the organizational strand. A field whose agreement falls below 0.60 after prompt and codebook revision and a repeated pilot is not automatically removed from AI assistance; it is reported with its statistic and its confidence interval stated, and the decision to retain or withdraw AI recommendation for that field is made on the reported evidence and documented in a preregistration update before the full run. Where a field's confidence interval spans 0.60, that fact is reported rather than resolved by the point estimate.

**Screening pilot.** The screening pilot is retained at approximately 100 records but the recall threshold is reported with its confidence interval, and the number of true positives in the calibration sample is reported alongside it, so that a recall figure resting on a small number of positives is visible as such. Where fewer than 25 records in the calibration sample are human-includes, the pilot is extended until at least 25 are accumulated before recall is assessed.

## 2.7 Seed composition and seed recency are registered as determinants of the descriptive map

**The gap.** The 23 seeds comprise 6 civic technology, 7 public interest technology and 10 "for good" works. Because the corpus is generated from the seeds by citation chasing, that composition shapes the distribution the descriptive map reports. RQ1 asks how the literature is distributed across disciplinary homes, application domains and normative lenses; the registered remedy for seed dependence is the leave-one-out check, which tests sensitivity to individual seeds and not to the composition of the set as a whole.

The organizational strand states the analogous constraint explicitly: frame composition sets the denominator for every count, so population-level proportions are placed out of scope. The literature strand made no corresponding statement.

A second property compounds this. Three seeds are too recently published for forward citation chasing to return a meaningful set: seed 13 (August 2025), seed 22 (March 2026) and seed 23 (May 2026). The expansion is therefore ascendancy-only for those seeds, and the "for good" tradition — which holds both the largest share of seeds and the most recent ones — will be covered more thoroughly backward than forward. This bears directly on RQ1, which asks how the distribution of the literature has changed over time.

**As revised.** Tier 1 descriptive distributions are reported as distributions over the assembled corpus and not as estimates of the composition of the TPG literature. The seed set's tradition composition is reported alongside them, together with per-seed forward and backward yields, so that seeds contributing in only one direction are visible. No claim is made that the relative sizes of the three traditions in the corpus reflect their relative sizes in the literature, and the seed composition is added to the coverage and selection biases addressed under Publication bias analyses.

## 2.8 The preliminary corpus cross-check is bounded

**The gap.** Search validation states that recovered records are cross-checked against the preliminary exploratory corpus, while Miscellaneous search strategy details states that the corpus is set aside and not carried forward. The cross-check is a use of that material, and no consequence, denominator or interpretation is registered for it. The organizational strand handles the parallel situation explicitly: substantial overlap with the ad hoc collection is expected by construction, neither high nor low overlap is diagnostic, and no comparison is reported.

**As revised.** The cross-check is retained as an internal diagnostic and is bounded on the same terms. Substantial but incomplete overlap between the preliminary corpus and the registered corpus is expected by construction, since the preliminary corpus informed the selection of the seeds. Neither a high nor a low overlap is diagnostic, no rate or proportion is computed from the comparison, and no result of it is reported as a finding. Where a record in the preliminary corpus is not recovered, it is treated exactly as an unrecovered validation work under 2.4 — the reason is established and reported — and it does not by itself trigger revision of the seed set.

---

# AMENDED FIELD TEXT

The passages below replace the corresponding text in the registration. Only changed passages are reproduced.

## Type of review — guidelines list

Add to the existing list:

- Sampling and saturation in the organizational strand: Palinkas et al. (2015) on stratified purposeful sampling; Francis et al. (2010) on operationalising data saturation through a declared initial analysis sample and stopping criterion; Guest et al. (2006) and Hennink & Kaiser (2022) on empirical saturation points; Malterud et al. (2016) on information power.
- Sampling frames for a population with no census frame: Kalton & Anderson (1986) on sampling rare populations; Hartley (1962) on multiple-frame sampling; Heckathorn (1997) on chain-referral approaches, which this design does not adopt and against which the non-frame probe is bounded.
- Agreement statistics: Landis & Koch (1977) for the kappa benchmark; Feinstein & Cicchetti (1990) for the conditions under which kappa is uninterpretable and percentage agreement is additionally reported.
- AI use: RAISE 1 and RAISE 3 (Responsible AI in Evidence Synthesis, 2025).

## Background — final paragraph of the first section

We compare the traditions on five dimensions adapted from Arnstein's (1969) ladder of citizen participation, which we use as a common analytic axis rather than as an evaluative scale: who participates; who benefits; what is meant by social good; who decides; and what counts as relevant technology. Decision authority is registered as a dimension in its own right rather than as a clause attached to the definition of social good, because it is the quantity the ladder itself is ordered on, and because the ladder's central distinction — that participation without decision authority is tokenism — is only observable if participation and decision authority are coded separately.

## Review stages — stage 6

6. Pilot Extraction / Charting (25 sources). Pilot the charting form — disciplinary home, application domain, normative lens, and the five framework dimensions (who participates, who benefits, what counts as social good, who decides, what counts as relevant technology) — on twenty-five included works drawn to span the three traditions and the recorded source types; refine the form.

## Primary research question 3

3. Compared on a common framework — who participates, who benefits, what counts as social good, who decides, and what counts as relevant technology — where do the three traditions converge and diverge?

## Secondary research question 6

6. How do organizations answer the same five framework dimensions, and which configurations of those answers appear in practice, in the literature, or in only one of the two?

## Dependent variables — literature strand

For each included work in the literature strand, the main variables are: tradition (public interest technology / civic technology / "for good" / adjacent); disciplinary home; application domain; normative lens; publication year; source type; and the five framework dimensions.

## Dependent variables — organizational strand

[Existing text, with "the four framework dimensions" replaced by "the five framework dimensions".]

## Query strings — route (2)

(2) Citation-network expansion (OpenAlex/Lens via citationchaser): not a Boolean query — the "query" is the identifier list of the 23 frozen seed articles, from which the tool retrieves backward references and forward citations. Twenty-two seeds are identified by DOI; seed 20 (CEUR-WS proceedings) carries no DOI and is identified by its OpenAlex work ID, recorded in the frozen seed file. Where a seed's citation neighbourhood is unavailable or materially incomplete in the index, that fact is recorded per seed and reported alongside the leave-one-out sensitivity check.

## Search validation procedure

Yes. We validate the strategy against a pre-specified set of known landmark works that any adequate search must recover. The set is recorded in an attachment to this update and frozen before the Search stage begins. No work in the validation set is among the 23 frozen seeds: a seed is removed from the candidate pool at deduplication as already included, so its non-appearance in the pool is an artifact of that step and carries no information about search adequacy. The check is run against the pre-deduplication pool, so that recovery is assessed before seeds are removed.

Arnstein (1969) is retained in the set but reported separately and does not count toward the pass criterion, because it is the analytic framework's own source and its recovery is close to guaranteed by backward chasing from the civic technology seeds.

Non-recovery of a validation work is recorded and reported in every case. Revision is not automatic. We first establish whether the work is (a) absent from the index, (b) present in the pool but excluded at screening, or (c) present in the index but unreachable from any seed's citation neighbourhood, and we report which. Only (c) bears on search adequacy. Where two or more validation works fall into (c), we add a targeted query rather than alter the seed set, because the seed set is the frozen input to the expansion and altering it changes the corpus definition; any addition is documented in a preregistration update before the full run.

We additionally cross-check recovered records against the preliminary exploratory corpus as an internal diagnostic. Substantial but incomplete overlap is expected by construction, since that corpus informed the selection of the seeds. Neither a high nor a low overlap is diagnostic, no rate or proportion is computed from the comparison, and no result of it is reported as a finding.

## Used exclusion criteria

A record is excluded as soon as any of the following is met (the reason is logged for the PRISMA-ScR flow):

1. Not English-language.
2. Not relevant to technology for the public good (TPG) — does not substantively engage any of the three traditions (public interest technology, civic technology, or the "for good" tradition) or the public-good orientation of technology (e.g., corporate social-responsibility, green-finance, or general AI/ML work with no public-good focus).
3. Ineligible source type — not a scholarly work (journal article, conference paper, book/chapter, thesis) or an influential grey-literature report/white paper (e.g., news items, blog posts, promotional or marketing pages).
4. Duplicate of a record already included.
5. Preprint superseded by a published version (the published version is retained).
6. Retracted. Applied at full-text screening and at any later point at which a retraction notice is identified. A record retracted after charting is removed from the analytic corpus and the removal is counted and reported. An expression of concern is not a retraction: such a record is retained and flagged in the shared dataset.

Records whose full text cannot be obtained are recorded as "not retrieved" rather than excluded.

## Miscellaneous search strategy details

The 23-article seed set is frozen and attached to this registration and is the sole input to the citation-network expansion; the preliminary corpus assembled during exploratory work is set aside and not carried forward. The attached seed file was revised on [DATE] to correct transcription and formatting errors identified by verifying every record field by field against its source; the revision log accompanying the file records each correction, and the 23 works identified are unchanged. Both the original and revised files remain available on the OSF project. Different citation indices have genuinely different coverage, so the resulting corpus is partly a function of the chosen index; this is acknowledged as a limitation.

Two properties of the seed set are recorded here because they shape the corpus. First, three seeds are preprints and one is CEUR-WS proceedings. The frozen identifier remains the input to the expansion for the duration of the review regardless of subsequent publication. Where a seed is published during the review, the publication is recorded in the seed file with its date and identifier, the published version is treated as the citable form in the write-up, and whether the index merges the preprint and published records is checked and reported; where it does not, the forward-citation set retrieved from the frozen identifier is reported as incomplete for that seed and its leave-one-out result is read against that fact. The seed set is not re-frozen and no seed is substituted.

Second, the seed set comprises 6 civic technology, 7 public interest technology and 10 "for good" works. Because the corpus is generated from the seeds by citation chasing, this composition shapes the distribution the descriptive map reports; the consequence is registered under Synthesis plan and Publication bias analyses.

Third, three seeds are recent enough that forward citation chasing will return little or nothing from them: seed 13 (August 2025), seed 22 (March 2026) and seed 23 (May 2026). For those seeds the expansion is effectively ascendancy-only. This interacts with the composition above, because the "for good" tradition holds both the largest share of seeds and the most recent ones, so its coverage will be broader backward than forward. The seed file carries a *Forward-chase viability* column recording this per seed in advance, and per-seed forward and backward yields are recorded at the Search stage and reported, so that a seed contributing in only one direction is visible rather than assumed symmetric.

## Entities to extract — literature strand, item 5

5. The five framework dimensions (derived from Arnstein's ladder) — who participates; who benefits; what is meant by social good; who decides; and what counts as relevant technology.

## Entities to extract — organizational strand

[Existing text, with "the four framework dimensions" replaced by "the five framework dimensions".]

## Extraction stages — stage (1)

(1) Training/pilot stage — the charting form is piloted on 25 included sources, drawn to span the three traditions and the recorded source types; both the AI-assisted procedure and a human blind to the AI chart the same sources, so the AI can be validated (below), and the form and prompts are refined. Changes are recorded in a preregistration update (charting is iterative; Levac et al., 2010).

## Extraction reliability — literature strand

The AI functions as a first-pass coder whose output is validated by a human. At the pilot, a human charts the twenty-five-source calibration set blind to the AI, and we compute AI-human agreement per field — Cohen's kappa for categorical entities (tradition, facets, source type, framework-dimension codes) and field-level accuracy for metadata — and report it with confidence intervals.

For metadata fields, the workflow proceeds to the full run only if field-level accuracy reaches 95%. For categorical interpretive entities the benchmark is Cohen's kappa at or above 0.60, reported with its confidence interval and with percentage agreement alongside it where the marginal distribution is too skewed for kappa to be interpretable.

The 0.60 benchmark is applied as a benchmark and not as an automatic gate. Kappa computed on twenty-five observations for a multi-category interpretive field carries substantial uncertainty, and a binary consequence applied to a point estimate of that precision would remove AI assistance from fields whose agreement is adequate and retain it on fields whose agreement is not. Where a field falls below the benchmark, the prompts and codebook are revised and the pilot repeated. Where it remains below the benchmark after revision, the field is reported with its statistic and confidence interval stated, and the decision to retain or withdraw AI recommendation for that field is made on the reported evidence and documented in a preregistration update before the full run. Where a field's confidence interval spans 0.60, that is reported rather than resolved by the point estimate.

In the full run, every interpretive field is human-validated (not blind, by design), and metadata are verified in full.

## Screening stages — pilot screening and AI validation

Before the full run, a calibration sample of approximately 100 records is screened by a human, blind to the AI, and independently by the AI-assisted procedure described below. Human and AI decisions are compared to estimate the AI's recall/sensitivity (primary) and specificity and to surface systematic error patterns. Recall is reported with its confidence interval, and the number of human-includes in the calibration sample is reported alongside it, so that a recall figure resting on few positives is visible as such. Where fewer than 25 records in the calibration sample are human-includes, the calibration sample is extended until at least 25 have accumulated before recall is assessed. The full AI-assisted run proceeds only if measured recall meets a pre-specified threshold of ≥95%; otherwise the prompt and criteria are revised and the pilot repeated. Validation results and any revisions are recorded in a preregistration update.

## Screening reliability — Group 3

**GROUP 3 — JUDGMENT-DEPENDENT FIELDS.** C3 (constitutive technology), C4 (public benefit), C5 (funder program), and the five framework dimensions.

[Remainder of the Group 3 text unchanged.]

## Screening reliability — final paragraph of the organizational strand description

C3 and the framework dimensions are the fields most exposed to judgment drift, and the framework dimensions were unanswered across the whole prior exploratory collection, which is why they are piloted and revised before scaling and are never coded by a single person. Who decides is expected to be the most frequently undetermined of the five, and its undetermined rate is reported per block alongside its agreement statistic.

## Sampling and sample size — the stopping rule

Sampling within a block continues until six consecutively coded organizations in that block produce no new code on any of the five framework dimensions. Saturation is assessed per block, not globally, and the count resets whenever a new code appears. An undetermined value neither resets the count nor counts toward the six, because it records that the available evidence does not reach the question rather than that the dimension has ceased to yield new answers; counting it would allow a block to terminate on absence of disclosure rather than exhaustion of variety. Records excluded at the second screening pass do not count toward the six, because a record that fails C3, C4, or C5 is never coded on the framework dimensions and so cannot bear on whether new codes are appearing; frame-operator records likewise do not count, because their inclusion is guaranteed rather than sampled. The saturation point reached in each block, the number of organizations coded to reach it, the number of undetermined values encountered on each dimension, and per-frame yield are all reported.

Ecosystem role is coded on the full instrument as registered but does not enter the saturation criterion. It is a closed controlled list rather than a rubric constructed at calibration, so it registers the first appearance of a fixed value within a block rather than the emergence of a new code, and it is exhausted early in every block while remaining capable of resetting the counter on a record whose framework-dimension answers are already familiar.

## Extraction reliability — organizational strand

[Existing text, with "the four framework dimensions" replaced by "the five framework dimensions" in the enumeration of Group 3 fields.]

## Data validation

Charted values are validated against the source during the human-validation step of extraction; metadata are cross-checked against DOIs via Crossref/OpenAlex; and we will screen included records against retraction registers (Crossref/Retraction Watch). A retracted record is excluded under exclusion criterion 6 and logged as such in the PRISMA-ScR flow; where the retraction is identified after charting, the record is removed from the analytic corpus and the removal is counted and reported. A record under an expression of concern is retained and flagged in the shared dataset. Interpretive codings are triangulated through the pilot AI–human agreement check and the verbatim-evidence requirement. Our validity criterion is that every coding be supported by explicit textual evidence; codings that fail this are re-coded or marked uncertain and excluded from claims that depend on them. Anomalous or inconsistent codings surfaced during synthesis are returned to the source for re-checking.

## Synthesis plan — Tier 1

Tier 1 — descriptive mapping (RQ1). Numerical summary of the charted facets: distributions and cross-tabs across discipline, domain, and lens; a publication timeline; and identification of anchor/hub works. These distributions are reported as distributions over the assembled corpus and not as estimates of the composition of the TPG literature. The tradition composition of the seed set (6 civic technology, 7 public interest technology, 10 "for good") is reported alongside them, and no claim is made that the relative sizes of the three traditions in the corpus reflect their relative sizes in the literature.

## Synthesis plan — Tier 3

Tier 3 — cross-tradition synthesis (RQ3). Compare the three traditions on the five framework dimensions; identify convergences and recurring tensions; and construct an integrated account of TPG.

## Synthesis plan — third organizational component

Third, a comparison against the literature findings on the five framework dimensions, addressing RQ6. This is a structural comparison of emphasis and configuration, not a distributional one: we report which configurations of the five dimensions appear in practice, which appear in the literature, and which appear in only one, without attaching population proportions to any of them.

## Synthesis plan — inductive coding

[Existing text, with "with an agreement statistic computed on a subsample" replaced by "with agreement between the two research assistants computed over all pooled phrases and reported".]

## Expectations — (c)

[Existing text, with "the configurations of the four framework dimensions" replaced by "the configurations of the five framework dimensions".]

## Publication bias analyses

Not applicable in the quantitative sense: with no pooled effect sizes, funnel plots, Egger's test, p-curve, and related corrections cannot be computed. We will instead address the analogous coverage and selection biases qualitatively — the dependence of the corpus on the seed set, including the tradition composition of that set; the chosen citation index; the incomplete indexing of preprint and proceedings seeds; the English-language restriction; and the field's own publication practices (including reliance on grey literature and preprints) — and report these in the limitations, supported by the leave-one-out and index-sensitivity checks below.

## Miscellaneous screening details — AI-use disclosure

[Existing text, with "Clause Opus 5" corrected to "Claude Opus 5".]

---

# ATTACHMENTS ADDED OR REPLACED

- **Search validation set (new).** The 8–10 landmark works, with full citations and identifiers, none of them among the 23 seeds. Frozen before the Search stage.
- **Frozen seed set (replaced).** Twenty-two corrections across the twenty-three records: two factual (seed 22's venue label, the identifier having been correct; seed 13's third author, Lisa M. Chambers to Lauren M. Chambers) and twenty formatting (BibTeX brace protection, an escaped ampersand, and ` and ` author separators). Four columns added — *Expansion identifier*, *Preprint / superseded*, *Forward-chase viability*, *Verified*. A *Revision log* sheet records every correction with its before and after, the date, the assurance that no stage had been executed, and three outstanding items: the OpenAlex work ID for seed 20, the per-seed forward and backward yields to be recorded at first run, and the check of whether the index merges seed 22's preprint with its published record. **The 23 works identified are unchanged; no seed has been added, removed or substituted.**
- **Organizational strand protocol workbook (replaced).** Codebook amended so the Group 3 framework-dimension fields are `who_participates`, `who_benefits`, `what_counts_as_social_good`, `who_decides` and `what_counts_as_relevant_technology`, all marked PILOT; `ecosystem_role` retained under functional role with a note that it does not enter the saturation criterion; the undetermined rule recorded against the stopping rule.
- **Literature charting form (replaced).** Amended to the same five dimensions, so that RQ3 and RQ6 compare the strands on a shared axis.

---

# CHECKLIST BEFORE FILING

- [ ] Fill the date and the validation-set citations.
- [ ] Search the full registration for "four" and confirm no surviving reference to four framework dimensions.
- [ ] Confirm the literature charting form and the organizational codebook name the same five dimensions in the same words.
- [ ] Enter the OpenAlex work ID for seed 20 in the seed file's Expansion identifier column, or record that none exists.
- [ ] Confirm the corrected seed file resolves for all 23 identifiers before the Search stage, and record per-seed forward and backward yields at first run.
- [ ] Deposit the revised seed file with its revision log, superseding but not deleting the original, so both versions remain retrievable.
- [ ] Check whether the index merges seed 22's preprint (arXiv 2505.22327) with its published EACL record, and report the result.
- [ ] Confirm the End date field: the organizational strand is estimated at ~480 research-assistant hours and ~135 lead-reviewer hours, which the End date field currently budgets at four to six weeks.

---

# References added by this update

Feinstein, A. R., & Cicchetti, D. V. (1990). High agreement but low kappa: I. The problems of two paradoxes. *Journal of Clinical Epidemiology*, 43(6), 543–549. https://doi.org/10.1016/0895-4356(90)90158-L

Cicchetti, D. V., & Feinstein, A. R. (1990). High agreement but low kappa: II. Resolving the paradoxes. *Journal of Clinical Epidemiology*, 43(6), 551–558. https://doi.org/10.1016/0895-4356(90)90159-M

Francis, J. J., Johnston, M., Robertson, C., Glidewell, L., Entwistle, V., Eccles, M. P., & Grimshaw, J. M. (2010). What is an adequate sample size? Operationalising data saturation for theory-based interview studies. *Psychology & Health*, 25(10), 1229–1245. https://doi.org/10.1080/08870440903194015

Guest, G., Bunce, A., & Johnson, L. (2006). How many interviews are enough? An experiment with data saturation and variability. *Field Methods*, 18(1), 59–82. https://doi.org/10.1177/1525822X05279903

Hartley, H. O. (1962). Multiple frame surveys. *Proceedings of the Social Statistics Section, American Statistical Association*, 203–206.

Heckathorn, D. D. (1997). Respondent-driven sampling: A new approach to the study of hidden populations. *Social Problems*, 44(2), 174–199. https://doi.org/10.2307/3096941

Hennink, M., & Kaiser, B. N. (2022). Sample sizes for saturation in qualitative research: A systematic review of empirical tests. *Social Science & Medicine*, 292, 114523. https://doi.org/10.1016/j.socscimed.2021.114523

Kalton, G., & Anderson, D. W. (1986). Sampling rare populations. *Journal of the Royal Statistical Society, Series A (General)*, 149(1), 65–82. https://doi.org/10.2307/2981886

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics*, 33(1), 159–174. https://doi.org/10.2307/2529310

Malterud, K., Siersma, V. D., & Guassora, A. D. (2016). Sample size in qualitative interview studies: Guided by information power. *Qualitative Health Research*, 26(13), 1753–1760. https://doi.org/10.1177/1049732315617444

Palinkas, L. A., Horwitz, S. M., Green, C. A., Wisdom, J. P., Duan, N., & Hoagwood, K. (2015). Purposeful sampling for qualitative data collection and analysis in mixed method implementation research. *Administration and Policy in Mental Health and Mental Health Services Research*, 42(5), 533–544. https://doi.org/10.1007/s10488-013-0528-y

Responsible AI in Evidence Synthesis (RAISE) (2025). Guidance and recommendations. Open Science Framework. https://osf.io/fwaud/
