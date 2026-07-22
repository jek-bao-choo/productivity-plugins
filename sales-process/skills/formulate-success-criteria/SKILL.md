---
name: formulate-success-criteria
description: >-
  Formulate POC/evaluation success criteria, current challenges, and future
  states from customer meeting notes and/or call transcripts, then produce a
  filled copy of the 2025 success criteria .xlsx template (columns: Success
  Criteria, Current Challenge, Future State, Product(s) Tested). Grounds each
  current challenge in what the customer actually said, formulates outcome-based
  success criteria and [DD] Datadog future states, and asks clarifying questions
  when the notes are unclear. Use when the user asks to create, formulate, draft,
  or build success criteria, or mentions "success criteria", "current challenge",
  "future state", a success criteria template/spreadsheet, or wants to turn
  meeting notes / a transcript into success criteria.
version: "0.1.0"
author: Jek Bao
tags: success-criteria, current-challenge, future-state, poc, evaluation, sales, meeting-notes, transcript
---

# Formulate Success Criteria

Turn customer meeting notes and/or call transcripts into a filled copy of the
success criteria workbook. The output is a `.xlsx` file based on the template in
`references/success-criteria-template.xlsx` with one row per success criterion,
populating four columns: **Success Criteria**, **Current Challenge**,
**Future State**, and **Product(s) Tested**. The **Validated Y / N** and
**In-app Recording** columns are left blank for the SE to fill in later.

## The #1 rule: ground challenges, formulate outcomes

- **Current Challenge must come from the notes/transcript.** Do not invent a pain
  the customer never expressed. If it is not in the input, it is not a challenge —
  ask about it (see Step 3) or leave it out.
- **Success Criteria and Future State may be formulated.** Once a challenge is
  grounded in the input, you may write a polished, outcome-oriented success
  criterion and a Datadog-oriented future state, even if the customer did not
  phrase it that way. This is the value of the skill.
- **Never invent products the customer's context does not support.** Only map to
  Datadog products that plausibly address a stated challenge.
- **Follow the column style guide below**, not fabricated content. Mirror the
  voice of each column; never invent details the customer's input does not support.

## Inputs

The user provides one or more of:
- **Meeting notes** (pasted text, a file, bullet points from a discovery call)
- **Call transcript** (raw or cleaned)
- Both

There may also be an account/customer name. If none can be identified, use
`unnamed` and proceed (do not block on it).

## Workflow

### Step 1: Ingest the input

Acknowledge what you received (notes, transcript, or both) and read all of it.
Extract the customer/account name for the output filename if present.

### Step 2: Extract current challenges (grounded)

Read through the input and pull out the customer's actual pains, gaps, and
frustrations. Typical signals: tool sprawl / consolidation, reactive detection
("customers report issues first"), slow/manual triage, alert fatigue, no
centralized logging, no end-to-end visibility, high MTTD/MTTR, cost/FinOps
pressure, security/compliance gaps, SLO/reporting needs.

Group related pains into distinct challenges — each challenge becomes one row.

### Step 3: Clarify when unclear (ask, do not guess)

Before formulating, decide whether the input is clear enough. **Ask the user
targeted clarifying questions** (use the AskQuestion tool when available) if any
of these are true:

- The challenges are vague or high-level with no concrete detail.
- It is unclear which Datadog products/solution areas are in scope.
- A stated pain could map to several very different success criteria.
- The input is too thin to formulate meaningful, testable criteria.

Keep it to a few focused questions at a time. Wait for answers before continuing.
If the input is already clear and specific, skip straight to Step 4.

### Step 4: Formulate each row

For each grounded challenge, formulate:

1. **Success Criteria** — outcome-oriented and testable, from the customer's
   desired-outcome perspective. Use a short headline (e.g. `Decrease MTTD/MTTR`,
   `Tool Consolidation`) or a numbered/bulleted list of concrete capabilities to
   validate, matching the depth of the input.
2. **Current Challenge** — the grounded pain from Step 2, in the customer's
   context. Preserve their specifics (tool names, environments, numbers).
3. **Future State** — how Datadog resolves it. Prefix with `[DD]` and name the
   specific Datadog products/capabilities that deliver the outcome. Keep it
   concise and benefit-led (single pane of glass, reduced MTTR, lower TCO,
   proactive detection).
4. **Product(s) Tested** — the Datadog products/pillars in scope for that row
   (e.g. Infrastructure Monitoring, APM, Log Management, RUM, DBM, NPM, CCM, CSM,
   Monitors/SLO/Event Management).

Use the column style guide below for phrasing patterns and apply the voice only
where the customer's input supports it.

### Step 5: Preview for approval

Present the proposed rows as a **Markdown table** (Success Criteria | Current
Challenge | Future State | Product(s) Tested) so the user can review and edit.
Ask whether to adjust anything before generating the workbook. Incorporate edits
and re-preview if requested.

### Step 6: Generate the filled workbook

On approval, write the rows to a JSON file and run the fill script:

```bash
python3 scripts/fill_success_criteria.py \
  --rows /tmp/success-criteria-rows.json \
  --output success-criteria/<customer>/success-criteria-<customer>-<ISO-date>.xlsx
```

Where the rows JSON is a list of objects:

```json
[
  {
    "success_criteria": "Decrease MTTD/MTTR",
    "current_challenge": "Issues are reported by customers first; triage is slow and manual.",
    "future_state": "[DD] Datadog correlates APM traces, logs, infra metrics, and RUM in one place to detect issues proactively and cut MTTD/MTTR.",
    "products": "Infrastructure Monitoring, APM, Log Management, DBM, NPM, Incident Management"
  }
]
```

The script is stdlib-only (no installs), copies the branded template, appends one
row per entry with the template's styling preserved, and leaves Validated Y/N and
In-app Recording blank. Report the output path and row count to the user.

## Column style guide (from the validated examples)

| Column | Voice |
|---|---|
| Success Criteria | Outcome-oriented; short headline or bulleted/numbered testable capabilities |
| Current Challenge | Customer's pain in their own context; grounded in the notes; may use Before/After structure |
| Future State | `[DD]`-prefixed, benefit-led, names the specific Datadog products that deliver the outcome |
| Product(s) Tested | Datadog products/pillars in scope for that row |

## Files

- `references/success-criteria-template.xlsx` — blank branded template (base for output)
- `scripts/fill_success_criteria.py` — fills the template from a rows JSON file
