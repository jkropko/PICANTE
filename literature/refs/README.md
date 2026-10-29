# refs/ — reference lists extracted from seed PDFs

Input for `match_references.py match refs/ round1/ manual/`.

Extracted 2026-10-28 from the open-access full texts below, using `extract_refs.py`
(text layer -> segmented entries -> parsed first author, year, title, DOI). The raw
reference text is kept in every row; parsed fields are heuristic and are checked at review.

| File | Seed | Source | Entries | With DOI | Complete? |
|---|---|---|---|---|---|
| seed07.csv | 7 Schank & McGuinness 2021 | Project MUSE PDF supplied by the team (not open access) | 129 | 0 | Endnotes — see below |
| seed06.csv | 6 Zhang et al. 2022 | arxiv.org/pdf/2204.11461 | 91 | 78 | Yes (numbered [1]–[91]) |
| seed13.csv | 13 Knodel et al. 2025 | arxiv.org/pdf/2508.07230 | 79 | 54 | Yes (numbered [1]–[79]) |
| seed16.csv | 16 Tomašev et al. 2020 | nature.com/articles/s41467-020-15871-z (reference list on public page) | 70 | 15 | Yes (numbered 1–70) |
| seed18.csv | 18 Cowls et al. 2021 | nature.com/articles/s42256-021-00296-0 (reference list on public page) | 27 | 14 | Yes (numbered 1–27) |
| seed20.csv | 20 Arora & Sarkar 2023 | ceur-ws.org/Vol-3582/FP_06.pdf | 102 | 91 | Yes (numbered [1]–[102]) |
| seed22.csv | 22 Karamolegkou et al. 2026 | PDF supplied by the team (aclanthology.org/2026.eacl-long.238) | 484 | 0 | Yes (Abdul-Mageed … Zogan; pp. 10–36, ends before Appendix A) |
| seed23.csv | 23 Nemkova et al. 2026 | arxiv.org/pdf/2605.22995 | 26 | 0 | Yes (author–year; ends before Appendix) |

## Seeds 16 and 18 (added 2026-10-28)

Selected by the threshold check: the publisher lists 70 references for seed 16 against 26 in
OpenAlex (37%), and 27 for seed 18 against 16 (59%). Both reference lists were taken from the
article pages (full text is paywalled for seed 18), parsed with extract_refs_nature.py; DOIs
come from the publisher's own [Article] links. The page text used is kept in `_sources/`
(the seed 18 section was saved from the fetched page text, preserving entries and links).

- **Seed 16 #68 carries a publisher error.** It cites Orife et al. 2020 (Masakhane) but links
  arXiv:1810.08810, which is Chouldechova & Roth (#45). The identifier is blanked so the entry
  is matched by title, not to the wrong work.
- Seed 16 #57 (Socher et al. 2013) cites a NeurIPS volume without a paper title; resolve by hand.
- Seed 18 #24 is seed 15 (Floridi et al. 2020). The link is kept; seeds are removed at
  deduplication.
- Seed 18 #21 and #26 are the same Strubell et al. 2019 work cited twice (proceedings and
  arXiv); they will resolve to one or two OpenAlex records depending on merging.

## Threshold check status (other seeds)

Publisher reference count vs OpenAlex backward count (round 1): seed 2, 65 vs 73 (covered);
seed 15, ~85–87 vs 75 (~87%); seed 17, ~87 vs 70 (~80%, borderline). Not yet counted: seeds
1, 3, 4, 5, 8, 9, 10, 11, 12, 19, 21.

## arXiv identifiers

Where an entry gives an arXiv identifier and no DOI, the doi column holds the matching
arXiv DOI (10.48550/arXiv.NNNN.NNNNN), so the entry is matched by exact lookup instead of title.
The identifier in the raw text is unchanged.

## Known gaps

- **Seed 22 was re-extracted from the full PDF** (replacing an earlier partial version).
  The two-column layout interleaves entries that cross a column break in plain text
  extraction, so each page's left and right columns were extracted separately (pdftotext
  cropping, pp. 10–36) before parsing. One merge was fixed by hand: Olsen et al. 2024 and
  Intergovernmental Panel on Climate Change 2022 (an organizational author with no comma)
  were split into rows 314 and 315. The paper has a single bibliography, so citations in the
  appendices are covered. No DOIs are given; 73 entries carry arXiv identifiers, and every
  entry goes through title matching.
- **Seed 14 has no file because it has no references.** The PDF (supplied by the team) is a
  one-page SIGIR '18 keynote abstract and speaker bio, with no reference list. OpenAlex's zero
  backward count is therefore correct, not an index gap. Seed 14 contributes forward citations
  only (10 in round 1). Note: the seed file classes it as "Survey"; it is a keynote abstract.
- **Seed 7 uses the book's endnotes** (decision 2026-10-28). 237 notes across the Preface and
  Chapters 1–7, numbering checked complete, became 129 unique cited works. Dropped, with every
  item logged in `_logs/seed07_endnotes_dropped.csv`: 69 personal communications (author
  interviews, e-mails), 30 "Ibid.", 11 short-form repeats or commentary, each confirmed to have
  its full citation elsewhere in the notes. Extracted with extract_refs_endnotes.py.
- **26 of the 32 Bibliography entries are not cited in any endnote** (e.g. Eubanks 2018,
  Noveck 2015, Goldsmith 2017, Gawande 2009). The Bibliography works as a further-reading list,
  not a subset of the notes. It is kept at `_alternates/seed07_bibliography.csv` (not read by
  match_references.py). Whether to add it is open; see the decision note in the update.
- Rows 14, 58 and 79 are discursive notes or unpublished internal analyses, not citable
  works; mark them not_in_openalex at review. Row 30 combines interviews with a Government
  Technology article; match it to the article.
- **Seed 7, endnote 1 cites validation work V7** (Freedman Consulting 2016, *A Pivotal
  Moment*). V7 tests the hand-searching arm. If the endnotes are used, record that V7 is
  also reachable through seed 7 by hand, and still assess V7 against hand-searching only.
- **Seeds with partial OpenAlex coverage** can only be identified once every seed's PDF
  reference count is compared with `yields.csv`. Add files for any seed the rule selects.

## Parsing caveats for reviewers

- Titles are cut at the first sentence-ending punctuation followed by a capital, so titles
  containing "?" mid-title (e.g. seed 23 #2 "Power to the People? Opportunities…") are
  truncated. Title matching will fall below threshold and flag them; resolve by hand.
- Non-scholarly entries (seed 22 #96, a bill; #166, a web page) will come back unmatched;
  mark them grey_literature or not_in_openalex.
- Seed 23 #6 and #7 are the same Floridi et al. 2020 work listed twice in the source.
  match_references.py adds each link once.
- Accented names may show spacing artifacts from the PDF text layer (e.g. "Cosi c").
  Only the first author's surname is used in matching.
