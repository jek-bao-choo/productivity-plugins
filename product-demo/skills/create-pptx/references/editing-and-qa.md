# Editing and Visual QA Reference

Detailed mechanics for building the deck and running the mandatory visual check loop.
All commands assume `SCRIPTS` points at this skill's `scripts/` directory and
`TEMPLATE` at `assets/2026_Datadog_Presentation_Template.pptx`.

## Build commands

```bash
# 1. Unpack
python3 $SCRIPTS/office/unpack.py "$TEMPLATE" unpacked/

# 2. Duplicate a source slide (e.g. slide7.xml = section-divider)
python3 $SCRIPTS/add_slide.py unpacked/ slide7.xml
# → prints <p:sldId id="XXX" r:id="rIdYYY"/> — insert into ppt/presentation.xml at desired position

# 3. Edit unpacked/ppt/slides/slide{N}.xml with StrReplace

# 4. Clean
python3 $SCRIPTS/clean.py unpacked/

# 5. Pack
python3 $SCRIPTS/office/pack.py unpacked/ output.pptx --original "$TEMPLATE"
```

Slide order lives in `unpacked/ppt/presentation.xml` → `<p:sldIdLst>`. Reorder by
rearranging `<p:sldId>` elements; delete by removing the `<p:sldId>` then running `clean.py`.
Never manually copy slide files — `add_slide.py` handles rels and `[Content_Types].xml`.

## Images before editing

Before editing slides, generate images for any slide that needs a screenshot mock-up,
architecture diagram, or system diagram. Place generated images into `unpacked/ppt/media/`
and wire them into the slide XML, or replace the placeholder image's relationship target.

## Visual Check Loop (Mandatory)

After packing the PPTX, always do a visual review of every slide. This is not optional —
font size problems, text overflow, and truncation are invisible until rendered.

### Render slides to images

```bash
python3 $SCRIPTS/office/soffice.py --headless --convert-to pdf output.pptx
rm -f slide-*.jpg
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

### Read and review every slide

Read each slide image using the Read tool. Look for:

| Issue type | What to look for |
|---|---|
| **Font too large** | Text wrapping to 3+ lines in a narrow column; text bleeding past its text box; bottom lines cut off with strikethrough or truncation artefacts |
| **Font too small** | Huge empty space in lower half of slide; content clustered in the top 30-40% |
| **Text overflow** | Characters or words cut off at the edge of a text box or slide boundary |
| **Leftover placeholders** | `Body, 16pt Normal`, `Heading, 20pt Bold`, `00%`, `lorem ipsum`, `Main text`, `Subtext` visible on any slide |
| **Missing content** | Slide has only 2-3 bullets when you know you set 5-7; bottom half totally blank |
| **Subtitle/title overlap** | On cover or section-divider slides: subtitle text box sitting on top of a multi-line title |
| **Column swap** | The left/right column content is reversed from intended (common with text-2col slides) |

### Build a fix plan

After reviewing all slides, write a compact issue table before fixing anything:

| Slide # | Issue | Fix |
|---|---|---|
| S7 | Only 3 of 7 criteria shown; bottom 60% blank | Add 4 more `<a:p>` elements to text box in slide27.xml |
| S11 | Title font ~60pt, overflows text box; bullets cut off | Reduce title `sz` to `2400` (24pt); bullets to `1600` (16pt) |
| S14 | Same overflow as S11 | Same fix |
| S1 | Subtitle overlaps multi-line title | Shorten title OR reduce title font size |

## Fix fonts in slide XML

Font sizes in PPTX XML are stored in the `sz` attribute on `<a:rPr>` elements, in hundredths of a point:

| Desired size | XML `sz` value |
|---|---|
| 60pt (cover title) | `6000` |
| 36pt (slide title) | `3600` |
| 28pt | `2800` |
| 24pt | `2400` |
| 20pt | `2000` |
| 18pt | `1800` |
| 16pt | `1600` |
| 14pt | `1400` |

To reduce font size, use Python regex on the slide XML:

```python
import re
from pathlib import Path

BASE = Path("unpacked/ppt/slides")
xml = (BASE / "slide5.xml").read_text()

# Reduce all explicit font sizes above 2400 (24pt) in the left-panel text boxes to 2000 (20pt)
# Be surgical: only target the specific text box, not the whole slide
xml = re.sub(r'(sz=")([3-9]\d{3}|[1-9]\d{4,})(">)', r'\g<1>2000\3', xml, count=20)

(BASE / "slide5.xml").write_text(xml)
```

## Add missing content (extra bullet points)

When a text box only has 3 bullet-level slots but you need 7 items, insert additional
`<a:p>` paragraphs after the last existing one. Copy the `<a:pPr>` formatting from an
adjacent paragraph to keep consistent indentation and line spacing:

```python
# After the last <a:p> in the text box, insert additional paragraphs
EXTRA_ITEMS = [
    "Pipeline overhead: Visible scan step via CI Visibility — minimal impact",
    "Critical findings: 100% trigger Slack/email alert",
    "Developer disruption: 0 merge blocks in Year 1 (PR Gate informational mode)",
    "CISO report: Weekly PDF delivered — at least 2 consecutive confirmed",
]
NEW_PARAS = ""
for item in EXTRA_ITEMS:
    NEW_PARAS += f'''
    <a:p>
      <a:pPr indent="0" lvl="0" marL="0" rtl="0" algn="l">
        <a:spcBef><a:spcPts val="0"/></a:spcBef>
        <a:spcAft><a:spcPts val="0"/></a:spcAft>
        <a:buNone/>
      </a:pPr>
      <a:r><a:rPr lang="en-US" sz="1800" b="0"/><a:t>{item}</a:t></a:r>
    </a:p>'''
# Insert before </p:txBody>
xml = xml.replace("</p:txBody>", NEW_PARAS + "\n  </p:txBody>", 1)
```

## Re-render and re-verify

After every round of fixes, re-render to images and re-read the affected slides.
Do not declare success until a full pass reveals no new issues. One fix often
creates another problem, so re-verify affected slides after each change.

## Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order, and leftover placeholders:

```bash
python -m markitdown output.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert|00%|Main text|Subtext"
```

If grep returns results, fix them before declaring success.

## Editing rules

- Bold headers, subheadings, and inline labels with `b="1"` on `<a:rPr>`.
- Never use unicode bullets (•); let bullets inherit from the layout or use `<a:buChar>` / `<a:buNone>`.
- Multi-item content → one `<a:p>` per item; never concatenate into one string.
- For new text with quotes, use XML entities: `&#x201C;` `&#x201D;` `&#x2018;` `&#x2019;`.
- Use `xml:space="preserve"` on `<a:t>` with leading/trailing spaces.
- Preserve Datadog branding — never alter the palette, logo, or master styling.

## Dependencies

- `pip install "markitdown[pptx]"` — text extraction
- `pip install Pillow` — thumbnail grids
- LibreOffice (`soffice`) — PDF conversion (auto-configured via `scripts/office/soffice.py`)
- Poppler (`pdftoppm`) — PDF to images
