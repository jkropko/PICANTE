# Preregistration Update

**Generalized Systematic Review Registration Form — OSF**

*Initial registration frozen 7/31/2026. This update submitted 8/19/2026.*

---

# Justification for update

## Assurance that no data have been observed

No component of the registered protocol has been executed. The citation-network search from the frozen seed set has not been run; no records have been retrieved, screened, or charted; the pilot screening and pilot charting sets have not been drawn. In the organizational strand, the frame register has not been frozen, no snapshot has been captured, no frame has been enumerated, and no organization has been screened or coded. The calibration rounds registered under Screening Reliability have not been conducted. None of the revisions below could therefore have been informed by results, because no results exist.

This update is filed specifically so that the changes are on the record before execution begins rather than after. It is filed before the organizational register's freeze date is set, so that the freeze date is chosen after these revisions are fixed rather than alongside them, and before the Search stage begins, so that the corrections to the search validation procedure are in place before the procedure is run.

The disclosures of prior exploratory work made in the initial registration and in Update 1 stand unchanged and are not repeated here. Nothing in the preliminary literature corpus or the ad hoc collection of 231 practitioner-organization records informed the revisions below.

Several revisions correct defects identified by re-reading the registration against its own frozen attachments: by checking the named landmark works against the frozen seed list, by checking the seed identifiers against the tool that consumes them, and by verifying every seed record field by field against its own source. That verification retrieved the twenty-three seed works' own bibliographic records only. It retrieved no candidate records, executed no search, ran no citation-network expansion, and produced no pool against which any registered analysis could have been computed.

---

## Class 1 — Corrections

These correct errors, omissions, and internal contradictions. None changes the design.

### 1.1 Model name in the screening AI-use disclosure

Update 1 recorded that the model name was corrected from "Clause Opus 5" to "Claude Opus 5". The correction reached the Software field and the extraction AI-use disclosure, both of which now read correctly, but not the screening AI-use disclosure under Miscellaneous screening details, which still reads "Clause Opus 5". It is corrected here. The AI-use disclosure must name the model correctly to serve its reproducibility function under RAISE.

### 1.2 Agreement statistic for the inductive category coding

Extraction Reliability specifies that agreement on category assignment is computed over all pooled non-lexicon phrases; the Synthesis Plan specifies a subsample. Resolved toward the full set, consistent with every other double-coded field in the organizational strand, where full double coding rather than subsampling is what makes the statistic computable over the analytic dataset.

### 1.3 Completing the RAISE citation

RAISE is a collection of three documents rather than one. The guidelines list is amended to cite RAISE 1 (recommendations for practice across the evidence synthesis ecosystem) and RAISE 3 (selecting and using AI tools, including ethical, legal and regulatory considerations), which are the parts that govern this protocol. RAISE 2 addresses tool development and is not applicable.

### 1.4 Methodological citations for the organizational strand

The guidelines list names the standards governing the literature strand but no source for the organizational strand's sampling and reliability procedures, which were registered in Update 1 without attribution. The list is completed below. No procedure changes; the sources are the ones the registered procedures already follow.

### 1.5 Corrections to the frozen seed file

Every record in the frozen seed set was checked field by field against its source: identifier, authors, year, title and venue. The check involved no retrieval of candidate records, no execution of the citation-network expansion, and no search. It produced twenty-one field-level corrections across twenty of the twenty-three records, none of which changes which work a record denotes. Seeds 4, 14 and 21 were not corrected. **No seed has been added, removed or substituted, and the twenty-three works identified are exactly those registered.**

A revised seed file supersedes the original as an attachment — the original is retained on the OSF project rather than deleted, so that a reader can verify for themselves that no work changed — and carries a revision-log sheet that records every correction with its before and after, the date, and the fact that no stage of the protocol had been executed.

The corrections fall into two kinds.

**Factual corrections (two records).**

*Seed 22 — venue.* The record gives the venue as *Findings of the Association for Computational Linguistics: EACL 2026* and the identifier as `10.18653/v1/2026.eacl-long.238`. The identifier is correct; the venue label is not. The work is a main-track long paper, published in *Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. 5110–5170, Rabat, Morocco. Verified against the ACL Anthology record and the EACL 2026 accepted-papers listing. The venue field is corrected.

*Seed 13 — author name.* The record gives the third author as Lisa M. Chambers. The author is Lauren M. Chambers, verified against arXiv:2508.07230. The name is corrected.

**Formatting corrections (twenty records).** The seed file had been exported from a BibTeX source with the source's escaping intact: an escaped ampersand in one venue string, brace protection around multi-word surnames in five author fields, and BibTeX's ` and ` separator in nineteen of the twenty-three author fields. All are normalised — escapes resolved, braces removed, author separators changed to semicolons. Every corrected record received at least one formatting correction; the two records carrying factual corrections received formatting corrections as well. The revision-log sheet records each correction individually with its before and after.

These corrections do not affect the citation-network expansion, which consumes identifiers rather than author strings. They are made because the seed file is a shared attachment under CC-BY 4.0 and the source of the citations in the eventual manuscript, and because leaving markup artifacts in a deposited dataset would propagate them into anything built from it.

**Four columns are added** to the seed file, recording per seed what the registered checks require: the identifier supplied to the expansion; preprint and supersession status; forward-chase viability; and the date on which the record was verified against its source. The first three are registered under 1.6, 2.5 and 2.7 below; the fourth records when each entry was checked and carries no registered commitment.

### 1.6 Seed 20 — no DOI, and the registered expansion input is a DOI list

Query strings states that the input to the citation-network expansion is "the DOI list of the 23 frozen seed articles." Seed 20 (Arora & Sarkar, 2023, CEUR-WS Vol-3582) has no DOI. As registered, it cannot be supplied to the expansion.

Corrected by amending Query strings to refer to the identifier list rather than the DOI list, and by adding an *Expansion identifier* column to the seed file in which the identifier actually supplied to the tool is recorded for every seed. Seed 20's cell is marked as outstanding: no identifier has been fabricated, and an OpenAlex work ID must be entered there before the Search stage begins.

Where a seed's citation neighbourhood is unavailable or materially incomplete in the index — which is expected for CEUR proceedings — that fact is recorded per seed and reported alongside the leave-one-out sensitivity check, so that a seed contributing no expansion is visible rather than silently inert. If no usable identifier exists at the Search stage, seed 20 is reported as contributing no citation neighbourhood, and it is not replaced.

### 1.7 Retraction screening has no registered consequence

Data validation states that included records are screened against retraction registers and that a retracted item will be "excluded or flagged," leaving it undetermined which. The exclusion criteria list five reasons, none of them retraction, so the PRISMA-ScR flow has no category to log such a record against. This is the same defect Update 1 corrected for the agreement thresholds: a rule with no specified consequence is not a constraint.

Resolved by adding retraction as exclusion criterion 6, applied at full-text screening and at any point thereafter when a retraction notice is identified, with the record logged as excluded for retraction in the PRISMA-ScR flow. Records retracted after charting are removed from the analytic corpus, and the count of such removals is reported. Expressions of concern are not retractions: a record under an expression of concern is retained and flagged in the shared dataset.

### 1.8 The End date contradicts the attached execution protocol

The End date field estimates the organizational strand at "~4–6 weeks", run in parallel with the literature strand, and derives a planned end date of 30 June 2027 from that figure together with the other stage durations. The organizational strand protocol attached to the same registration estimates the same work at approximately 480 research-assistant hours and 135 lead-reviewer hours — on the attachment's own reckoning, about 1.5 to 1.7 semesters for two assistants working ten hours a week. The registration and its attachment therefore give figures for the same stage that differ by roughly a factor of five, and the planned end date rests on the smaller one.

The organizational-strand revision is a correction rather than a design change. No stage is added, removed, or altered in scope; no procedure changes; the work described is exactly the work already registered in Update 1, whose per-record commitments — full double coding of every Group 3 field, adjudication of every disagreement, verification of every AI proposal against its source, and an individual location determination for several hundred records at C2 — are what the 480-hour figure counts. The correction reconciles the registration to its own attachment.

**As revised.** The organizational strand's duration is stated as approximately two academic semesters of part-time work by two research assistants, consistent with the attached protocol's estimate, in place of "~4–6 weeks".

Two literature-strand durations are revised in the same recalculation. These two are not corrections: they follow from the pilot sizes registered under 2.6, which is a design change, and they appear here only so that the End date field is not left contradicting a change made elsewhere in this update. They are recorded in this item rather than in 2.6 because splitting a single registered field across two items would be worse than noting the mixed status here. The charting pilot rises from ten to twenty-five included sources, each charted both by a human blind to the AI and by the AI, and its duration is revised from approximately two weeks to approximately three to four weeks. The screening pilot remains at approximately 100 records in the ordinary case but may extend to a maximum of 250 where human-includes are sparse, and its duration is revised from approximately two weeks to approximately two to four weeks. No other stage duration changes. The planned end date is moved to 9/16/2026 accordingly.

Two further points are recorded so that the revised date is not read as a commitment the design cannot support. First, the organizational strand runs in parallel with the literature strand but is not independent of it: the strands meet at the Synthesis stage, so the later of the two governs. Second, the strand's critical path runs through adjudication by the lead reviewer, because the saturation counter advances only on adjudicated codes; a backlog in adjudication stalls coding regardless of research-assistant availability. Nothing in the protocol is time-boxed, and extending the schedule requires no further registration change.

The search expiration interacts with this. The registered expiration is 12 months from the search, after which the citation-network expansion is re-run from the frozen seeds and newly included records are reported. On the revised schedule the expiration may fall before submission, in which case the refresh is run as registered; this is noted here so that the interaction is anticipated rather than discovered.

---

## Class 2 — Design changes

Registered before execution. Each states what was registered, what replaces it, and why.

### 2.1 The framework dimensions become five

**As registered.** Four dimensions: who participates; who benefits; what counts as social good and who decides; what counts as relevant technology.

**As revised.** Five dimensions: who participates; who benefits; what counts as social good; **who decides**; what counts as relevant technology.

The change separates decision authority from the definition of the good, which the registered wording bundled into a single dimension. It applies to the literature charting form and the organizational instrument together, because the dimensions are the shared axis on which RQ3 and RQ6 compare the strands.

**Rationale.** The dimensions are derived from Arnstein's (1969) ladder of citizen participation, and the ladder has one axis: decision power. Its rungs, from manipulation through tokenism to citizen control, are degrees of who holds authority over a decision. Registering that quantity as a subordinate clause attached to a different dimension demotes the ladder's own subject within a framework that claims the ladder as its source.

Separating it also restores a distinction the ladder exists to draw. Arnstein's central move is that participation without decision authority is tokenism: consultation, placation and informing are rungs precisely because people take part without deciding. With participation and decision authority as separate coded fields, a source or an organization that involves a community while reserving determination of the good to itself or its funder is directly observable. Bundled into another dimension, that configuration cannot be recorded as such.

The revision bears on registered expectations. Expectation (b) anticipates that civic technology is the most participation-oriented and the "for good" tradition the most method-first; the place those traditions are most likely to diverge is who has standing to decide what problem is worth solving. Expectation (c) concerns configurations of the dimensions that recur across organizations, and the configurations of interest are exactly those in which participation and decision authority come apart.

**What is not claimed.** The revision does not assert that "what counts as social good" and "who decides" are unrelated, only that they are separately answerable and that sources and organizations frequently answer one and not the other. We anticipate that "who decides" will be undetermined or not reported more often than any other dimension, because neither literature nor organizational self-description reliably states where authority over the definition of the good sits. That rate is reported as a finding about what the field articulates rather than as a deficiency of the instrument.

**Consequences for reliability.** "Who decides" becomes a coded field in its own right in both strands. In the organizational strand it is a Group 3 field, double-coded in full by both research assistants and adjudicated, with its own kappa reported at calibration, midpoint and end. Where its marginal distribution is too skewed for kappa to be interpretable, percentage agreement is additionally reported. If its agreement remains below the 0.60 benchmark after codebook revision and a repeated calibration round, it is reported with its statistic stated, restricted to descriptive use, and excluded from comparative claims across blocks or frames — the treatment registered in Update 1 for any Group 3 field failing the benchmark.

### 2.2 Ecosystem role is removed from the saturation criterion

**As registered.** Sampling within a block continues until six consecutively coded organizations produce no new code on any of the four framework dimensions or on ecosystem role.

**As revised.** Sampling within a block continues until six consecutively coded organizations produce no new code on any of the five framework dimensions. Ecosystem role remains a coded field on the instrument, with its registered controlled values and its registered coding workflow. It is removed from the saturation criterion only.

**Rationale.** Ecosystem role is a closed five-value list fixed in the codebook rather than a rubric constructed at calibration. It cannot produce a new code in the sense the stopping rule is designed to detect. What it can register is the first appearance of one of its five values within a block, which is a different event: not evidence that a dimension is still yielding conceptual variety, but a categorical fact about organizational function.

Two consequences follow, running in opposite directions. The field will exhaust its values early in every block — funders enter each block by construction under the frame-operator rule, and university programs and research centers surface the *studies* and *trains* values readily — after which it contributes nothing to the counter for the remainder of collection. Before that point, a single record that is a block's first convener resets the counter even where its answers on every framework dimension are already familiar, extending sampling for a reason unrelated to the criterion the rule is meant to apply.

The registered rule was written when the framework dimensions numbered four. With five dimensions, four of which are answered against rubrics constructed at calibration rather than against a fixed list, the criterion does not require a supplementary field to remain demanding.

**What does not change.** The threshold of six is unchanged and remains fixed in advance. The rule remains assessed per block rather than globally. Only an adjudicated new code resets the counter. Records excluded at the second screening pass and frame-operator records continue not to count toward the six. The exhaustion contingency is unchanged.

### 2.3 Undetermined values and the saturation counter

Registered here because it would otherwise be resolved by discretion during collection, and because it cannot be settled honestly once coding has begun: a rule written after coders have seen how these pages read would be informed by that observation.

**As registered.** The registration specifies that a coder who cannot determine a field records it as undetermined with a note, that the record is routed to adjudication, and that the proportion of undetermined values per field is reported. It does not specify what an undetermined value does to the saturation counter.

**As revised.** An undetermined value on a framework dimension neither resets the saturation counter nor counts toward the six. The record is coded, retained and reported as normal; it is transparent to the stopping rule alone. Where every framework dimension on a record is undetermined, the record does not advance the counter at all.

**Rationale.** An undetermined value records that the available evidence does not reach the question. It is not evidence that the dimension has stopped yielding new answers. Counting it toward the six would allow a block to terminate on absence of disclosure rather than exhaustion of conceptual variety, and the two are distinguishable only if the rule treats them differently. This is a live rather than a hypothetical concern: the framework dimensions were unanswered across the whole prior exploratory collection, and the newly separated "who decides" dimension is expected to be the most frequently undetermined of the five. The cost is a longer coding queue in blocks where organizational disclosure is thin. That cost is accepted in preference to a stopping point that cannot be interpreted.

**Interaction with 2.1, stated rather than left to be noticed.** Given that expectation, the rule registered here — which makes undetermined values transparent to the counter — has a consequence worth naming: the newly separated dimension will contribute less to the stopping rule than the other four. That consequence is accepted, and the dimension is not retained in the criterion for the sake of appearances. Where the dimension is answered, it is the most informative of the five for the comparisons the review exists to make, so a new value on it should reset the counter exactly as a new value on any other dimension does. Where it is not answered, the alternative — allowing silence about decision authority to count toward saturation — would let a block terminate precisely because organizations do not disclose the thing the study most wants to know. The undetermined rate for this dimension is reported per block alongside its agreement statistic and is treated as a finding about what organizations articulate, not as a defect of the instrument.

### 2.4 The search validation set is rebuilt so that it can fail

**As registered.** "We validate the strategy against a pre-specified set of known landmark works that any adequate search must recover (e.g., Arnstein 1969; Schrock 2019; Zhang et al. 2022; Shi et al. 2020; Schank & McGuinness 2021)."

**The defect.** Three of the five named works are themselves frozen seeds: Schrock (2019) is seed 4, Zhang et al. (2022) is seed 6, and Schank & McGuinness (2021) is seed 7. Deduplication removes the 23 seeds from the candidate pool as already included. Those three works therefore cannot appear in the pool, and the check as written would report them as not recovered — a failure produced entirely by the study's own deduplication step and carrying no information about search adequacy.

The registered remedy compounds the problem. The response to a non-recovery is "we revise the seed set or add a targeted query," so a spurious failure would trigger revision of the frozen instrument on the basis of an artifact.

The two remaining works are not equivalent as tests. Arnstein (1969) is the framework's own source and is cited by several civic technology seeds, so backward chasing will recover it almost by construction. That leaves one work, Shi et al. (2020), genuinely testing whether the expansion reaches beyond the seeds' immediate neighbourhood.

**As revised.** The validation set is replaced by works that are not seeds, drawn across the three traditions and across source types, and expanded so that a single miss is interpretable. The check is run against the pre-deduplication pool, so that recovery is assessed before seeds are removed and seed-derived hits are distinguishable from genuine recoveries.

The revised set comprises 8 works, listed here by full citation with a stable identifier where one exists. No work in the set is among the 23 frozen seeds, and no work in the set may be added to the seed set at any point during the review. The set is distributed across public interest technology, civic technology and the "for good" tradition.

Each work is recorded with the arm of the search it tests. Most test the citation-network expansion and are expected to be reachable from the seed neighbourhood. At least two are grey-literature items testing the targeted hand-searching of venue and organization websites, which is the arm by which the protocol expects to reach material that citation indices cover poorly; these are assessed against that arm and not against the expansion. This distinction is registered because a grey-literature report absent from the citation index would otherwise be recorded as a non-recovery of a kind the protocol has already said does not bear on search adequacy, and would therefore test nothing.

**The pass criterion has two parts, because the set tests two arms.** The causes (a), (b) and (c) distinguished below are expansion concepts: cause (c), unreachability from any seed's citation neighbourhood, is not a question that can be asked of a work assessed against the hand-searching arm. A single criterion stated in those terms would therefore count the grey-literature works toward a threshold they cannot trigger.

For the works testing the citation-network expansion, the criterion is as stated under *Consequence of a miss* below: where two or more are unreachable from the seed neighbourhood, a targeted query is added. The threshold is two rather than one because a single unreachable work can reflect the idiosyncratic citation profile of that work — an unusually isolated venue, a paper that few of its natural citers have cited — whereas two independently unreachable works indicate a systematic gap in what the seed neighbourhood reaches. It is an absolute count rather than a proportion, and does not move with the size of the counting subset, because what it is meant to detect is evidence of a gap rather than a failure rate. Arnstein (1969) is recorded in the set but excluded from this count, because it is the framework's own source and its recovery is close to guaranteed by backward chasing from the civic technology seeds; its recovery is reported separately. The set contains at least five works counting toward this part of the criterion.

For the grey-literature works testing the targeted hand-searching of venue and organization websites, the question is whether hand-searching the venue or organization that published the work surfaced it. Non-recovery here indicates that the hand-searching arm lacks the coverage the protocol assumes, not that the expansion is inadequate, and the response is correspondingly different: we record which venues or organizations were searched, add those that were not, and report the addition. This is the first registered consequence attaching to the hand-searching arm, which the registration otherwise describes only as "targeted hand-searching of key venue and organization websites for grey literature".

The set is recorded in an attachment to this update and frozen on filing. It is frozen at filing rather than at the start of the Search stage so that it is covered by the assurance given above, under which no stage of the protocol had been executed. A pre-2000 foundational work is not required. Backward-chasing depth is better tested by including a work situated two or three citation hops from the seed set, where one can be identified, than by a work old enough that it cannot substantively engage traditions that did not yet exist and would be correctly excluded at screening if recovered.

**Consequence of a miss.** Non-recovery of a validation work is recorded and reported with the review in every case. Revision of the seed set is not automatic: we first establish whether the work is (a) absent from the index, (b) present in the pool but excluded at screening, or (c) present in the index but unreachable from any seed's citation neighbourhood, and we report which. Only (c) bears on search adequacy. Where two or more of the expansion-testing validation works are unreachable from the seed neighbourhood, we add a targeted query rather than alter the seed set, because the seed set is the frozen input to the expansion and altering it changes the corpus definition; any addition is documented in a preregistration update before the full run.

### 2.5 Superseded seeds

**The gap.** Three seeds are arXiv preprints (6, 13, 23) and one is CEUR proceedings (20). Exclusion criterion 5 removes preprints superseded by a published version, and deduplication removes the preprint in favour of the published version — but seeds are removed from the candidate pool before either rule applies, and the seed set is frozen and is the sole input to the expansion. Nothing registers what happens when a seed is published during the review. Over an eleven-month review with two seeds dated 2025 and 2026, this is likely rather than hypothetical. The question is not only bookkeeping: citation indices sometimes merge preprint and published records and sometimes do not, so the two identifiers can return different citation neighbourhoods.

**Already realised at filing.** This is not a prospective concern only. Seed 22 exists in both forms as of filing: an arXiv preprint (2505.22327, v1 May 2025, v2 January 2026) and the published EACL 2026 record cited in the seed file. Seed 6 is a 2022 arXiv preprint (10.48550/arXiv.2204.11461) and is old enough that a published version is likely to exist; its status is established before the Search stage and recorded in the seed file rather than left to be discovered during the expansion. For every seed found to exist in both forms, whether the index merges the two records is checked at the Search stage and reported, and the forward-citation set is read against that result.

**As revised.** The frozen identifier remains the input to the citation-network expansion for the duration of the review, regardless of subsequent publication. The seed file carries a *Preprint / superseded* column in which each seed's status is recorded, flagging the three arXiv seeds and noting seed 22's dual existence. Where a seed is published during the review, the publication is recorded in that column with its date and identifier, the published version is treated as the citable form in the write-up, and whether the index merges the two records is checked and reported. Where the index does not merge them, the forward-citation set retrieved from the frozen identifier is reported as incomplete for that seed, and the seed's leave-one-out result is read against that fact. The seed set is not re-frozen and no seed is substituted.

### 2.6 Pilot sizes, and the literature-strand charting gate for interpretive fields

**As registered.** The charting pilot is ten included sources. The AI-recommendation workflow proceeds to the full run only if Cohen's kappa reaches 0.60 per categorical interpretive field, with fields failing after revision reverting to unassisted human charting.

**The defect.** Cohen's kappa computed on ten observations for a multi-category interpretive field is unstable in both directions: it will fail fields whose agreement is adequate and pass fields whose agreement is not. The registration attaches a binary consequence — removing AI assistance from a field for the whole corpus — to an estimate that cannot support one. The organizational strand, by contrast, calibrates on approximately twenty organizations twice and treats 0.60 as a benchmark governing how a field is reported rather than who codes it. The stricter consequence currently rests on the weaker estimate.

**As revised.** The charting pilot is increased from ten to twenty-five included sources, drawn to span the three traditions and the source types recorded in the charting form. Kappa, its confidence interval, and percentage agreement are reported per field. This change applies to the categorical interpretive entities only.

**The metadata gate is retained unchanged:** field-level accuracy of 95% or above remains a hard condition of proceeding to the full run for metadata fields, and a metadata field below it after revision is extracted by the human without AI assistance. Metadata extraction has a determinate right answer against which accuracy can be measured on twenty-five observations; interpretive coding does not, which is the whole basis of the distinction below.

For the interpretive entities the threshold is retained at 0.60 but is applied as a benchmark rather than a gate, matching the organizational strand. A field whose agreement falls below 0.60 after prompt and codebook revision and a repeated pilot is not automatically removed from AI assistance; it is reported with its statistic and its confidence interval stated, and the decision to retain or withdraw AI recommendation for that field is made on the reported evidence and documented in a preregistration update before the full run. Where a field's confidence interval spans 0.60, that fact is reported rather than resolved by the point estimate.

**Screening pilot.** The screening pilot is retained at approximately 100 records but the recall threshold is reported with its confidence interval, and the number of human-includes in the calibration sample is reported alongside it, so that a recall figure resting on a small number of positives is visible as such. Where fewer than 25 records in the calibration sample are human-includes, the sample is extended, to a maximum of 250 records in total. The cap is registered because the calibration sample is screened by a human blind to the AI, so an uncapped extension would transfer a large and unbounded share of the full screening workload into the pilot — which is the cost the AI-assisted design exists to avoid. If 25 human-includes have not accumulated at 250 records, recall is assessed on what has accumulated and reported with its confidence interval and its denominator stated, and the pilot is not extended further.

**The screening gate remains binary, and the difference from the charting benchmark is principled rather than inconsistent.** Recall computed on twenty-five positives is no more precise than kappa computed on twenty-five records, so the argument above cannot be what distinguishes them. What distinguishes them is the asymmetry of the errors, registered in Update 1 and unchanged here. A screening error in the exclude direction removes a record from the review permanently and invisibly: it is never charted, never appears in the flow diagram as anything but an exclusion, and cannot be recovered at a later stage. An error in the retain direction is caught at full text. Sensitivity therefore has to be guaranteed conservatively even on an imprecise estimate, because the cost of being wrong is unbounded and unobservable. A charting error distorts the map equally in either direction and remains visible in the charted data, so it can be reported and judged rather than gated. The gate is retained where the estimate is weak but the consequence of proceeding wrongly is irreversible, and relaxed where the estimate is equally weak but the consequence is not.

### 2.7 Seed composition and seed recency are registered as determinants of the descriptive map

**The gap.** The 23 seeds comprise 6 civic technology, 7 public interest technology and 10 "for good" works. Because the corpus is generated from the seeds by citation chasing, that composition shapes the distribution the descriptive map reports. RQ1 asks how the literature is distributed across disciplinary homes, application domains and normative lenses; the registered remedy for seed dependence is the leave-one-out check, which tests sensitivity to individual seeds and not to the composition of the set as a whole. The organizational strand states the analogous constraint explicitly: frame composition sets the denominator for every count, so population-level proportions are placed out of scope. The literature strand made no corresponding statement.

A second property compounds this. Three seeds are too recently published for forward citation chasing to return a meaningful set: seed 13 (August 2025), seed 22 (March 2026) and seed 23 (May 2026). These are a different three from the preprint seeds identified under 2.5, overlapping with them at seeds 13 and 23. The expansion is therefore ascendancy-only for those seeds, and the "for good" tradition — which holds both the largest share of seeds and the most recent ones — will be covered more thoroughly backward than forward. This bears directly on RQ1, which asks how the distribution of the literature has changed over time.

**As revised.** Tier 1 descriptive distributions are reported as distributions over the assembled corpus and not as estimates of the composition of the TPG literature. The seed set's tradition composition is reported alongside them, together with per-seed forward and backward yields, so that seeds contributing in only one direction are visible. No claim is made that the relative sizes of the three traditions in the corpus reflect their relative sizes in the literature, and the seed composition is added to the coverage and selection biases addressed under Publication bias analyses.

### 2.8 The preliminary corpus cross-check is removed

**As registered.** Search validation states: "We additionally cross-check recovered records against the preliminary exploratory corpus."

**The problem.** The registration states elsewhere that the preliminary corpus is set aside and not carried forward, so the cross-check is the one surviving use of material the protocol otherwise excludes. No consequence, denominator or interpretation is registered for it. Any bounded version would have to state — following the treatment the organizational strand already registers for its ad hoc collection — that substantial but incomplete overlap is expected by construction, that neither a high nor a low overlap is diagnostic, that no rate is computed, and that no result is reported. A check with all of those properties yields nothing.

**As revised.** The cross-check is removed. The preliminary corpus is set aside without exception, matching the treatment of the ad hoc organizational collection and removing the last inconsistency between "set aside and not carried forward" and its actual use. The function it gestured at — establishing that the search reaches known relevant work — is discharged by the validation set registered under 2.4, which is frozen in advance, has a stated pass criterion, distinguishes the reasons a work might be missed, and can therefore fail. Nothing is lost that was previously being measured, because nothing was previously being measured.

### 2.9 Lens.org is dropped; OpenAlex becomes the sole index of record

**As registered.** "Primary citation index for citation chasing: OpenAlex and Lens.org." The two are named jointly in Databases, Interfaces, Query strings, Software and Search strategy justification, with no division of labour stated between them.

**As revised.** OpenAlex is the sole citation index of record. It runs the citation-network expansion and supplies the citation edge list for the silo analysis. Lens.org is removed from the protocol. The index-sensitivity check registered as sensitivity analysis (b) is retained, with Semantic Scholar named as the comparator in place of Lens. Crossref's role is narrowed to metadata validation and retraction screening. The registration's "citation data are retrieved from the citation index (OpenAlex/Crossref)" is amended to name OpenAlex alone, so that the edge list has a single provenance. Crossref is not used as an index-sensitivity comparator: its citation coverage reflects what individual publishers have chosen to deposit, so differences between an OpenAlex-derived edge list and Crossref would largely record deposition practice rather than index coverage, and would have to be explained away rather than interpreted.

**Rationale.** The registration never assigned the two indices distinct roles, and two fields already depart from the joint naming: citation data are registered as retrieved from "OpenAlex/Crossref" and metadata cross-checks from "Crossref/OpenAlex", with Lens absent from both. The design therefore already implied a division of labour it did not state. This revision states it and simplifies to one index. Three considerations favour OpenAlex specifically, and none of them is a claim about relative data quality.

*Licensing.* OpenAlex data are CC0. The registration commits to sharing the full set of records identified through the searches under CC-BY 4.0 with no embargo. Records derived from a CC0 source can be redistributed without qualification; records derived under Lens's Acceptable Use and Attribution terms may not be compatible with that commitment. The organizational strand already registers a licence-compatibility provision for its frames — check before redistributing, cite rather than redistribute where incompatible — and the literature strand had no equivalent. Resolving to a CC0 index removes the question rather than requiring the provision.

*Access.* Lens's free API tier is a trial valid for a limited period from approval, intended for non-commercial or limited academic use; sustained programmatic access runs through an institutional subscription or a paid plan. A multi-month expansion with a twelve-month expiration refresh is not reliably supported by trial access, and the protocol should not place its search of record on an access path the team may not hold. OpenAlex's API is keyed and metered but free at the volumes this expansion requires, and its full dataset remains freely downloadable irrespective of API terms.

*Reproducibility.* OpenAlex publishes the complete dataset as a dated CC0 snapshot. Pinning the expansion to a specific snapshot fixes the index state, which is a stronger reproducibility guarantee than a live query against either service and which bears directly on the limitation the registration already carries.

The Software field's index version string is corrected in the same move. It currently records "Lens.org / OpenAlex index (8.5)"; no version 8.5 corresponds to either service in any form we can identify. The replacement text below removes the unresolvable string and records instead the two things that are reproducible: the OpenAlex snapshot date, or the API access dates where the live API is used.

Lens.org's distinguishing capability is its unified patent and scholarly corpus with patent-to-literature citation linkage. That capability is not used by this review, whose corpus is entirely scholarly and grey literature.

**What this costs, stated plainly.** Reducing to one index makes the registered limitation — that the corpus is partly a function of the chosen index — more rather than less applicable, and we do not present this change as improving coverage. The mitigation is that the dependence becomes auditable: with a pinned snapshot a reader can name the exact index state the corpus was drawn from, which a live two-index configuration does not permit. Sensitivity analysis (b) is retained with a named comparator so that the dependence is measured rather than only acknowledged.

---

# List of updated registration questions

- Used exclusion criteria
- Primary research question(s)
- Secondary research question(s)
- Search strategy justification
- Dependent variable(s) / outcome(s) / main variables
- Expectations / hypotheses
- Search validation procedure
- Type of review
- Extraction stages
- Screening reliability
- End date
- Sensitivity analyses / robustness checks
- Interfaces
- Sampling and sample size
- Inclusion and exclusion criteria
- Software
- Screening stages
- Background
- Query strings
- Review stages
- Miscellaneous search strategy details
- Extraction reliability
- Miscellaneous synthesis details
- Entities to extract
- Databases
- Publication bias analyses
- Synthesis plan
- Data validation

---

# Landing page

## Intended use

This Generalized Systematic Review Registration Form is intended as a general-purpose registration form. The form is designed to be applicable to reviews across disciplines (i.e., psychology, economics, law, physics, or any other field) and across review types (i.e., scoping review, review of qualitative studies, meta-analysis, or any other type of review). That means that the reviewed records may include research reports as well as archive documents, case law, books, poems, etc. This form, therefore, is a fall-back for more specialized forms and can be used if no specialized form or registration platform is available.

## Citation

Van den Akker, O. R., Peters, G. Y., Bakker, C., Carlsson, R., Coles, N. A., Corker, K. S., Feldman, G., Moreau, D., Nordström, T., Pickering, J. S., Riegelman, A., Topor, M., Veggel, N., Yeung, S., Mellor, D., & Pfeiffer, N. Generalized Systematic Review Registration Form. MetaArXiv. https://doi.org/g5fj.

---

# Review methods

*In this section, you register the general type, background and goals of your review.*

## Type of review

This is a scoping review conducted with a meta-narrative synthesis (a "scoping-informed meta-narrative review"), complemented by a descriptive analysis of an original dataset of practitioner organizations. It is a qualitative, interpretive synthesis and evidence-mapping study; it is not a meta-analysis (no statistical pooling of effect sizes) and not a systematic review of intervention effectiveness. The scoping component maps the extent, range, and distribution of the literature; the meta-narrative component reconstructs and contrasts how distinct research traditions have conceptualized the topic.

Guidelines, tools, and checklists used to prepare the protocol:

- **Scoping methodology:** Arksey & O'Malley (2005), as refined by Levac et al. (2010); JBI/Peters et al. (2015, 2020) guidance, including the Population–Concept–Context (PCC) framework for eligibility criteria.
- **Reporting standard:** PRISMA-ScR (Tricco et al., 2018).
- **Meta-narrative synthesis, method and reporting:** Greenhalgh et al. (2005) and the RAMESES publication standards for meta-narrative reviews (Wong et al., 2013).
- **Review-type selection:** Grant & Booth's typology of reviews (2009) and Munn et al. (2018) on choosing a scoping over a systematic review.
- **Search and analysis:** Lecy & Beatty (2012) for citation-network / constrained-snowball searching; Braun & Clarke (2006) for thematic analysis in the qualitative coding.
- **AI use:** RAISE 1 and RAISE 3 (Responsible AI in Evidence Synthesis, 2025).
- **Sampling and saturation in the organizational strand:** Palinkas et al. (2015) on stratified purposeful sampling; Francis et al. (2010) on operationalising data saturation through a declared initial analysis sample and stopping criterion; Guest et al. (2006) and Hennink & Kaiser (2022) on empirical saturation points; Malterud et al. (2016) on information power.
- **Sampling frames for a population with no census frame:** Kalton & Anderson (1986) on sampling rare populations; Hartley (1962) on multiple-frame sampling; Heckathorn (1997) on chain-referral approaches, which this design does not adopt and against which the non-frame probe is bounded.
- **Agreement statistics:** Landis & Koch (1977) for the kappa benchmark; Feinstein & Cicchetti (1990) for the conditions under which kappa is uninterpretable and percentage agreement is additionally reported.

## Review stages

1. **Preparation.** Finalize and freeze the seed set (23 survey/definitional "hub" articles, with DOIs); specify eligibility criteria using the Population–Concept–Context framework; register this protocol on OSF.
2. **Search.** Identify records via (a) keyword searching and (b) forward/backward citation-network chasing seeded by the 23 frozen seeds (constrained snowball; Lecy & Beatty, 2012). Export the candidate pool and remove duplicates.
3. **Pilot Screening / AI validation** (~100 records, extending to a maximum of 250 where human-includes are sparse). A calibration sample is screened by the human reviewer, blind to the AI, and independently by the AI-assisted procedure. Human–AI agreement (percentage agreement and Cohen's kappa) and the AI's recall/sensitivity and specificity are computed and reported with confidence intervals and with the number of human-includes in the sample stated; the exclusion criteria and AI prompt are refined as needed before the full run.
4. **Prereg Update.** Record any refinements to the eligibility criteria arising from the pilot.
5. **Screening.** Two-stage screening (title/abstract, then full text) of the full candidate pool; log exclusions with reasons for the PRISMA-ScR flow diagram.
6. **Pilot Extraction / Charting (25 sources).** Pilot the charting form — disciplinary home, application domain, normative lens, and the five framework dimensions (who participates, who benefits, what counts as social good, who decides, what counts as relevant technology) — on twenty-five included works drawn to span the three traditions and the recorded source types; refine the form.
7. **Prereg Update.** Record any refinements to the charting form arising from the pilot.
8. **Extraction / Charting.** Chart all included works on the finalized form.
9. **Synthesis.** (a) Descriptive numerical mapping of the charted data; (b) meta-narrative synthesis of the three traditions and their cross-tradition comparison; (c) citation-network analysis to test cross-tradition citation ("silo" test); qualitative coding follows Braun & Clarke (2006).
10. **Reporting.** Write up per PRISMA-ScR (search/selection) and RAMESES (meta-narrative synthesis), including the completed PRISMA-ScR flow diagram.

**Notes.** A parallel organizational strand runs alongside the literature strand and is brought into the Synthesis stage. Its procedure is specified in this update under Inclusion and exclusion criteria, Other search strategies, Sampling and sample size, Screening reliability, Data management and sharing, Entities to extract, Sensitivity analyses, and Synthesis plan, and in full in the organizational strand protocol attached to this registration. Its stages are:

- **O1.** Fix the lexicon, criteria, standing rules, and register composition. Completed by the freezing of this update.
- **O2.** Freeze the register on a single stated date after this update is filed, and capture an archived snapshot of every frame source.
- **O3.** Enumerate each frame in full from its snapshot, under the boundary definition recorded in the register, and deduplicate to organization-level units.
- **O4.** First screening pass: apply C1 and C2 to every enumerated record, with AI first-pass extraction on mechanical fields and human verification of every proposal.
- **O5.** Compute the lexicon proxy and build the coding queue: stratify by frame and proxy, and fix the round-robin draw order with a recorded seed.
- **O6.** Calibrate: all three coders independently code a shared set, revise the codebook and the framework-dimension wording where disagreement is attributable to the instrument, and repeat on a fresh set. Calibration records are not part of the analytic dataset. The AI roles are validated against the adjudicated calibration values before any analytic record is processed.
- **O7.** Second screening pass and coding: apply C3, C4, C5 and the full instrument to records drawn from the queue, until the stopping rule is met in each block. Judgment-dependent fields are coded independently by both research assistants and adjudicated; the AI codes them blind, its output withheld until adjudication is recorded.
- **O8.** Boundary audits and supplementary probe.
- **O9.** Validate and report: reliability statistics, sensitivity analyses, and PRISMA-style accounting.

Consistent with scoping-review methodology, we do not conduct formal critical appraisal of study quality; this is a deliberate, documented choice.

## Current review stage

This is a preregistration update. The initial registration was frozen on 7/31/2026.

At the moment of freezing this update, the review remains at the end of the Preparation stage, before the Search stage of the registered protocol begins. No stage of the registered protocol has been executed at any point, either before or after the initial registration was frozen. Per-stage status:

- **Preparation** — completed. Eligibility criteria (PCC) defined; the analytic framework specified; the seed set of 23 hub articles finalized and frozen (attached to the initial registration); the data-charting form drafted but not yet piloted. For the organizational strand, the sampling frames, screening criteria, standing rules, codebook, and analysis plan are specified in this update and attached to it.
- **Search** — not started. The citation-network expansion (forward and backward citation chasing from the 23 frozen seeds) will begin only after this update is frozen.
- **Pilot Screening / Screening** — not started.
- **Pilot Extraction / Extraction (Charting)** — not started.
- **Organizational strand: enumeration, screening, and coding** — not started.
- **Synthesis / Reporting** — not started.

**Disclosure of prior exploratory work.** Earlier exploratory work informed this protocol and is set aside rather than used as data. A preliminary literature corpus, assembled from an initial seed set, informed the eligibility criteria, the analytic framework, and the selection of the frozen seed articles; the registered review will be conducted afresh from the frozen seed set. An ad hoc collection of 231 practitioner-organization records, assembled before registration, informed the design of the organizational instrument; it is set aside as exploratory, holds the same status as the preliminary literature corpus, and is not analyzed as data. It was assembled from a partially overlapping set of sources: five of the frames in the registered register — the Civic Tech Field Guide, the Alliance of Civic Technologists, the archived Code for America brigade roster, the PIT University Network, and Fast Forward — were among its sources, while several sources it used are not in the register, and the register adds frames it did not use. Substantial but incomplete overlap between that collection and the registered sample is therefore expected by construction. Neither a high nor a low overlap is diagnostic of anything, and no comparison between the two is reported.

**Disclosure of pre-registration inspection.** Before filing this update, the sources named in the organizational frame register were examined to establish whether each exists in an enumerable form, what enumerating it would cost, and where freeze dates could fall. For the Civic Tech Field Guide this included counting records by type and country and measuring field completeness in the public data export. No records were screened against the criteria, matched or deduplicated across frames, or charted on any instrument field. Frame overlap and unique-organization yield are registered analyses and were not computed.

## Start date

The start date was 7/28/2026, the day the preparation stage was initiated. The initial registration was frozen on 7/31/2026. This update is submitted on 8/19/2026.

## End date

Planned end date: 30 June 2027 (approximately 11 months from the start of the Search stage).

Three stage durations are revised; the rest are unchanged.

- **Pilot screening and criteria refinement:** ~2–4 weeks (was ~2 weeks). The calibration sample remains approximately 100 records in the ordinary case but may extend to a maximum of 250 where human-includes are sparse.
- **Pilot extraction and charting-form refinement:** ~3–4 weeks (was ~2 weeks). The pilot rises from ten to twenty-five included sources, each charted both by a human blind to the AI and by the AI.
- **Organizational strand:** approximately two academic semesters of part-time work by two research assistants (was ~4–6 weeks), consistent with the estimate in the organizational strand protocol attached to this registration (approximately 480 research-assistant hours and 135 lead-reviewer hours).

The revisions are arithmetic: no stage is added, removed, or altered in scope. The first two follow from the pilot sizes registered in this update; the third reconciles the field to its own attachment.

The organizational strand runs in parallel with the literature strand but the two meet at the Synthesis stage, so the later of the two governs the end date. Within the organizational strand the critical path runs through adjudication by the lead reviewer, because the saturation counter advances only on adjudicated codes. Nothing in the protocol is time-boxed; extending the schedule requires no further registration change. The screening estimate will still be firmed up with PredicTER after the Search stage, and the planned end date will be revised in a further preregistration update if the candidate pool is substantially larger or smaller than anticipated.

## Background

Many overlapping movements now build and study technology intended to serve the public rather than private interest, but they describe themselves with an inconsistent and proliferating vocabulary. Three traditions dominate: public interest technology (PIT), civic technology, and the "for good" tradition (data science, technology, and AI for social good). These have developed in largely separate scholarly communities, using different terms for similar work and the same terms for different ideas. This fragmentation sorts similar practices into silos and obscures tacit assumptions about what counts as social good, what counts as technological work, who participates, and who benefits.

We compare the traditions on five dimensions adapted from Arnstein's (1969) ladder of citizen participation, which we use as a common analytic axis rather than as an evaluative scale: who participates; who benefits; what is meant by social good; who decides; and what counts as relevant technology. Decision authority is registered as a dimension in its own right rather than as a clause attached to the definition of social good, because it is the quantity the ladder itself is ordered on, and because the ladder's central distinction — that participation without decision authority is tokenism — is only observable if participation and decision authority are coded separately.

Existing reviews address the traditions one at a time — e.g., Zhang et al. (2022) and Saldivar et al. (2019) on civic technology, Shi et al. (2020) on AI for social good, Aragón et al. (2020) on civic-technology research challenges — or survey the practitioner landscape (Freedman Consulting, 2016; Knight Foundation). None treats the three as parallel traditions within a single field, and none pairs a synthesis of the literature with data on the organizations that actually do the work. This review addresses those gaps: it maps the field ("technology for the public good," TPG), reconstructs and compares the three traditions on a common framework, and characterizes TPG in both research and practice.

## Primary research question(s)

These questions informed the search, screening, charting, and synthesis of the literature:

1. How is the TPG research literature distributed across disciplinary homes, application domains, and normative lenses, and how has that distribution changed over time?
2. For each tradition (PIT, civic technology, "for good"), how does it define its object of study, define "social good," and select its characteristic methods and exemplary works?
3. Compared on a common framework — who participates, who benefits, what counts as social good, who decides, and what counts as relevant technology — where do the three traditions converge and diverge?

## Secondary research question(s)

These are additional analyses, including the parallel organizational strand, that took a less central role in designing the literature search. They are numbered continuously with the primary questions so that the synthesis tiers can refer to them unambiguously.

4. To what extent do the three traditions cite one another versus operate as citation silos (measured as the proportion of cross-tradition vs. within-tradition citations in the corpus)?
5. How do TPG practitioner organizations describe their focus, and do those self-descriptions sort onto the three traditions, blur across them, or reveal categories absent from the literature?
6. How do organizations answer the same five framework dimensions, and which configurations of those answers appear in practice, in the literature, or in only one of the two?

## Expectations / hypotheses

As a primarily qualitative and interpretive review we hold expectations rather than formal hypotheses.

**(a)** The three traditions are substantially siloed, with low cross-tradition citation.

**(b)** The "for good" tradition is the most rooted in computational and analytical fields and the most method-first, civic technology the most participation-oriented and empirically grounded in HCI/CSCW, and public interest technology the most foundation-derived and field-building.

**(c)** Practitioner organizations' self-descriptions blur across the three traditions in identifiable and recurring ways rather than mapping cleanly onto them. This is registered as a structural claim, not a frequency claim: the organizational design does not license population-level proportions, so the expectation is not evaluated by how often blurring occurs in any population. It is evaluated from the inductive category coding and from the configurations of the five framework dimensions, asking whether a given blurred configuration recurs across multiple organizations and whether it appears in more than one block. "More than one block" means the configuration is present in each, not that its rate is compared between them, which the design does not license. The multi-frame subset provides supporting evidence where its minimum size is met (see Sensitivity analyses), but the expectation does not depend on it.

**(d)** The three traditions differ in the organizational infrastructure they have built. Public interest technology and civic technology have membership networks that organizations join and thereby declare themselves; the "for good" tradition organizes instead through fellowships, accelerator cohorts, funder portfolios, and university programs. We expect this difference to show in the unit-resolution outcomes: that organizations recruited through the "for good" block will resolve to programs inside larger institutions at a higher rate than those recruited through the civic technology block.

This comparison is restricted to Blocks B and C and explicitly excludes Block A. The PIT University Network lists universities rather than organizations, so Block A's unit-resolution rate is set by that frame's listing convention rather than by the tradition's organizational form, and would exceed both other blocks for a reason unrelated to the expectation being tested.

We note in advance that frame type and tradition are not separable even within the Block B to Block C comparison. Block C is built from funder portfolios, which fund programs housed in universities and larger nonprofits, while Block B is built from rosters of standalone groups. A difference in the predicted direction is therefore consistent with the expectation without confirming it, and will be reported as such rather than as evidence that the traditions differ independently of how their frames are constituted.

That the "for good" block contains no identity-type frame is a property of the frame register as constructed, not a prediction; it is recorded under Sampling and sample size.

Reflexively, we note that the research team engaged with a preliminary literature corpus and with an ad hoc organizational collection before registration, and approaches the material from a defined disciplinary vantage; these may color the meta-narrative interpretation, and we will document analytic decisions accordingly (per RAMESES).

## Dependent variable(s) / outcome(s) / main variables

This is a descriptive review with no outcome variable in the associational sense.

For each included work in the **literature strand**, the main variables are: tradition (public interest technology / civic technology / "for good" / adjacent); disciplinary home; application domain; normative lens; publication year; source type; and the five framework dimensions.

For the **citation analysis:** within- versus cross-tradition citation.

For the **organizational strand**, the main variables are: provenance (originating frame, block, admission mechanism, frame type, date identified); screening outcomes on each criterion and the first criterion failed; unit-resolution outcome; frame-operator status and the frames operated; organizational status (active / dormant / closed) with date and dated evidence artifact; tier (self-applies a lexicon label, or does the work without the field vocabulary); self-applied label recorded verbatim, with the lexicon term matched, the URL, access date, placement, and whether the organization is describing itself or quoting another party; self-descriptive phrases that match no lexicon term, recorded verbatim; ecosystem role (practices / funds / studies / trains / convenes); named partner organizations; legal form; headquarters location; founding year; funding sources; staff expertise; technologies; and the same five framework dimensions used in the literature strand.

## Independent variable(s) / intervention(s) / treatment(s)

Not applicable. This review does not concern an intervention, treatment, or causal association, so there are no independent variables. In the cross-tradition comparison and the citation analysis, "tradition membership" functions as a classification/grouping variable, but no manipulation or comparator group is involved.

## Additional variable(s) / covariate(s)

No statistical covariates, moderators, or mediators are modeled. Variables used descriptively to stratify or contextualize the main variables include: publication year (temporal trends), geographic focus (e.g., Global North vs. Global South), and, for organizations, sector (nonprofit, government, for-profit, university) and funding source.

## Software

- **OS:** macOS 15.7.7
- **Reference management and de-duplication:** Zotero (9.0.6) / BibTeX.
- **Citation-network searching:** the OpenAlex API, accessed with a registered API key, and/or a dated OpenAlex data snapshot; the citationchaser R package (0.0.4) is used where it supports OpenAlex and can supply an API key, and the expansion is scripted directly against the API where it cannot. The OpenAlex snapshot date or API access dates are recorded and reported. Research Rabbit (Major release 2026-07-09) is retained as a supplementary discovery tool only. The Lens.org index is not used; see Databases.
- **Screening:** Rayyan (1.7.7).
- **Data charting/extraction and record-keeping:** Microsoft Excel (365) / Google Sheets.
- **Citation-network analysis:** CitNetExplorer (1.0.0).
- **Descriptive analysis and figures:** R (4.6.1) / Python (3.14.6).
- **AI-assisted title/abstract screening:** Claude Opus 5, accessed via API, with a fixed prompt and default temperature settings; access dates recorded.
- **Reporting:** LaTeX (Overleaf 6.2.2).

## Funding

This project is unfunded.

## Conflicts of interest

We use practitioner networks, funder portfolios, and directories as frames to identify candidate organizations. Author Jonathan Kropko leads and co-founded Code for Charlottesville, which is reachable through the civic technology block of the frame register, and is a participant in the Alliance of Civic Technologists, which is itself one of the frames.

Because every organization that operates or publishes a frame enters the candidate pool by construction (see Sampling and sample size), the Alliance of Civic Technologists will itself be screened and coded as a record. A conflicted organization is not removed from the pool; the conflict changes who codes it and how that coding is reported.

Records for any organization in which an author holds a governance or staff role are handled as follows. The conflicted author does not screen, code, adjudicate, or review the coding of those records at any stage. Each such record is coded independently by both research assistants, and where their codings differ the disagreement is reported rather than adjudicated, because the person who would ordinarily adjudicate is the conflicted party. Every such record is flagged as author-conflicted in the shared dataset, and every recusal is logged and reported with the review.

We note a residual limitation that this procedure reduces but does not remove. The research assistants are supervised by the conflicted author, so their independence from the conflict is structural rather than complete. Independent double coding and the reporting of unadjudicated disagreement are intended to make any resulting bias visible in the shared data rather than to eliminate it, and readers should weigh the coding of author-conflicted records accordingly.

## Overlapping authorships

One or more members of the research team are co-authors of works that may be included. None of the team has authorship on any of the 23 frozen seed articles, so the seed set itself is unaffected.

In the literature strand, full-run screening, charting, and synthesis are conducted by a single reviewer (see Screening Reliability and Extraction Reliability). The organizational strand is staffed differently: two research assistants work on that strand alongside the lead reviewer, and the division of coding responsibility between them is specified under Screening Reliability. Where a coder is an author of a record under assessment, they will recuse themselves from that record, and screening and charting of it will be carried out by another member of the research team who is not an author of it. Every recusal will be logged in the screening and extraction logs, identifying the record and the substituting coder, and reported with the review.

In the literature strand, should no unconflicted team member be available for a given record, the record will be retained and its coding flagged as author-conflicted in the shared dataset. This fallback does not apply to the organizational strand, where the two research assistants are always available as unconflicted coders; conflicted organizational records are handled by the procedure registered under Conflicts of Interest, which governs in case of any apparent conflict between the two fields.

Recusal is not applied to synthesis, which is holistic and thematic rather than record-by-record; conflict at the synthesis level is addressed through the peer debriefing registered under Synthesis Reliability.

---

# Search strategy

*In this section, you register your search strategy: the procedures you designed to obtain all (potentially) relevant sources to review (e.g., articles, books, preprints, reports, case law, policy papers, archived documents).*

## Databases

Primary citation index for citation chasing: OpenAlex. Keyword search for seed identification: Google Scholar. Preprint repositories: arXiv and SSRN.

Two further services are used in bounded roles and neither contributes to the corpus or to the citation edge list. Crossref is used for metadata validation only — DOI resolution and field cross-checking — and for retraction screening alongside Retraction Watch. Semantic Scholar is used solely as the comparator index for the index-sensitivity check registered under Sensitivity analyses.

## Interfaces

Unlike aggregator interfaces (Ovid, EBSCO), these databases are searched through their own native interfaces/APIs: OpenAlex via the OpenAlex API and, where supported, the citationchaser R package; Google Scholar via the Google Scholar web interface; arXiv via the arXiv website/API; SSRN via the SSRN website. Where the expansion is run against a dated OpenAlex data snapshot rather than the live API, the snapshot date is recorded and reported. Research Rabbit was used in preliminary exploratory work and is retained only as a supplementary discovery tool, not as the search of record.

## Grey literature

Grey literature is eligible and actively sought, because a substantial part of the public-interest-technology tradition is published as reports rather than articles. Strategies:

(a) preprints via arXiv (cs.CY, cs.AI, cs.CL, cs.HC) and SSRN;
(b) foundation and organizational reports/white papers (e.g., New America, Ford Foundation, Knight Foundation, mySociety, Freedman Consulting) located through targeted website searching and through citation chasing;
(c) theses and dissertations via institutional repositories (DSpace) and ProQuest;
(d) conference proceedings (ACL Anthology, ACM Digital Library, IEEE Xplore, AAAI) captured via citation chasing.

## Inclusion and exclusion criteria

**Framework:** Population–Concept–Context (PCC), per JBI scoping-review guidance.

- **Population:** actors involved in TPG — technologists, academics, practitioner and partner organizations, governments, and communities.
- **Concept:** TPG and its three constituent traditions (public interest technology, civic technology, and the "for good" tradition), and how each is defined and practiced.
- **Context:** English-language sources; no geographic restriction; no date restriction.
- **Types of sources:** peer-reviewed articles, conference proceedings, books and chapters, theses, and influential grey literature.
- **Inclusion:** work that substantively engages one of the three traditions or the public-good orientation of technology.

**Exclusion.** A record is excluded as soon as any of the following is met (the reason is logged for the PRISMA-ScR flow):

1. Not English-language.
2. Not relevant to technology for the public good (TPG) — does not substantively engage any of the three traditions (public interest technology, civic technology, or the "for good" tradition) or the public-good orientation of technology (e.g., corporate social-responsibility, green-finance, or general AI/ML work with no public-good focus).
3. Ineligible source type — not a scholarly work (journal article, conference paper, book/chapter, thesis) or an influential grey-literature report/white paper (e.g., news items, blog posts, promotional or marketing pages).
4. Duplicate of a record already included.
5. Preprint superseded by a published version (the published version is retained).
6. Retracted. Applied at full-text screening and at any later point at which a retraction notice is identified. A record retracted after charting is removed from the analytic corpus and the removal is counted and reported. An expression of concern is not a retraction: such a record is retained and flagged in the shared dataset.

Records whose full text cannot be obtained are recorded as "not retrieved" rather than excluded.

### Organizational strand eligibility

Candidate organizations are identified through a frozen register of sampling frames (attached to this registration), not through open searching. Eligibility is determined by five pass/fail criteria applied in order, with each exclusion logged against the first criterion failed:

**C1. Organization-level unit.** The candidate has its own name, its own web presence, and evidence of staffing or governance. Where a frame listing cannot be resolved to any organization at all — a project name with no organization behind it, a dead link, an entry that proves to be a page on another organization's site — the record is coded `unresolvable` rather than failed, and the count is reported. This is distinct from `unit_unresolved` under the unit-resolution rule below, which applies where an institution is identified but the frame names no unit within it.

**C2. United States.** Headquarters or principal operations are in the United States. Where a frame's own location metadata is absent or unreliable, location is determined from the organization's own materials rather than from the frame.

**C3. Constitutive technology.** Removing the technology from the organization's work, does the core activity survive? An organization for which it does — one that uses technology as internal or operational infrastructure, or that receives technology work performed by others — fails this criterion.

**C4. Public benefit.** The intended beneficiary is the public rather than the organization's own members or industry. For-profit entities qualify only on structural commitment evidenced in incorporation status or a governing document — public-benefit corporation status, B-Corp certification, or an equivalent commitment recorded in articles or bylaws. A mission statement, values page, or impact-marketing claim is not sufficient on its own.

**C5. Funder program.** Applies to funders only: the funder maintains a named technology program or portfolio as a primary activity. Not applicable to non-funders.

Recent activity is deliberately not a criterion. Organizational status — active, dormant, or closed — is coded as a variable with a date and a dated evidence artifact. Gating on activity would remove dormant and closed organizations from the sample, biasing results toward survivors and making claims about field dynamics impossible; coding it preserves those records and converts survivorship into a sensitivity analysis.

Two standing rules govern every frame.

**Unit resolution.** Where a frame lists an institution rather than an organization — a university, a government agency, a corporate parent — the record resolves to the unit or units the frame itself names, whether through a designated representative's stated affiliation, a program or center in the frame's own listing, or a project the frame has funded or profiled. That unit is the unit of analysis; the parent institution does not enter the sample. Where the frame names no unit, the record is logged as unresolved, excluded from full coding, and counted. Where a coder is independently aware of a qualifying unit that the frame does not name, that unit is not added on the coder's initiative; it is logged, counted, and available for a sensitivity check. Where a frame names a fiscal sponsor rather than the sponsored project, the record resolves to the sponsored project if the frame names it and it meets C1 independently, and otherwise to the sponsor, with the routing recorded; both are never entered as separate records.

**Frame operators.** Every organization that operates, convenes, or publishes a frame used in this study enters the candidate pool by construction, independent of whether it appears in any frame's own listings. Frame operators are screened on C1 to C5 and coded on the full instrument like any other record, and are flagged as operators with the frames they operate recorded. They are reported separately and excluded from every within-block rate and saturation count, because their inclusion is guaranteed rather than sampled.

Coding is based solely on public and self-reported information. The access date and source URL are recorded for every organization. An archived capture is made of every frame source page on its freeze date, and of every page supporting a coded self-label, a non-lexicon self-description, or a status determination. Pages consulted but not relied upon for a coded value are recorded by URL and access date without an archived capture, because archiving every page consulted across the enumerated pool is not achievable within the archiving services' rate limits.

## Query strings

Two identification routes.

**(1) Seed identification (Google Scholar):** seven keyword queries, one per concept, with the "for good" tradition split into five sub-queries to capture its label variants:

1. "civic technology"
2. "public interest technology"
3. "tech for good" OR "technology for good" OR "data for good" OR "data science for social good"
4. "AI for social good" OR "artificial intelligence for social good" OR "AI for good" OR "AI for social impact"
5. "machine learning for social good" OR "NLP for social good" OR "computing for social good"
6. "AI4SG" OR "AI4SI" OR "DSSG" OR "NLP4SG" OR "D4G"
7. "generative AI for social good" OR "agentic AI for social good" OR "conversational AI for social good"

**(2) Citation-network expansion (OpenAlex):** not a Boolean query — the "query" is the identifier list of the 23 frozen seed articles, from which the tool retrieves backward references and forward citations. Twenty-two seeds are identified by DOI; seed 20 (CEUR-WS proceedings) carries no DOI and is identified by its OpenAlex work ID, recorded in the frozen seed file. Where a seed's citation neighbourhood is unavailable or materially incomplete in the index, that fact is recorded per seed and reported alongside the leave-one-out sensitivity check.

## Search validation procedure

Yes. We validate the strategy against a pre-specified set of known landmark works that any adequate search must recover. The set is recorded in an attachment to this update and frozen on filing, so that it falls under the assurance that no stage of the protocol had been executed. No work in the validation set is among the 23 frozen seeds, and no work in the set may be added to the seed set at any point during the review: a seed is removed from the candidate pool at deduplication as already included, so its non-appearance in the pool is an artifact of that step and carries no information about search adequacy. The check is run against the pre-deduplication pool, so that recovery is assessed before seeds are removed.

Each work is recorded with the arm of the search it tests. Most test the citation-network expansion. At least two are grey-literature items testing the targeted hand-searching of venue and organization websites, and are assessed against that arm rather than against the expansion, because a grey-literature report absent from the citation index would otherwise register as a non-recovery of a kind that does not bear on search adequacy and would test nothing.

The pass criterion has two parts, because the set tests two arms.

For the works testing the citation-network expansion, non-recovery is recorded and reported in every case, and revision is not automatic. We first establish whether the work is (a) absent from the index, (b) present in the pool but excluded at screening, or (c) present in the index but unreachable from any seed's citation neighbourhood, and we report which. Only (c) bears on search adequacy. Where two or more of these works fall into (c), we add a targeted query rather than alter the seed set, because the seed set is the frozen input to the expansion and altering it changes the corpus definition; any addition is documented in a preregistration update before the full run. The threshold is two rather than one because a single unreachable work can reflect that work's own citation profile, whereas two independently unreachable works indicate a systematic gap; it is an absolute count and does not move with the size of the counting subset. Arnstein (1969) is recorded in the set but excluded from this count, because it is the analytic framework's own source and its recovery is close to guaranteed by backward chasing from the civic technology seeds; its recovery is reported separately. At least five works count toward this part of the criterion.

For the grey-literature works testing the hand-searching arm, cause (c) does not apply, because unreachability from a citation neighbourhood is not a question that can be asked of a work assessed against hand-searching. The question is instead whether hand-searching the venue or organization that published the work surfaced it. Non-recovery indicates that the hand-searching arm lacks the coverage the protocol assumes rather than that the expansion is inadequate; we record which venues and organizations were searched, add those that were not, and report the addition.

## Other search strategies

The core method is a constrained snowball (Lecy & Beatty, 2012) combining the ascendancy approach (backward reference chasing) and the descendancy approach (forward citation chasing via OpenAlex/Crossref) from the frozen seeds, iterated on records that pass relevance screening until saturation. We supplement with targeted hand-searching of key venue and organization websites for grey literature.

**Organizational strand.** Practitioner organizations are not identified by searching. They are enumerated from a frozen register of sampling frames attached to this registration, under boundary definitions recorded in that register, and screened against the criteria given under Inclusion and exclusion criteria. The enumeration procedure, the frames, and the sampling logic are specified under Sampling and sample size. No keyword or database searching is used to identify candidate organizations, and organizations encountered incidentally during the literature search do not enter the organizational candidate pool.

## Procedures to contact authors

We do not plan to contact authors. The review synthesizes published and publicly available texts and does not require unpublished data or clarification from authors. (Data for the parallel organizational strand are drawn from organizations' public and self-reported information, not from author correspondence.)

## Results of contacting authors

Not applicable — no author contact is planned.

## Search expiration and repetition

Given the rapid growth of the literature, we set a search expiration of 12 months. If more than 12 months elapse between the search and final submission, we will re-run the citation-network expansion from the frozen seeds and report any newly included records. This is not registered as a living review, so no fixed repeated-search cadence is planned beyond the expiration refresh.

## Search strategy justification

Keyword-only searching is inadequate here because the field's defining problem is terminological fragmentation: work on the same practice is indexed under incompatible labels, so any single vocabulary systematically misses cross-tradition material. A seed-based citation-network search bridges those vocabularies by following references and citations rather than terms. We use OpenAlex as the search of record rather than Research Rabbit because it provides an open, broad-coverage and reproducible index with transparent, exportable, date-stamped forward and backward chasing, whereas Research Rabbit's recommendations are algorithmic and not reproducibly auditable. We use OpenAlex rather than Lens.org because its data are CC0 and therefore redistributable under the open licence this registration commits to, because its full dataset is published as a dated snapshot that fixes the index state, and because its access terms do not depend on a subscription the team may not hold; the choice is not a claim about relative coverage or data quality. English-only and the grey-literature inclusion are pragmatic scope decisions balancing coverage against feasibility; grey literature is retained because it is central to the PIT tradition. We do not contact authors because the aim is to map published conceptualizations, not to obtain new data. The 12-month expiration reflects how quickly the AI end of the field is moving.

## Miscellaneous search strategy details

The 23-article seed set is frozen and attached to this registration and is the sole input to the citation-network expansion; the preliminary corpus assembled during exploratory work is set aside and not carried forward. The attached seed file was revised on 9/16/2026 to correct transcription and formatting errors identified by verifying every record field by field against its source; the revision log accompanying the file records each correction, and the 23 works identified are unchanged. Both the original and revised files remain available on the OSF project. Different citation indices have genuinely different coverage, so the resulting corpus is partly a function of the chosen index; this is acknowledged as a limitation.

Three properties of the seed set are recorded here because they shape the corpus.

First, three seeds are preprints and one is CEUR-WS proceedings. The frozen identifier remains the input to the expansion for the duration of the review regardless of subsequent publication. Where a seed is published during the review, the publication is recorded in the seed file with its date and identifier, the published version is treated as the citable form in the write-up, and whether the index merges the preprint and published records is checked and reported; where it does not, the forward-citation set retrieved from the frozen identifier is reported as incomplete for that seed and its leave-one-out result is read against that fact. The seed set is not re-frozen and no seed is substituted.

Second, the seed set comprises 6 civic technology, 7 public interest technology and 10 "for good" works. Because the corpus is generated from the seeds by citation chasing, this composition shapes the distribution the descriptive map reports; the consequence is registered under Synthesis plan and Publication bias analyses.

Third, three seeds are recent enough that forward citation chasing will return little or nothing from them: seed 13 (August 2025), seed 22 (March 2026) and seed 23 (May 2026) — a different three from the preprint seeds noted above, overlapping with them at seeds 13 and 23. For those seeds the expansion is effectively ascendancy-only. This interacts with the composition above, because the "for good" tradition holds both the largest share of seeds and the most recent ones, so its coverage will be broader backward than forward. The seed file carries a *Forward-chase viability* column recording this per seed in advance, and per-seed forward and backward yields are recorded at the Search stage and reported, so that a seed contributing in only one direction is visible rather than assumed symmetric.

---

# Screening

*In this section, you register your screening procedure: the procedure you designed to eliminate all irrelevant sources from the results of the search strategy (and retain the relevant sources).*

## Screening stages

**Deduplication (pre-screening).** Pooled records from the citation-network expansion and keyword searches are de-duplicated by DOI and normalized title; the 23 frozen seed articles (already included) are removed from the candidate pool; and where a preprint and its published version both appear, the preprint is removed in favor of the published version. Deduplication is performed computationally (a script / reference-manager routine) with a human check of near-duplicates.

**Pilot screening and AI validation.** Before the full run, a calibration sample of approximately 100 records is screened by a human, blind to the AI, and independently by the AI-assisted procedure described below. Human and AI decisions are compared to estimate the AI's recall/sensitivity (primary) and specificity and to surface systematic error patterns. Recall is reported with its confidence interval, and the number of human-includes in the calibration sample is reported alongside it, so that a recall figure resting on few positives is visible as such. Where fewer than 25 records in the calibration sample are human-includes, the sample is extended to a maximum of 250 records in total; if 25 human-includes have not accumulated by then, recall is assessed on what has accumulated and reported with its confidence interval and denominator stated. The full AI-assisted run proceeds only if measured recall meets a pre-specified threshold of ≥95%; otherwise the prompt and criteria are revised and the pilot repeated. Validation results and any revisions are recorded in a preregistration update.

**Stage 1 — title/abstract screening (computer recommendation, human-verified).** Titles, abstracts, and keywords are screened together (as is standard for scoping reviews). For each record, a large language model (Claude Opus 5) is prompted with the exclusion criteria and returns a recommended include/exclude decision with a brief rationale. A human reviewer verifies every recommendation. Because a missed eligible study is costlier than a wrongly retained one, the human applies heightened scrutiny to AI "exclude" recommendations, and any AI–human disagreement is resolved in favor of retention to full text ("when in doubt, keep in"). The AI makes no autonomous exclusions; the human retains final decision authority on every record. Both the AI recommendation and the human decision are logged for each record.

**Stage 2 — full-text screening (human).** Full texts are retrieved for records passing Stage 1 and assessed against the exclusion criteria by a human reviewer. The AI generates supporting summaries but does not make decisions at this stage. Exclusions are logged with a reason; records whose full text cannot be obtained are recorded as "not retrieved" (distinct from excluded) in the PRISMA-ScR flow.

Screening decisions are human-authored throughout; AI is used only as a verified recommender at Stage 1.

## Screened fields / blinding

No fields are blinded. Title, abstract, keywords, authors, publication venue, and year are all visible to the human reviewer; the AI recommender is supplied the title, abstract, and keywords together with the exclusion criteria. Blinding is not applied because (a) scoping reviews do not require it; (b) the meta-narrative synthesis explicitly uses venue, discipline, and author community to assign each source to a research tradition, so those fields are analytically necessary; and (c) with a small team, meaningful blinding is not feasible. We acknowledge that visible venue and author information could introduce prestige bias, and we mitigate this by applying explicit, piloted exclusion criteria consistently and by retaining borderline cases for full-text assessment.

## Used exclusion criteria

A record is excluded as soon as any of the following is met (the reason is logged for the PRISMA-ScR flow):

1. Not English-language.
2. Not relevant to technology for the public good (TPG) — does not substantively engage any of the three traditions (public interest technology, civic technology, or the "for good" tradition) or the public-good orientation of technology (e.g., corporate social-responsibility, green-finance, or general AI/ML work with no public-good focus).
3. Ineligible source type — not a scholarly work (journal article, conference paper, book/chapter, thesis) or an influential grey-literature report/white paper (e.g., news items, blog posts, promotional or marketing pages).
4. Duplicate of a record already included.
5. Preprint superseded by a published version (the published version is retained).
6. Retracted. Applied at full-text screening and at any later point at which a retraction notice is identified. A record retracted after charting is removed from the analytic corpus and the removal is counted and reported. An expression of concern is not a retraction: such a record is retained and flagged in the shared dataset.

Records whose full text cannot be obtained are recorded as "not retrieved" rather than excluded.

## Screener instructions

These instructions govern the literature strand. Screening and coding in the organizational strand are carried out by three coders under the division of labour, calibration procedure, and AI roles registered under Screening Reliability, and recusal there follows Conflicts of Interest rather than the authorship rule below.

The human reviewer is instructed to:

1. apply the exclusion criteria in the order listed and exclude a record as soon as one is met, recording the reason;
2. treat the AI recommendation as advisory only and independently verify every AI decision, giving extra scrutiny to any AI "exclude" recommendation to avoid dropping eligible studies;
3. resolve any AI–human disagreement in favor of retention to full text ("when in doubt, keep in");
4. at Stage 1, exclude only on clear grounds and retain any record whose TPG-relevance is uncertain;
5. judge relevance to TPG by whether the work engages one of the three traditions or the public-good orientation of technology, per the PCC concept definition;
6. recuse themselves from any record they have authored, per Overlapping Authorships, and log the recusal; and
7. log, for every record, the AI recommendation, the human decision, and any exclusion reason.

*No files selected.*

## Screening reliability

**Literature strand.** This is a single-human-reviewer, AI-assisted design. Stage 1 (title/abstract): two agents contribute — a large language model that recommends a decision and a human who verifies it. Independence is preserved at the validation step: on the pilot calibration sample of ~100 records, the human screens blind to the AI's output, and we compute human–AI agreement as percentage agreement and Cohen's κ, alongside the AI's recall/sensitivity and specificity. In the full run, the single human verifies all AI recommendations (not blind, by design). Stage 2 (full-text): screened by a single human reviewer. We declare that, apart from the AI-recommender step and the blinded pilot, full-run screening is conducted by one reviewer; this is acknowledged as a limitation.

**Organizational strand.** This strand is coded by three people — the lead reviewer and two research assistants — with AI assistance in three defined roles. Responsibility is specified per field below, so that for every field it is fixed in advance who proposes a value, who decides it, and who checks it.

The governing constraint is that AI never precedes independent human judgment on a judgment-dependent field. If both research assistants saw the same AI recommendation before coding, their codings would be correlated through it, and the human-to-human agreement statistic would measure the model's persuasiveness rather than the reliability of the instrument.

**Group 1 — Mechanical fields.** Enumeration from the frozen frame snapshots; deduplication candidates; C1 (organization-level unit); C2 (United States); status and its dated evidence artifact; ecosystem role; named partner organizations; and the descriptive fields.

> *Proposed by:* the AI model (Role 1), which returns a value together with the supporting passage. *Decided by:* one research assistant, who verifies every proposal against the source and accepts, corrects, or records the field as undetermined. No proposal is accepted without the source being opened. *Checked by:* the lead reviewer, on a random ten per cent of records in each block, comparing the recorded value against the recorded evidence. The error rate found is reported, as is the rate at which assistants corrected or overrode the model.

**Group 2 — Self-label and non-lexicon description fields.** The verbatim self-applied phrase; the lexicon term matched; the URL and access date; the placement of the phrase; the speaker (whether the organization is describing itself or quoting a funder, partner, or news source); non-lexicon self-descriptions recorded verbatim; and the tier assignment that follows from them.

> *Proposed by:* the AI model (Role 2), which returns candidate passages with their exact character span, URL, and section of the page, and proposes no value for any field in this group. *Decided by:* one research assistant, for every field in the group. Whether a phrase is categorial, what its placement is, who the speaker is, and what tier follows are human judgments throughout, because each depends on features of the page a text match cannot establish. The model locates; the human judges. *Checked by:* the lead reviewer, on the same random ten per cent as Group 1. Tier is additionally re-derived from the recorded phrase, placement, and speaker for every record, so that a tier assignment inconsistent with its own evidence is caught rather than relied upon.

**Group 3 — Judgment-dependent fields.** C3 (constitutive technology), C4 (public benefit), C5 (funder program), and the four framework dimensions.

> *Coded by:* both research assistants, independently, for every record. These fields are double-coded in full, not on a sample. *Decided by:* the lead reviewer, who adjudicates every disagreement, except on author-conflicted records, where the disagreement is reported unadjudicated (see Conflicts of Interest). *Also coded by:* the AI model (Role 3), independently and blind. Its output is withheld from both assistants and from the lead reviewer until the adjudicated human value has been recorded, and it never contributes to a coded value. It supports a separately reported human-to-AI agreement statistic and a targeted review pass over records where the model disagrees with both human coders or where all three diverge.

C3 and the framework dimensions are the fields most exposed to judgment drift, and the framework dimensions were unanswered across the whole prior exploratory collection, which is why they are piloted and revised before scaling and are never coded by a single person. Who decides is expected to be the most frequently undetermined of the five, and its undetermined rate is reported per block alongside its agreement statistic.

**Calibration and training.** Before any record is coded for the analytic dataset, the three human coders independently code a shared calibration set of approximately twenty organizations drawn across all three blocks. Coding is discussed, the codebook and field wording are revised where the disagreement is attributable to the instrument rather than to the coder, and the calibration is repeated on a fresh set. Calibration records are not part of the analytic dataset. The AI roles are validated against the adjudicated calibration values before any analytic record is processed (see Extraction Reliability).

**Ongoing reliability.** Because Group 3 fields are double-coded in full, agreement between the two assistants is computed over all coded records rather than over a subsample. It is recomputed and reported at the midpoint and at the end of the coding period as well as at calibration, so that drift over time is visible rather than assumed absent.

**Uncertainty is recorded, not resolved by guessing.** Any coder who cannot determine a field from the available evidence records it as undetermined with a note, and the record is routed to adjudication rather than assigned a value. A field left undetermined after adjudication is reported as such; the proportion of undetermined values per field is reported with the results, because a field that is frequently undetermined is a finding about what organizations disclose rather than a gap to be filled.

**Guardrails on AI use.** Verbatim fidelity is enforced programmatically rather than trusted: any phrase the model returns as extracted text must appear as an exact substring of the fetched page text, and extractions failing that check are rejected automatically and the field routed to a human. The model is instructed to return undetermined where evidence is absent, and model confidence never substitutes for evidence. No AI is used in the inductive coding of non-lexicon self-descriptions (see Synthesis plan): that step exists to surface vocabulary the frozen lexicon does not contain, and a model grouping the phrases would impose the prior vocabulary the step is designed to escape. Categories are constructed by human coders working independently; a model may be used afterwards to organize already-coded excerpts, which is a non-decisional use disclosed under Miscellaneous synthesis details. The lexicon proxy that stratifies the coding queue is deterministic pattern matching against the frozen lexicon, not a model, and is not an AI role.

Contributor roles for all three coders will be reported using the CRediT taxonomy.

## Screening reconciliation procedure

AI–human divergence (Stage 1 full run): resolved by the human in favor of retention to full text ("when in doubt, keep in"); the human decision governs, and no record is excluded on the AI's recommendation alone. Pilot disagreements: examined qualitatively to identify systematic error patterns and to refine the AI prompt and exclusion criteria before the full run (recorded in a preregistration update). Because full-run screening uses one human reviewer, no inter-human reconciliation applies; the only divergences reconciled are AI–human, resolved as above.

## Sampling and sample size

**Literature strand.** We will retain all sources that pass screening; we do not sample from them. Because this is a descriptive and interpretive review, not a hypothesis-testing study of an association, no statistical power analysis or minimum sample size applies. The one place a floor matters is the meta-narrative synthesis: if any tradition yields too few sources for a robust narrative, we will report it descriptively, temper our claims for that tradition, and flag the sparsity as a finding rather than over-interpret.

**Organizational strand: frame register.** Organizations are identified through a frozen register of frames arranged in three blocks, one per tradition. Each frame is a vehicle through which organizations of that tradition identify themselves or are selected.

- **Block A (public interest technology)** comprises the PIT University Network member roster and the Ford Foundation Technology and Society grantee portfolio.
- **Block B (civic technology)** comprises the United States organization listings of the Civic Tech Field Guide, the Alliance of Civic Technologists member list, and the archived Code for America brigade roster, the last of which is a historical frame supporting the closure and field-dynamics analysis.
- **Block C ("for good")** comprises the Fast Forward portfolio, the Patrick J. McGovern Foundation grantee listing, and four named Google.org cohorts: the 2019 AI Impact Challenge, the 2025 Google.org Accelerator: Generative AI, and the 2026 Impact Challenge cohorts for AI for Government Innovation and for AI for Science.

Google.org does not maintain a standing portfolio, so the frame is defined as the union of these four cohorts, named here, rather than as a live listing; cohorts other than these four do not enter the frame regardless of when they are announced. Where a named cohort's participant list is not yet published at the freeze date, that cohort is recorded as pending and enumerated when its list is published, with the enumeration date recorded separately from the frame freeze date; if it remains unpublished at the close of coding, it is reported as unenumerated and the frame is analyzed without it. The 2019 cohort is included to give Block C a historical arm comparable to the archived brigade roster in Block B; because it is seven years old, its organizations are expected to show a substantially higher rate of dormant and closed status than the later cohorts, and status is therefore reported by cohort rather than pooled across the frame. Each frame is enumerated in full from an archived snapshot captured on its stated freeze date, under a boundary definition recorded in the frame register; where a source is version-controlled, the frame is pinned to a specific commit rather than a date.

**What this update fixes, and what follows it.** This update fixes the composition of the register — which frames are in it, which are excluded and why — together with each frame's enumeration route and boundary definition, the standing rules, the screening criteria, the draw rule, and the stopping rule. It does not fix the contents of any frame, because no frame has yet been captured. Snapshot capture, enumeration, and all subsequent stages follow the freezing of this update. A single freeze date is set for the register after filing and before any enumeration; it is recorded in the frame register, and the snapshots and their capture dates are deposited in the OSF project for this registration at that point. The freeze date is chosen without reference to the contents of any frame, and no frame is inspected between the filing of this update and the freeze beyond what is needed to confirm that its listing is reachable.

No frame in the register was selected on the basis of gap analysis against the prior exploratory collection, and no frame was selected in order to reach organizations that collection had missed. The "for good" block contains no identity-type frame because no United States membership roster for that tradition was located before registration; this is a property of the frame register as constructed and is treated as a finding rather than as a prediction (see Expectations).

Blocks are the unit of balance; frames within a block are not assumed equivalent, and no claim rests on the blocks being of equal size.

**Admission mechanism.** Each frame is typed by how an organization enters it: self-declaration (an identity roster), selection (a funder portfolio or accelerator cohort), or affiliation (a coalition). This is recorded per record, because it is a confound the analysis must hold rather than ignore.

**Screening and sampling.** Screening proceeds in two passes. The first pass applies C1 and C2 to every enumerated record. These are the criteria that can be resolved from a frame listing and a brief check of the organization's own site; they are not uniformly inexpensive, because where a frame's location metadata is missing, C2 requires an individual determination from the organization's materials, and for the largest frame this applies to several hundred records. The second pass applies the judgment-dependent criteria (C3, C4, C5) and the full instrument to sampled records.

**Draw rule.** Records that pass the first pass enter a coding queue whose order is fixed in advance, so that the point at which sampling stops does not depend on the order in which coders happen to open records. Within each block, records are stratified two ways: by originating frame, and by a lexicon proxy indicating whether any frozen lexicon term appears in the text of the organization's own homepage. The proxy is computed by an automated text match at enumeration and recorded as a separate field. It is explicitly **not** the tier assignment: tier is a coded judgment requiring the placement of the phrase and the identity of the speaker, made later by a human, and the proxy is neither used as tier nor reported as tier. Its only function is to order the queue. Records surfaced by more than one frame are assigned to the stratum of the frame that surfaced them first in the register's stated order, and the multi-frame provenance is retained in the data.

Records are drawn in round-robin rotation across the strata of a block, at random within each stratum, using a recorded seed. Where a stratum is exhausted the rotation continues over the remainder. This guarantees that the six-record saturation window always spans strata rather than sitting within a single frame or a single side of the lexicon proxy, so saturation means that nothing new is appearing anywhere in the block rather than that one frame has been worked through. It also guarantees that organizations whose homepages carry no field vocabulary are reached before sampling can stop; those organizations are where blur across traditions is most likely to be visible, and a queue that could exhaust itself before reaching them would undercut the expectation the strand exists to test.

Sampling within a block continues until six consecutively coded organizations in that block produce no new code on any of the five framework dimensions. Saturation is assessed per block, not globally, and the count resets whenever a new code appears. An undetermined value neither resets the count nor counts toward the six, because it records that the available evidence does not reach the question rather than that the dimension has ceased to yield new answers; counting it would allow a block to terminate on absence of disclosure rather than exhaustion of variety. Records excluded at the second screening pass do not count toward the six, because a record that fails C3, C4, or C5 is never coded on the framework dimensions and so cannot bear on whether new codes are appearing; frame-operator records likewise do not count, because their inclusion is guaranteed rather than sampled. The saturation point reached in each block, the number of organizations coded to reach it, the number of undetermined values encountered on each dimension, and per-frame yield are all reported.

Ecosystem role is coded on the full instrument as registered but does not enter the saturation criterion. It is a closed controlled list rather than a rubric constructed at calibration, so it registers the first appearance of a fixed value within a block rather than the emergence of a new code, and it is exhausted early in every block while remaining capable of resetting the counter on a record whose framework-dimension answers are already familiar.

Where a block exhausts its frames before reaching the stopping rule, the block is reported as exhausted, with the number of organizations coded and the state of the saturation counter at exhaustion, and the exhaustion is treated as a finding about that tradition's organizational density. Frames are not added mid-collection to compensate.

The threshold of six is set in advance and is not revised after coding begins. It is lower than would be appropriate for a single coder because the judgment-dependent fields are independently double-coded and adjudicated (see Screening Reliability), so a new code appearing in a single coder's judgment alone does not reset the counter; only an adjudicated new code does.

**Boundary audits.** Where a frame's own metadata is used to define the frame boundary, the cost of that boundary is measured rather than assumed. For the Civic Tech Field Guide, whose boundary uses the directory's own record-type field, two audit samples of 100 records each are drawn — one from United States records not typed as organizations, one from United States records with no type recorded — using a random draw with a recorded seed, and screened against C1. The resulting pass rates, with confidence intervals, are reported as a bound on the frame's completeness. The audits are run to their full sample size regardless of interim results.

**Out of scope.** No population-level proportion, coverage estimate, or rate over any population beyond the frame set is reported. Frame composition sets the denominator for every count this instrument produces, so such claims would not be interpretable, and the design gives them up explicitly rather than reporting them with caveats.

**Non-frame probe.** One supplementary probe is conducted, not optional. When coding is complete, all organizations named in the `partner_orgs_named` field of included records that are not themselves in the candidate pool are assembled, and 50 are drawn at random with a recorded seed and coded on the label fields only. Its sole purpose is to check whether organizations reached by no frame use the same non-lexicon vocabulary as those inside the frame set. It is not a coverage instrument and carries no denominator; no rate over any population is computed from it. If fewer than 50 such organizations exist, all are coded and the number is reported.

No statistical power calculation applies. The four framework questions are piloted and revised before sampling begins, because preliminary work indicates they are difficult to answer as currently worded. This pilot is the same exercise as the coder calibration described under Screening Reliability, not an additional round: the questions are revised between the first and second calibration rounds, and the revised wording is the one carried into coding.

## Screening procedure justification

The two-stage design (title/abstract, then full text) is the standard, efficient approach that balances recall against workload. AI-assisted Stage 1 screening with mandatory human verification is justified by the potentially large candidate pool a citation-network expansion produces: it reduces reviewer workload while keeping decision authority with the human, and it is validated against blind human screening on a pilot before use (per RAISE). We do not blind bibliographic fields because scoping reviews do not require it and because the meta-narrative synthesis depends on venue, discipline, and author community to assign traditions; we mitigate the resulting prestige-bias risk with explicit, piloted criteria and by retaining borderline cases. Exclusion criteria follow directly from the PCC eligibility definition and are applied conservatively on relevance. Reliability is assured primarily through AI-validation against a blinded human pilot rather than full dual-human screening — a pragmatic choice for a small team, acknowledged as a limitation. Reconciliation always favors retention because, in evidence synthesis, a missed eligible study (false negative) is costlier than a wrongly retained one (false positive).

## Data management and sharing

We will openly share, on the OSF project for this registration:

(a) the full set of records identified through the searches, in BibTeX/RIS and CSV/XLSX;
(b) the screening log, recording for every record its AI recommendation, the human decision, the screening stage, any exclusion reason, and any author-conflict recusal, in CSV/XLSX;
(c) the frozen 23-article seed list;
(d) the final charted dataset; and
(e) for the organizational strand, the frozen frame register with each frame's enumeration route, boundary definition, and archived snapshot reference; the organizational screening log with the first criterion failed for every exclusion; the final organizational dataset with its codebook; and the reproducibility materials for the sampling procedure — the random seeds used for the draw rule, the boundary audits, and the supplementary probe, the resulting coding-queue order, and the script and frozen lexicon used to compute the lexicon proxy; and the organizational strand's AI materials — the model and version, the frozen prompts for each of the three roles, and the per-field log of every AI proposal against the human decision recorded for it, including the blind third coder's output, which is released with the dataset after adjudication is complete.

Files will be shared under CC-BY 4.0 with no embargo.

Where a frame's own data are redistributed rather than merely used to identify candidates, the source's license is checked for compatibility with CC-BY 4.0 before redistribution, and any frame whose license is incompatible is cited rather than redistributed.

## Miscellaneous screening details

**AI-use disclosure (per RAISE, Responsible AI in Evidence Synthesis, 2025).** We will use a large language model, Claude Opus 5, accessed via API with a fixed, archived prompt and default temperature settings, to recommend include/exclude decisions during title/abstract screening. It will be used as decision support only: every recommendation will be verified by a human reviewer who retains final authority, and the model will make no autonomous exclusions. Before the full run, we will validate it against blinded human screening on ~100 records and will report its recall/sensitivity and specificity; the full run will proceed only if recall meets our pre-specified threshold of ≥95%, and otherwise we will revise the prompt and criteria and repeat the pilot. No AI tool will be used for data extraction beyond the roles specified in the Extraction section, or for quality appraisal or synthesis decisions.

**Organizational strand AI-use disclosure (per RAISE, 2025).** An AI model assists the organizational strand in three defined roles, specified under Screening Reliability: first-pass extraction on mechanical fields with every proposal human-verified; evidence location for the self-label block, with all judgment reserved to the human coder; and a blind third coder on the judgment-dependent fields whose output is withheld until the adjudicated human value is recorded and which never contributes to a coded value. The model proposes outcomes for the two cheap screening criteria, C1 and C2, as part of Role 1, and a research assistant verifies every such proposal against the source; no record is included or excluded on a model proposal alone, and the model plays no part in the judgment-dependent criteria C3, C4 and C5 beyond the blind third coding of Role 3, which is withheld until the human value is adjudicated. The model does not assign tier, does not adjudicate disagreements, and is not used in the inductive coding of non-lexicon self-descriptions. The model and version, and the exact prompts for each role, are recorded with the codebook and shared with the review; prompts are frozen before the analytic dataset is coded and any revision is versioned and reported. The lexicon proxy that stratifies the coding queue is deterministic pattern matching against the frozen lexicon rather than a model.

---

# Extraction

*In this section, you register your plans for data extraction: the procedures you designed to extract the data you are interested in from the included sources. Examples of such data are text fragments, effect sizes, study design characteristics, year of publication, characteristics of measurement instruments, final verdicts and associated penalties in a legal system, company turnovers, sample sizes, or prevalences.*

## Entities to extract

**Literature strand.** From each included source we will extract (as a chart):

1. **Metadata** — authors, year, title, publication venue, and publication/source type (journal article, conference paper, book/chapter, thesis, grey-literature report).
2. **Tradition assignment** — the primary tradition the source belongs to (public interest technology, civic technology, the "for good" tradition, or adjacent/foundational).
3. **Faceted classification** — disciplinary home; application domain; and normative lens (per the project's coding scheme).
4. **Source role/type** — e.g., survey/review, definitional/conceptual, empirical, critical/position.
5. **The five framework dimensions** (derived from Arnstein's ladder) — who participates; who benefits; what is meant by social good; who decides; and what counts as relevant technology.
6. **The source's own definition of its key term** (e.g., how it defines "civic tech" / "public interest technology" / "for good"), extracted verbatim where stated.
7. **Meta-narrative elements** (qualitative fragments/themes) — the source's stated origins/paradigm, exemplars it treats as canonical, methods it uses, and how it defines "the good."
8. **Citation data** — the source's references and citing works, used to compute within- vs. cross-tradition citation for the silo analysis.

Fields not addressed by a source are charted as "not reported."

**Organizational strand.** Each organization is coded on its own instrument, recorded in the codebook attached to this registration. Fields comprise: provenance and screening (identifier, originating frame or frames, block, admission mechanism, frame type, date identified, the lexicon proxy used to stratify the coding queue, outcome on each of C1 to C5, screening decision, first criterion failed, merge target, unit-resolution outcome and note, frame-operator flag, frames operated, operator status); organizational status (active / dormant / closed, with date and a dated evidence artifact); tier and label (tier; the self-applied phrase recorded verbatim; the lexicon term or terms matched; the URL, access date, placement of the phrase, and whether the organization is describing itself or quoting a funder, partner, or news source); self-descriptive phrases that match no term in the frozen lexicon, recorded verbatim, with the same evidence requirements as a lexicon hit; functional role (ecosystem role; named partner organizations); the five framework dimensions; and descriptive fields (name, headquarters, focus, projects, founding year, mission, staff expertise, contact, legal form, funding sources, technologies).

The lexicon proxy records whether any frozen lexicon term appears in the text of the organization's own homepage, computed by automated text match at enumeration. It takes three values — true, false, and undetermined — because a page that could not be fetched or that yielded too little text to read has not established the absence of the vocabulary, and treating such a record as false would place it in the wrong stratum for a reason unrelated to how the organization describes itself. Undetermined records are resolved by hand before the queue is built. The proxy is a sampling aid only: it is not the tier assignment, which is a human judgment requiring the placement of the phrase and the identity of the speaker, and it is neither reported as tier nor used to prefill the tier field.

The lexicon of self-identification terms is frozen and recorded in the codebook. Every term derives from the manuscript's own taxonomy, so the instrument operationalizes the argument rather than importing vocabulary the study does not engage. Self-descriptive phrases are recorded verbatim before being matched to the lexicon, never the reverse, so that an unanticipated label surfaces as a finding rather than being recorded as an absence. Terms surfaced during the review that are absent from the lexicon are reported as findings and are not added to the lexicon mid-collection.

## Extraction stages

**(1) Training/pilot stage** — the charting form is piloted on 25 included sources, drawn to span the three traditions and the recorded source types; both the AI-assisted procedure and a human blind to the AI chart the same sources, so the AI can be validated (below), and the form and prompts are refined. Changes are recorded in a preregistration update (charting is iterative; Levac et al., 2010).

**(2) Final extraction stage,** using a two-tier AI-assisted workflow:

1. **Metadata (AI-assisted).** A large language model (Claude Opus 5) extracts the metadata entities (authors, year, title, venue, publication/source type). A human verifies these fields for all sources.
2. **Interpretive entities (AI recommends, human validates).** For tradition assignment, faceted classification, source role/type, the four framework dimensions, the source's key-term definition, and the meta-narrative themes, the model returns a recommended value with a supporting quotation/rationale, and a human validates every recommendation, giving heightened scrutiny where the model's rationale is weak or the evidence is thin. The model makes no autonomous charting decisions; the human retains final authority on every field.
3. **Citation data** are retrieved from OpenAlex, not from the LLM. OpenAlex is the sole provenance of the citation edge list used for the silo analysis; Crossref is used for metadata validation and retraction screening only.

## Extractor instructions

These instructions govern the literature strand; organizational coding follows Screening Reliability.

Extractors will:

1. for metadata, confirm each AI-extracted field against the source for all sources and correct errors;
2. for every interpretive field, treat the AI recommendation as advisory, check it against the source text, and accept, revise, or reject it, recording the final human decision and the supporting passage;
3. resolve any AI–human divergence by human judgment, defaulting to the coding best supported by explicit textual evidence;
4. apply the controlled vocabulary defined for each facet and extract the key-term definition verbatim where stated;
5. mark any entity not addressed by the source as "not reported" rather than allowing the model to infer it;
6. recuse themselves from any source they have authored, per Overlapping Authorships, and log the recusal; and
7. log, for every field, the AI recommendation, the human decision, and the evidence location.

The extraction codebook and the exact AI prompts are stored in the OSF project as `extraction_codebook`.

*No files selected.*

## Extractor masking

Extractors will not be masked to the research questions or framework (masking is neither feasible nor appropriate for interpretive charting). The AI is supplied the source text (or title/abstract/full text as available) together with the codebook definitions for the field it is charting; it is not given the review's hypotheses. Expectation-driven coding is mitigated by explicit piloted definitions, mandatory verbatim evidence, and validation of the AI against blind human coding.

## Extraction reliability

### Literature strand

The AI functions as a first-pass coder whose output is validated by a human. At the pilot, a human charts the twenty-five-source calibration set blind to the AI, and we compute AI–human agreement per field — Cohen's kappa for categorical entities (tradition, facets, source type, framework-dimension codes) and field-level accuracy for metadata — and report it with confidence intervals.

For metadata fields, the workflow proceeds to the full run only if field-level accuracy reaches 95%. For categorical interpretive entities the benchmark is Cohen's kappa at or above 0.60, reported with its confidence interval and with percentage agreement alongside it where the marginal distribution is too skewed for kappa to be interpretable.

The 0.60 benchmark is applied as a benchmark and not as an automatic gate. Kappa computed on twenty-five observations for a multi-category interpretive field carries substantial uncertainty, and a binary consequence applied to a point estimate of that precision would remove AI assistance from fields whose agreement is adequate and retain it on fields whose agreement is not. Where a field falls below the benchmark, the prompts and codebook are revised and the pilot repeated. Where it remains below the benchmark after revision, the field is reported with its statistic and confidence interval stated, and the decision to retain or withdraw AI recommendation for that field is made on the reported evidence and documented in a preregistration update before the full run. Where a field's confidence interval spans 0.60, that is reported rather than resolved by the point estimate.

In the full run, every interpretive field is human-validated (not blind, by design), and metadata are verified in full.

### Organizational strand

Two agreement statistics are computed for this strand and reported separately: agreement between the two human coders, which measures the reliability of the instrument, and agreement between the adjudicated human value and the blind AI coding, which measures the model. Neither substitutes for the other, and the human-to-human statistic is the one on which any decision about a field's usability rests.

Because the Group 3 fields are double-coded in full (see Screening Reliability), we compute and report Cohen's kappa between the two research assistants over all coded records for each of those fields — C3 (constitutive technology), C4 (public benefit), C5 (funder program), and the five framework dimensions — at the final calibration round, at the midpoint of coding, and at the end. Where a field's marginal distribution is too skewed for kappa to be interpretable, we additionally report percentage agreement.

The benchmark is kappa at or above 0.60 for each judgment-dependent field, matching the literature strand. Unlike the literature strand, failing that benchmark does not change who codes the field. Double coding is retained for every Group 3 field regardless of its agreement, because withdrawing it would remove the only mechanism that reveals the problem and would leave the least reliable field the least checked. Instead, a field whose agreement remains below the benchmark after codebook revision and a repeated calibration round is reported with its agreement statistic stated, is restricted to descriptive use, and is excluded from any comparative claim across blocks or frames; which fields this applied to, and what their agreement was, is reported with the results. Low agreement on a framework dimension is itself informative, since it indicates that organizations' self-descriptions do not support a stable reading of that dimension.

Organizational status is calibrated on the same set, because the distinction between dormant and closed is genuinely ambiguous for small volunteer organizations and status is an analytic variable rather than a gate.

The inductive category coding described under Synthesis Plan is carried out after charting is complete by both research assistants working independently over the full set of pooled non-lexicon phrases, with the lead reviewer adjudicating disagreements, on the same terms as a Group 3 field. Agreement between the two assistants on category assignment is computed over all pooled phrases and reported. No AI is used at this step.

Adjudication by the lead reviewer resolves the coded value where the research assistants disagree, except on author-conflicted records, where the disagreement is reported unadjudicated (see Conflicts of Interest). Adjudicated records are identified in the shared dataset so that the agreement statistics can be recomputed by a reader without them.

**AI validation in the organizational strand.** Before the model is used on any record entering the analytic dataset, it processes the calibration set and its output is compared against the adjudicated human values. Role 1 proceeds only if field-level accuracy on Group 1 fields reaches 95 per cent; fields below that threshold after prompt revision are coded by a research assistant without AI assistance, and this is reported. Role 2 is judged on whether the returned passages contain the phrase the human coder ultimately selected, reported as a recall figure; it has no gate, because a missed passage costs search time rather than accuracy and the human reads the page regardless.

Role 3 has no threshold and no gate, because it never contributes to a coded value. Human-to-AI agreement is computed per judgment-dependent field, using the same statistics as the human-to-human comparison, and is reported separately from it and clearly labelled, so that neither is mistaken for the other. Where the model disagrees with both human coders, or where all three diverge, the record is flagged and reviewed after the adjudicated value has been recorded; any change resulting from that review is logged with its reason, and the count of such changes is reported.

Every AI proposal and the corresponding human decision is logged per field, so that the rate at which humans overrode the model can be recomputed by a reader.

In the full run, every interpretive field is human-validated (not blind, by design), and metadata are verified in full.

## Extraction reconciliation procedure

AI–human divergence: resolved by the human, who selects the value best supported by explicit evidence in the source; no field is finalized on the AI's recommendation alone. Pilot disagreements are examined for systematic causes (e.g., boundary ambiguity in a facet definition) and used to refine the prompts and codebook before the full run, with changes logged in a preregistration update.

## Extraction procedure justification

The two-tier AI design matches task risk to oversight. Metadata extraction is low-judgment and well within current AI capability, so AI extraction with human verification is efficient and safe. The interpretive entities — tradition, facets, framework dimensions, themes — are judgment-laden, and current guidance holds that AI is not yet validated for autonomous extraction of such content (RAISE, 2025); we therefore restrict the AI to a recommendation role with mandatory human validation and final authority, and we validate it against blind human coding before use. This preserves the reliability of the interpretive coding while reducing reviewer workload on a large corpus. Controlled vocabularies, verbatim-evidence requirements, and per-field agreement thresholds make the coding consistent and auditable. Single-human oversight is a pragmatic assurance level for a small team, acknowledged as a limitation.

## Data management and sharing

In addition to the complete charted dataset (CSV/XLSX, with codebook, source DOIs, open license, OSF DOI, no embargo — as previously specified), we will share the AI-assisted extraction log, recording for every field the AI recommendation and the final human decision, so the human–AI workflow is fully auditable. FAIR / 5-star open-data efforts are as described previously.

## Miscellaneous extraction details

**AI-use disclosure (per RAISE, Responsible AI in Evidence Synthesis, 2025).** We will use a large language model, Claude Opus 5, accessed via API with fixed, archived prompts and default temperature settings, in two roles during data extraction: (a) to extract metadata, which a human will verify; and (b) to recommend values for interpretive fields (tradition, faceted classification, source role, the four framework dimensions, key-term definitions, and meta-narrative themes), each of which a human will validate, retaining final authority. The model will make no autonomous extraction decisions. Before the full run we will validate the model against blind human coding on the pilot set and will report per-field agreement (accuracy); the full run will proceed only if agreement meets the pre-specified thresholds, and otherwise we will revise the prompts/codebook and repeat the pilot. Because LLM outputs are non-deterministic and version-dependent, we will record and report the model version, access dates, and exact prompts. Citation data will be obtained from the citation index rather than the model, and no AI tool will be used for quality appraisal or synthesis decisions.

---

# Synthesis and quality assessment

*In this section, you register the procedure for the review's synthesis: the procedure you designed to use the data that was extracted from each source to answer your research question(s). This often includes transforming the raw extracted data, verifying validity, applying predefined inference criteria, interpreting results, and presenting results. Additionally, you register procedures you designed to assess bias in individual sources and the synthesis itself.*

## Planned data transformations

No effect-size conversion or numeric aggregation applies (this is a descriptive and interpretive review). We will transform the charted data by:

(a) tabulating the categorical entities into frequency counts and cross-tabulations (disciplinary home × application domain × normative lens, by tradition, and by publication year) to build the descriptive map;
(b) collapsing any residual free-text codes into the controlled vocabularies defined in the codebook;
(c) thematically coding the qualitative fragments (the four framework dimensions, key-term definitions, and meta-narrative themes) into higher-order themes following Braun & Clarke (2006); and
(d) assembling the extracted references/citations into a citation edge list among included sources for the network analysis.

These transformations yield the main variables of interest specified in the Review Methods section.

## Missing data

Entities not addressed by a source are charted as "not reported" and retained as such; we will not impute missing values and will not contact authors to obtain them. Missingness is treated as informative — for example, a tradition that rarely specifies "who decides what social good means" is a finding — and we will report the proportion of "not reported" per field, noting it in denominators for descriptive counts. Analyses will proceed on available data, with any field too sparse to support a claim flagged rather than over-interpreted.

## Data validation

Charted values are validated against the source during the human-validation step of extraction; metadata are cross-checked against DOIs via Crossref; and we will screen included records against retraction registers (Crossref/Retraction Watch). A retracted record is excluded under exclusion criterion 6 and logged as such in the PRISMA-ScR flow; where the retraction is identified after charting, the record is removed from the analytic corpus and the removal is counted and reported. A record under an expression of concern is retained and flagged in the shared dataset. Interpretive codings are triangulated through the pilot AI–human agreement check and the verbatim-evidence requirement. Our validity criterion is that every coding be supported by explicit textual evidence; codings that fail this are re-coded or marked uncertain and excluded from claims that depend on them. Anomalous or inconsistent codings surfaced during synthesis are returned to the source for re-checking.

## Quality assessment

Consistent with scoping-review methodology (Arksey & O'Malley, 2005; Munn et al., 2018), we will not conduct a formal risk-of-bias or quality appraisal of individual sources (e.g., Cochrane RoB, GRADE), and we will not use source quality to weight inclusion or synthesis. This is a deliberate, documented choice: the review's aim is to map and interpret how a field conceptualizes itself, not to estimate an effect whose credibility depends on study quality. In place of quality appraisal, we characterize each source's type and role (survey, definitional, empirical, critical/position) descriptively, and — following RAMESES for the meta-narrative component — we appraise sources for their contribution to a tradition's storyline rather than their methodological rigor.

## Synthesis plan

The synthesis proceeds in four tiers, mapped to the research questions.

**Tier 1 — descriptive mapping (RQ1).** Numerical summary of the charted facets: distributions and cross-tabs across discipline, domain, and lens; a publication timeline; and identification of anchor/hub works. These distributions are reported as distributions over the assembled corpus and not as estimates of the composition of the TPG literature. The tradition composition of the seed set (6 civic technology, 7 public interest technology, 10 "for good") is reported alongside them, and no claim is made that the relative sizes of the three traditions in the corpus reflect their relative sizes in the literature.

**Tier 2 — meta-narrative synthesis (RQ2).** For each tradition, reconstruct its storyline (origins/paradigm, definition of "the good," exemplars, trajectory) from the charted definitions and themes, using thematic analysis (Braun & Clarke, 2006) and reported per RAMESES.

**Tier 3 — cross-tradition synthesis (RQ3).** Compare the three traditions on the five framework dimensions; identify convergences and recurring tensions; and construct an integrated account of TPG.

**Tier 4 — citation-network analysis (RQ4, secondary).** From the citation edge list, compute within- vs. cross-tradition citation to test siloing, and cluster via co-citation / bibliographic coupling (CitNetExplorer / VOSviewer).

The organizational strand is synthesized in parallel and addresses RQ5 and RQ6. Three components carry it.

**First, a structural comparison between blocks.** Because frame composition sets the denominator for every count the instrument produces, the comparison rests on measures that do not require a population denominator: unique-organization yield per frame and per block, and the rate at which records resolve to programs inside larger institutions rather than to standalone organizations.

The unit-resolution comparison is made between Blocks B and C only. Block A is excluded because the PIT University Network lists universities rather than organizations, so that block's rate is set by a frame's listing convention rather than by the tradition's organizational form. Within the B-to-C comparison, frame type and tradition are not separable, because Block C is built from funder portfolios that fund programs housed in larger institutions while Block B is built from rosters of standalone groups; a difference in the predicted direction is reported as consistent with the expectation rather than as confirming it.

That the "for good" block contains no identity-type frame is a property of the frame register as constructed and is described where the register is specified, under Sampling and sample size. It is not a measure and is not reported as a result of the comparison.

Screening pass rates and tier rates are not comparable across blocks, because admission mechanisms differ and selection-based frames pre-vet for precisely what the unit and constitutive-technology criteria test; both are reported per frame, for description only, alongside a statement of what that frame selects for.

Frame redundancy is reported per block as description and is not compared across blocks as evidence of relative population size, because two of the three blocks contain frames with structural relationships to one another — a funder that helped create the network the other frame enumerates, and a successor network to a sunset one — that manufacture overlap independently of field size.

**Second, an inductive coding of self-descriptions, which answers the third clause of RQ5.** Self-descriptive phrases that match no term in the frozen lexicon are pooled across included records and coded into emergent categories in a second pass after charting is complete, with agreement between the two research assistants computed over all pooled phrases and reported. We report which categories recur across multiple organizations, whether each recurs within one block or cuts across blocks, and whether any is used by frame operators as well as by the organizations they recruit. A phrase used by a single organization is not reported as a category. Categories so identified are reported as results and are not added to the frozen lexicon. We state as a limitation that the absence of emergent categories cannot be distinguished from the frames having admitted only organizations whose vocabulary already fits.

**Third, a comparison against the literature findings on the five framework dimensions, addressing RQ6.** This is a structural comparison of emphasis and configuration, not a distributional one: we report which configurations of the five dimensions appear in practice, which appear in the literature, and which appear in only one, without attaching population proportions to any of them.

**Contingencies.** If a tradition yields too few sources for a defensible narrative, we report it descriptively and flag the sparsity; if citation coverage is incomplete for some sources, the silo analysis is reported as exploratory with its coverage stated; if a block of the organizational frame register is exhausted before saturation, the exhaustion is reported as a finding about that tradition's organizational density rather than remedied by adding frames.

## Criteria for conclusions / inference criteria

No significance testing or effect-size threshold applies. For the qualitative tiers, our inference criterion is thematic saturation — a theme or storyline element is reported when it is supported by convergent evidence across multiple sources and additional sources cease to add new elements — with all claims traceable to charted evidence (the RAMESES "synthesizing argument"). For the citation-silo tier, we will report the observed proportion of cross-tradition versus within-tradition citations descriptively and interpret it relative to what proportion would be expected under random citation, rather than applying an arbitrary cutoff; a marked deficit of cross-tradition citation will be characterized as siloing.

## Synthesist blinding

Synthesists will not be blinded to the research questions or framework; blinding is neither feasible nor appropriate for an interpretive meta-narrative synthesis, in which the synthesist must understand the conceptual apparatus to construct the storylines. Following RAMESES, we mitigate the resulting interpretive risk through documented reflexivity, an audit trail linking every claim to charted evidence, and peer debriefing.

## Synthesis reliability

Synthesis will be conducted by a single synthesist; independence procedures are not implemented, and reliability is instead supported by an evidence-linked audit trail, reflexive memoing, and peer debriefing with a colleague not involved in coding. Single-synthesist synthesis is acknowledged as a limitation.

## Synthesis reconciliation procedure

Inter-synthesist reconciliation is not applicable; interpretive decisions will be checked through peer debriefing and revised where the evidence does not support them.

## Publication bias analyses

Not applicable in the quantitative sense: with no pooled effect sizes, funnel plots, Egger's test, p-curve, and related corrections cannot be computed. We will instead address the analogous coverage and selection biases qualitatively — the dependence of the corpus on the seed set, including the tradition composition of that set; the chosen citation index; the incomplete indexing of preprint and proceedings seeds; the recency of three seeds, which are correctly indexed but too recently published to have accumulated forward citations, so that the expansion is ascendancy-only for them and the corpus is covered less thoroughly forward than backward in the tradition holding those seeds; the English-language restriction; and the field's own publication practices (including reliance on grey literature and preprints) — and report these in the limitations, supported by the leave-one-out and index-sensitivity checks below.

## Sensitivity analyses / robustness checks

**Literature strand.**

- **(a) Seed leave-one-out** — re-run the expansion omitting each seed in turn to assess how dependent the corpus is on individual seeds.
- **(b) Index sensitivity** — compare corpus and citation results against Semantic Scholar, reporting the proportion of the corpus and of the citation edge list recoverable from it, so that the corpus's dependence on OpenAlex is measured rather than only acknowledged. Where the comparator's coverage of a source type is known to be limited, that is stated rather than treated as a discrepancy.

**Organizational strand.**

- **(e) Leave-one-frame-out** — re-run block-level results dropping each frame in turn, to expose results driven by a single frame's composition, the direct analogue of the seed leave-one-out above.
- **(f) Multi-frame subset** — analyze organizations claimed by frames from two or more blocks, within which blur is measured immune to recruitment bias, since those organizations were recruited by every tradition that claims them. This subset may be small: the blocks recruit from different traditions by design, and Block A carries only two frames. The analysis is therefore conducted only where the subset contains at least ten organizations; below that threshold it is reported as not conducted, with the count given and the organizations listed, since a near-empty intersection is itself informative about how separate the traditions' recruitment channels are.
- **(g) Activity sensitivity** — re-run the main descriptive results excluding dormant and closed organizations, which shows what an activity gate would have done while preserving the survivorship analysis such a gate would have destroyed.
- **(h) Unit-resolution sensitivity** — report, per frame, the counts of records logged as unresolvable, as `unit_unresolved`, and as known but not surfaced by their frame, as a bound on how much the unit rule and the frame boundaries exclude. This is a reported bound rather than a recomputation: those records are logged and counted but deliberately not coded, so results cannot be recalculated with them included, and the count is the strongest statement the rule permits.
- **(i) Boundary audits** — report the C1 pass rates from the two Civic Tech Field Guide audit samples as a bound on that frame's completeness.

Results that change materially under any of these checks will be reported as such. Every organizational result is reported per frame before any pooled figure. Each reported figure carries a population statement naming what it was computed over — the frame or frames, the block, whether frame-operator records are included, and whether the denominator is the enumerated pool, the screened pool, or the coded sample — so that no figure can be read as describing a population wider than the records it was computed from.

## Synthesis procedure justification

The transformations are descriptive and thematic rather than statistical because the research questions concern how a field is conceptualized and distributed, not the size of an effect; this also makes quality appraisal, meta-analytic pooling, and publication-bias correction inapplicable, consistent with scoping-review and meta-narrative conventions. Saturation and evidence-traceability are the appropriate inference criteria for an interpretive synthesis. Blinding is replaced by reflexivity and an audit trail because the synthesis is inherently theory-laden. The robustness checks target the biases that do threaten this design — seed dependence and index coverage — which is where rigor is most at risk. Single-synthesist assurance reflects a pragmatic balance for a small team, acknowledged as a limitation.

## Synthesis data management and sharing

We will openly share, on the OSF project: the analysis scripts (R and/or Python, as .R / .py and RMarkdown / Jupyter notebooks) used for the descriptive tabulations, figures, and citation-network analysis; the coding/theme structure and reflexive memos (plain text / Open Document); and the outputs (figures and tables). Files will use open formats, carry the OSF DOI, and be released under CC-BY 4.0 / CC0 with no embargo, following FAIR principles.

## Miscellaneous synthesis details

The synthesis integrates the literature and organizational strands on the shared framework dimensions, so that how the field conceptualizes its work and how organizations enact it are answered on common axes. Following RAMESES, we will maintain a reflexive account of how the research team's prior exposure and disciplinary vantage may shape interpretation.

**AI-use disclosure (per RAISE 1 and RAISE 3, Responsible AI in Evidence Synthesis, 2025).** We will use a large language model, Claude Opus 5, accessed via API with a fixed, archived prompt and default temperature settings, to recommend include/exclude decisions during title/abstract screening. It will be used as decision support only: every recommendation will be verified by a human reviewer who retains final authority, and the model will make no autonomous exclusions. Before the full run, we will validate it against blinded human screening on ~100 records, extending to a maximum of 250 where human-includes are sparse, and will report its recall/sensitivity and specificity with confidence intervals, together with the number of human-includes in the calibration sample; the full run will proceed only if recall meets our pre-specified threshold of ≥95%, and otherwise we will revise the prompt and criteria and repeat the pilot. No AI tool will be used for data extraction beyond the roles specified in the Extraction section, or for quality appraisal or synthesis decisions.

This applies to the organizational strand's synthesis components as well. The inductive coding of non-lexicon self-descriptions, which answers the third clause of RQ5, is carried out without AI assistance: both research assistants construct categories independently over the full set of pooled phrases and the lead reviewer adjudicates, as registered under Extraction Reliability. A model may be used afterwards to organize excerpts that have already been coded into categories by the human coders, which is a non-decisional use and is disclosed on the same terms as above. The structural comparison between blocks, the interpretation of the unit-resolution and yield measures, and the comparison of organizational findings against the literature findings are human judgments throughout.
