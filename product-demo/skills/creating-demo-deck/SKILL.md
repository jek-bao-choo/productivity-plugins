---
name: creating-demo-deck
description: >-
  Create a Datadog-branded product demo deck from meeting notes, built as a
  Claude Artifact with its Datadog presentation styles. Use when the user asks
  to "create a demo deck", "generate a pptx", "build a Datadog presentation",
  "turn my meeting notes into slides", or mentions producing a customer demo
  presentation. Runs a fixed pipeline: answering-rfp first (every tech stack
  item and whether Datadog supports it), then creating-solution-architecture,
  then a 28-slide deck from both outputs, with a six-part agenda (Intro &
  Whiteboard, Observe, Act, Secure, Why Datadog, Next Steps & Close), a
  benefits tracker after each part, the architecture diagram, a tech stack
  backup slide, concise wording limits, and a mandatory review.
version: "0.5.0"
---

# Create Datadog Demo Deck

Turn customer meeting notes into a Datadog-branded demo deck. The deck is the last of
three deliverables, always produced in this order:

1. **`answering-rfp`** turns the notes into an RFP response CSV that states, for **every
   known tech stack item**, whether Datadog supports it.
2. **`creating-solution-architecture`** draws the architecture diagram from the notes and
   the RFP output.
3. **This skill** builds the deck as a **Claude Artifact**, using the Artifact's Datadog
   presentation styles and format, from the notes, the RFP output and the architecture.

Never start a later stage before the earlier one has finished and saved its output. This
file holds everything the deck stage needs: the pipeline, the slide flow and layouts from
the 2026 Datadog Presentation Template, the agenda, tracker and stack designs, the wording
rules, the review checklist, and test prompts.

**Keep every word on the deck concise, succinct, and short.** The audience should read a
slide in seconds and then listen. Follow [Writing rules](#writing-rules) on every slide.
When text does not fit, cut it; never shrink the font or pad empty space.

**The deck never claims more than the RFP says.** Datadog capabilities on any slide must
match a `Yes`, `Partial` or `Comply` row in the RFP CSV. `Partial` items name their limit.
`Clarification` (prospect side unclear) and `Skipped` (no source confirms Datadog support)
items are never presented as supported.

## Workflow

```
- [ ] Step 1: answering-rfp on the notes → RFP CSV + tech stack coverage check
- [ ] Step 2: creating-solution-architecture on the notes + RFP output → .excalidraw + .svg
- [ ] Step 3: Ask the remaining deck questions
- [ ] Step 4: Slide plan with every slide's final wording, agenda, benefits and stack tables
- [ ] Step 5: Collect the images (architecture .svg, any mock-ups)
- [ ] Step 6: Build the deck as a Claude Artifact
- [ ] Step 7: Review against the checklist → fix → re-review
```

### Step 1: Answer the RFP first (answering-rfp)

Invoke the `answering-rfp` skill with the `Skill` tool. Pass the user's notes as-is, plus
this instruction:

> Give every known tech stack item in these notes its own row: each language, framework,
> runtime, version, rendering or compilation mode, cloud, orchestration, OS, database,
> cache, queue, CI/CD tool, and existing monitoring tool. State clearly whether Datadog
> supports it (Yes, Partial, Comply, Clarification, or Skipped).

Let `answering-rfp` run its own workflow to the end, including its plan approval with the
user. Continue only when it has saved the CSV (`rfp-response-<account>-<timestamp>.csv`)
and given its Clarification Summary and Skipped Summary.

**Tech stack coverage check (very important).** Before moving on:

1. From the notes, list every known tech stack item yourself, one technology per line.
2. Match each item to its CSV row. Every item needs its own row with a supportability
   verdict and a one-sentence response.
3. If any item is missing, merged with another, or has no verdict, go back to
   `answering-rfp` and have it add or split the rows in the same CSV. Repeat until every
   item is covered.
4. Show the user the coverage as a table: `| Tech stack item | Datadog support | How |`,
   with Partial, Clarification and Skipped items called out. Skipped items need a Datadog
   SE to verify them; never upgrade them yourself. Only then continue.

### Step 2: Draw the architecture (creating-solution-architecture)

Invoke the `creating-solution-architecture` skill with the `Skill` tool. Pass the original
notes as-is, the RFP CSV path, the Clarification Summary and the Skipped Summary, plus this
instruction:

> Use the RFP CSV as the source of truth for Datadog support. Draw collection and
> telemetry flows only for items marked Yes, Partial or Comply (Partial with its
> workaround, for example OpenTelemetry). Put every Clarification and Skipped item in the
> "Not drawn: needs confirmation" box.

Let it run its own workflow, including its clarifying questions. Continue only when it has
saved `<customer>-architecture.excalidraw` and `<customer>-architecture.svg`.

### Step 3: Ask the remaining deck questions

Many answers now come from the notes, the RFP output and the architecture; do not ask
again for anything they cover. Never fabricate content. Confirm what is still missing:

- **Customer name**, presenter name(s), **contact details** (slides 1, 2, 26)
- **Presentation date** and delivery context
- **Top 3 customer challenges** (slide 3)
- **3 Datadog use cases**, the challenge each solves (slides 4, 8-15), and which one is
  **Observe**, **Act** and **Secure** (ask if they do not map cleanly). Each use case
  must rest on supported RFP rows
- **Customer questions or quotes**, and who said them (agenda column 3; with none, the
  column becomes From My Notes)
- **Success criteria** count (Intro row) and platform or trust **objections** (Why Datadog row)
- **Benefits to the customer** per part for the trackers (slides 7, 10, 13, 16, 22, 25).
  Propose them from the notes and confirm
- **Current vs target state** (slides 5, 18), **competitors** (slide 19), **business
  value / ROI** (slide 21), a **customer story** and **next steps** (slide 24)
- Whether to keep the optional **reference resources** slide (slide 28)
- Which use cases need a **screenshot mock-up** (slides 9, 12, 15)
- Whether the user also needs a **.pptx export** of the Artifact

Use the AskQuestion tool when available; otherwise ask conversationally. Ask only what is
genuinely missing.

### Step 4: Build the slide plan

Write the plan as a markdown table before building anything: one row per slide of the
[slide flow](#slide-flow), with the layout and each slide's text drafted at its final
length within the [word limits](#word-limits). Add three content tables:

- **Agenda**: one row per part with use case, column 3 items (and their style: quote,
  question or note), attribution, and What Demonstrates It.
- **Benefits**: one row per part, two or three benefit lines each.
- **Stack**: one row per tech stack item with its RFP CSV row number, Datadog support
  (copied from the CSV) and a short "how" (see [Tech stack slide](#tech-stack-slide)).

The user reviews the real wording before anything is built. Use the earlier outputs:

- **RFP CSV**: capabilities on the use-case slides (9, 12, 15), the capability recap
  table (19) and What Demonstrates It come from its `Yes`, `Partial` and `Comply` rows.
  Demo URLs (slides 9, 12, 15) come from its Demo URL column; reference links (slide 28)
  from its Doc URL column. Its open Clarification questions and Skipped items (for
  Datadog to verify) become technical next steps on slide 24.
- **Architecture**: the `.svg` goes on slide 6. Current vs target state (slides 5, 18)
  must match its two views; its "Not drawn" items must not appear as working on any slide.

### Step 5: Collect the images

The architecture `.svg` from Step 2 goes on slide 6 as is. Generate other images only for
slides that still need a screenshot mock-up (usually the use-case detail slides 9, 12,
15).

### Step 6: Build the deck as a Claude Artifact

Build all slides in one Claude Artifact, using its Datadog presentation styles and format
for backgrounds, colours, type, logo and footer. Follow the [slide flow](#slide-flow) and
[slide layouts](#slide-layouts) for what goes on each slide and where, and the
[agenda](#agenda-and-tracker-design) and [stack](#tech-stack-slide) designs for the custom
slides. Use the approved wording from Step 4 exactly; do not add text while building.

- Where the Artifact's styles and the layouts below disagree, the Artifact's styles win
  on look (colours, fonts, backgrounds); the layouts win on content and order.
- Keep each slide's text in real text elements, not images, so it stays editable.
- If the user wants a `.pptx`, export it from the Artifact if it can; otherwise say so.

### Step 7: Review (mandatory)

Look at every slide in the rendered Artifact and check:

| Check | Pass when |
|---|---|
| Wording | Every line and slide is within the [word limits](#word-limits); no filler, no dash-joined clauses, no full stops on bullets |
| Placeholders | No `[...]`, "Heading, 20pt Bold", "lorem ipsum" or template hints left |
| Fit | No text cut off, overflowing a card, or running into the footer; nothing shrunk below the layout sizes |
| Agenda | Title "Agenda for <Customer>"; six parts in order; correct column 3 header; quotes verbatim with roles; no invented quotes |
| Trackers | Six of them, at slides 7, 10, 13, 16, 22, 25; the highlighted row is the part just covered; earlier rows show benefits, later rows dimmed; rows in the same place on every tracker |
| Architecture | Slide 6 shows the Step 2 `.svg`, readable and uncut; slides 5 and 18 match its two views |
| Stack coverage | Every tech stack row in the RFP CSV is on the stack slide, with the same verdict as the CSV |
| Overclaiming | No slide shows a capability the RFP marks Clarification or Skipped; every Partial item states its limit |
| Use cases | Titles match on slides 2, 4, 8, 11, 14; demo URLs start with `https://demo.datadoghq.com/` |

Write a fix table (`| Slide | Issue | Fix |`), fix the Artifact, and review the changed
slides again. Repeat until every check passes. Static template text you did not write
(for example "Relatable Customer Success & Next Steps for <Customer>") may stay.

One request ends with all three deliverables: the RFP CSV, the architecture diagram
(`.excalidraw` + `.svg`), and the deck Artifact (plus its `.pptx` export if asked).

## Slide flow

| # | Slide | Layout | Agenda part | Content |
|---|---|---|---|---|
| 1 | Title / customer intro | Cover | — | "<Customer> & Datadog", AE and SE names, date |
| 2 | Agenda | Agenda table | — | See [agenda design](#agenda-and-tracker-design) |
| 3 | Top 3 challenges | Stacked cards | Intro & Whiteboard | Customer pains |
| 4 | 3 proposed use cases | Three cards | Intro & Whiteboard | Use cases mapped to challenges |
| 5 | Current vs target state | Two cards | Intro & Whiteboard | Matches the architecture's two views |
| 6 | Solution architecture | Title + image | Intro & Whiteboard | The Step 2 `.svg` |
| 7 | Benefits tracker | Agenda table | Intro & Whiteboard | After Intro & Whiteboard |
| 8 | Use Case 1 divider | Divider (blue) | Observe | "Use Case 1" + use case title |
| 9 | Use Case 1 details + demo | Title + content | Observe | Supported capabilities, demo points, demo URL |
| 10 | Benefits tracker | Agenda table | Observe | After Observe |
| 11 | Use Case 2 divider | Divider (magenta) | Act | "Use Case 2" + use case title |
| 12 | Use Case 2 details + demo | Title + content | Act | Supported capabilities, demo points, demo URL |
| 13 | Benefits tracker | Agenda table | Act | After Act |
| 14 | Use Case 3 divider | Divider (teal) | Secure | "Use Case 3" + use case title |
| 15 | Use Case 3 details + demo | Title + content | Secure | Supported capabilities, demo points, demo URL |
| 16 | Benefits tracker | Agenda table | Secure | After Secure |
| 17 | Recap divider | Divider (orange) | Why Datadog | "Recap" / "Current State vs. Target State" |
| 18 | Current vs target recap | Two cards | Why Datadog | "<Customer>'s Current State vs. Target State"; mirrors slide 5 |
| 19 | Capability recap table | Title + table | Why Datadog | Datadog vs incumbents, from RFP rows |
| 20 | Takeaways | Divider (blue) | Why Datadog | "Takeaways" + the one-line business value |
| 21 | Business value | Title + content | Why Datadog | "Business Values for <Customer>"; quantified value |
| 22 | Benefits tracker | Agenda table | Why Datadog | After Why Datadog |
| 23 | Customer success + next steps divider | Sub-divider (green) | Next Steps & Close | "Relatable Customer Success & Next Steps for <Customer>" |
| 24 | Customer story + next steps | Three cards | Next Steps & Close | Story, Strategic, Technical (incl. open RFP items) |
| 25 | Benefits tracker | Agenda table | Next Steps & Close | After Next Steps & Close; full benefits recap |
| 26 | Thank you / contacts | Cover | — | "Thank you", AE and SE names, date |
| 27 | Your stack on Datadog (backup) | Title + table | — | See [Tech stack slide](#tech-stack-slide); continues on 27b if over 10 rows |
| 28 | Reference resources (optional) | Title + content | — | Doc URLs from the RFP; drop if none |

- Use Case 1 is Observe, 2 is Act, 3 is Secure. Use case titles on slides 2, 4, 8, 11 and
  14 must match.
- Demo URLs on slides 9, 12, 15 start with `https://demo.datadoghq.com/`.
- The SE name: ask, or use the presenter from the notes. Never guess names.

## Slide layouts

The gist of the 2026 Datadog Presentation Template (theme "2025_DD_v1"), for the Artifact
to follow. Canvas 16:9 (13.33 × 7.5 in). Positions are inches from the top left.

**Brand.** Primary purple `#8000FF`; accents green `#00E37D`, blue `#0060FF`, orange
`#FF5E00`, cyan `#00CAFF`, amber `#FF9B00`, pink `#FF0080`; deep purple `#5C00EF`; grey
`#C7C7C7`; text black on light slides, white on gradient slides. Font Roboto (Roboto Mono
for code). Every light slide has the Datadog logo and slide number bottom right
(about 11.6, 7.06).

| Layout | Background | Elements and type |
|---|---|---|
| **Cover** (1, 26) | Purple to magenta gradient with large faceted shapes; big white Datadog logo bottom right | Title 72pt bold white at 0.77, 0.66, 11.8 wide; subtitle 24pt white below (AE name, SE name), date 18pt |
| **Title + content** (9, 12, 15, 21, 28) | Light gradient: white to pale blue, lilac top right | Title 36pt bold black at 0.76, 0.39, 11.8 × 0.95. Body at 0.75, 1.53, 11.8 × 5.3: heading 20pt bold, level 1 20pt no bullet, level 2 20pt bullet, level 3 18pt |
| **Stacked cards** (3) | Light gradient | Three full-width white rounded cards (11.7 × 1.6) at y 1.57, 3.42, 5.27, each with a 0.1 in left accent bar: purple `#5C00EF`→`#9C43FE`, blue `#0060FF`→`#00CAFF`, purple `#8000FF`→pink `#FF0080`. Heading 20pt bold, description 18pt |
| **Three cards** (4, 24) | Light gradient | Three white cards 3.78 × 5.29 at x 0.78, 4.78, 8.78, y 1.58, rounded top corners, 0.1 in top accent bar in the same three gradients. Heading 18pt bold ("Use Case 1: <name>"; "Strategic"; "Technical"), body 18pt, level 3 16pt |
| **Two cards** (5, 18) | Light gradient | Two white cards 5.78 × 5.29 at x 0.78 and 6.78, y 1.58; top bars purple (Current State, left) and blue (Target State, right). Heading 20pt bold, body 20pt, level 3 18pt |
| **Title + table** (19, 27) | Light gradient | Title as above; table at 0.75, 1.53, 11.8 wide. Slide 19: columns "Strategic capability for <Customer>", "Datadog's Advantages", "Others"; one row per use case |
| **Title + image** (6) | Light gradient | Title "Solution architecture"; image fitted inside 0.7, 1.3, 11.9 × 5.55, aspect kept, centred |
| **Divider** (8, 11, 14, 17, 20) | Full-bleed gradient with faceted shapes: blue/cyan (8, 20), magenta/purple (11), teal/cyan/green (14), orange/pink (17) | Title 66pt white at 0.76, 0.76; subtitle 24pt white at 0.76, 2.27 |
| **Sub-divider** (23) | Green/teal/blue gradient | Title 54pt bold white, two lines, lower left; subtitle 24pt |
| **Agenda table** (2 and trackers) | Light gradient | See [Agenda and tracker design](#agenda-and-tracker-design) |

Template guidance to keep in the content:

- **Takeaways / business value**: lead with a measurable outcome, for example "20% lower
  MTTD", MTTR, mean time to remediation, log cost, tool-switching cost. Business value
  covers three dimensions: Process, Productivity, Price.
- **Next steps (slide 24)**: the story card names a similar customer from
  `https://www.datadoghq.com/customers/`. Strategic offers: Observability Maturity
  Assessment or Value Assessment workshop. Technical offers: technical deep dive, PoC
  planning session, success criteria scoping workshop.

## Agenda and benefits trackers

### Structure

Title **Agenda for <Customer>** with the real customer name. Always six parts in this
order; keep the rule of three use cases.

| Part | Use case column | Colour |
|---|---|---|
| Intro & Whiteboard | — | orange |
| Observe | Use Case 1 pill | blue |
| Act | Use Case 2 pill | purple |
| Secure | Use Case 3 pill | red |
| Why Datadog | — | orange |
| Next Steps & Close | — | green |

- **Observe**: the visibility or detection use case. **Act**: the response or remediation
  use case. **Secure**: the security or protection use case. If the three do not fit, ask
  the user how to map them; rename a part only when they agree.
- Use case titles are short outcomes ("See failing bill payments before customers call"),
  not product names.

### Agenda columns (slide 2)

PART · USE CASE · CUSTOMER QUESTION or FROM MY NOTES · WHAT DEMONSTRATES IT

- **Notes have customer questions or quotes** → header CUSTOMER QUESTION. Verbatim words
  go in curly quotes. A concern with no verbatim wording becomes a short question in
  italics.
- **No questions or quotes** → header FROM MY NOTES, with short points from the notes.
- Decide the header once for the whole column. Never invent a quote. Add an attribution
  (a role, not a name) only when the notes say who said it. Split a double question into
  two short ones. One to three items per part.
- **What Demonstrates It**: products or artefacts that answer the row. Intro: the success
  criteria count ("6 success criteria") or the whiteboard ("Current vs target
  whiteboard"). Observe/Act/Secure: products in that demo. Why Datadog: what answers the
  objections. Next Steps: the proposed next step ("PoC + QVA"). Only products in the notes
  or the demo plan.

### Benefits trackers (slides 7, 10, 13, 16, 22, 25)

PART · USE CASE · BENEFITS TO <CUSTOMER> · WHAT DEMONSTRATES IT

- Covered parts show their benefits in full colour; the part just covered is highlighted
  (tinted card, coloured border, halo on its dot); later parts are dimmed with benefits
  hidden. Rows stay in the same place on every tracker. The last tracker shows every row
  and doubles as the benefits recap.
- Benefits are short outcomes in the customer's terms ("Engineering knows before the call
  center", not "RUM alerts"), derived from the notes. Never invent numbers.
- Intro benefits cover the shared starting point ("6 success criteria agreed up front");
  Next Steps benefits cover the path forward ("PoC + QVA proves the 6 criteria").
- The header uses the customer's short name ("BENEFITS TO BITSBURG").

### Agenda and tracker design

Light gradient background. Title "Agenda for <Customer>", 40pt bold, top left. Under it a
row of grey column headers (11pt bold caps, `#5F6368`), then six white rounded row cards
(border `#E2E2EA`) filling the space down to the footer, with a thin vertical timeline
(`#C9BDEB`) on the left and a coloured dot per row.

| Column | Width | Content |
|---|---|---|
| Part | about 2.2 in | Part name, 19pt bold, in the part colour |
| Use case | about 2.6 in | Rounded pill in the part's light colour: "Use Case N" 10.5pt bold in the part colour, title 13pt bold near-black; "—" for non use-case parts |
| Column 3 | about 4.2 in (3.7 on trackers) | 12pt items; quotes in curly quotes, questions italic, attribution 10pt grey `#80868B` |
| What Demonstrates It | about 2.5 in (2.95 on trackers) | Entries joined with " · ", 12.5pt bold, in the part colour |

| Part | Text | Dot | Light (pill, halo) | Tint (highlighted card) |
|---|---|---|---|---|
| Intro & Whiteboard, Why Datadog | `#B4621A` | `#F0A23B` | `#FCE7C8` | `#FFF8EE` |
| Observe | `#2F4FD8` | `#5B8DEF` | `#DCE5FC` | `#F4F7FE` |
| Act | `#6D28D9` | `#8B5CF6` | `#E6DDFB` | `#F7F3FE` |
| Secure | `#B42828` | `#E04848` | `#FAE3E3` | `#FEF5F5` |
| Next Steps & Close | `#2E7D32` | `#4CBB5E` | `#D6F0DA` | `#F3FBF4` |

Tracker states: parts already covered as on the agenda; the part just covered on a card
tinted in its tint colour with a 1.75pt border in its dot colour and a halo (light colour)
behind its dot; later parts dimmed (text `#A3A7AE`, pill `#F1F2F5`, dot `#D3D6DC`) with
column 3 and What Demonstrates It left empty. Size rows from all six parts' benefits so
the rows sit in the same place on every tracker.

## Tech stack slide

A backup slide after Thank you: one row per tech stack item, with Datadog's support taken
from the RFP CSV. It answers "do you support X?" without breaking the demo flow.

- Title "Your stack on Datadog". A plain table: TECHNOLOGY · DATADOG SUPPORT · HOW DATADOG
  COVERS <CUSTOMER>, header 11pt bold grey caps, rows 14pt with a thin bottom border.
  Technology bold; support bold in colour: Yes and Comply green `#2E7D32`, Partial orange
  `#B4621A`, Clarification purple `#6D28D9`, Skipped grey `#80868B`.
- Legend under the table, 11pt grey: "Partial: supported with limits. Clarification: to
  confirm with you. Skipped: Datadog to verify."
- **Coverage is mandatory.** Every RFP CSV row in a tech stack category (Frontend,
  Backend, Infrastructure Platform, Database & Data Store Technical Stack, or Integration
  & Extensibility) gets a row, and the support value is copied from the CSV, never
  changed. Check this row by row against the CSV before building and again in Step 7.
- Technology names the item and version (5 words max); "how" is the Datadog product or the
  open question (10 words max), shortened from the CSV response. Skipped rows have no CSV
  response; write "Datadog SE to verify".
- Order rows frontend, backend, infrastructure, data stores, integrations. Over 10 rows
  continue on a second slide, "Your stack on Datadog (2/2)".

## Writing rules

1. **Rule of 3.** Three bullets per box, four at most. Three takeaways. Three next steps
   per column.
2. **Fragments, not sentences.** "MTTR down 40%", not "We expect to reduce MTTR by 40%."
   No full stops at the end of bullets.
3. **One idea per line.** If a line needs "and" to join two ideas, split it or drop one.
4. **Lead with the outcome or the number.**
5. **Customer's words over Datadog's**: bill payments, call center, fraud agent.
6. **Digits for numbers**: "6 success criteria", "40%", "2 weeks".
7. **No filler**: in order to, leverage, utilize, seamless, robust, comprehensive,
   holistic, cutting-edge, best-in-class, world-class, state-of-the-art, empower, unlock,
   game-changing, very, really, basically, actually.
8. **No dash joiners.** Never join clauses with " — " or " - "; use a comma, a colon or a
   new line. (The agenda's "—" empty-cell marker is fine.)
9. **Cut, don't shrink.** Remove the weakest point; never shrink fonts below the template
   sizes or pad empty space. White space is fine.

### Word limits

| Element | Max |
|---|---|
| Slide title; divider subtitle; agenda use case | 8 words |
| Heading in a card or column | 6 words |
| Bullet or body line | 12 words |
| Challenge description | 15 words |
| Takeaway; business value line (number first) | 10 words |
| Next step | 8 words |
| Content slide total, excluding title | 60 words |
| Agenda quote (verbatim; trim with "…") | 20 words |
| Agenda question | 15 words |
| Agenda note; attribution | 12 words; 4 words |
| Tracker benefit | 8 words |
| What Demonstrates It | 5 entries, 4 words each |
| Stack slide item; how | 5 words; 10 words |

Count words against this table in Step 4 (the plan) and again in Step 7 (the review).
Agenda, tracker and stack slides follow their own rows; every other slide follows the
general rows, including the 60-word slide total.

| Before | After |
|---|---|
| Our solution provides comprehensive end-to-end visibility across your entire stack | One view across every service |
| Reduce Mean Time To Resolution by approximately 40% through faster root cause analysis | MTTR down 40% |
| Leverage Datadog's robust log management capabilities to lower costs | Lower log costs, same search power |
| Datadog Cluster Agent — collects cluster-level metadata and reduces API server load | Cluster Agent: less load on the API server |

## Test prompts

Use these to check the skill after changes. Every run must also pass the Step 7 review.

1. **Full technical notes.** "Discovery call with GlobalRetail Inc. On Prometheus + Grafana
   + ELK, evaluating Datadog vs New Relic. Challenges: no unified observability across AWS
   EKS (us-east-1) and legacy VMs; no tracing for checkout and payment services; slow
   incident response from fragmented logs. Use cases: APM for checkout, Kubernetes
   monitoring via Cluster Agent, log management for the VMs. Target: replace
   Prometheus/Grafana/ELK. ROI: MTTR down 40%. Presenter Jane Doe; contact John Smith, VP
   Engineering; 2026-08-20. Include reference resources."
   *Expect:* runs `answering-rfp` first, with its own rows for EKS, the legacy VMs (OS
   unknown: Clarification), the checkout and payment services (language unknown:
   Clarification), Prometheus, Grafana and ELK, each Yes/Partial only with a cited source
   (otherwise Skipped); shows the coverage table; then `creating-solution-architecture`
   with the notes and the CSV, leaving unclear flows in "Not drawn"; then asks how to map
   the use cases to Observe/Act/Secure (none is security); FROM MY NOTES column; benefits
   use the 40% MTTR figure and invent no others; a 28-slide Artifact with the architecture
   on slide 6 and every CSV tech stack row on the stack slide.
2. **Thin notes.** "Customer runs everything on Azure VMs, wants better log monitoring, no
   APM yet, unhappy with Splunk licensing. Challenges: costly Splunk logs, no tracing. One
   use case: log management to replace Splunk. Presenter: me. No date, competitor or ROI."
   *Expect:* `answering-rfp` rows for Azure VMs and Splunk, with Clarification or Skipped
   for the unknowns; the architecture skill asks its own questions; the deck stage asks
   for the customer name and the missing use cases instead of inventing them; FROM MY
   NOTES column.
3. **Customer quotes.** "Bitsburg Bank. Head of Platform: 'We have the data. We do not have
   the answers. Someone still has to go and look.' Call center hears about failed bill
   payments before engineering; LLM fraud agent health and cost unknown. CTO: 'The hard
   part is determining which one is real before an attacker or a customer feels the
   impact.' Worried about yet another tool and trusting AI with bank data. 6 success
   criteria. Use cases: see failing bill payments before customers call; restore them
   faster under governance; protect customers from account compromise. Next step: PoC +
   QVA. Show the benefits as I go through the demo."
   *Expect:* the RFP and architecture stages run first; "Agenda for Bitsburg Bank" with
   CUSTOMER QUESTION, verbatim quotes with role attribution, italic questions for unquoted
   concerns, no invented quotes; six trackers with BENEFITS TO BITSBURG, the right row
   highlighted on each; nothing on any slide claims more than the RFP CSV.
