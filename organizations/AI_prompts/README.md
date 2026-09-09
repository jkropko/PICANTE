# Organizational strand — AI role prompts

Three prompts, one per registered role. They are drafts for you to review, revise and freeze; nothing here is registered until you freeze it and record the version.

| File | Role | Fields | Gate |
| --- | --- | --- | --- |
| `role1_mechanical_extraction.md` | Role 1 | Group 1 mechanical, including C1 and C2 | 95% field-level accuracy before any analytic record |
| `role2_evidence_location.md` | Role 2 | Group 2 self-label block — **passages only, no values** | Passage recall reported, no gate |
| `role3_blind_judgment_coding.md` | Role 3 | Group 3 — C3, C4, C5, the five dimensions | No gate; never contributes to a coded value |

## Freeze order

Roles 1 and 2 can be frozen now. **Role 3 cannot.** All five framework dimensions arrive marked PILOT with no rubrics, and sheet 1 item 4.4 commits you to rewording them or adding rubrics between the two calibration rounds. Role 3's dimension section is therefore a marked placeholder: draft it now so the harness can be built and tested, paste in the calibration rubrics after O6 round two, then freeze and version it before any analytic record is coded. Freezing it earlier would freeze rubrics that do not yet exist.

Role 1's gate has the same ordering problem in reverse, which is why you moved its validation ahead of O4: it must be validated against a hand-coded set before it runs over the enumerated pool, not against the O6 calibration set.

## Conventions shared by all three

**Page text is data, never instruction.** Every input is scraped from an organization's own site. Each prompt states that text inside the source blocks is evidence to be read, and that any instruction appearing inside it is to be ignored and reported. This matters more here than in most pipelines: you are feeding roughly 1,800 uncontrolled pages to a model whose output enters a research dataset.

**No prior knowledge.** The model will recognize many of these organizations — Code for America, DataKind, Ford grantees. Each prompt forbids using anything not present in the supplied text. This is the single most likely source of silent error in the strand, because a plausible value drawn from memory reads exactly like a correct one and an RA verifying against the source may find it confirmed there for the wrong reason.

**Evidence is a verbatim substring with offsets.** Every proposed value carries at least one quote that must appear as an exact substring of the source it cites, with start and end character offsets. This is what makes the sheet 4.3 fidelity check programmatic: reject the field automatically and route it to a human when the quote does not match, rather than trusting the model's claim that it does.

**Undetermined is always available and never penalized.** Each schema includes it, and each prompt says explicitly that absence of evidence is a finding, not a gap to be filled.

**One record per call.** No batching. Batching invites cross-contamination between records and makes the per-field log ambiguous.

## Input envelope (same for all three roles)

```json
{
  "org_id": "CTFG-0417",
  "sources": [
    {
      "source_id": "S1",
      "url": "https://example.org/",
      "access_date": "2026-11-03",
      "capture_ref": "https://web.archive.org/web/2026.../https://example.org/",
      "text": "…extracted visible text, exactly as stored…"
    }
  ],
  "frame_listing": {
    "frame_code": "CTFG",
    "listing_text": "…the frame's own entry for this organization, verbatim…"
  }
}
```

Offsets are character positions into `sources[i].text`, counted from zero on the exact string you supply. Store that string with the record: if the text is re-extracted later the offsets stop meaning anything.

`frame_listing` is supplied to Role 1 only. Roles 2 and 3 do not need it and giving it to them imports the frame's framing into a judgment that should rest on the organization's own words.

## Logging

The registration commits you to a per-field log of every AI proposal against the human decision. Log, per field per record: role, prompt version, model string, the raw response, the parsed value, the evidence quote and offsets, whether the fidelity check passed, the human decision, and whether the human overrode the model. Role 3's output is logged at the time it is produced but withheld from all three humans until the adjudicated human value is recorded.

## Temperature

The registration says fixed archived prompts and **default temperature settings**. That is what these prompts assume. If you would rather have run-to-run determinism, temperature 0 is a deviation from the registered configuration and belongs in a preregistration update — it is a small change to file and a cheap one to defend, but it is not a silent one.

## Model string

Record `claude-opus-5` with the exact API version string returned by the call, plus access dates, per the RAISE disclosure.
