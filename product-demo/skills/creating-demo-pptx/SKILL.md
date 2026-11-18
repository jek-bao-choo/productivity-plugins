---
name: creating-demo-pptx
description: >-
  Create a Datadog-branded product demo PowerPoint (.pptx) from meeting notes,
  built on the bundled 2026 Datadog Presentation Template. Use when the user asks
  to "create a demo deck", "generate a pptx", "build a Datadog presentation",
  "turn my meeting notes into slides", or mentions producing a customer demo
  presentation. Follows a fixed 26-slide customer-demo flow with a six-part
  agenda (Intro & Whiteboard, Observe, Act, Secure, Why Datadog, Next Steps &
  Close), a benefits tracker after each part, and a mandatory visual QA loop.
version: "0.3.0"
---

# Create Datadog Demo PPTX

Turn customer meeting notes into a polished, Datadog-branded demo deck built on the
bundled template `assets/2026_Datadog_Presentation_Template.pptx` (~20 pre-designed slides,
purple/violet/white palette, Datadog logo). Input: the user's meeting notes. Output: a
finished `.pptx` following the preferred slide flow, opening with the six-part agenda
table and returning to it as a benefits tracker after each part, both described in
[references/agenda.md](references/agenda.md).

**Keep every word on the deck concise, succinct, and short.** The audience should read a
slide in seconds and then listen. Follow [references/writing-style.md](references/writing-style.md):
the rule of 3 (three bullets per box, four at most), fragments not sentences, the
customer's words, no filler, no dash-joined clauses, and the word limits table (titles 8
words, bullets 12, 60 words per slide). When text does not fit, cut it; never shrink the
font or pad empty space.

## Setup

Set these paths (relative to this skill's directory) before running commands:

```bash
SCRIPTS="$(pwd)/scripts"          # or the absolute path to this skill's scripts/
TEMPLATE="$(pwd)/assets/2026_Datadog_Presentation_Template.pptx"
```

## Workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Ask clarifying questions
- [ ] Step 2: Build the slide plan (markdown table) and the agenda spec (agenda.json, with benefits)
- [ ] Step 3: Generate any needed images (mock-ups / diagrams)
- [ ] Step 4: Build the deck (unpack → duplicate → edit → clean → pack)
- [ ] Step 5: Visual Check Loop (mandatory) → fix → re-verify
- [ ] Step 6: Generate the architecture diagram (invoke creating-architecture-via-excalidraw)
```

### Step 1 — Ask clarifying questions first

Before creating the pptx, ask the user for anything missing from their notes. Do not
fabricate content. At minimum confirm:

- **Customer name**, presenter name(s), and **contact details** (slides 1, 2 and 25)
- **Presentation date** and delivery context
- The **top 3 customer challenges** (slide 3)
- The **3 Datadog use cases**, which maps to each challenge (slides 4, 7-14), and which
  one is **Observe**, **Act** and **Secure** on the agenda (ask if they do not map cleanly)
- Any **customer questions or quotes**, and who said them, for the agenda's
  Customer Question column (if there are none, the column becomes From My Notes)
- The **success criteria** count for the agenda's Intro & Whiteboard row, and the
  customer's platform or trust **objections** for its Why Datadog row
- The **benefits to the customer** of each part, in their own terms, for the benefits
  trackers (slides 6, 9, 12, 15, 21, 24). Propose them from the notes and confirm
- **Current state vs. target state** details (slides 5, 17)
- **Competitors / incumbents** for the capability comparison (slide 18)
- **Business value / ROI** figures (slide 20)
- A **relevant customer story** and **strategic + technical next steps** (slide 23)
- Whether to include the optional **reference resources** slide (slide 26)
- Which **use cases need a screenshot mock-up, architecture, or system diagram**
- **Output file path/name** for the finished deck

Use the AskQuestion tool when available; otherwise ask conversationally. Ask only what is
genuinely missing — infer the rest from the notes.

### Step 2 — Build the slide plan

Write the plan as a markdown table before touching any files. Map each row of the
preferred flow to the template source slide it will be duplicated from, and to the agenda
part it belongs to. See [references/slide-flow.md](references/slide-flow.md) for the full
26-slide flow and mapping guidance.

Then write `agenda.json` for slide 2 and the six benefits trackers: the six fixed parts,
the use case titles, the customer questions (or notes) per part, the benefits per part,
and what demonstrates each part. Show the agenda and the benefits to the user as markdown
tables alongside the slide plan. Rules for every column, the
Customer Question vs From My Notes switch, and the spec format are in
[references/agenda.md](references/agenda.md).

Draft every slide's text in the plan at its final length, within the word limits in
[references/writing-style.md](references/writing-style.md), so the user reviews the real
wording before anything is built.

Analyze the template first:

```bash
python3 $SCRIPTS/thumbnail.py "$TEMPLATE"
python -m markitdown "$TEMPLATE"
```

### Step 3 — Generate images

Before editing slides, generate images for any slide that needs a screenshot mock-up,
architecture diagram, or system diagram (typically the use-case detail slides 8, 11, 14).

### Step 4 — Build the deck

Unpack, duplicate the mapped source slides, reorder in `<p:sldIdLst>`, edit content, clean,
and pack. Complete all structural changes before editing text. Full commands, editing
rules, and pitfalls are in [references/editing-and-qa.md](references/editing-and-qa.md).

```bash
python3 $SCRIPTS/office/unpack.py "$TEMPLATE" unpacked/
python3 $SCRIPTS/add_slide.py unpacked/ slide7.xml   # duplicate a source slide
python3 $SCRIPTS/build_agenda.py unpacked/ agenda.json  # rebuild slide 2 as the agenda table
python3 $SCRIPTS/build_agenda.py unpacked/ agenda.json --benefits observe --slide slide22.xml  # one per tracker
# edit the other unpacked/ppt/slides/slide{N}.xml with StrReplace
python3 $SCRIPTS/clean.py unpacked/
python3 $SCRIPTS/office/pack.py unpacked/ output.pptx --original "$TEMPLATE"
```

The six benefits trackers are duplicates of slide 2 (`add_slide.py unpacked/ slide2.xml`),
one placed after each part. Insert each printed `<p:sldId>` into `presentation.xml` before
running the next `add_slide.py`, otherwise the duplicates get the same slide ID and packing
fails. Never hand-edit the agenda or tracker slides; change `agenda.json` and rerun
`build_agenda.py`.
Preserve Datadog branding — only replace placeholder text and visuals; never alter the
palette, logo, or master styling.

### Step 5 — Visual Check Loop (mandatory)

After packing, render every slide to an image and review it. Font size problems, text
overflow, and truncation are invisible until rendered — this step is not optional.

1. Render to images (`soffice` → `pdftoppm`), then Read every slide image.
2. Run `python3 $SCRIPTS/check_wording.py output.pptx` to flag long lines, wordy slides,
   filler words, dash joiners, and leftover placeholders.
3. Build a fix plan table of the visual and wording issues before fixing anything.
4. Fix fonts / content in the slide XML. Fix wordiness by cutting words, not by shrinking
   the font.
5. Re-render, rerun the wording check, and re-verify affected slides. One fix often
   creates another.
6. Repeat until a full pass reveals no new issues and the wording check passes.

Detailed issue checklist, font-size table, and fix snippets are in
[references/editing-and-qa.md](references/editing-and-qa.md).

### Step 6 — Generate the architecture diagram

The deck isn't the only thing these discovery notes are good for. Once the deck passes
Step 5, the same meeting notes almost always carry enough technical detail (environments,
services, compliance, network constraints) to also sketch the customer's monitoring
architecture — so this is a mandatory final step, not an optional add-on.

Invoke the `creating-architecture-via-excalidraw` skill via the `Skill` tool, passing it the
original discovery/meeting notes from Step 1 as-is. Don't pre-filter or summarize them —
that skill has its own clarifying-questions step and will ask about anything it still
needs (intake region, compliance requirements, collection-method preferences) that the
notes don't cover.

The end result of one request is both deliverables: the finished `.pptx` and an
Excalidraw architecture diagram (or its `.excalidraw` JSON fallback) built from the same
notes.

## Resources

- **[references/slide-flow.md](references/slide-flow.md)** — the preferred 26-slide flow and template mapping
- **[references/agenda.md](references/agenda.md)** — the six-part agenda and benefits trackers: structure, column rules, spec format, build and QA
- **[references/writing-style.md](references/writing-style.md)** — concise wording rules, word limits, before/after examples, `check_wording.py`
- **[references/editing-and-qa.md](references/editing-and-qa.md)** — build commands, font tables, fix snippets, visual QA loop
- **`scripts/`** — PPTX editing utilities (`unpack.py`, `add_slide.py`, `build_agenda.py`, `check_wording.py`, `clean.py`, `pack.py`, `thumbnail.py`, `office/soffice.py`)
- **`assets/2026_Datadog_Presentation_Template.pptx`** — the branded source template
