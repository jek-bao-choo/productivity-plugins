# Editing and QA Reference

Build mechanics for the PoC scoping deck. All commands assume `SKILL` points at this
skill's directory and the `py` shell function is defined as described in SKILL.md's Setup section.

## Build pipeline

```bash
py "$SKILL/scripts/office/unpack.py" "$TEMPLATE" unpacked/
python3 "$SKILL/scripts/fill_deck.py" --list unpacked/ --pretty > tokens.json
# write fill.json from tokens.json, then:
python3 "$SKILL/scripts/fill_deck.py" --apply unpacked/ --map fill.json --report
py "$SKILL/scripts/clean.py" unpacked/
py "$SKILL/scripts/office/pack.py" unpacked/ "$OUT" --original "$TEMPLATE"
```

`pack.py` validates against the bundled OOXML schemas and auto-repairs common issues.
It reports `All validations PASSED!` on success and refuses to write on failure, so
treat a validation error as a real problem rather than something to bypass with
`--validate false`.

## Writing the fill map

`fill.json` is a JSON object of token to replacement. Three key forms:

```json
{
  "[Prospect / Customer Name]": "Northwind Bank",
  "5:[12]": ["12", "12", "9"],
  "[Champion Name] >> [email]": ["dana@nw.example", "marc@nw.example", "aiko@nw.example"]
}
```

- **Plain key** — replaces every occurrence deck-wide. Use for unique tokens.
- **`N:token`** — restricts to slide position N.
- **`anchor >> token`** — restricts to the `<p:sp>` shape that also contains `anchor`.

An anchor only reaches within a single shape. It works on slide 8, where each contact
panel is one text box holding names and emails together. It does not work on slide 5,
where every cell of the MTTD grid is a separate shape — scope that one by slide.

A string value replaces all matched occurrences; a list replaces successive occurrences
in document order.

**Prefer anchors over slide scoping for repeated tokens.** Document order is not visual
order. On slide 8 the prospect's contact panel is stored before Datadog's despite
rendering on the right, so an ordered list scoped only by slide puts the AE's email in
the champion's block — and the deck looks perfectly fine until someone reads it.

Anchored keys are applied before unanchored ones, because an anchor has to still be
present in the slide when its key runs. If you replace `[Champion Name]` with a real
name in the same map, the anchor `[Champion Name] >> [email]` still resolves; the
script handles the ordering for you.

`--report` prints what remains. Every remaining token must be accounted for in
`open-questions.md`.

## Setting the Datadog site

The deck ships pointing at US1. After the region is known, rewrite the URLs on slides
10, 12 and 15, and fix slide 10's now-stale footnote.

| Site | App URL | Cloud |
|---|---|---|
| US1 (East) | `https://app.datadoghq.com/` | AWS |
| US3 (West) | `https://us3.datadoghq.com/` | Azure |
| US5 (Central) | `https://us5.datadoghq.com/` | GCP |
| EU1 | `https://app.datadoghq.eu/` | GCP |
| AP1 | `https://ap1.datadoghq.com/` | AWS |

URLs live in two places per slide — the visible `<a:t>` text and the `Target` attribute
of the matching entry in `ppt/slides/_rels/slideN.xml.rels`. Change both, or the deck
will display one address and navigate to another.

```bash
grep -o 'Target="[^"]*datadoghq[^"]*"' unpacked/ppt/slides/_rels/slide1{0,2,5}.xml.rels
```

**Do not blanket-replace `app.datadoghq.com` across slide 10.** That slide's table is a
reference listing all five sites, and the US1 row legitimately contains
`https://app.datadoghq.com/`. A global replace rewrites it, leaving a table with two EU
rows and no US1 — which looks plausible enough to survive a skim. Change the *hyperlink
targets* and the footnote, and leave the table alone.

Leave the table entirely alone. Moving the `RECOMMENDED` badge to the prospect's row
seems tidier but makes things worse: the badge is a separately styled red run, so
moving it as plain text loses the colour, and the extra line pushes the table past its
container and clips the Japan row. The footnote below the table is the right place to
state which site this deck targets.

`https://docs.datadoghq.com/...` and `https://help.datadoghq.com/` are site-independent
— leave them alone.

## Editing any text, not just placeholders

Run-splitting is not a placeholder problem — it is a property of this whole deck. Two
strings you will almost certainly want to change are stored across multiple runs, so
`sed` and `str.replace` on the raw XML silently do nothing:

- slide 10's presenter footnote, which concatenates to
  `note: All hyperlinks shown in this document are linked to US1.Please change to your relevant data center if required.`
  (no space after `US1.` once the runs are joined)
Slide 14's subtitle looks like a third case and is not — see "Things that look broken
and are not" in `slide-map.md`. Its two lines are separated by an `<a:br/>`, so joining
the runs produces a convincing-looking run-on sentence. `fill_deck.py` refuses to
collapse a paragraph containing a line break, and reports it as a miss.

Route every text edit through `fill_deck.py --apply`, whose keys are arbitrary strings
rather than bracketed tokens. It matches across runs and reports a zero-hit key, so a
failed edit is visible instead of silent:

```json
{
  "How to get help Raising a Datadog support ticket": "How to get help: raising a Datadog support ticket"
}
```

To get the exact string to match, read the concatenated paragraph text rather than
trusting what the slide looks like:

```bash
python3 -c "
from xml.etree import ElementTree
A='{http://schemas.openxmlformats.org/drawingml/2006/main}'
r=ElementTree.parse('unpacked/ppt/slides/slide14.xml').getroot()
for p in r.iter(A+'p'):
    t=''.join(x.text or '' for x in p.iter(A+'t'))
    if t.strip(): print(repr(t))
"
```

## Removing a slide

To drop slide 13 when RUM is out of scope:

1. Delete its `<p:sldId>` from `<p:sldIdLst>` in `unpacked/ppt/presentation.xml`.
2. Run `clean.py`, which collects the orphaned slide part, its rels, its now-unreferenced
   media, and the matching `[Content_Types].xml` override.

Never delete slide XML by hand — the dangling relationship and content-type override
will make PowerPoint report the file as corrupt.

## Adding a slide

```bash
py "$SKILL/scripts/add_slide.py" unpacked/ slideLayout29.xml   # from a layout
py "$SKILL/scripts/add_slide.py" unpacked/ slide3.xml          # duplicate a slide
```

It prints a line like `<p:sldId id="278" r:id="rId25"/>`. **You must insert that into
`<p:sldIdLst>` in `ppt/presentation.xml` yourself, at the position you want** — the
script appends the part and wires up rels and content types, but does not touch slide
order.

Duplicating an existing slide inherits its styling and is usually less work than
starting from a bare layout. For the tech-stack slide, duplicating slide 3 gives you
the two-panel comparison structure ready to retitle.

Do all structural changes (add, remove, reorder) **before** editing text, so slide
positions stop moving under you. `fill_deck.py`'s `N:` scoping uses presentation
position, and inserting a slide renumbers everything after it — insert the tech-stack
slide after position 4 and the MTTD slide becomes 6, so `"5:[12]"` silently matches
nothing. Re-run `--list` after restructuring and take your slide numbers from that.

## Visual check

Font overflow and truncation are invisible until rendered, so render when you can:

```bash
py "$SKILL/scripts/office/soffice.py" --headless --convert-to pdf "$OUT"
pdftoppm -jpeg -r 150 "${OUT%.pptx}.pdf" slide
```

Then Read every `slide-*.jpg`. This needs LibreOffice (`soffice`) and Poppler
(`pdftoppm`), neither of which `uv` can provide. If they are absent, say so plainly and
fall back to the text checks below rather than skipping QA silently.

`thumbnail.py` produces a labelled contact sheet instead, which is quicker for spotting
layout breakage across the whole deck:

```bash
py "$SKILL/scripts/thumbnail.py" "$OUT" grid --cols 4
```

What to look for:

| Issue | Signal |
|---|---|
| Font too large | Text wrapping to 3+ lines in a narrow column; text bleeding past its box; bottom lines clipped |
| Font too small | Large empty space in the lower half; content clustered in the top third |
| Text overflow | Words cut off at a box or slide edge |
| Leftover placeholder | Any `[...]` or `…` still visible |
| Wrong person, right slot | Slide 8 — check each email sits under the matching name |
| Overlap | Cover and divider slides: subtitle sitting on a multi-line title |

Font sizes live in the `sz` attribute of `<a:rPr>`, in hundredths of a point:

| Size | `sz` |
|---|---|
| 60pt cover title | `6000` |
| 36pt slide title | `3600` |
| 28pt | `2800` |
| 24pt | `2400` |
| 20pt | `2000` |
| 18pt | `1800` |
| 16pt | `1600` |
| 14pt | `1400` |

Re-render after every round of fixes. One fix often causes another — shortening a title
can leave a subtitle floating, and reflowing a bullet list can push content off-slide.

## Text checks — always run these

These need no extra tooling, so there is no excuse for skipping them.

```bash
# Nothing left unfilled that is not a known open question
python3 "$SKILL/scripts/fill_deck.py" --list unpacked/ --pretty | \
  python3 -c "import json,sys; s=json.load(sys.stdin)['summary']; print(s['unique_tokens'], s['blank_markers'], s['literals'])"

# Embedded fonts survived the repack — this one only bites on someone else's laptop
unzip -l "$OUT" | grep -c 'ppt/fonts/.*fntdata'      # expect 10
unzip -p "$OUT" ppt/presentation.xml | grep -c embeddedFontLst   # expect 1

# The deck opens and reports the expected slide count
unzip -p "$OUT" docProps/app.xml | grep -o '<Slides>[0-9]*</Slides>'
```

Re-unpack the finished `.pptx` and run `--list` against *that*, not against the working
directory. It is the only check that reflects what the prospect will actually open.
