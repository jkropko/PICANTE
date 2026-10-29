# Preregistration Update 3

**Generalized Systematic Review Registration Form — OSF**

*Initial registration frozen 7/31/2026. Update 2 submitted 8/19/2026. This update submitted 10/29/2026.*

This document is complete: the justification for Update 3 is followed by the full registration form, with every field in its current form. Where a field is not revised here, its text is carried forward from Update 2 unchanged. The disclosures of prior exploratory work made in the initial registration, in Update 1 and in Update 2 stand and are carried forward in the form.

---

# Justification for update

## What had been observed when this update was written

Unlike Update 2, this update is not filed before any stage of the protocol was executed, and it does not give the assurance Update 2 gave. The Search stage has begun. What had and had not been done when the changes below were decided is recorded here so that a reader can judge which changes could have been informed by results.

**Executed.**

- **Round 1 of the citation-network expansion** was run on 28 October 2026 against the live OpenAlex API, with a registered API key, from the 22 seeds that have an OpenAlex record. Every request was logged with a UTC timestamp, and every raw response was saved. The run retrieved 773 backward links and 1,423 forward links, giving a pre-deduplication pool of 1,955 records, the seeds included. Per-seed yields are reported under 1.2 and in the seed file.
- **Mechanical checks on the round-1 output**: the OpenAlex record each seed DOI resolved to, per-seed yields against OpenAlex's own citation counts, whether OpenAlex merges seed 22's preprint and published records, the round-1 position of the validation works (below), and descriptive properties of the pool (missing abstracts, missing DOIs, flagged retractions, repeated titles, record types, languages).
- **Reference counts for every seed**, from the seed PDFs or, for seeds 16 and 18, from the reference lists on the publishers' public article pages, compared against the OpenAlex backward count (2.2).
- **Extraction of reference lists** for the 12 seeds the threshold in 2.2 selects: 1,153 references in total, deposited with this update as `literature/refs/`, with a README recording each list's source, extraction method and every correction made by hand.

**Not executed.** No record has been screened, by a human or by the model. The pilot screening sample has not been drawn. No record has been charted. The extracted reference lists have not been matched to OpenAlex: no manual link has been created and no record has entered the pool through them. Deduplication has not been run.

**Organizational strand.** Separately from the literature strand, and after Update 2 was filed, the frame register was frozen and every frame captured (O2: capture on 23 and 24 September 2026, freeze date recorded as 24 September 2026), and enumeration and deduplication (O3) have begun. No organization has been screened or coded. Nothing in this update concerns the organizational strand except the correction to its stage status under Current review stage, and none of its changes was informed by the organizational data.

**Results that were seen before the changes were decided, and that bear on them.**

1. Six seeds returned no references from OpenAlex (6, 7, 13, 14, 22, 23), and seed 20 has no OpenAlex record. This is what prompted the manual reference supplement (2.1).
2. Seeds 4, 9, 11, 12, 16 and 18 returned between 37% and 72% of the references their reference lists contain. This was seen before the threshold in 2.2 was confirmed (see 2.2 for the order of events).
3. Of the five validation works that count toward the expansion criterion, three (V1, V2, V3) were reached in round 1, and two (V4, Berendt 2019; V5, Fung 2006) were not. Arnstein (1969), V8, was reached by backward chasing from seed 3, as anticipated. None of the 1,153 extracted references is V4 or V5. This was seen before the rule in 2.5 was decided, and 2.5 is constructed so that it cannot alter the registered verdict on V4 or V5.

None of the changes below was informed by the content of any retrieved record beyond these counts and identities, because no record has been read for eligibility.

---

## Class 1 — Corrections

These correct errors, residual inconsistencies left by Update 2, and facts about the seeds established at the Search stage. None changes the design.

### 1.1 "Four framework dimensions" persists in five fields

Update 2 (item 2.1) made the framework dimensions five, separating "who decides" from "what counts as social good". The change did not reach five places in the form, which still refer to four dimensions: Screening reliability (Group 3 fields), Sampling and sample size (the pilot of the framework questions), Extraction stages (the interpretive entities), Miscellaneous extraction details (the AI-use disclosure), and Planned data transformations (item c). Each is corrected to five. In every case the field governs the same coding as before; only the count was stale.

### 1.2 Facts about the seeds established at the Search stage

The registration required several seed properties to be established before or at the Search stage. They are recorded here and in the seed file (`TPG_seed_set_v2.xlsx`); v1 is retained on the OSF project. No seed is added, removed or substituted.

- **Seed 20** (Arora & Sarkar 2023, CEUR-WS Vol-3582) has no DOI and no OpenAlex record, established by searching OpenAlex for the work at the Search stage. Under Update 2 item 1.6 it is reported as contributing no citation neighbourhood and is not replaced. Its reference list is used under 2.1.
- **Seed 6** (Zhang et al. 2022) has not been published as of 28 October 2026; the frozen arXiv identifier remains the expansion input. Its OpenAlex record (indexed from arXiv and DataCite) holds no reference list and 5 citing works.
- **Seed 22**: OpenAlex does not merge the arXiv preprint (arXiv:2505.22327) with the published EACL 2026 record. At the check, the preprint record had no citing works, so no forward citations were lost; the check is repeated at the expiration refresh. Seed 22's forward set is reported as potentially incomplete, as Update 2 item 2.5 requires.
- **Seed 14** (Ghani 2018) is a one-page SIGIR keynote abstract with no reference list. Its OpenAlex count of zero references is correct, not an index gap, and it contributes forward citations only. The seed file classed it as a survey; the type is corrected to keynote abstract. The seed remains in the frozen set.
- **Seeds 13 and 23** returned no references and no citing works; **seed 22** returned no references and 2 citing works. With seed 20, seeds 13, 22 and 23 contribute nothing or almost nothing to round 1 from OpenAlex.
- **OpenAlex records whose title did not match the seed file** (seeds 2, 5, 7 and 14) are checked by hand against the source before matching, and the result is recorded in the seed file. Where OpenAlex holds a second record for the same work, the record the frozen DOI resolves to remains the expansion input, the second record is recorded and reported, and the seed's forward set is reported as potentially incomplete. This applies the principle Update 2 item 2.5 registered for preprint and published records to any duplicate record. It matters most for seed 7, whose DOI resolves to a record with no references and 2 citing works.

Per-seed yields from round 1 are recorded in the seed file's *Forward-chase viability* column and reported with the review.

### 1.3 Citationchaser is named for an index the protocol no longer uses

Interfaces and Software name the citationchaser R package for the expansion "where it supports OpenAlex". Citationchaser retrieves from Lens.org, which Update 2 item 2.9 removed. The expansion is run by scripts written against the OpenAlex API (`expansion_round1.py`, `checks_round1.py`), deposited in the repository and on OSF; citationchaser is removed from both fields.

### 1.4 "OpenAlex/Crossref" remains in Other search strategies

Other search strategies describes forward chasing "via OpenAlex/Crossref". Update 2 item 2.9 made OpenAlex the sole citation index and confined Crossref to metadata validation and retraction screening. The field is corrected to OpenAlex.

### 1.5 The planned end date

Update 2 item 1.8 states that "the planned end date is moved to 9/16/2026", while the End date field it revised gives 30 June 2027. The field is correct and the sentence in item 1.8 is an error: 9/16/2026 is the date the seed file was revised, not an end date. The planned end date remains 30 June 2027, to be revised after PredicTER is run on the deduplicated pool, as registered.

### 1.6 Review stages describes every seed as having a DOI

Review stages describes the seed set as "23 survey/definitional 'hub' articles, with DOIs". Seed 20 has no DOI (Update 2 item 1.6), and seed 14 is a keynote abstract (1.2 above). The stage description is corrected.

---

## Class 2 — Design changes

### 2.1 A manual reference supplement for seeds whose reference lists the index does not hold

**The gap.** The expansion's backward arm depends on OpenAlex holding each seed's reference list. OpenAlex obtains reference lists largely from publishers' Crossref deposits; arXiv preprints are registered with DataCite, which carries none, and some publishers deposit none. At round 1, six seeds returned no references (6, 7, 13, 14, 22, 23), seed 20 has no record at all, and several more returned well under their actual reference lists. One of the six, seed 14, genuinely has no references. For the rest, the registered treatment (Update 2 item 1.6) is to record the seed as materially incomplete and report it with the leave-one-out check. That treatment is retained, but on its own it leaves nearly a third of the seed set contributing little or nothing backward, concentrated in the "for good" tradition and in the most recent seeds — the same concentration Update 2 item 2.7 registered as a determinant of the descriptive map.

**As revised.** For each seed selected by the threshold in 2.2, the reference list is extracted from the seed's own full text and each reference is matched to an OpenAlex record. Matched works enter the pre-deduplication pool as backward links from that seed, labelled `manual_pdf` and kept distinguishable from links OpenAlex supplied throughout the review. The frozen seed identifiers remain the expansion input; nothing here substitutes a seed or changes which works the seeds are.

**Extraction.** Reference lists are extracted from the seed PDFs (supplied by the team, or open access) or, where the full text is not open and the publisher lists references on the public article page, from that page. Each extracted list is checked against the source's own numbering or count. Every correction made by hand is recorded. The extracted lists, the source text used for page-derived lists, and the extraction scripts are deposited.

**Matching.** Each reference is matched to OpenAlex by the first applicable route, and the route is recorded:

1. **DOI.** A DOI given in the reference, or an arXiv identifier converted to its arXiv DOI, is looked up directly.
2. **Title.** Otherwise, OpenAlex is searched by title, restricted to the reference's year plus or minus one year. Venue text left on the end of a parsed title (for example "arXiv preprint arXiv:…" or a journal name and volume) is removed first. The search requires every title word to match; only where that returns no candidate is OpenAlex's relevance search used instead, with the same year restriction, and the row is marked as a relevance-search fallback. Whichever search supplies the candidates, the best candidate is accepted automatically only if its normalized title similarity is at least 0.90 and the reference's first-author surname matches the candidate's first author.
3. **Review.** Every reference not matched automatically, and every DOI match whose first author does not match, is reviewed by hand and recorded as one of: matched by hand (with the OpenAlex ID), not in OpenAlex, grey literature, or rejected.

**Verification.** A second team member checks every reference matched by hand and a random 10% of automatic title matches, drawn with a recorded seed (20261028). The proportion of sampled automatic matches confirmed is reported. Grey-literature items found this way do not enter the pool through this route; they are recorded and passed to the targeted hand-searching arm.

**Reporting.** For each seed, the review reports the number of references in its list, the number OpenAlex supplied, the number matched through the supplement and by which route, the number already present among the OpenAlex links, and the number not in OpenAlex or grey literature. Records that enter the pool only through the supplement are reported as a separate identification source in the PRISMA-ScR flow ("records identified from seed reference lists").

**What it does not do.** The supplement restores backward links only. It cannot restore forward citations missing from the index, and no other index or search engine is used for them: Google Scholar is not reproducible, and Semantic Scholar is registered only as the comparator for sensitivity analysis (b). Seeds with incomplete forward sets remain reported as such.

**Rationale.** Under-indexing of preprints, proceedings and some publishers is a property of the index, not of the literature, and it falls unevenly across the traditions. A manual supplement with a fixed procedure, a labelled provenance and a with-and-without sensitivity check corrects the backward arm without making the corpus depend on undocumented choices.

### 2.2 The threshold that selects seeds for the supplement

**As revised.** A seed receives a manual reference file when the number of references OpenAlex returned for it is below 80% of the number of references in its reference list, counted as raw entries. Seed 20, which has no OpenAlex record, is included by definition. Seed 14 is not included, because it has no reference list.

**Raw counts.** Raw counts include grey literature, which OpenAlex cannot hold, so a seed can fall below the threshold even when OpenAlex holds every scholarly reference it cites. This errs toward inclusion, and its only cost is labour: on such a seed, matching returns references already present among the OpenAlex links, and these are reported as such and add no new link.

**Order of events.** An 80% threshold was proposed before any seed's reference count was known. The counts were then computed for all 22 seeds with an OpenAlex record, and the threshold was confirmed at 80% after they had been seen. At 80%, the seeds selected are 4, 6, 7, 9, 11, 12, 13, 16, 18, 22 and 23, plus seed 20 by definition. The nearest seed to the boundary is seed 17, at 83% (70 of 84). Because the threshold was confirmed after the counts were known, sensitivity analysis (c) reports the corpus with seed 17's extracted list added, which is what an 85% threshold would have produced; no other seed lies between 80% and 85%.

### 2.3 Seed 7's reference list is its endnotes

Seed 7 (Schank & McGuinness 2021) is a book with 237 endnotes and a separate 32-entry Bibliography. **As revised**, the endnotes are its reference list: backward chasing follows what a work cites, and the Bibliography functions as a further-reading list. Twenty-six of its 32 works are cited in no endnote.

The endnotes yield 129 unique cited works. Items dropped from the endnotes, each logged with its reason, are personal communications (69: author interviews and e-mails), "Ibid." (30), and short-form repeats or commentary (11), each short form confirmed to have its full citation elsewhere in the notes. The 26 Bibliography-only works are listed in the deposit and reported, but are not added.

### 2.4 The supplement applies to seeds only

**As revised.** The supplement applies to the seeds. Records chased in later rounds of the snowball are not given manual reference lists. Where a record that passes relevance screening is chased and OpenAlex returns no references or no citing works for it, that is recorded per record and reported per round, so that the extent to which later rounds are ascendancy- or descendancy-limited by the index is visible. Extending the supplement to every chased record would require obtaining and extracting the full text of every under-indexed included record, an unbounded workload that the seed set does not impose.

### 2.5 When a validation work is unreachable, and a reported-only check for paths through excluded records

**The gap.** Update 2 item 2.4 classifies a missed expansion-testing validation work as (a) absent from the index, (b) present in the pool but excluded at screening, or (c) present in the index but unreachable from any seed's citation neighbourhood, and adds a targeted query where two or more fall into (c). It does not say when the classification is made, and it does not anticipate a work whose only path from the seeds runs through a record that is itself excluded. V5 (Fung 2006) was included as the two-to-three-hop test precisely because it is expected to be reached through Arnstein (1969). Arnstein is a work of participation theory, so whether it passes relevance screening is open, and if it does not, the snowball never chases from it.

**As revised.**

1. **Timing.** Classification into (a), (b) or (c) is made at saturation of the snowball, not after round 1. The round-1 position is reported as interim. As of round 1, V1, V2 and V3 have been reached and V4 and V5 have not (see "What had been observed").
2. **The registered verdict is unchanged.** Reachability for the criterion means reachability through the expansion as run: through the seeds, through links supplied by OpenAlex or by the supplement in 2.1, and through records that passed relevance screening and were chased. A work not reached that way at saturation, and present in the index, falls in (c), and the targeted-query rule applies as registered.
3. **A separate, reported-only path check.** For each expansion-testing validation work in (c), the review reports whether it cites, or is cited by, any record in the pre-deduplication pool that was excluded at screening, naming that record. A work reachable only through an excluded record is reported as "reachable only through an excluded record", alongside its (c) classification and not in place of it. The check adds nothing to the corpus, does not count toward the criterion, and cannot prevent the targeted query from being triggered.

**Rationale.** The check distinguishes a seed set that cannot reach a work from a screening decision that cut the path to it. That is the information the validation set exists to give, and the registered criterion alone conflates the two. Because the check is reported-only, it could not have been chosen to rescue V4 or V5, whose interim status was known when it was decided.

**V7.** *A Pivotal Moment* (Freedman Consulting 2016), validation work V7, is cited in seed 7's endnotes and in the reference lists of seeds 11 and 13. It continues to be assessed only against the hand-searching arm, as registered. Its appearance in seed reference lists is recorded and reported, and if it is matched to an OpenAlex record through the supplement, that is reported too, without changing the arm it tests. V3 (Züger & Asghari 2023) is also cited in seed 11's reference list; it was already reached in round 1.

### 2.6 The citation edge list for the silo analysis keeps a single provenance

Update 2 item 2.9 gave the edge list a single provenance, OpenAlex. The supplement creates links from another source. **As revised**, the primary silo analysis (Tier 4) uses OpenAlex-supplied links only, preserving the single provenance registered in Update 2. The analysis is repeated with the `manual_pdf` links added, and both are reported under sensitivity analysis (c). Seed composition, recency and missing reference lists all bear on the silo analysis through the backward links, so both versions are needed to read it.

### 2.7 Seed composition, revisited at round 1

Update 2 item 2.7 registered the seed set's tradition composition (6 civic technology, 7 public interest technology, 10 "for good") and seed recency as determinants of the descriptive map. Round 1 shows the composition of the seeds' actual contributions is more uneven than the composition of the set. Of the 10 "for good" seeds, seed 20 has no record, seed 23 contributed nothing, seed 22 contributed 2 forward links, and seed 14 contributes forward only. Three "for good" seeds (15, 16 and 18) account for 988 of the 1,423 forward links. **As revised**, per-seed and per-tradition yields are reported for the OpenAlex links and for the manual supplement separately, alongside the seed composition already registered. No claim about the relative sizes of the traditions is made from the corpus, as Update 2 registered.

### 2.8 AI use in the Search stage

An AI assistant (Claude Opus 5.5, Anthropic, in the Claude desktop application) was used at the Search stage:

- to write the scripts that retrieve the round-1 expansion, check its output and match references to OpenAlex;
- to extract reference lists from seed full texts into structured files;
- to compute reference counts.

It made no eligibility judgment and no inclusion decision. Every extracted list was checked against its source's numbering or count. Every parsed field is subject to the review in 2.1, and the corrections made by hand are recorded in the deposit. This is disclosed under RAISE, and the AI-use disclosure under Miscellaneous search strategy details is extended accordingly.

---

# List of updated registration questions

- Review stages
- Current review stage
- Start date
- End date
- Software
- Interfaces
- Query strings
- Search validation procedure
- Other search strategies
- Miscellaneous search strategy details
- Screening stages
- Screening reliability
- Sampling and sample size
- Data management and sharing (Screening)
- Entities to extract
- Extraction stages
- Miscellaneous extraction details
- Planned data transformations
- Synthesis plan
- Publication bias analyses
- Sensitivity analyses / robustness checks

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

1. **Preparation.** Finalize and freeze the seed set (23 survey/definitional "hub" works: 22 identified by DOI and one, seed 20, by its proceedings URL, having no DOI; seed 14 is a keynote abstract); specify eligibility criteria using the Population–Concept–Context framework; register this protocol on OSF.
2. **Search.** Identify records via (a) keyword searching and (b) forward/backward citation-network chasing seeded by the 23 frozen seeds (constrained snowball; Lecy & Beatty, 2012), with (c) a manual reference supplement for seeds whose reference lists the index does not hold, selected by a registered threshold (Update 3 items 2.1–2.4). Export the candidate pool and remove duplicates.
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

This is a preregistration update (Update 3). The initial registration was frozen on 7/31/2026.

At the moment of freezing this update, the literature strand is in the Search stage. Per-stage status:

- **Preparation** — completed. The seed set is frozen; the seed file was revised at the Search stage to record established facts about the seeds (Update 3 item 1.2), with no seed added, removed or substituted. The data-charting form is drafted but not yet piloted.
- **Search** — begun. Round 1 of the citation-network expansion was run on 28 October 2026 against the live OpenAlex API, from the 22 seeds with an OpenAlex record, retrieving a pre-deduplication pool of 1,955 records (seeds included). Reference lists were extracted for the 12 seeds selected by the threshold in Update 3 item 2.2. Not yet done: matching the extracted references to OpenAlex, deduplication, later snowball rounds, targeted hand-searching, and the search validation check, which is made at saturation.
- **Pilot Screening / Screening** — not started. No record has been screened.
- **Pilot Extraction / Extraction (Charting)** — not started.
- **Organizational strand** — O1 completed. O2 completed after Update 2 was filed: every frame was captured on 23 and 24 September 2026 and the register freeze date recorded as 24 September 2026. O3 (enumeration and deduplication) begun. No organization has been screened or coded.
- **Synthesis / Reporting** — not started.

What had been observed when this update was written, and which of its changes those observations could have informed, is set out under "What had been observed when this update was written" at the head of Update 3.

**Disclosure of prior exploratory work.** Earlier exploratory work informed this protocol and is set aside rather than used as data. A preliminary literature corpus, assembled from an initial seed set, informed the eligibility criteria, the analytic framework, and the selection of the frozen seed articles; the registered review is conducted afresh from the frozen seed set. An ad hoc collection of 231 practitioner-organization records, assembled before registration, informed the design of the organizational instrument; it is set aside as exploratory, holds the same status as the preliminary literature corpus, and is not analyzed as data. It was assembled from a partially overlapping set of sources: five of the frames in the registered register — the Civic Tech Field Guide, the Alliance of Civic Technologists, the archived Code for America brigade roster, the PIT University Network, and Fast Forward — were among its sources, while several sources it used are not in the register, and the register adds frames it did not use. Substantial but incomplete overlap between that collection and the registered sample is therefore expected by construction. Neither a high nor a low overlap is diagnostic of anything, and no comparison between the two is reported.

**Disclosure of pre-registration inspection.** Before filing Update 2, the sources named in the organizational frame register were examined to establish whether each exists in an enumerable form, what enumerating it would cost, and where freeze dates could fall. For the Civic Tech Field Guide this included counting records by type and country and measuring field completeness in the public data export. No records were screened against the criteria, matched or deduplicated across frames, or charted on any instrument field. Frame overlap and unique-organization yield are registered analyses and were not computed.

## Start date

The start date was 7/28/2026, the day the preparation stage was initiated. The initial registration was frozen on 7/31/2026. Update 2 was submitted on 8/19/2026. The Search stage began on 10/28/2026. This update (Update 3) is submitted on 10/29/2026.

## End date

Planned end date: 30 June 2027. The Search stage began on 28 October 2026. Update 2 item 1.8 stated that the planned end date was moved to 9/16/2026; that statement was an error and is corrected by Update 3 item 1.5. The date in this field is the planned end date.

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
- **Citation-network searching:** the OpenAlex API, accessed with a registered API key, and/or a dated OpenAlex data snapshot, through Python scripts written for the review (`expansion_round1.py` for retrieval, `checks_round1.py` for the round-1 checks) and deposited with it; every request is logged with a UTC timestamp and every raw response is retained. The OpenAlex snapshot date or API access dates are recorded and reported. Research Rabbit (Major release 2026-07-09) is retained as a supplementary discovery tool only. Neither the Lens.org index nor the citationchaser R package, which retrieves from Lens.org, is used; see Databases.
- **Manual reference supplement (Update 3 item 2.1):** reference lists extracted from seed full texts with poppler `pdftotext` and the extraction scripts deposited with the review (`extract_refs*.py`, `extract_columns.sh`); references matched to OpenAlex with `match_references.py`, which logs every request and every decision.
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

Unlike aggregator interfaces (Ovid, EBSCO), these databases are searched through their own native interfaces/APIs: OpenAlex via the OpenAlex API, using scripts deposited with the review; Google Scholar via the Google Scholar web interface; arXiv via the arXiv website/API; SSRN via the SSRN website. Where the expansion is run against a dated OpenAlex data snapshot rather than the live API, the snapshot date is recorded and reported. Research Rabbit was used in preliminary exploratory work and is retained only as a supplementary discovery tool, not as the search of record.

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

**(2) Citation-network expansion (OpenAlex):** not a Boolean query — the "query" is the identifier list of the 23 frozen seed articles, from which the tool retrieves backward references and forward citations. Twenty-two seeds are identified by DOI. Seed 20 (CEUR-WS proceedings) carries no DOI and, as established at the Search stage, has no OpenAlex record; it supplies no identifier to the expansion, contributes no citation neighbourhood from the index, and is not replaced. Where a seed's citation neighbourhood is unavailable or materially incomplete in the index, that fact is recorded per seed and reported alongside the leave-one-out sensitivity check.

**(3) Manual reference supplement (seed reference lists):** not a query. For each seed selected by the registered threshold — OpenAlex returning fewer than 80% of the references in the seed's own reference list, counted as raw entries, with seed 20 included by definition — the reference list is extracted from the seed's full text and each reference is matched to OpenAlex by DOI (including arXiv DOIs), or else by title within one year of the reference's year (a search requiring every title word, with OpenAlex's relevance search used only where that returns no candidate) with an automatic match only at normalized title similarity ≥ 0.90 and a matching first-author surname; everything else is reviewed by hand. Procedure, verification and reporting are specified under Other search strategies and in Update 3 items 2.1–2.4.

## Search validation procedure

Yes. We validate the strategy against a pre-specified set of known landmark works that any adequate search must recover. The set is recorded in an attachment to this update and frozen on filing, so that it falls under the assurance that no stage of the protocol had been executed. No work in the validation set is among the 23 frozen seeds, and no work in the set may be added to the seed set at any point during the review: a seed is removed from the candidate pool at deduplication as already included, so its non-appearance in the pool is an artifact of that step and carries no information about search adequacy. The check is run against the pre-deduplication pool, so that recovery is assessed before seeds are removed.

Each work is recorded with the arm of the search it tests. Most test the citation-network expansion. At least two are grey-literature items testing the targeted hand-searching of venue and organization websites, and are assessed against that arm rather than against the expansion, because a grey-literature report absent from the citation index would otherwise register as a non-recovery of a kind that does not bear on search adequacy and would test nothing.

The pass criterion has two parts, because the set tests two arms.

For the works testing the citation-network expansion, non-recovery is recorded and reported in every case, and revision is not automatic. We first establish whether the work is (a) absent from the index, (b) present in the pool but excluded at screening, or (c) present in the index but unreachable from any seed's citation neighbourhood, and we report which. Only (c) bears on search adequacy. Where two or more of these works fall into (c), we add a targeted query rather than alter the seed set, because the seed set is the frozen input to the expansion and altering it changes the corpus definition; any addition is documented in a preregistration update before the full run. The threshold is two rather than one because a single unreachable work can reflect that work's own citation profile, whereas two independently unreachable works indicate a systematic gap; it is an absolute count and does not move with the size of the counting subset. Arnstein (1969) is recorded in the set but excluded from this count, because it is the analytic framework's own source and its recovery is close to guaranteed by backward chasing from the civic technology seeds; its recovery is reported separately. At least five works count toward this part of the criterion.

For the grey-literature works testing the hand-searching arm, cause (c) does not apply, because unreachability from a citation neighbourhood is not a question that can be asked of a work assessed against hand-searching. The question is instead whether hand-searching the venue or organization that published the work surfaced it. Non-recovery indicates that the hand-searching arm lacks the coverage the protocol assumes rather than that the expansion is inadequate; we record which venues and organizations were searched, add those that were not, and report the addition.

**When the classification is made.** Classification of a missed expansion-testing work into (a), (b) or (c) is made at saturation of the snowball, not after its first round; the round-1 position is reported as interim. Reachability for the criterion means reachability through the expansion as run: through the seeds, through links supplied by OpenAlex or by the manual reference supplement, and through records that passed relevance screening and were chased.

**Paths through excluded records (reported only).** For each expansion-testing work in (c), we additionally report whether it cites, or is cited by, any record in the pre-deduplication pool that was excluded at screening, naming that record. A work reachable only through an excluded record is reported as such alongside its (c) classification, not in place of it. This check adds nothing to the corpus, does not count toward the criterion, and cannot prevent the targeted query from being triggered; it exists to distinguish a seed set that cannot reach a work from a screening decision that cut the path to it.

**Validation works in seed reference lists.** Where a validation work appears in a seed's own reference list, that is recorded and reported. Such a work is still assessed only against the arm registered for it: V7 (*A Pivotal Moment*), which is cited in the reference lists of seeds 7, 11 and 13, remains a test of the hand-searching arm.

## Other search strategies

The core method is a constrained snowball (Lecy & Beatty, 2012) combining the ascendancy approach (backward reference chasing) and the descendancy approach (forward citation chasing via OpenAlex) from the frozen seeds, iterated on records that pass relevance screening until saturation. We supplement with targeted hand-searching of key venue and organization websites for grey literature.

**Manual reference supplement (seeds only).** Where OpenAlex does not hold a seed's reference list, or holds less than 80% of it (raw counts; seed 20 included by definition; seed 14, a keynote abstract, has no reference list), the list is extracted from the seed's full text — for seed 7, a book, from its endnotes, excluding personal communications, "Ibid." and short-form repeats, each logged — and every reference is matched to OpenAlex: by DOI where one is given or derivable from an arXiv identifier; otherwise by title within one year of the reference's year — after removing venue text left on the end of the parsed title, by a search requiring every title word, and only where that returns no candidate by OpenAlex's relevance search, with such rows marked — accepted automatically only at normalized title similarity ≥ 0.90 with a matching first-author surname, whichever search supplied the candidate; and otherwise by hand, recording each reference as matched by hand, not in OpenAlex, grey literature, or rejected. A second team member checks every hand match and a random 10% of automatic title matches (recorded seed 20261028), and the confirmation rate is reported. Matched works enter the pre-deduplication pool as backward links from that seed, labelled `manual_pdf`; grey-literature items are passed to the hand-searching arm. The supplement restores backward links only and is applied to seeds, not to records chased in later rounds; where a chased record has no references or no citing works in OpenAlex, that is recorded per record and reported per round.

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

Fourth, facts established at the Search stage (Update 3 item 1.2; seed file `TPG_seed_set_v2.xlsx`). Seed 20 has no OpenAlex record. Seed 6 remains unpublished; its record holds no reference list. Seed 22's preprint and published records are not merged by OpenAlex. Seed 14 is a keynote abstract with no reference list and contributes forward citations only. At round 1, seeds 6, 7, 13, 22 and 23 returned no references from OpenAlex, and seeds 13 and 23 no citing works. Three "for good" seeds (15, 16, 18) account for 988 of the 1,423 forward links retrieved in round 1, so the "for good" tradition's coverage is concentrated in few seeds as well as being broader backward than forward. Per-seed and per-tradition yields are reported separately for the OpenAlex links and for the manual reference supplement. Where OpenAlex holds more than one record for a seed, the record its frozen identifier resolves to remains the expansion input, the other is recorded and reported, and the seed's forward set is reported as potentially incomplete.

**AI-use disclosure for the Search stage (per RAISE).** An AI assistant (Claude Opus 5.5, Anthropic, used in the Claude desktop application) was used to write the scripts that retrieve and check the expansion and match references to OpenAlex, to extract reference lists from seed full texts into structured files, and to compute reference counts. It made no eligibility judgment and no inclusion decision. Every extracted list was checked against the source's own numbering or count, every hand correction is recorded with the deposit, and every parsed field is subject to the matching review described under Other search strategies.

---

# Screening

*In this section, you register your screening procedure: the procedure you designed to eliminate all irrelevant sources from the results of the search strategy (and retain the relevant sources).*

## Screening stages

**Deduplication (pre-screening).** Pooled records from the citation-network expansion and keyword searches are de-duplicated by DOI and normalized title; the 23 frozen seed articles (already included) are removed from the candidate pool; and where a preprint and its published version both appear, the preprint is removed in favor of the published version. Deduplication is performed computationally (a script / reference-manager routine) with a human check of near-duplicates. Records identified only through the manual reference supplement are pooled with the expansion's records before deduplication and keep their provenance label, so that the PRISMA-ScR flow reports them as a separate identification source ("records identified from seed reference lists").

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

**Group 3 — Judgment-dependent fields.** C3 (constitutive technology), C4 (public benefit), C5 (funder program), and the five framework dimensions.

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

**What Update 2 fixed, and what followed it.** Update 2 fixed the composition of the register — which frames are in it, which are excluded and why — together with each frame's enumeration route and boundary definition, the standing rules, the screening criteria, the draw rule, and the stopping rule. It did not fix the contents of any frame. After it was filed, every frame was captured on 23 and 24 September 2026 and the register freeze date was recorded as 24 September 2026, at the close of capture; per-frame capture timestamps and file hashes are recorded in the capture log, and the snapshots are deposited in the OSF project and the repository. Enumeration and all subsequent stages follow the freeze.

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

No statistical power calculation applies. The five framework questions are piloted and revised before sampling begins, because preliminary work indicates they are difficult to answer as currently worded. This pilot is the same exercise as the coder calibration described under Screening Reliability, not an additional round: the questions are revised between the first and second calibration rounds, and the revised wording is the one carried into coding.

## Screening procedure justification

The two-stage design (title/abstract, then full text) is the standard, efficient approach that balances recall against workload. AI-assisted Stage 1 screening with mandatory human verification is justified by the potentially large candidate pool a citation-network expansion produces: it reduces reviewer workload while keeping decision authority with the human, and it is validated against blind human screening on a pilot before use (per RAISE). We do not blind bibliographic fields because scoping reviews do not require it and because the meta-narrative synthesis depends on venue, discipline, and author community to assign traditions; we mitigate the resulting prestige-bias risk with explicit, piloted criteria and by retaining borderline cases. Exclusion criteria follow directly from the PCC eligibility definition and are applied conservatively on relevance. Reliability is assured primarily through AI-validation against a blinded human pilot rather than full dual-human screening — a pragmatic choice for a small team, acknowledged as a limitation. Reconciliation always favors retention because, in evidence synthesis, a missed eligible study (false negative) is costlier than a wrongly retained one (false positive).

## Data management and sharing

We will openly share, on the OSF project for this registration:

(a) the full set of records identified through the searches, in BibTeX/RIS and CSV/XLSX;
(b) the screening log, recording for every record its AI recommendation, the human decision, the screening stage, any exclusion reason, and any author-conflict recusal, in CSV/XLSX;
(c) the frozen 23-article seed list;
(d) the final charted dataset; and
(e) for the organizational strand, the frozen frame register with each frame's enumeration route, boundary definition, and archived snapshot reference; the organizational screening log with the first criterion failed for every exclusion; the final organizational dataset with its codebook; and the reproducibility materials for the sampling procedure — the random seeds used for the draw rule, the boundary audits, and the supplementary probe, the resulting coding-queue order, and the script and frozen lexicon used to compute the lexicon proxy; and the organizational strand's AI materials — the model and version, the frozen prompts for each of the three roles, and the per-field log of every AI proposal against the human decision recorded for it, including the blind third coder's output, which is released with the dataset after adjudication is complete.

(f) for the Search stage, the raw OpenAlex responses and the per-request access log for every expansion round; the per-seed yields; the scripts used to retrieve, check and match; the extracted seed reference lists with their README, the source text used for page-derived lists, and the log of items dropped from seed 7's endnotes; seed 7's Bibliography; and the matching log, recording for every extracted reference its route, candidate, similarity score, review decision and reviewer, together with the verification sample and its confirmation rate. Full texts of seeds are not redistributed where their licences do not permit it.

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
8. **Citation data** — the source's references and citing works, used to compute within- vs. cross-tradition citation for the silo analysis. Citation data come from OpenAlex; for seeds, references obtained through the manual reference supplement are held as a separately labelled set (`manual_pdf`) and enter the silo analysis only in its sensitivity version (Update 3 item 2.6).

Fields not addressed by a source are charted as "not reported."

**Organizational strand.** Each organization is coded on its own instrument, recorded in the codebook attached to this registration. Fields comprise: provenance and screening (identifier, originating frame or frames, block, admission mechanism, frame type, date identified, the lexicon proxy used to stratify the coding queue, outcome on each of C1 to C5, screening decision, first criterion failed, merge target, unit-resolution outcome and note, frame-operator flag, frames operated, operator status); organizational status (active / dormant / closed, with date and a dated evidence artifact); tier and label (tier; the self-applied phrase recorded verbatim; the lexicon term or terms matched; the URL, access date, placement of the phrase, and whether the organization is describing itself or quoting a funder, partner, or news source); self-descriptive phrases that match no term in the frozen lexicon, recorded verbatim, with the same evidence requirements as a lexicon hit; functional role (ecosystem role; named partner organizations); the five framework dimensions; and descriptive fields (name, headquarters, focus, projects, founding year, mission, staff expertise, contact, legal form, funding sources, technologies).

The lexicon proxy records whether any frozen lexicon term appears in the text of the organization's own homepage, computed by automated text match at enumeration. It takes three values — true, false, and undetermined — because a page that could not be fetched or that yielded too little text to read has not established the absence of the vocabulary, and treating such a record as false would place it in the wrong stratum for a reason unrelated to how the organization describes itself. Undetermined records are resolved by hand before the queue is built. The proxy is a sampling aid only: it is not the tier assignment, which is a human judgment requiring the placement of the phrase and the identity of the speaker, and it is neither reported as tier nor used to prefill the tier field.

The lexicon of self-identification terms is frozen and recorded in the codebook. Every term derives from the manuscript's own taxonomy, so the instrument operationalizes the argument rather than importing vocabulary the study does not engage. Self-descriptive phrases are recorded verbatim before being matched to the lexicon, never the reverse, so that an unanticipated label surfaces as a finding rather than being recorded as an absence. Terms surfaced during the review that are absent from the lexicon are reported as findings and are not added to the lexicon mid-collection.

## Extraction stages

**(1) Training/pilot stage** — the charting form is piloted on 25 included sources, drawn to span the three traditions and the recorded source types; both the AI-assisted procedure and a human blind to the AI chart the same sources, so the AI can be validated (below), and the form and prompts are refined. Changes are recorded in a preregistration update (charting is iterative; Levac et al., 2010).

**(2) Final extraction stage,** using a two-tier AI-assisted workflow:

1. **Metadata (AI-assisted).** A large language model (Claude Opus 5) extracts the metadata entities (authors, year, title, venue, publication/source type). A human verifies these fields for all sources.
2. **Interpretive entities (AI recommends, human validates).** For tradition assignment, faceted classification, source role/type, the five framework dimensions, the source's key-term definition, and the meta-narrative themes, the model returns a recommended value with a supporting quotation/rationale, and a human validates every recommendation, giving heightened scrutiny where the model's rationale is weak or the evidence is thin. The model makes no autonomous charting decisions; the human retains final authority on every field.
3. **Citation data** are retrieved from OpenAlex, not from the LLM. OpenAlex is the sole provenance of the citation edge list used for the primary silo analysis; links from the manual reference supplement are labelled and used only in the sensitivity version of that analysis. Crossref is used for metadata validation and retraction screening only.

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

**AI-use disclosure (per RAISE, Responsible AI in Evidence Synthesis, 2025).** We will use a large language model, Claude Opus 5, accessed via API with fixed, archived prompts and default temperature settings, in two roles during data extraction: (a) to extract metadata, which a human will verify; and (b) to recommend values for interpretive fields (tradition, faceted classification, source role, the five framework dimensions, key-term definitions, and meta-narrative themes), each of which a human will validate, retaining final authority. The model will make no autonomous extraction decisions. Before the full run we will validate the model against blind human coding on the pilot set and will report per-field agreement (accuracy); the full run will proceed only if agreement meets the pre-specified thresholds, and otherwise we will revise the prompts/codebook and repeat the pilot. Because LLM outputs are non-deterministic and version-dependent, we will record and report the model version, access dates, and exact prompts. Citation data will be obtained from the citation index rather than the model, and no AI tool will be used for quality appraisal or synthesis decisions.

---

# Synthesis and quality assessment

*In this section, you register the procedure for the review's synthesis: the procedure you designed to use the data that was extracted from each source to answer your research question(s). This often includes transforming the raw extracted data, verifying validity, applying predefined inference criteria, interpreting results, and presenting results. Additionally, you register procedures you designed to assess bias in individual sources and the synthesis itself.*

## Planned data transformations

No effect-size conversion or numeric aggregation applies (this is a descriptive and interpretive review). We will transform the charted data by:

(a) tabulating the categorical entities into frequency counts and cross-tabulations (disciplinary home × application domain × normative lens, by tradition, and by publication year) to build the descriptive map;
(b) collapsing any residual free-text codes into the controlled vocabularies defined in the codebook;
(c) thematically coding the qualitative fragments (the five framework dimensions, key-term definitions, and meta-narrative themes) into higher-order themes following Braun & Clarke (2006); and
(d) assembling the extracted references/citations into a citation edge list among included sources for the network analysis, with each link labelled by provenance (OpenAlex or `manual_pdf`).

These transformations yield the main variables of interest specified in the Review Methods section.

## Missing data

Entities not addressed by a source are charted as "not reported" and retained as such; we will not impute missing values and will not contact authors to obtain them. Missingness is treated as informative — for example, a tradition that rarely specifies "who decides what social good means" is a finding — and we will report the proportion of "not reported" per field, noting it in denominators for descriptive counts. Analyses will proceed on available data, with any field too sparse to support a claim flagged rather than over-interpreted.

## Data validation

Charted values are validated against the source during the human-validation step of extraction; metadata are cross-checked against DOIs via Crossref; and we will screen included records against retraction registers (Crossref/Retraction Watch). A retracted record is excluded under exclusion criterion 6 and logged as such in the PRISMA-ScR flow; where the retraction is identified after charting, the record is removed from the analytic corpus and the removal is counted and reported. A record under an expression of concern is retained and flagged in the shared dataset. Interpretive codings are triangulated through the pilot AI–human agreement check and the verbatim-evidence requirement. Our validity criterion is that every coding be supported by explicit textual evidence; codings that fail this are re-coded or marked uncertain and excluded from claims that depend on them. Anomalous or inconsistent codings surfaced during synthesis are returned to the source for re-checking.

## Quality assessment

Consistent with scoping-review methodology (Arksey & O'Malley, 2005; Munn et al., 2018), we will not conduct a formal risk-of-bias or quality appraisal of individual sources (e.g., Cochrane RoB, GRADE), and we will not use source quality to weight inclusion or synthesis. This is a deliberate, documented choice: the review's aim is to map and interpret how a field conceptualizes itself, not to estimate an effect whose credibility depends on study quality. In place of quality appraisal, we characterize each source's type and role (survey, definitional, empirical, critical/position) descriptively, and — following RAMESES for the meta-narrative component — we appraise sources for their contribution to a tradition's storyline rather than their methodological rigor.

## Synthesis plan

The synthesis proceeds in four tiers, mapped to the research questions.

**Tier 1 — descriptive mapping (RQ1).** Numerical summary of the charted facets: distributions and cross-tabs across discipline, domain, and lens; a publication timeline; and identification of anchor/hub works. These distributions are reported as distributions over the assembled corpus and not as estimates of the composition of the TPG literature. The tradition composition of the seed set (6 civic technology, 7 public interest technology, 10 "for good") is reported alongside them, together with per-seed and per-tradition yields for the OpenAlex links and the manual reference supplement separately, and no claim is made that the relative sizes of the three traditions in the corpus reflect their relative sizes in the literature.

**Tier 2 — meta-narrative synthesis (RQ2).** For each tradition, reconstruct its storyline (origins/paradigm, definition of "the good," exemplars, trajectory) from the charted definitions and themes, using thematic analysis (Braun & Clarke, 2006) and reported per RAMESES.

**Tier 3 — cross-tradition synthesis (RQ3).** Compare the three traditions on the five framework dimensions; identify convergences and recurring tensions; and construct an integrated account of TPG.

**Tier 4 — citation-network analysis (RQ4, secondary).** From the citation edge list, compute within- vs. cross-tradition citation to test siloing, and cluster via co-citation / bibliographic coupling (CitNetExplorer / VOSviewer). The primary analysis uses OpenAlex-supplied links only; it is repeated with the manual reference supplement's links added, and both are reported (sensitivity analysis c).

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

Not applicable in the quantitative sense: with no pooled effect sizes, funnel plots, Egger's test, p-curve, and related corrections cannot be computed. We will instead address the analogous coverage and selection biases qualitatively — the dependence of the corpus on the seed set, including the tradition composition of that set; the chosen citation index; the incomplete indexing of preprint and proceedings seeds, and the absence from the index of several seeds' reference lists, which the manual reference supplement restores backward only; the recency of three seeds, which are correctly indexed but too recently published to have accumulated forward citations, so that the expansion is ascendancy-only for them and the corpus is covered less thoroughly forward than backward in the tradition holding those seeds; the English-language restriction; and the field's own publication practices (including reliance on grey literature and preprints) — and report these in the limitations, supported by the leave-one-out and index-sensitivity checks below.

## Sensitivity analyses / robustness checks

**Literature strand.**

- **(a) Seed leave-one-out** — re-run the expansion omitting each seed in turn to assess how dependent the corpus is on individual seeds.
- **(b) Index sensitivity** — compare corpus and citation results against Semantic Scholar, reporting the proportion of the corpus and of the citation edge list recoverable from it, so that the corpus's dependence on OpenAlex is measured rather than only acknowledged. Where the comparator's coverage of a source type is known to be limited, that is stated rather than treated as a discrepancy.
- **(c) Manual reference supplement** — report the corpus and the silo analysis with and without the links obtained through the manual reference supplement, and, because the 80% selection threshold was confirmed after the seeds' reference counts were seen, with seed 17's extracted reference list added (the nearest seed to the threshold, at 83%; this is what an 85% threshold would have produced). The leave-one-out check in (a) is run on the corpus including the supplement.

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
