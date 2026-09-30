# PICANTE O3 — Unit-resolution worksheet: instructions for RAs

Sep 30, 2026

## What you are doing

You are deciding, for 455 records, whether each one is already an organization or an institution that needs narrowing to a unit inside it. This is Rule 1 of the protocol: a university, government agency or corporate parent never enters the sample itself; the unit the frame names does.

The file is `organizations/O3_enumeration_and_deduplication/run/unit_resolution_worksheet.csv`. It lives on Jon's machine, not on GitHub. There is one row per record.

For every row, answer two questions in order:

1. Is this listing already an organization-level unit (a nonprofit, a company, a center, a lab, a project)? If yes, the answer is `AS_LISTED`.
2. If it is an institution, does **the frame's own text** name a unit inside it? If yes, `RESOLVED` to that unit. If no, `UNIT_UNRESOLVED`.

Rows arrive for one of three reasons, shown in `unit_resolution_note`: the whole frame lists institutions (all of PIT-UN and Ford), the frame names a fiscal sponsor (some McGovern rows), or the name looks like an institution (56 rows from CTFG, CFA, McGovern and Google.org).

## The columns

The first seven columns are context written by the script. **Never edit them.** `frame_listing_text` is your main evidence: for PIT-UN it holds the designee, their positions and the listed websites; for Ford and McGovern it holds the grant description.

| Column | Leave alone? | What it holds |
| --- | --- | --- |
| `source_key` | Yes | The record's ID; how your answer is matched back |
| `originating_frame` | Yes | Which frame the record came from |
| `name`, `website_url` | Yes | What the frame lists |
| `frame_listing_text` | Yes | The frame's own text about the record |
| `fiscal_sponsor_named` | Yes | Filled only if the frame names a fiscal sponsor |
| `unit_resolution_note` | Yes | Why the row is on the worksheet |
| `decision` | Fill in | `AS_LISTED`, `RESOLVED` or `UNIT_UNRESOLVED` |
| `resolved_unit_name` | Fill in for `RESOLVED` | The unit's name |
| `resolved_unit_url` | Fill in for `RESOLVED` | The unit's own website; needed at O5, so find it if you can |
| `resolution_basis` | Fill in for `RESOLVED` | Where in the frame the unit is named, e.g. "Designee's position: Director, Center for X" |
| `sponsor_routing` | Fill in if a sponsor is named | `PROJECT` or `SPONSOR` |
| `known_not_surfaced` | Optional | Units you know of that the frame does not name; separate several with `;` |
| `coder` | Fill in, every row | Your initials |
| `note` | Optional | Anything worth saying, including "for Jon" |

**The three decisions:**

- `AS_LISTED` — the listing is already an organization or a unit. Nothing about the record changes.
- `RESOLVED` — an institution, and the frame names a unit inside it. Name, URL and basis are all required. If the frame names several units, **copy the row once per unit** and mark each copy `RESOLVED`.
- `UNIT_UNRESOLVED` — an institution, and nothing in the frame names a unit. The record is counted but not coded.

**Fiscal sponsors.** Where `fiscal_sponsor_named` is filled, choose one routing, never both. `PROJECT` when the frame names the sponsored project and it could stand as an organization on its own; this is usually the listed grantee, so the decision is `AS_LISTED`. `SPONSOR` otherwise, with decision `RESOLVED` and the sponsor as `resolved_unit_name`.

## Worked examples

Rows marked *illustrative* are invented to show the reasoning; decide the real rows from their own listing text.

| Frame | Listing | What the frame says | Decision | What to fill in |
| --- | --- | --- | --- | --- |
| Ford | Candid | Grant: "General Support" | `AS_LISTED` | coder |
| CTFG | Tow Center for Digital Journalism at Columbia University | The name itself is a center | `AS_LISTED` | coder |
| CTFG | Citizen University | A nonprofit whose name contains "University"; flagged by name only | `AS_LISTED` | coder; note "name-flag false positive" |
| McGovern | University of Chicago (Nightingale Open Science) | The grantee name names the project | `RESOLVED` | name: Nightingale Open Science; its URL; basis: "Grantee name names the project" |
| McGovern | \[C\]Worthy | Fiscal sponsor: Convergent Research Inc.; grant: "to build open-source modeling infrastructure…" | `AS_LISTED` + `PROJECT` if \[C\]Worthy stands as its own organization; otherwise `RESOLVED` + `SPONSOR` | routing; if SPONSOR, the sponsor's name, URL and basis |
| PIT-UN | *Illustrative:* Example State University | Designee's position: "Director, Center for Civic Data" | `RESOLVED` | name: Center for Civic Data, Example State University; its URL; basis: "Designee's position" |
| PIT-UN | *Illustrative:* Example Tech | Designee heads Lab A; co-designee heads Center B | `RESOLVED`, split | two rows, one per unit, each with its own basis |
| McGovern | *Illustrative:* Big University | Grant text names no lab or program | `UNIT_UNRESOLVED` | coder; if you know the lab, put it in `known_not_surfaced`, not in the decision |
| CTFG | State of Vermont | A state government; the listing names no office | `UNIT_UNRESOLVED` | coder |

**A case to send to Jon.** Arizona State University's PIT-UN listing gives the designee as an associate vice provost and lists `pit.asu.edu` among its websites. Whether a program website listed by the frame counts as the frame naming that program is a judgment for Jon, not a call to make row by row.

## Rules

- **The frame's text is the only evidence for a decision.** A unit counts only if the frame itself names it: in the name, the listing text, the grant description or a listed website. What you know from elsewhere, or find by searching, goes in `known_not_surfaced`, never in the decision.
- **You may look up a URL.** Finding the website of a unit the frame already names is fine; choosing the unit from outside knowledge is not.
- **Never edit the context columns, change a `source_key`, or delete a row.** Copying a row to split it is the only structural change allowed.
- **Every row needs a decision and your initials.** A blank row is not an `AS_LISTED` row.

**When unsure:** leave `decision` blank and write "for Jon" in `note`, with one line on what is unclear. Jon decides. The script refuses to run while any row is blank, so nothing slips through undecided.

**The UVA row (PIT-UN).** Everyone on the team is affiliated, so this row follows a special procedure:

1. Each of you resolves it separately, on your own copy of the row, before comparing.
2. Record both answers and their bases in `note`.
3. If either of you finds a unit the frame names, use it. Only if neither does is it `UNIT_UNRESOLVED`. This keeps the team from resolving its own institution out of the sample.
4. Jon does not take part in this row.

**Who takes which rows** (decided 2026-09-30): **Akshita** takes Ford (258 rows). **Carmen** takes PIT-UN, McGovern, CTFG, CFA and Google.org (197 rows). **Both** resolve the UVA row, separately. Where the same institution appears in both halves (a university that is a Ford grantee and also in McGovern or PIT-UN), compare notes so it is resolved the same way.

The split balances effort rather than rows. Of Akshita's 258 Ford rows, 35 have institution-like names and need real Rule 1 work; most of the rest should be quick `AS_LISTED` calls. Nearly all of Carmen's 197 rows need judgment. If Carmen falls well behind, move the 28 name-flagged CTFG, CFA and Google.org rows to Akshita; keep PIT-UN and McGovern together, since they share many universities.

## Saving and handing back

- **In Excel, save as "CSV UTF-8"**, not plain "CSV". Plain CSV on a Mac garbles accented names such as *Señora* or *Université*.
- **Keep a backup copy** before you start and at the end of each session. The script that made the worksheet overwrites it if it is run again.
- **When you finish,** give the file back to Jon. He runs `apply-resolutions`, which checks every row and names any row with a problem: a blank decision, missing initials, a `RESOLVED` row without a basis, or a sponsor row without a routing. Fix those rows and hand it back again.
