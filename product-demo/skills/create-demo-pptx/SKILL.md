---
name: create-demo-pptx
description: >-
  Create a Datadog-branded product demo PowerPoint (.pptx) from meeting notes,
  built on the bundled 2026 Datadog Presentation Template. Use when the user asks
  to "create a demo deck", "generate a pptx", "build a Datadog presentation",
  "turn my meeting notes into slides", or mentions producing a customer demo
  presentation. Follows a fixed 20-slide customer-demo flow and includes a
  mandatory visual QA loop.
version: "0.1.0"
---

# Create Datadog Demo PPTX

Turn customer meeting notes into a polished, Datadog-branded demo deck built on the
bundled template `assets/2026_Datadog_Presentation_Template.pptx` (~20 pre-designed slides,
purple/violet/white palette, Datadog logo). Input: the user's meeting notes. Output: a
finished `.pptx` following the preferred slide flow.

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
- [ ] Step 2: Build the slide plan (markdown table)
- [ ] Step 3: Generate any needed images (mock-ups / diagrams)
- [ ] Step 4: Build the deck (unpack → duplicate → edit → clean → pack)
- [ ] Step 5: Visual Check Loop (mandatory) → fix → re-verify
```

### Step 1 — Ask clarifying questions first

Before creating the pptx, ask the user for anything missing from their notes. Do not
fabricate content. At minimum confirm:

- **Customer name**, presenter name(s), and **contact details** (slides 1 and 19)
- **Presentation date** and delivery context
- The **top 3 customer challenges** (slide 3)
- The **3 Datadog use cases** and which maps to each challenge (slides 4, 6-11)
- **Current state vs. target state** details (slides 5, 13)
- **Competitors / incumbents** for the capability comparison (slide 14)
- **Business value / ROI** figures (slide 16)
- A **relevant customer story** and **strategic + technical next steps** (slide 18)
- Whether to include the optional **reference resources** slide (slide 20)
- Which **use cases need a screenshot mock-up, architecture, or system diagram**
- **Output file path/name** for the finished deck

Use the AskQuestion tool when available; otherwise ask conversationally. Ask only what is
genuinely missing — infer the rest from the notes.

### Step 2 — Build the slide plan

Write the plan as a markdown table before touching any files. Map each row of the
preferred flow to the template source slide it will be duplicated from. See
[references/slide-flow.md](references/slide-flow.md) for the full 20-slide flow and mapping
guidance. Analyze the template first:

```bash
python3 $SCRIPTS/thumbnail.py "$TEMPLATE"
python -m markitdown "$TEMPLATE"
```

### Step 3 — Generate images

Before editing slides, generate images for any slide that needs a screenshot mock-up,
architecture diagram, or system diagram (typically the use-case detail slides 7, 9, 11).

### Step 4 — Build the deck

Unpack, duplicate the mapped source slides, reorder in `<p:sldIdLst>`, edit content, clean,
and pack. Complete all structural changes before editing text. Full commands, editing
rules, and pitfalls are in [references/editing-and-qa.md](references/editing-and-qa.md).

```bash
python3 $SCRIPTS/office/unpack.py "$TEMPLATE" unpacked/
python3 $SCRIPTS/add_slide.py unpacked/ slide7.xml   # duplicate a source slide
# edit unpacked/ppt/slides/slide{N}.xml with StrReplace
python3 $SCRIPTS/clean.py unpacked/
python3 $SCRIPTS/office/pack.py unpacked/ output.pptx --original "$TEMPLATE"
```

Preserve Datadog branding — only replace placeholder text and visuals; never alter the
palette, logo, or master styling.

### Step 5 — Visual Check Loop (mandatory)

After packing, render every slide to an image and review it. Font size problems, text
overflow, and truncation are invisible until rendered — this step is not optional.

1. Render to images (`soffice` → `pdftoppm`), then Read every slide image.
2. Build a fix plan table of issues before fixing anything.
3. Fix fonts / content in the slide XML.
4. Re-render and re-verify affected slides. One fix often creates another.
5. Repeat until a full pass reveals no new issues.

Detailed issue checklist, font-size table, and fix snippets are in
[references/editing-and-qa.md](references/editing-and-qa.md).

## Resources

- **[references/slide-flow.md](references/slide-flow.md)** — the preferred 20-slide flow and template mapping
- **[references/editing-and-qa.md](references/editing-and-qa.md)** — build commands, font tables, fix snippets, visual QA loop
- **`scripts/`** — PPTX editing utilities (`unpack.py`, `add_slide.py`, `clean.py`, `pack.py`, `thumbnail.py`, `office/soffice.py`)
- **`assets/2026_Datadog_Presentation_Template.pptx`** — the branded source template
