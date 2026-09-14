---
name: creating-poc-scoping-deck
description: >-
  Create a Datadog-branded PoC scoping deck for a prospect from meeting notes,
  built on the bundled 2026 PoC Scoping Template. Reads notes in .gdoc, .md,
  .txt, .docx, .xlsx, and .pdf. Use when the user asks to "create a PoC scoping
  deck", "build a POC scoping presentation", "turn my discovery notes into a
  scoping deck", mentions preparing a proof-of-concept scoping or kick-off
  meeting with a prospect, or wants success criteria, roles, cadence and MTTD
  value framed as slides. Asks clarifying questions rather than inventing
  customer data, and also writes a scoping summary and an open-questions list.
version: "0.1.0"
author: Jek Bao
tags: poc, scoping, pptx, presentation, datadog, prospect, discovery, meeting notes
---

# Create a PoC Scoping Deck

Turn discovery notes into the deck you present to a prospect to scope a Proof of
Concept, built on `assets/poc_scoping_template_2026.pptx` (19 Datadog-branded slides,
purple/magenta palette, embedded Roboto). Input: meeting notes in any mix of `.gdoc`,
`.md`, `.txt`, `.docx`, `.xlsx`, `.pdf`. Output: a filled `.pptx`, plus `scoping.md`
recording what was extracted and `open-questions.md` listing every gap.

The template is a finished deck in a fixed narrative order, not a parts bin. Almost all
the work is replacing bracketed placeholders (`[Prospect / Customer Name]`,
`[Success criteria 1]`, the MTTD numbers) with grounded content — so this is a
fill-and-verify job, and the verification matters as much as the fill.

## Setup

```bash
SKILL="$(pwd)"        # or the absolute path to this skill's directory
TEMPLATE="$SKILL/assets/poc_scoping_template_2026.pptx"
py() { uv run --with defusedxml --with lxml --with Pillow python3 "$@"; }
```

`unpack.py`, `pack.py`, `clean.py` and `thumbnail.py` need `defusedxml`/`lxml`/`Pillow`;
`uv run --with` supplies them without touching the system environment. If `uv` is not
installed, use `py() { python3 "$@"; }` and `pip install defusedxml lxml Pillow` first.

`fill_deck.py` and `extract_notes.py` are stdlib-only (except PDF notes, which need
`pypdf` — run that script with `uv run` and it resolves itself).

Define `py` as a **function, not a variable**. Zsh does not word-split on expansion, so
`PY="uv run ..."` then `$PY script.py` fails there with "command not found" while
working fine in bash. A function behaves the same in both.

## Workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Ingest the meeting notes
- [ ] Step 2: Build the scoping picture
- [ ] Step 3: Ask about the gaps
- [ ] Step 4: Write scoping.md and open-questions.md
- [ ] Step 5: Shape the deck (drop and add slides)
- [ ] Step 6: Fill the deck and pack it
- [ ] Step 7: Verify
```

### Step 1 — Ingest the meeting notes

```bash
uv run "$SKILL/scripts/extract_notes.py" notes.docx transcript.pdf costs.xlsx
```

Everything arrives as one markdown stream with a `## <filename>` header per input.

A `.gdoc` file is a link stub, not the document — the script prints `GDOC_URL: <url>`
instead of text. Fetch that URL with `WebFetch`. If it is private and the fetch fails,
ask for a `.docx` or `.pdf` export rather than proceeding with a file you could not
read; silently continuing means the deck is built from partial evidence and nobody
knows which part is missing.

### Step 2 — Build the scoping picture

Read the notes and assemble what the deck needs, slide by slide, using
[references/intake-checklist.md](references/intake-checklist.md). Sort every field into
grounded (stated in the notes), derivable (follows from what is stated), or missing.

Then inventory the template so you know exactly what you are filling:

```bash
py "$SKILL/scripts/office/unpack.py" "$TEMPLATE" unpacked/
python3 "$SKILL/scripts/fill_deck.py" --list unpacked/ --pretty > tokens.json
```

`--list` groups tokens by shape, so you can see which tokens share a block. That
grouping is what lets you target an ambiguous token later.
[references/slide-map.md](references/slide-map.md) explains what each slide is for.

### Step 3 — Ask about the gaps

**The notes are evidence, not a starting point for invention.** Fill what they support,
ask about what they do not, and leave the original bracket standing for anything still
unanswered.

This matters more here than on most decks. A scoping deck is a commitment document —
the prospect reads the success criteria as what you have agreed to prove, and the MTTD
numbers as a claim about their business. A deck that *looks* complete but quietly
invents an incident count or names a champion nobody mentioned is worse than one with
visible blanks, precisely because it looks finished: it gets presented, and the
fabrication surfaces in front of the customer instead of in front of you.

So: never substitute a plausible-looking guess for a fact you do not have. A bracket is
a question you can still ask. A wrong number is a credibility problem.

Two areas are almost never covered by discovery notes, and both are worth asking about
directly:

- **Slide 5, the MTTD inputs** — incidents per year, FTEs per incident, hours per
  incident. These come from the customer's own incident record. The modelled "with
  Datadog" figures only carry weight if the "before" figures are theirs.
- **Slide 8, the contact roster** — names, titles, phone numbers, emails on both sides.

Also confirm the **Datadog site** (it drives every URL on slides 10, 12 and 15, and the
deck ships pointing at US1) and whether **RUM is in scope** (if not, drop slide 13).

Use `AskUserQuestion` when available; otherwise ask conversationally. Batch the
questions into one round grouped by topic rather than drip-feeding them — the user can
see the whole shape of what is missing and answer in one pass. Ask only what is
genuinely missing; re-asking something the notes already answer reads as not having
read them.

### Step 4 — Write scoping.md and open-questions.md

Before touching the deck, write both files to `pocs/<customer>/`:

- **`scoping.md`** — current and future state, business use cases, success criteria,
  tech stack, roles, cadence, region, timeline. Mark each item grounded or derived, so
  a reader can tell what came from the customer and what you inferred.
- **`open-questions.md`** — every remaining gap, written as a question you could send
  to the prospect as-is ("How many major incidents did you handle in the last 12
  months?" rather than "MTTD data missing").

These are the durable record. The deck is a snapshot of one meeting; these files are
what you carry into the next one.

### Step 5 — Shape the deck

Do every structural change first, while nothing depends on slide positions yet.
Inserting or removing a slide renumbers every slide after it, and `fill_deck.py`'s
`N:` scoping counts presentation positions — so filling first and restructuring
afterwards silently breaks the scoped replacements.

**Drop slide 13** (RUM SDKs) when RUM is out of scope: remove its `<p:sldId>` from
`ppt/presentation.xml`, then let `clean.py` collect the orphaned part.

**Add the two slides the template promises and omits**, but only when the notes support
them — an empty slide is worse than an absent one:

- **Tech stack / environment**, after slide 4. Agenda step 3 promises "Identify env,
  services & apps — tech stack (incl. ver), pre-prod, owners & size" and no slide
  delivers it. Include versions; "Java" without "17" does not tell you whether the
  tracer is compatible.
- **Timeline / milestones**, before the Next steps divider. The cover subtitle promises
  "PoC scoping, alignment, **and schedule**". Skip it if the notes contain no dates —
  slide 18 already drives to the Mutual Activity Plan, which is where dates belong.

Duplicating slide 3 gives you a ready two-panel structure for either.

```bash
py "$SKILL/scripts/add_slide.py" unpacked/ slide3.xml
```

It prints a `<p:sldId .../>` line that **you** must insert into `<p:sldIdLst>` at the
position you want — it does not reorder for you. Re-run `fill_deck.py --list` after
restructuring so your slide numbers are the new ones.

### Step 6 — Fill the deck and pack it

Write `fill.json` mapping tokens to replacements, then apply:

```bash
python3 "$SKILL/scripts/fill_deck.py" --apply unpacked/ --map fill.json --report
```

PowerPoint splits one visible string across several runs, so `[Prospect / Customer
Name]` is often stored as three fragments. `fill_deck.py` matches across the whole
paragraph, which is why a plain find-and-replace is not good enough here.

Repeated tokens need scoping — `[email]` appears 5 times, `[AE Name]` 3 times. Use
`"8:[email]"` for slide scoping and `"[Champion Name] >> [email]"` to pin a token to
the shape containing an anchor. **Prefer the anchor form**: document order is not
visual order, and on slide 8 the prospect panel is stored before Datadog's despite
rendering on the right. Anchors also survive the renumbering that `N:` does not.

A token that matches nothing is reported on stderr and exits non-zero. Treat that as a
failure, not noise — it usually means a slide moved or the token was mistyped.

Two values are hardcoded as literal text rather than brackets, so nothing flags them:
`Jek Bao Choo` on slide 1 and `VP of Engineering` on slide 8. `--list` reports them
under `literals`. Confirm both — the wrong name on a cover slide is the most
embarrassing failure this skill can produce.

Then set the region, apply the template's own defect fixes, and pack. Commands, the
site URL table, and the defect list are in
[references/editing-and-qa.md](references/editing-and-qa.md).

```bash
py "$SKILL/scripts/clean.py" unpacked/
py "$SKILL/scripts/office/pack.py" unpacked/ \
    "pocs/<customer>/poc-scoping-<customer>-<ISO-date>.pptx" --original "$TEMPLATE"
```

Preserve the branding — only replace placeholder text. Never alter the palette, the
logo, the master styling, or `ppt/fonts/`.

### Step 7 — Verify

Render and read every slide when LibreOffice and Poppler are available. If they are
not, say so plainly rather than skipping QA quietly, and rely on the text checks.

Always run the text gate, on the **packed output** rather than the working directory:

```bash
py "$SKILL/scripts/office/unpack.py" "$OUT" check/
python3 "$SKILL/scripts/fill_deck.py" --list check/ --pretty
unzip -l "$OUT" | grep -c 'ppt/fonts/.*fntdata'    # expect 10 — embedded Roboto
```

Two invariants before you call it done:

1. **Every remaining token appears in `open-questions.md`.** That is what makes a
   partially-filled deck safe to hand over — each blank is a known, asked question
   rather than an oversight.
2. **The MTTD arithmetic multiplies out.** Incidents × FTEs × hours must equal the
   total, and the percentage must match. A prospect's finance team will check.

Detailed issue checklist, font-size table, and render commands are in
[references/editing-and-qa.md](references/editing-and-qa.md).

## Resources

- **[references/slide-map.md](references/slide-map.md)** — what each of the 19 slides is for, the tokens on it, hardcoded values, template defects, and unused layouts
- **[references/intake-checklist.md](references/intake-checklist.md)** — what to extract per slide, and what to ask when the notes are silent
- **[references/editing-and-qa.md](references/editing-and-qa.md)** — build pipeline, fill-map syntax, region URLs, adding and removing slides, QA checks
- **`scripts/extract_notes.py`** — meeting notes in six formats to one markdown stream
- **`scripts/fill_deck.py`** — list and fill placeholders across split runs (`--list`, `--apply`)
- **`scripts/`** — PPTX utilities (`add_slide.py`, `clean.py`, `thumbnail.py`, `office/unpack.py`, `office/pack.py`, `office/soffice.py`)
- **`assets/poc_scoping_template_2026.pptx`** — the branded source template
