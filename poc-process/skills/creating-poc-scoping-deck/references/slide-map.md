# PoC Scoping Template — Slide Map

What is on each slide of `assets/poc_scoping_template_2026.pptx`, and what has to be
filled in. Read this before building the fill map.

The deck is 19 slides, 16:9, one master, 40 layouts (only 5 in use). It was authored in
Google Slides and exported, so every shape is named `Google Shape;NNN;pNN` and **only
slides 4, 6 and 17 use the layout's body placeholder** — everything else is a
free-floating, absolutely-positioned text box. That is why the fill works by matching
text tokens rather than by placeholder index.

## Narrative arc

Slide 2 states the spine itself, in three braces: **Why PoC? → What is part of the
PoC? → Who would be involved?**

| Act | Slides | Job |
|---|---|---|
| Frame | 1–2 | Who we are meeting and what we will cover |
| Why | 3–5 | Pain, the prize, and the money case |
| Who and how | 6–8 | Cadence, mutual responsibilities, named contacts |
| What | 9–15 | What week 1 actually looks like, and how to get unstuck |
| Close | 16–19 | Commitments, and the drive to the Mutual Activity Plan |

The centre of gravity is the **MAP (Mutual Activity Plan)**, referenced on slides 7 and
18. Everything before it justifies it; everything after it schedules it. A scoping deck
that does not end with an agreed MAP has not done its job.

## Per-slide detail

| # | Title | Layout | Fill |
|---|---|---|---|
| 1 | Cover | `Cover_1` | `[Prospect / Customer Name]`, `[Date]`, `[AE Name]`, and the literal `Jek Bao Choo` |
| 2 | Agenda — 5-step chevron | `Title + Content_gradient bg` | none |
| 3 | Current & Future States | `Title + Content_gradient bg` | 6 bracketed blocks |
| 4 | Define Success Criteria | `Title + Content_gradient bg` | `[Business use cases 1-3]`, `[Success criteria 1-3]` |
| 5 | MTTD Calculation | `Title + Content_gradient bg` | `[99]`, `[12]`×3, `[22]`, `[19,000]`, `[72]`, `[10,368]`, `[45]`×2 |
| 6 | Meeting Cadence Alignment | `Title + Content_gradient bg` | 4 `…` blanks |
| 7 | Roles & responsibilities — Venn | `Title + Content_gradient bg` | `[Prospect]`; two `Notes` callouts |
| 8 | Roles & responsibilities — Contacts | `Title + Content_gradient bg` | full roster; the literal `VP of Engineering` |
| 9 | Divider — "A glimpse of the PoC kick-off" | `Callout_pink` | none |
| 10 | Step 1: Set up one Datadog account | `Title + Content_gradient bg` | data-centre choice |
| 11 | Step 2: Integrate with cloud providers | `Title + Content_gradient bg` | none |
| 12 | Step 3: Install the Datadog Agents | `Title + Content_gradient bg` | region URLs |
| 13 | Step 4: Add the Datadog RUM SDKs | `Title + Content_gradient bg` | drop if RUM is out of scope |
| 14 | Divider — "Support" | `Divider_2` | subtitle is a run-on (see Defects) |
| 15 | Step 5: How to raise a support ticket | `Title + Content_gradient bg` | region URLs |
| 16 | Divider — "Next steps" | `Callout_pink` | none |
| 17 | Next steps — cadence | `Title + Content_gradient bg` | 3 `…` blanks |
| 18 | Next steps — 5-step chevron | `Title + Content_gradient bg` | kick-off date, prerequisites |
| 19 | Thank you | `Cover` | `[AE Name]`, `[SE Name]` |

Run `fill_deck.py --list` for the authoritative inventory — it groups tokens by shape,
which is what you need to pick anchors.

## Slides that need care

**Slide 5 (MTTD).** The `[12]` appears three times and `[45]` twice, so scope them by
slide: `"5:[12]": ["12","12","9"]`. Anchors do **not** work here — each cell of the grid
is its own `<p:sp>`, so `"Before Datadog >> [12]"` matches nothing. Worse, the shapes
overlap and their z-order is untidy, so document order does not follow reading order.
Fill it, then read the slide back and confirm each number landed in the cell you meant.
The grid reads: incidents/year × FTEs/incident ×
hours/incident = total hours/year, once for "Before Datadog" and once for "With
Datadog", then a % reduction row. The `~` on `~[19,000]` sits outside the bracket, so
the token is `[19,000]`. Make the arithmetic actually work — a value slide with numbers
that do not multiply out is worse than no value slide, because a CFO will check.

**Slide 8 (Contacts).** Two shapes: the **prospect** panel (Champion, DevOps, SRE) is
stored *first* in the XML even though it renders on the right, and the **Datadog** panel
(AE, SE) second. Ordering by document position therefore puts the AE's address in the
champion's slot. Anchor instead:

```json
"[Champion Name] >> [email]": ["dana@acme.com", "marc@acme.com", "aiko@acme.com"],
"[AE Name] >> [email]":       ["priya@datadoghq.com", "sam@datadoghq.com"]
```

**Slides 6 and 17** are near-duplicates — 17 is 6 minus the "Showback PoC meeting"
block. Fill both, and keep them consistent; contradicting cadence slides in one deck
undermine the commitment you are asking for.

**Slide 7** has two callout bubbles both reading `Notes`. They are meant to be annotated
live during the meeting. Leave them unless the notes say otherwise.

## Hardcoded values that look filled but are not

Two strings are baked in as literal text rather than brackets, so nothing flags them:

| Slide | Literal | Treat as |
|---|---|---|
| 1 | `Jek Bao Choo` | the SE name (slide 19 correctly uses `[SE Name]`) |
| 8 | `VP of Engineering` | the champion's title (every other title is bracketed) |

`fill_deck.py --list` reports these under `literals`. Shipping a deck with the wrong
person's name on the cover is the single most embarrassing failure this skill can have,
so always confirm both.

## Defects in the source template

Fix these while the deck is unpacked; they are template bugs, not prospect content.

- **Slide 10** — two badge groups (`1.`, `2.`) are positioned at x = −0.38in, off the
  canvas. They never render. Delete them or move them on-slide.
- **Slide 10** — footnote reads `note: All hyperlinks shown in this document are linked
  to US1. Please change to your relevant data center if required.` Once you have set
  the region, this instruction-to-the-presenter is stale; rewrite or remove it.
- **Slide 15** — the slide-number placeholder sits at (12.37, 6.78) instead of
  (12.95, 7.12) like every other slide.
- **Slides 3 and 8** — an empty duplicate sub-header text box.
- **Slide 14** — subtitle reads `How to get help Raising a Datadog support ticket`, two
  sentences run together. Separate them.

## Branding — do not change

Theme `2025_DD_v1`. `dk2` `#8000FF` is Datadog purple; accents `#00E37D`, `#0060FF`,
`#FF5E00`, `#00CAFF`, `#FF9B00`, `#FF0080`.

Typography is Roboto / Roboto Medium / Roboto Mono, and the fonts are **embedded** via
`ppt/fonts/*.fntdata` plus `p:embeddedFontLst` in `ppt/presentation.xml`. Both must
survive the repack or the deck renders in a fallback face on any machine without Roboto
installed — which is most prospect laptops, and you will not see it on your own.

## Unused layouts

35 of the 40 layouts are unused, so extending the deck needs no new design work:

| Layout | File | Good for |
|---|---|---|
| `Content 1/3_purple` | `slideLayout29.xml` | sidebar + content (tech stack) |
| `TWO_OBJECTS` | `slideLayout40.xml` | side-by-side (tech stack, timeline) |
| `From_To_purple` | `slideLayout21.xml` | current → future state |
| `Screenshot` | `slideLayout23.xml` | architecture or UI |
| `Agenda` | `slideLayout3.xml` | a real agenda layout (slide 2 does not use it) |
| `Subdivider_*`, `Divider_1/3/4/5` | various | extra section breaks |

## Gaps the template does not cover

Two promises the deck makes and does not keep. Fill them when the notes support it; see
Step 5 of SKILL.md.

1. **Tech stack / environment.** Agenda step 3 promises "Identify env, services & apps —
   tech stack (incl. ver), pre-prod, owners & size". No slide delivers it.
2. **Schedule.** The cover subtitle says "PoC scoping, alignment, **and schedule**", but
   timing appears only as "cadence" and a "PoC kick-off date" on slide 18.
