# Agenda Slide (slide 2) and Benefits Trackers (slides 6, 9, 12, 15, 21, 24)

The agenda is a four-column table with a timeline down the left. The same table comes back
after each part of the demo as a **benefits tracker**, so the customer sees their benefits
build up as the demo goes on. All seven slides are built by `scripts/build_agenda.py` from
one JSON spec, never by hand-editing, so the layout, colours and row sizing stay
consistent.

## Structure

Title: **Agenda for <Customer>**, using the real prospect or customer name from the notes.

Always exactly six parts, in this order. Keep the rule of three: three use-case parts,
no more, no fewer.

| # | Part | Use case column | Colour |
|---|------|-----------------|--------|
| 1 | Intro & Whiteboard | — | orange |
| 2 | Observe | Use Case 1 pill | blue |
| 3 | Act | Use Case 2 pill | purple |
| 4 | Secure | Use Case 3 pill | red |
| 5 | Why Datadog | — | orange |
| 6 | Next Steps & Close | — | green |

Columns: **PART** · **USE CASE** · **CUSTOMER QUESTION** or **FROM MY NOTES** · **WHAT DEMONSTRATES IT**

## Mapping use cases to Observe, Act, Secure

- **Observe**: the visibility or detection use case (see the problem before customers do).
- **Act**: the response or remediation use case (find the cause and fix it faster).
- **Secure**: the security or protection use case.

Order the three use cases from the notes to fit these parts. If the notes have no
security use case, or the three use cases do not fit Observe, Act and Secure, ask the user
in Step 1 how to map them. Do not silently rename the parts; only set a part's `label`
override when the user has agreed to a different name.

Use case titles are short outcome statements, not product names
("See failing bill payments before customers call", not "RUM and APM").

## The third column: Customer Question vs From My Notes

Decide once for the whole column:

- **Notes contain customer questions or quotes** → set `"has_customer_questions": true`.
  The header reads **CUSTOMER QUESTION**.
  - Verbatim customer words → `"style": "quote"`. The script adds curly quotes.
  - A customer concern from the notes with no verbatim wording → rephrase it as a short
    question, `"style": "question"` (rendered italic).
- **Notes contain no customer questions or quotes** → set `"has_customer_questions": false`.
  The header reads **FROM MY NOTES**. Use short points from the notes with `"style": "note"`.

Rules:

- Never invent a quote. Only use `quote` for words the notes attribute to the customer.
- Set `attribution` (role, for example "Head of Platform" or "VP Eng, CTO") only when the
  notes say who said it. Prefer roles over personal names.
- One to three items per row, within the word limits in
  [writing-style.md](writing-style.md): quotes 20 words (trim with "…", keeping the
  customer's exact words), questions 15, notes 12, attribution 4. Split a double question
  into two short ones: "Another tool to live in? Can we trust AI with bank data?"

## What Demonstrates It

The Datadog products, features or artefacts that answer that row, joined with " · ".

- **Intro & Whiteboard**: the success criteria count when the notes have them
  ("6 success criteria"); otherwise what the whiteboard covers
  ("Current vs target whiteboard").
- **Observe / Act / Secure**: the products shown in that use case's demo.
- **Why Datadog**: what answers the customer's platform or trust objections
  (for example Slack, MCP, Pup CLI, Bits Testing).
- **Next Steps & Close**: the concrete next step being proposed (for example "PoC + QVA").

Two to five entries per row, four words each at most. Only list products that appear in
the notes or the demo plan.

## Benefits trackers

After each part, show the agenda again with a **BENEFITS TO <CUSTOMER>** column in place
of the customer questions:

| Columns | PART · USE CASE · BENEFITS TO <CUSTOMER> · WHAT DEMONSTRATES IT |
|---|---|
| Parts already covered | Full colour, benefits and products shown |
| The part just covered | Highlighted: tinted card, coloured border, halo on its timeline dot |
| Parts still to come | Dimmed grey, benefits and products hidden |

Six trackers, one at the end of each part (slides 6, 9, 12, 15, 21, 24). The last one,
after Next Steps & Close, has every row filled in and doubles as the full benefits recap.
Row heights are computed from all six parts' benefits, so the rows stay in the same place
on every tracker slide.

Benefit rules:

- Two or three lines per part, each a short outcome in the customer's terms, 8 words at
  most ("Engineering knows before the call center", not "RUM alerts").
- Derive benefits from the notes: the pain each part removes, the success criteria it
  proves. Never invent numbers; only quote a figure (MTTR, cost) that is in the notes.
- Intro & Whiteboard benefits are about the shared starting point
  ("Bitsburg's own numbers on the table", "6 success criteria agreed up front").
- Next Steps & Close benefits are about the path forward
  ("A clear path to value", "PoC + QVA proves the 6 criteria").
- Propose the benefits in the Step 2 plan and let the user adjust them before building.
- `customer_short` sets the name in the column header ("BENEFITS TO BITSBURG");
  it defaults to `customer`.

## Spec format

```json
{
  "customer": "Bitsburg Bank",
  "customer_short": "Bitsburg",
  "has_customer_questions": true,
  "parts": {
    "intro": {
      "items": [{"text": "We have the data. We do not have the answers. Someone still has to go and look.", "style": "quote"}],
      "attribution": "Head of Platform",
      "demonstrates": ["6 success criteria"],
      "benefits": ["Bitsburg's own numbers on the table", "6 success criteria agreed up front"]
    },
    "observe": {
      "use_case": "See failing bill payments before customers call",
      "items": [
        {"text": "Why does the call center hear about failed payments before engineering does?", "style": "question"},
        {"text": "Is the fraud agent healthy, and what is it costing us?", "style": "question"}
      ],
      "demonstrates": ["Journey Monitoring", "RUM", "APM", "LLM Observability", "Bits Detection"],
      "benefits": ["Engineering knows before the call center", "AI fraud agent health and cost in view"]
    },
    "act": {
      "use_case": "Restore failed bill payments faster, under governance",
      "items": [
        {"text": "Half of our incident time is spent... proving that the network or legacy core did not cause the problem.", "style": "quote"},
        {"text": "Both grouped the alerts and stopped there.", "style": "quote"}
      ],
      "demonstrates": ["Bits AI SRE investigation", "approval + audit trail", "verified recovery"],
      "benefits": ["Wrong suspects ruled out with evidence", "Named approver and a full audit trail"]
    },
    "secure": {
      "use_case": "Protect customers from account compromise",
      "items": [{"text": "The hard part is determining which one is real before an attacker, or a customer, feels the impact.", "style": "quote"}],
      "attribution": "CTO",
      "demonstrates": ["Cloud SIEM", "Bits AI Security Analyst"],
      "benefits": ["The real threat found among normal logins", "Analysts review a verdict, not raw logs"]
    },
    "why_datadog": {
      "items": [{"text": "Another tool to live in? Can we trust AI with bank data?", "style": "question"}],
      "demonstrates": ["Slack", "MCP", "Pup CLI", "Bits Testing"],
      "benefits": ["No new tool to live in", "Bank-grade trust built in"]
    },
    "next_steps": {
      "items": [{"text": "Is this a new way of operating, and a platform worth standardizing on?", "style": "question"}],
      "attribution": "VP Eng, CTO",
      "demonstrates": ["PoC + QVA"],
      "benefits": ["A clear path to value", "PoC + QVA proves the 6 criteria"]
    }
  }
}
```

All six part keys, a `use_case` for observe/act/secure, at least one item and at least one
`demonstrates` entry per part are required, plus `benefits` for every part when building a
tracker. Text over the word limits, more than 3 items or benefits, more than 5
`demonstrates` entries, and dash-joined clauses are errors too. The script exits with a
list of every problem; shorten them and rerun.

## Build

Run after the deck's structural changes (Step 4) and before the other text edits.

1. Create the six trackers by duplicating the agenda slide, one at a time. After each
   `add_slide.py`, insert the printed `<p:sldId>` into `<p:sldIdLst>` right after the last
   slide of its part (slides 5, 8, 11, 14, 20, 23 of the final flow) **before** running the
   next one; back-to-back duplicates otherwise get the same ID and packing fails.

   ```bash
   python3 $SCRIPTS/add_slide.py unpacked/ slide2.xml   # → e.g. Created slide21.xml; insert its sldId
   ```

2. Build the agenda and each tracker:

   ```bash
   python3 $SCRIPTS/build_agenda.py unpacked/ agenda.json                                 # slide2.xml
   python3 $SCRIPTS/build_agenda.py unpacked/ agenda.json --benefits intro       --slide slide21.xml
   python3 $SCRIPTS/build_agenda.py unpacked/ agenda.json --benefits observe     --slide slide22.xml
   python3 $SCRIPTS/build_agenda.py unpacked/ agenda.json --benefits act         --slide slide23.xml
   python3 $SCRIPTS/build_agenda.py unpacked/ agenda.json --benefits secure      --slide slide24.xml
   python3 $SCRIPTS/build_agenda.py unpacked/ agenda.json --benefits why_datadog --slide slide25.xml
   python3 $SCRIPTS/build_agenda.py unpacked/ agenda.json --benefits next_steps  --slide slide26.xml
   ```

   Use the file names `add_slide.py` actually printed. `--benefits` refuses to overwrite
   `slide2.xml`, so the agenda itself cannot be turned into a tracker by mistake.

The script keeps the title and slide-number placeholders, replaces every other shape on
the slide, sizes rows to their content and shrinks fonts together (down to 72%) if the
table would run into the Datadog footer. It prints the font scale it used and warns if the
content still does not fit; shorten items rather than accept the warning.

## Visual check

Read the rendered agenda slide in Step 5 and confirm:

- The title shows the real customer name, not "Bitsburg Bank" or a placeholder.
- The third column header matches the notes (Customer Question vs From My Notes).
- All six rows sit above the Datadog footer logo; no text touches a card or pill edge.
- On each tracker, the highlighted row is the part just covered, earlier rows show their
  benefits, later rows are dimmed, and the rows do not shift between tracker slides.
- The font scale printed by the script is 80% or more. Below that the body text is hard
  to read when presenting: cut items or shorten them and rebuild.
