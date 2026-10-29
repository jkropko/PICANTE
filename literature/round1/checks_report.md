# Round-1 checks

Run 2026-10-28 23:08 UTC.

## 1. Seed resolution

| Seed | OpenAlex ID | Title match | Flag |
|---|---|---|---|
| 1 | W2625441184 | 1.00 |  |
| 2 | W2803741631 | 0.71 | CHECK BY HAND |
| 3 | W2954061405 | 1.00 |  |
| 4 | W2945957289 | 1.00 |  |
| 5 | W3109719383 | 0.49 | CHECK BY HAND |
| 6 | W4224935343 | 1.00 |  |
| 7 | W4234973976 | 0.47 | CHECK BY HAND |
| 8 | W3174021967 | 1.00 |  |
| 9 | W3196559827 | 1.00 |  |
| 10 | W3175045805 | 1.00 |  |
| 11 | W4399039118 | 1.00 |  |
| 12 | W4403775069 | 1.00 |  |
| 13 | W4416241850 | 1.00 |  |
| 14 | W2811457281 | 0.71 | CHECK BY HAND |
| 15 | W3014499801 | 0.91 |  |
| 16 | W3025490408 | 1.00 |  |
| 17 | W3174262803 | 1.00 |  |
| 18 | W3129979751 | 1.00 |  |
| 19 | W4388400861 | 1.00 |  |
| 20 | — | — | not resolved (expected only for seed 20) |
| 21 | W4405205175 | 1.00 |  |
| 22 | W7140094533 | 1.00 |  |
| 23 | W7162295528 | 1.00 |  |

## 2. Per-seed yields

Forward should equal cited_by_count (a gap means paging stopped early or the index changed mid-run). Zero backward on an indexed seed means OpenAlex holds no reference list for it: record as materially incomplete (prereg 1.6).

| Seed | Backward | Forward | cited_by_count | Viability (seed file) | Flag |
|---|---|---|---|---|---|
| 1 | 27 | 34 | 34 | Expected normal |  |
| 2 | 73 | 66 | 66 | Expected normal |  |
| 3 | 66 | 76 | 76 | Expected normal |  |
| 4 | 22 | 20 | 20 | Expected normal |  |
| 5 | 48 | 15 | 16 | Expected normal | forward ≠ cited_by_count (+1) |
| 6 | 0 | 5 | 5 | Expected normal | no references indexed |
| 7 | 0 | 2 | 2 | Expected normal | no references indexed; low forward for a 'normal' seed |
| 8 | 74 | 47 | 47 | Expected normal |  |
| 9 | 13 | 21 | 22 | Expected normal | forward ≠ cited_by_count (+1) |
| 10 | 54 | 11 | 12 | Expected normal | forward ≠ cited_by_count (+1) |
| 11 | 38 | 12 | 12 | Expected normal |  |
| 12 | 17 | 3 | 3 | Expected normal | low forward for a 'normal' seed |
| 13 | 0 | 0 | 0 | LIMITED — too recent | no references indexed |
| 14 | 0 | 10 | 10 | Expected normal | no references indexed |
| 15 | 75 | 425 | 430 | Expected normal | forward ≠ cited_by_count (+5) |
| 16 | 26 | 354 | 356 | Expected normal | forward ≠ cited_by_count (+2) |
| 17 | 70 | 22 | 22 | Expected normal |  |
| 18 | 16 | 209 | 212 | Expected normal | forward ≠ cited_by_count (+3) |
| 19 | 81 | 12 | 13 | Expected normal | forward ≠ cited_by_count (+1) |
| 21 | 73 | 77 | 80 | Expected normal | forward ≠ cited_by_count (+3) |
| 22 | 0 | 2 | 2 | LIMITED — too recent | no references indexed |
| 23 | 0 | 0 | 0 | LIMITED — too recent | no references indexed |

## 3. Preprint and published records

Seed 22: published record W7140094533, preprint record W4416048247 -> **NOT MERGED**. Preprint has 0 citing works not in seed 22's forward set; report its forward set as incomplete (prereg 2.5).

Seed 6 (arXiv): cited_by_count 5.

Seed 13 (arXiv): cited_by_count 0.

Seed 23 (arXiv): cited_by_count 0.

## 4. Search validation (pre-deduplication pool)

| V | Arm | Counts | OpenAlex ID | In pool | Reached via | Status |
|---|---|---|---|---|---|---|
| 1 | Citation-network expansion | Yes | W2406178417 | True | seed 5 backward | recovered |
| 2 | Citation-network expansion | Yes | W2084779139 | True | seed 5 backward | recovered |
| 3 | Citation-network expansion | Yes | W4281606481 | True | seed 11 backward, seed 15 forward | recovered |
| 4 | Citation-network expansion | Yes | W2898730196 | False |  | not yet reached (would be (c) if still absent at saturation) |
| 5 | Citation-network expansion | Yes | W2140150066 | False |  | not yet reached (would be (c) if still absent at saturation) |
| 6 | Targeted hand-searching | No  | — | — | — | hand-searching arm: check at that stage |
| 7 | Targeted hand-searching | No  | — | — | — | hand-searching arm: check at that stage |
| 8 | Citation-network expansion | NO  | W2008251417 | True | seed 3 backward | recovered |

Expansion-counting works (V1–V5) not reached in round 1: **2**. Threshold for adding a targeted query: 2 unreachable at saturation.

## 5. Pool quality

- Records (pre-dedup, seeds included): 1955
- Missing abstract: 488 (25%) — these need full text at Stage 1
- Missing DOI: 74
- Flagged retracted by OpenAlex: 2 ['W4390245066', 'W4319296160']
- Normalized titles appearing more than once: 50 (candidate duplicates for the human check)
- Types: {'article': 1074, 'book-chapter': 329, 'conference-paper': 255, 'preprint': 76, 'book': 57, 'review': 54, 'book-review': 23, 'editorial': 20, 'paratext': 20, 'other': 14, 'dissertation': 11, 'reference-entry': 9, 'report': 7, 'conference-abstract': 2, 'dataset': 2, 'data-paper': 1, 'erratum': 1}
- Languages: {'en': 1879, 'ng': 17, 'pt': 12, 'es': 11, 'de': 8, 'fr': 8, 'uk': 5, 'it': 4}
