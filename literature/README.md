# Search stage — literature strand

`tpg_search.py` runs the Search stage as registered in Preregistration Update 3 (items 3.1–3.5). It uses only the Python standard library and `openpyxl`, and writes everything to one SQLite database: every retrieved record, every parent through which each record was reached, each generation's screening pool, and a log of every API request with its timestamp (the API key is redacted).

## Before the first run

1. Put your email in `search_config.json` (OpenAlex's polite pool). If you have an OpenAlex API key, set it as the environment variable `OPENALEX_API_KEY`; it is never written to the database.
2. Record seed 20's identifier, as Update 3 C6 requires. Add it to `seed_identifier_overrides` as `{"20": "W…"}`, or `{"20": "none"}` if no usable identifier exists. Until you do, `resolve` stops before making any request.
3. If seed 6 has a published version, add `"seed 6": ["10.48550/arXiv.2204.11461", "<published DOI>"]` under `merge_checks`.
4. Run the tests: `python3 test_tpg_search.py`.

## Order of use

| Step | Command | Registered in |
| --- | --- | --- |
| Load seeds and validation set | `python3 tpg_search.py init` | — |
| Resolve seeds; preprint merge checks | `python3 tpg_search.py resolve` | items 1.6, 2.5; C6 |
| Generation 1 | `python3 tpg_search.py gen1` | item 3.1 |
| Keyword arm (same time as gen 1) | `python3 tpg_search.py keyword` | item 3.4 |
| Hand-search list, component 3 | `python3 tpg_search.py handsearch-list` | item 3.5 |
| Validation, V1–V4 | `python3 tpg_search.py validate --generation 1` | item 3.3 |
| Export for screening | `python3 tpg_search.py export --generation 1 --out gen1.csv` (and `--arm keyword`) | — |
| Pilot draw (after dedup) | `python3 tpg_search.py sample dedup_gen1.csv --n 100 --seed <S> --out pilot.csv` | Screening stages |
| Pilot extension | same command with `--offset 100 --n 50` and the same seed | Update 2, item 2.6 |
| Load full-text includes | `python3 tpg_search.py load-includes includes_gen1.csv` | — |
| Stopping rule | `python3 tpg_search.py status` | item 3.1 |
| Generation 2 (refused if the rule says stop) | `python3 tpg_search.py gen 2` | item 3.1 |
| Validation, V5 | `python3 tpg_search.py validate --generation 2` | item 3.3 |
| Drift-check draw | `sample` on that generation's export, with its own recorded seed | item 3.2 |
| Leave-one-out | `python3 tpg_search.py loo` | item 3.3 |

The includes file has three columns: `openalex_id`, `arm` (`expansion`, `keyword` or `handsearch`), and `generation` (blank for the keyword and hand-search arms). An expansion include that wasn't in that generation's screening pool is rejected.

## Safeguards built in

- `gen1`, each later generation, and the keyword arm refuse to run twice.
- Generation 4 is refused, and a later generation is refused when the stopping rule says stop. `--override-stop` exists only so that a deviation can be run and reported, not hidden.
- Keyword-arm and hand-search includes neither seed later generations nor count toward the two-link threshold.
- `sample` sorts the pool before shuffling, so a draw depends only on the seed, not on file order. An extension with `--offset` continues the same random sequence.
