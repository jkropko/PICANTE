# Organization Data Collection Methodology

## Why are we collecting data on civic tech / PIT / tech for good organizations?

Generally, we are trying to characterize the entire field of study and practice of applying technology for good causes. Describing the academic literature only gets us part of the way there. Most of this work is conducted by organizations, and we miss a big part of the story if we ignore them.

We are trying to address two specific research questions:

1. How do these organizations describe their work? What phrases do they use? Are they connecting and forming movements around terminology that we don't see yet?

2. For these organizations, we are trying to answer the same questions that we pose in the literature review: how do they define "social good" and who do these projects serve? Who is deciding that? Who is invited to participate? And what counts as technology?

## What we did last time: a mix of strategies

- Snowball sampling (seeing new organizations that are referred to by others)
- Keyword searching (Googling it)
- Geographical stratification (at least one org from each of the top census MSA regions)
- AI scraping and annotation

## Where it failed us

- We couldn't be sure that we were using search terms that gave us a complete picture of the space. We probably missed big parts of the field because we didn't have the language.
- We found it very hard to record and explain what we did and why. That was going to bite us in the butt for writing the paper and passing peer review.
- It was partly arbitrary. Some organizations were borderline. It created judgment calls that other team members wouldn't have made the same way. Or it turned into a huge time-wasting exercise if we come up with better rules on the fly and go back and re-evaluate everything according to the new rules, only to find another problem we'd have to go back and fix.
- We probably weren't going to pass journals' new standards for where AI is allowed and not allowed.

## So we need a strategy that accomplishes the following

- It gives us a finite number of organizations to draw from, instead of an infinite pool of endless googling.
- It gives us clear rules for which organizations make the cut and which don't.
- It hits organizations that originate from different traditions: civic tech, PIT, tech for good.
- But it doesn't require us to conduct a whole big fat census of all eligible organizations, or make claims about the overall proportion of organizations that come from each source.
- It allows a lot of flexibility in terms of language, so that different ways of thinking can emerge instead of being ignored by us because we used the wrong search terms.
- It gives us a reasonable stopping rule so that we don't have to manually code every organization.
- It puts AI exactly where a human can check its work cheaply, and keeps it away from the judgments that make this study worth doing — which is also what the newly widely-adopted rules require (https://osf.io/fwaud/overview).

---

# Here's the new plan

## Step 1: Start from eight frames

We start with eight organizations that support or fund many other groups and publish a list of them, and that situate themselves in one of Public Interest Tech, Civic Tech, or tech "for good." Those combined lists are our starting point. We call these eight "frames."

- PIT University Network
- Ford Foundation
- Civic Tech Field Guide
- Alliance of Civic Technologists
- Code for America (archived)
- Fast Forward
- McGovern Foundation
- Google.org (four named cohorts)

Not all of these publish the same kind of list, and the difference matters. Some are membership rosters, where an organization chose to put itself on the list. Others are grants databases or accelerator cohorts, where a funder picked the organization. We record which kind each record came from, because "we chose to call ourselves this" and "somebody gave us money" are different facts and we don't want to blur them together.

## Step 2: Pull the rosters and merge duplicates

We pull all affiliated organizations from the eight frames' lists and put them into a CSV.

**We work from a frozen snapshot, not the live sites.** Every list is captured on one fixed date, and that date is chosen before anyone looks at what's inside any of them. From then on, the snapshot is the list. If you notice a new member on a live site while you're working, don't add it — the pool is fixed.

We then search for duplicates, because one organization can fall under more than one umbrella, and merge duplicated rows. We have an `originating_frame` feature that can take on multiple values, and **merging must preserve all of them.** An organization claimed by both Ford and the Field Guide is one of the most interesting records we have, and that's only visible if we keep both frames on it.

## Step 3: The two cheap screening criteria

Many of the organizations on these lists will not really be the kinds of organizations we think of as PIT, civic tech, or tech for good. We have five screening questions to narrow down the field, and some are much easier to check than others. We do the two easy ones now, on everything, and save the three hard ones for later.

**Screening criterion 1.** Does the organization have its own name, its own web presence, and evidence of staffing or governance? If not, remove it and don't consider criterion 2.

**Screening criterion 2.** Is the organization based in the US (headquarters or principal operations)?

AI does the first scan, proposes answers, and provides citations. RAs verify the findings. **No proposal can be accepted without the organization's website being opened.**

### A note on what these lists actually contain

Some frames list institutions rather than organizations. PIT-UN lists universities. Ford lists grants. When you hit one of these:

- Resolve the record to whichever unit **the frame itself names** — a center, a program, a project, a designated representative's stated affiliation. That unit is the record. The parent university or agency does not enter the sample.
- If the frame names no unit at all, log it as `unit_unresolved` and move on.
- **If you happen to know of a qualifying unit that the frame doesn't name, do not add it.** Log it as `unit_known_not_surfaced` and move on. This one feels wrong, so here's why: if we add organizations we happen to know about, the boundary of our sample depends on which of us was assigned the record and what we each happened to have heard of. We can't reproduce that or describe it in a paper. Logging it turns invisible under-coverage into a number we can report.

After this stage, only records that pass both criteria continue to Step 4.

## Step 4: Run the lexicon script

We run a Python script that scrapes the remaining organizations' websites. It uses fixed regular expressions to check whether at least one of a small lexicon of relevant terms appears on the page. For every website we get TRUE (a lexicon term was found) or FALSE (the page was read and no terms were found). If a record comes back UNDETERMINED because the page couldn't be scraped, we resolve it by looking at the website ourselves. **UNDETERMINED is not FALSE** — a page that failed to load hasn't told us anything about the organization's vocabulary, and coding it FALSE would put it in the wrong bucket for a reason that has nothing to do with how the organization describes itself.

**What's the point of doing this?** Not to find out what organizations call themselves — that comes later, when you read the page and record their exact words. This is a sorting device. Some organizations use our vocabulary and some don't, and the ones that don't are where the interesting language is. If we didn't sort on this, we could easily code sixty organizations that all describe themselves as civic tech, hit our stopping rule, and never reach the ones that describe the same work some other way.

## Step 5: Build the strata

The eight frames, crossed with the TRUE and FALSE values from the lexicon search, give us sixteen "strata" or buckets. We randomize the order in which organizations within each bucket are drawn, using a recorded seed.

We will rotate across the buckets in the steps that follow, which keeps us working across all of them instead of being consumed by the largest ones. The Civic Tech Field Guide alone is about 60% of the pool; without rotation we would effectively be studying that one directory. This is a standard move — Palinkas et al. (2015) call it stratified purposeful sampling, and it's the recognized way to make a purposive sample span the variation you care about instead of piling up wherever the records are densest.

## Step 6: Calibration round one — the three harder screening criteria

We are almost ready to start coding, but first we have to get on the same page about how we make coding decisions — both for the remaining screening criteria and for the variables we want to code.

**Drawing the calibration set.** We draw **six organizations from each block** — eighteen in total — using a separate recorded seed, so the analytic queue built in Step 5 is left untouched. Within each block we spread the draw across that block's strata and make sure both TRUE and FALSE lexicon values are represented, since that's what tests the hard judgments. We don't take one from every stratum: Block A has only four strata against six in the other blocks, and Block A is where the unit-resolution rule bites hardest, so a per-stratum draw would leave the block that most needs calibrating with the fewest records.

These eighteen organizations are **set aside permanently.** They never enter the results, no matter how they code.

This two-part structure — a first set used to build the categories, then a rule for how many more records we'll code without anything new appearing — follows Francis et al. (2010), who call the two pieces the *initial analysis sample* and the *stopping criterion*. Our calibration rounds are the first; the six-in-a-row rule in Step 10 is the second. Their point is that both numbers should be declared before collection, not chosen afterwards.

Then we apply the three harder screening criteria:

**Screening criterion 3.** Is this a tech organization, or an organization that uses tech but isn't really about tech? In other words, if you removed technology from the organization's description, would the organization still exist? If it would, it fails.

**Screening criterion 4.** Does the organization work for the public, or for its own members (the way a chamber of commerce works for its member businesses)? For-profit companies only pass this if the public-benefit commitment is structural — public-benefit corporation status, B-Corp certification, or something equivalent written into their articles or bylaws. A mission statement or a values page is not enough.

**Screening criterion 5.** (Funders only.) Do they run a program or portfolio that explicitly describes itself as being about technology? Write `N/A` for everyone who isn't a funder.

In the full dataset we stop as soon as an organization fails one criterion and don't look at the rest. **But in calibration we each code all three for all eighteen**, so we can compare our answers on every criterion. If we stopped at the first failure, we'd barely have any codings of criterion 4 to compare.

## Step 7: Calibration round one — everything else

For the same eighteen organizations, **regardless of how they scored on the screening criteria**, we each code all the other variables and generate our own ideas of rubrics. Then we meet, compare, and agree on a unified rubric.

Coding the excluded ones matters. An organization that fails criterion 3 still has a mission, a stated beneficiary, and an implied answer about who decides — and if our rubric only works on organizations that clearly belong, we want to find that out now rather than in month three.

A few fields on the list below aren't coded by hand at all — `org_id`, `block`, `date_identified`, and `lexicon_proxy` are assigned mechanically when the record enters the pool. They're listed so you know what's in the dataset, not because you fill them in.

### Provenance and sampling

- `org_id` — stable unique key, assigned after deduplication to the organization-level unit
- `originating_frame` — which frame or frames surfaced this organization; multiple values allowed, and merging duplicates must preserve all of them
- `block` — A (PIT), B (civic tech), or C ("for good"); operator and probe records sit outside the blocks
- `admission_mechanism` — how the organization entered its frame: self-declaration, selection, affiliation, or none
- `frame_type` — what kind of list surfaced it: identity roster, coalition, funder portfolio, accelerator, corporate philanthropy
- `date_identified` — when the organization entered the candidate pool
- `unit_resolution_flag` — `resolved`, `unit_unresolved`, or `unit_known_not_surfaced` (see Step 3)
- `unit_resolution_note` — one line explaining the flag; required whenever it isn't `resolved`
- `frame_operator` — TRUE if this organization runs one of our frames
- `frame_operated` — which frames it operates
- `operator_status` — whether the frame it runs is current or historical
- `lexicon_proxy` — TRUE, FALSE, or UNDETERMINED from the Step 4 script. A sorting device for the queue; never reported as tier

### Status

- `status` — active, dormant, or closed
- `status_date` — date of the most recent activity, or of closure
- `status_evidence` — the specific dated artifact supporting the call, with URL and access date

**Dormant and closed organizations stay in the sample.** This will feel like a mistake the first few times. It isn't. If we dropped the dead ones, every finding we report would secretly be a finding about survivors — and this field has been contracting, so the organizations that closed are part of the story.

### Self-label and non-lexicon description

- `self_label_verbatim` — the exact phrase the organization applies to itself, quoted
- `self_label_lexicon_hit` — which of the twelve frozen lexicon terms it matched
- `nonlexicon_self_description` — a categorial self-description matching no lexicon term, recorded verbatim, one entry per phrase. **Do not normalize it toward a lexicon term or toward another organization's wording.** This field carries our first research question. Once all coding is finished, we pool every one of these phrases and sort them into categories, following Braun and Clarke's (2006) thematic analysis done inductively — the categories come up out of the phrases rather than being decided in advance. Akshita and Carmen each build categories independently over the whole set and Jon adjudicates. No AI is used at that step, because a model grouping the phrases would impose exactly the vocabulary the step exists to escape
- `self_label_url` — the page the phrase appears on
- `self_label_access_date` — date accessed, with an archived capture
- `self_label_placement` — homepage, about, mission, annual report, or other; guards against blog and job-post false positives
- `self_label_speaker` — the organization describing itself, or quoting a funder, partner, or news source
- `tier` — Tier 1 self-applies a lexicon label; Tier 2 does the work with none of the vocabulary. **Both are included.** See the explanation below

#### What tier is, and why Tier 2 organizations stay in

Tier records one thing: does the organization use our field's vocabulary about itself, or not?

**Tier 1** means somewhere on its own site, describing itself, the organization uses one of the twelve frozen lexicon terms — "we're a civic tech nonprofit," "a public interest technology organization," "we build tech for good."

**Tier 2** means a frame nominated this organization, it does recognizably the same kind of work, and it never uses any of those words. It describes itself some other way, or in no categorical way at all.

Tier 2 organizations are not failures or edge cases to be cleaned out. They may be the most valuable records we collect. The whole premise of this project is that the field is fragmented by vocabulary — that people doing the same work call it different things and don't find each other. If we only kept the organizations that already speak our language, we'd be proving our own premise by construction, and we'd never see the alternative vocabularies that answer research question one.

**An example.** Suppose the Code for America brigade roster surfaces a small volunteer group in Ohio. You open their site. Their About page says:

> *"We're neighbors who build simple tools for local government. We meet Tuesdays."*

That's Tier 2. No lexicon term appears anywhere — not "civic tech," not "govtech," not "open government." But they were on a civic tech roster, they build tools for public institutions, and they'd pass every screening criterion. They stay in, they get coded on everything, and their phrase — *neighbors who build simple tools for local government* — goes in `nonlexicon_self_description`, verbatim, exactly as written. Do not tidy it into "civic tech volunteers." That phrase is data.

Now suppose their homepage banner instead read *"Columbus's civic tech brigade."* Tier 1, `self_label_verbatim` is "civic tech brigade," `self_label_lexicon_hit` is "civic tech," placement is homepage, speaker is self.

**Three things that trip people up.**

*The lexicon script's TRUE/FALSE is not the tier.* The script only checked the homepage for a pattern. Tier is your judgment after reading the site. An organization can come back FALSE from the script and be Tier 1 because the phrase sits on their About page. It can come back TRUE and be Tier 2 — see the next point.

*Who is speaking matters.* If a grantee page says *"the Ford Foundation supports our work as part of its public interest technology portfolio,"* that phrase belongs to Ford, not to them. The organization hasn't called itself anything. Record `self_label_speaker` as `other`, and that phrase does not make them Tier 1.

*Where it appears matters.* A phrase in a job posting or a two-year-old blog post is weaker evidence than one in the mission statement. That's what `self_label_placement` is for. A term that appears only in a job ad usually isn't self-identification.

### Framework dimensions

These five are the same five we code on the literature side, so that we can compare what the field writes against what the field does. They are adapted from Arnstein's (1969) ladder of citizen participation, which we use as a shared analytic axis — a way of asking the same questions of everyone — not as a scale that ranks anybody.

- `who_participates` — who the organization treats as taking part in its work
- `who_benefits` — who the work is understood to be for. Not the same as the next field: an organization can define the good as something broad and diffuse while the people it actually serves are a narrow, named group, and that gap is worth seeing
- `what_counts_as_social_good` — how the organization defines the good it pursues
- `who_decides` — who is positioned to determine what counts as good: the organization itself, its funder, a board, a partner institution, or the community served. Expect this one to be `undetermined` more often than any of the others, because organizations rarely say out loud where that authority sits. That's a result, not a failure
- `what_counts_as_relevant_technology` — what the organization treats as the relevant technology of its work. This is about conceptual scope, not tooling: a group whose "technology" is a text-message hotline and a group whose "technology" is a machine-learning pipeline are answering this differently. **Not the same as the `technologies` field below**, which just records what they actually use

**Why `who_decides` is its own field.** Arnstein's ladder is a ladder of one thing: who holds the power to decide. Its whole point is that you can involve people without giving them any say — that's what she calls tokenism. If participation and decision authority sat in the same field, we couldn't record the case we most want to find: an organization that consults its community and still reserves every real decision to itself or its funder.

### Functional role

- `ecosystem_role` — practices, funds, studies, trains, convenes; multiple allowed, fixed list, not the same as legal form. Coded on every record, but it is **not** part of the stopping rule

### Functional and descriptive

- `partner_orgs_named` — host or partner organizations the record itself names; also the source list for the partner probe
- `ctfg_networks` — network affiliations from the Field Guide export, verbatim, CTFG records only; populated on ~9%, so a blank means nothing
- `name`, `hq`, `focus`, `projects`, `founded`, `mission`, `expertise`, `contact` — basic descriptive facts
- `org_form` — nonprofit, for-profit, government, university, or public-private partnership; what the organization *is*, not what it does
- `funding_foundations`, `grants`, `other` — funding sources as publicly reported
- `technologies` — the technology types the organization actually uses, six-way select: SE (software engineering / product build), DS (data science, analytics, ML/AI), OD (open data, open source, civic data infrastructure), UX (design, research, service design), POL (policy, governance, standards, procurement), HW (hardware, devices, connectivity). Descriptive only — this is *what they use*, not the `what_counts_as_relevant_technology` dimension above

**If you can't determine a field, write `undetermined` and a short note. Don't guess.** How often a field comes back undetermined is itself a result — it tells us what organizations do and don't disclose.

## Step 8: Calibration round two

We repeat Steps 6 and 7 on eighteen more organizations, drawn the same way, to confirm the rubrics are working. **Fresh organizations, not the same ones** — re-coding the first set would only tell us whether we remember what we agreed.

Same workflow as round one: all three of us code everything independently, all three screening criteria on every record, all variables regardless of screening outcome. What changes is what we do with the result. Round one produced the rubrics; round two tells us whether they work. After these eighteen we meet and assess how well we're agreeing.

We measure agreement with Cohen's kappa — the proportion of records we coded identically, *after subtracting the agreement two people would get by guessing*. Our benchmark is 0.60, which Landis and Koch (1977) label "substantial." We also report plain percentage agreement on any field where one answer dominates: if 95% of organizations get the same code, two coders can agree almost every time and still produce a kappa near zero. That's a known artifact of the statistic rather than a sign we're coding badly — Feinstein and Cicchetti (1990) named it, and reporting both numbers is the standard response.

These eighteen are also set aside permanently. Thirty-six organizations total leave the pool through calibration.

## Step 9: Code the rest

Now we start entering data for each organization, one at a time, rotating across the strata in the randomized order fixed in Step 5.

**Two things change from calibration, and they matter.**

**First: Akshita and Carmen now code independently and do not discuss records with each other.** On the screening criteria 3, 4 and 5 and on the framework dimensions, you each code every record on your own, and Jon resolves the disagreements. This will feel unhelpful and it is the entire point — if you talk it through first, your answers agree because you talked, and the agreement numbers we report stop meaning anything. Ask Jon, not each other.

**Second: an AI model also codes those same fields, blind.** Its answers are withheld from all three of us until the human answer is final. Do not go looking for them. If you saw the model's answer before coding, your judgment and Carmen's would both be shaped by it, and again the agreement number would be measuring the model rather than us. We report the model's agreement separately, as a check on the model.

Also: from here on, we **do** stop at the first screening failure. An organization that fails criterion 3 is excluded, and you don't code criteria 4 and 5 or any of the other variables for it. Record which criterion it failed.

### How each field gets coded in this stage

**Provenance and sampling** — `org_id`, `originating_frame`, `block`, `admission_mechanism`, `frame_type`, `date_identified`, `unit_resolution_flag`, `unit_resolution_note`, `frame_operator`, `frame_operated`, `operator_status`
AI proposes a value with its supporting passage; one RA opens the source and accepts, corrects, or marks it undetermined. Jon re-checks a random 10% per block.

**`lexicon_proxy`**
No AI and no coder — the fixed pattern-matching script from Step 4 produced this already.

**Status** — `status`, `status_date`, `status_evidence`
AI proposes with a passage; one RA verifies against the source.

**Self-label block** — `self_label_verbatim`, `self_label_lexicon_hit`, `nonlexicon_self_description`, `self_label_url`, `self_label_access_date`, `self_label_placement`, `self_label_speaker`
AI points to candidate passages with their exact character spans and proposes no value. One RA reads the page and decides every field. Anything the model returns as a quote is automatically rejected unless it matches the page exactly.

**`tier`**
The RA's judgment alone. The model contributes nothing here, not even a suggestion, because tier depends on where the phrase sits and who is speaking. Jon re-derives tier from the recorded phrase, placement, and speaker for every record.

**Framework dimensions** — `who_participates`, `who_benefits`, `what_counts_as_social_good`, `who_decides`, `what_counts_as_relevant_technology`
Akshita and Carmen each code independently for every record, without conferring. Jon adjudicates every disagreement. The model codes separately in the dark, withheld until the human value is final.

**`ecosystem_role`**
AI proposes from the fixed five-value list with a passage; one RA verifies.

**Functional and descriptive** — `partner_orgs_named`, `ctfg_networks`, `name`, `hq`, `focus`, `projects`, `founded`, `mission`, `expertise`, `contact`, `org_form`, `funding_foundations`, `grants`, `other`, `technologies`
AI proposes with a passage; one RA verifies against the source.

## Step 10: The stopping rule

There are three blocks of organizations: public interest technology, civic tech, and tech for good. Within a block, we code organizations until **six in a row produce no new value** on any of these five fields:

- `who_participates`
- `who_benefits`
- `what_counts_as_social_good`
- `who_decides`
- `what_counts_as_relevant_technology`

Then we stop coding that block. We're finished when all three blocks have hit the rule.

Why six? A rule like this needs a number fixed in advance, and ours is lower than you'll see in most qualitative work — Guest et al. (2006) found saturation around twelve interviews, and Hennink and Kaiser's (2022) review of the empirical literature puts it in the nine-to-seventeen range. Two things let us go lower. First, we aren't interviewing anyone; we're coding public text against a rubric we already built in Steps 6–8, so the categories aren't being discovered from scratch. Second, and more importantly, every one of these five fields is coded twice and adjudicated. Malterud et al. (2016) call this *information power* — the more each record tells you, the fewer records you need — and double coding is exactly that. It's also why a stray novel answer from one coder can't reset our counter.

Four details on the count:

- Only an **adjudicated** new value resets the counter. A new category one of you proposes that Jon adjudicates away doesn't move it.
- **An `undetermined` value does nothing to the counter** — it doesn't reset it, and it doesn't count toward the six. Undetermined means the evidence didn't reach the question, which isn't the same as the question having stopped producing new answers. Without this rule, six organizations in a row that simply don't say who decides would stop a block for the wrong reason.
- Organizations excluded at criteria 3, 4 or 5 don't count toward the six — they were never coded on these fields, so they can't tell us whether new answers are still appearing.
- The count is per block. Block A can finish while Block C keeps going.

`ecosystem_role` is **not** on this list, though you still code it on every record. It's a fixed list of five values rather than a rubric we build at calibration, so it can't produce a genuinely new code — it can only register the first time a block sees a funder or a convener. That happens early and then never again, and in the meantime a single first-of-its-kind convener could reset the counter on a record whose answers were otherwise completely familiar.

If a block runs out of organizations before six in a row come back empty, that's a finding about how thin that tradition's organizational layer is, and we report it as one. We don't go add more frames to fill it out.

---

## References

Most of what's above is standard practice rather than something we invented. These are the sources behind the choices that might otherwise look arbitrary.

**Arnstein, S. R. (1969).** A ladder of citizen participation. *Journal of the American Institute of Planners*, 35(4), 216–224. https://doi.org/10.1080/01944366908977225
Where the five framework dimensions come from. Arnstein's ladder is explicitly a ranking, ordered on one quantity — decision authority — which is why `who_decides` stands on its own. We borrow the ladder's questions as a shared axis, not its ordering.

**Braun, V., & Clarke, V. (2006).** Using thematic analysis in psychology. *Qualitative Research in Psychology*, 3(2), 77–101. https://doi.org/10.1191/1478088706qp063oa
The method behind the inductive coding of non-lexicon phrases.

**Feinstein, A. R., & Cicchetti, D. V. (1990).** High agreement but low kappa: I. The problems of two paradoxes. *Journal of Clinical Epidemiology*, 43(6), 543–549. https://doi.org/10.1016/0895-4356(90)90158-L

**Cicchetti, D. V., & Feinstein, A. R. (1990).** High agreement but low kappa: II. Resolving the paradoxes. *Journal of Clinical Epidemiology*, 43(6), 551–558. https://doi.org/10.1016/0895-4356(90)90159-M
Why we report percentage agreement alongside kappa on lopsided fields.

**Francis, J. J., Johnston, M., Robertson, C., Glidewell, L., Entwistle, V., Eccles, M. P., & Grimshaw, J. M. (2010).** What is an adequate sample size? Operationalising data saturation for theory-based interview studies. *Psychology & Health*, 25(10), 1229–1245. https://doi.org/10.1080/08870440903194015
The shape of our design: an initial analysis sample to build the categories, then a stopping criterion, both declared in advance.

**Guest, G., Bunce, A., & Johnson, L. (2006).** How many interviews are enough? An experiment with data saturation and variability. *Field Methods*, 18(1), 59–82. https://doi.org/10.1177/1525822X05279903
The benchmark study on where saturation actually falls in practice.

**Hennink, M., & Kaiser, B. N. (2022).** Sample sizes for saturation in qualitative research: A systematic review of empirical tests. *Social Science & Medicine*, 292, 114523. https://doi.org/10.1016/j.socscimed.2021.114523
A review of 23 empirical tests of saturation — context for why six is defensible but on the aggressive side.

**Landis, J. R., & Koch, G. G. (1977).** The measurement of observer agreement for categorical data. *Biometrics*, 33(1), 159–174. https://doi.org/10.2307/2529310
Source of the 0.60 benchmark. "Substantial" is their word for the 0.61–0.80 band.

**Malterud, K., Siersma, V. D., & Guassora, A. D. (2016).** Sample size in qualitative interview studies: Guided by information power. *Qualitative Health Research*, 26(13), 1753–1760. https://doi.org/10.1177/1049732315617444
Why double coding lets us stop sooner: more information per record means fewer records needed.

**Palinkas, L. A., Horwitz, S. M., Green, C. A., Wisdom, J. P., Duan, N., & Hoagwood, K. (2015).** Purposeful sampling for qualitative data collection and analysis in mixed method implementation research. *Administration and Policy in Mental Health and Mental Health Services Research*, 42(5), 533–544. https://doi.org/10.1007/s10488-013-0528-y
Stratified purposeful sampling — the logic behind the sixteen buckets and the rotation.

**Responsible AI in Evidence Synthesis (RAISE) (2025).** Guidance and recommendations. Open Science Framework. https://osf.io/fwaud/
The rules governing where AI can and cannot be used, and what has to be disclosed. RAISE 1 (recommendations for practice) and RAISE 3 (selecting and using tools) are the relevant parts for us.

---

## Additional methodological references

You don't need these to do the work. They're here because reviewers will eventually ask why our sampling is built the way it is, and these are the sources that answer that. Each names, in survey-methods language, something the plan above does in plain language.

**Hartley, H. O. (1962).** Multiple frame surveys. *Proceedings of the Social Statistics Section, American Statistical Association*, 203–206. (Conference proceedings; no DOI.)
The origin of *multiple-frame sampling* — drawing one sample from several overlapping lists rather than one complete list. That is exactly our eight-frame register, and it is why an organization appearing on two lists is a feature to record rather than a duplicate to discard. Hartley's literature also develops estimators that correct for overlap; we deliberately do not use them, since we make no population estimates. Citing it lets us say what we're not doing and why.

**Kalton, G., & Anderson, D. W. (1986).** Sampling rare populations. *Journal of the Royal Statistical Society, Series A (General)*, 149(1), 65–82. https://doi.org/10.2307/2981886
The standard reference for the situation we're actually in: there is no list of "US technology-for-public-good organizations," and the population is too thin to find by sampling the general population. Kalton and Anderson review the available responses — screening, disproportionate sampling, multiple frames, snowballing — which is a fair description of the menu we chose from. The design's whole shape follows from having no frame for the population itself, only frames related to it.

**Heckathorn, D. D. (1997).** Respondent-driven sampling: A new approach to the study of hidden populations. *Social Problems*, 44(2), 174–199. https://doi.org/10.2307/3096941
The best-known alternative to what we're doing, and worth citing precisely because we rejected it. Chain-referral methods follow links from one member to the next when no frame exists. Our partner probe is a deliberately limited cousin of that: we follow named-partner links out of the frame set, but only to check vocabulary, with no denominator and no population estimate attached. Naming this preempts the obvious reviewer question — "why not just snowball?" — and the answer is that our previous attempt did, and it produced a sample nobody could describe.
