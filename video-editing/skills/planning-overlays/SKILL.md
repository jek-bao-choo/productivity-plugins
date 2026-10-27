---
name: planning-overlays
description: >-
  This skill should be used when the user wants to plan overlay beats
  (lower-third cards and occasional full-frame takeovers) on top of an approved
  storytelling plan (plan/STORY.md, plan/DESIGN.md, plan/beat-sheet.json) for an
  edited video. It applies when the user says "plan the overlays", "run
  planning-overlays", "plan lower thirds", "where should cards and takeovers
  go", "check overlay coverage", or "write overlay-beats.json and OVERLAYS.md",
  even if they don't name the skill. It is agent 4 of the editing pipeline and
  usually follows planning-storytelling. Use it for the planning step only, not for
  building HyperFrames compositions or rendering. The skill runs read-only
  pre-flight checks, builds or reuses beats_tools.py, scans storyboard coverage
  for pacing gaps, proposes one overlay or none per topic span, picking a card
  type for each from a fixed card library and using the Datadog design system
  by default, stops for the user's choices, then writes plan/overlay-beats.json,
  plan/overlay-beats.md and plan/OVERLAYS.md, and stops before any build.
version: "0.2.0"
author: productivity-plugins
---

# Planning Overlays

This is agent 4 (planning-overlays) of the video editing pipeline.

Follow this tested prompt exactly as written; do not reinterpret or simplify it.

```
Plan the overlay beats for this video: lower-third cards and occasional
full-frame takeovers that sit on top of the approved storytelling plan.
Planning only: no compositions, no HyperFrames, no rendering. Work in two
phases and stop between them for my approval.

How this fits the storytelling plan
- The storytelling plan (plan/STORY.md, plan/DESIGN.md,
  plan/beat-sheet.json) is approved and governs. Overlays never redraw,
  move or relabel world elements, never change a camera window, and use
  the same design system and timing window.
- If the storyboard already carries an idea visually, that idea gets no
  overlay.

Locked cut
- Use raw.clean.mp4 + raw.mistakes-transcript.json if both exist;
  otherwise raw.silenced.mp4 + raw.silence-transcript.json.
- The video duration must be within 0.1s of the transcript's
  audio_duration_secs. If not, stop.

Script
- beats_tools.py (in this folder): reuse it from
  <PATH TO PREVIOUS FOLDER>/beats_tools.py and copy it in if it isn't
  already here. Only write a new one if it's missing, from the spec
  below, in Python with only the standard library. Show the full script
  only if it is new or changed. Run Python with -I.

Safety
- Never modify the locked video, its transcript, raw.mp4, any earlier
  step's files, or the existing plan files (STORY.md, DESIGN.md,
  beat-sheet.json, beat-sheet.md). Record their md5s before starting and
  confirm them at the end.
- New plan files open with mode "x": plan/overlay-beats.json,
  plan/overlay-beats.md, plan/OVERLAYS.md. If any exists, stop and tell
  me.
- Scratch files go to /tmp/overlays/. Build and iterate the overlay file
  there (a generator that computes start = anchor start - 0.20 from the
  transcript), run check until it has 0 errors, then write it to plan/.

Pre-flight (read-only, report results)
- plan/STORY.md, plan/DESIGN.md and plan/beat-sheet.json exist. Read
  them: the canvas, sections, layers per beat, and the speaker inset's
  canvas rect (that becomes inset_rect).
- ffmpeg and /opt/homebrew/bin/ffprobe exist.
- story_tools.py index <transcript> if story_tools.py is here; otherwise
  print an indexed word list yourself to
  /tmp/overlays/transcript-indexed.txt.
- beats_tools.py coverage plan/beat-sheet.json --transcript <transcript>
  with the default thresholds, and again with the thresholds you propose
  for this video's length.

=== OVERLAY RULES ===

Core goal. Every overlay answers exactly one of these (its "answers"):
- remember: what should the viewer remember?
- structure: what concept needs visual structure?
- emphasis: what stat, contrast or pivot deserves emphasis?
- pacing: where is it quiet enough that the viewer may drift?
Never add an overlay just because a gap exists. A gap is filled only
where the narration has a topic, transition, proof point or mental model
that benefits from support. "pacing" still needs a supportable concept.

Beat types
- card (lower third): the speaker stays visible and the card supports
  the current idea. Uses: explanation scaffolds, topic labels,
  equation-style mental models (A + B = outcome), small lists, "what
  this means" translations, pacing fills in long talking-head or demo
  stretches. One card per topic span, not many small flashes. A card
  lives across its whole topic; if the narration evolves, build a
  subline or list item in midway (builds) instead of starting a new card.
- takeover (full frame): a major thesis, "in this video" overview,
  section marker, big stat, short quote or contrast that should briefly
  own the frame. 4-12s, occasional punctuation, at most one per section,
  never over a long explanation. It hides the speaker; count it against
  presence.
- none: the default when the storyboard already shows the idea.

Card types (the build step's card library; pick one per overlay)
  card kind:
    lt-headline   headline + optional subline; no items
    lt-list       headline + 1-4 items (items build in at their phrases)
    lt-equation   2-3 terms as items, joined by + = or ->; only the
                  result term may use Signal ink; joiners go in
                  operators [strings], one between each pair of items
                  (e.g. ["+", "="])
  takeover kind:
    to-statement  headline + optional source line (subline); no items
    to-stat       headline = number + unit + short label; no items; the
                  number uses Signal ink and may roll as an odometer;
                  write the number and unit as one token (40ms, 3x,
                  99.9%) so the headline stays within 3 words
    to-overview   headline + 1-4 items, for an "in this video" moment
If none fits, say so in Phase 1 and propose a new type with its slot
limits; don't invent one silently. If I approve it, add it to
beats_tools.py's card type table with its kind and item range, and show
the diff before Phase 2 check.

Placement
- Cards sit in the lower half, never cover the face or overlap the
  speaker inset, never cover what the viewer must read on screen at that
  moment (check frames at the card's times), and keep 60px from every
  frame edge. Prefer bottom-centre; when the inset is bottom-right, use
  the lower-left area that stays clear of it.
- Card width up to ~70% of the canvas width, max 1280px.
- One overlay on screen at a time. Clear 0.1-0.5s before the next one
  unless the handoff is intentional (say so in notes).

Timing
- Anchor every overlay to the first word of its topic. Start 0.15-0.25s
  before that word (the storytelling window, so both layers check the
  same way). Keep it until the topic ends or hands off. Time each build
  to its spoken phrase.
- Failure to avoid: a card on the right topic that lasts 5-8s while the
  speaker keeps discussing it for 20-40s.
- Defaults: card 12-30s, long-topic card 25-45s with builds, overview
  takeover 8-10s, stat takeover 5-8s.

Pacing (thresholds are parameters; propose values for this video)
- Long-form defaults: at most 20s without a new visual idea in the early
  span (first 60s), 30s strict and 45s maximum after that.
- For a short video, propose tighter values in Phase 1 with the reason;
  use the approved values in Phase 2.
- Report gaps from the coverage scan, not from file order.

Writing (glance comprehension: under one second)
- headline 1-3 words; optional subline up to 7 words with no closing
  full stop (a fragment, not a sentence); items up to 3 words each,
  within the card type's item count. Short noun phrases, direct labels,
  one mental model per card, numbers only when meaningful, verbs when
  they clarify the action.
- Never repeat the voiceover, use hype words, highlight more than one
  word, or explain how to use the video inside the graphic.
- Overlay words count toward the storyboard's ~20 words per section.
- Never label real footage with a name that's only a spoken example.

Style (from plan/DESIGN.md; Datadog by default)
- Card: frosted ground plate (Ground #140A22 at ~0.72 opacity with
  backdrop blur), radius 40 superellipse, three-layer neutral shadow,
  top-lit edge light. Headline type 42 in #ECEAF2; subline and items 30
  in #CFCADB; list markers in Signal ink #D3A6FF. Only a true stat
  number or one power word may use Signal ink. Nothing warm unless a
  human is involved.
- Takeover: a full-frame plate on Ground with sparse type (60 or 84 for
  the statement, 30 for a source line), entering and leaving by clip
  wipe over the world while the camera holds still underneath; never a
  cross-fade, never a world reset.
- No logos or brand marks.
- Motion: entrances cubic-bezier(0.16,1,0.3,1), exits faster, no
  back.out on overlays (the storyboard owns it), deterministic only.

What to preserve
- If I said an overlay is too long, don't restore it to satisfy a
  coverage rule; fill after it with a shorter card if the topic needs it.
- Approved card style and typography stay stable; adjust only local size
  or weight.
- If the face matters at a moment, prefer a card to a takeover.

=== beats_tools.py SPEC ===
Words = transcript entries with type "word" (or no type) and numeric
start/end, indexed 0..n-1. Exit codes: 0 ok (warnings allowed),
1 errors, 2 bad input (unreadable JSON, no words list, no
audio_duration_secs, no overlays list).

coverage BEATSHEET --transcript T [--overlays O] [--early 20]
         [--early-span 60] [--strict 30] [--max 45]
  Events = storyboard beats that draw new elements, have captions, or
  change camera_window from the previous beat (the first beat always
  counts), plus each overlay start and each overlay build time. Gaps run
  between consecutive points of [0, events..., duration]. A gap starting
  before --early-span is flagged EARLY if longer than --early, otherwise
  STRICT if longer than --strict; any gap longer than --max is MAX.
  Print the event count and each flagged gap (flag, range, length, the
  events on each side). Always exits 0 unless the input is bad.

check OVERLAYS --beatsheet B --transcript T [--budget 20]
  Overlays file: { canvas {width, height}, inset_rect [x0,y0,x1,y1],
  overlays [{id, kind card|takeover, card (type from the table above),
  section, anchor {index, text, start}, start, end, headline, subline
  (optional), items (optional), operators (lt-equation only), builds
  [times] (optional), placement [x0,y0,x1,y1] (cards), answers
  remember|structure|emphasis|pacing, notes (optional)}] }
  Card types: lt-headline (card, 0 items), lt-list (card, 1-4),
  lt-equation (card, 2-3), to-statement (takeover, 0), to-stat
  (takeover, 0), to-overview (takeover, 1-4).
  Errors:
  - missing or duplicate id; bad kind or answers; non-numeric start/end
    or end <= start; unknown section; end after the video
  - anchor index out of range, anchor text != transcript text, or anchor
    start off by more than 0.0015s; lead outside 0.15-0.25s (+-0.0015)
  - headline not 1-3 words; subline over 7 words; subline ending in
    . ! or ?; an item over 3 words; a build time not strictly inside the
    overlay
  - card missing or not a known type; card type of the other kind (then
    skip its item-count check); item count outside the card type's range
  - lt-equation without operators, or operators count != items - 1
  - card without a placement rect; placement within 60px of any frame
    edge; placement overlapping inset_rect
  - two overlays on screen at the same time
  Warnings:
  - takeover outside 4-12s; card shorter than 8s
  - card placement starting above the frame's vertical midline
  - card wider than min(1280, 0.72 x canvas width)
  - less than 0.1s between one overlay ending and the next starting
    (only for overlays that don't overlap; an overlap is already an
    error)
  - section words over --budget, counting storyboard label and caption
    words plus overlay headline, subline and item words
  Report: words per section (storyboard + overlays); speaker-on-screen %
  (each storyboard beat's speaker_visible from its enter to the next
  beat's enter, speaker visible before the first beat, minus takeover
  time); for each overlay, the storyboard beats it sits over as
  id:layer.

self-test (run first; fix the script if anything differs)
  Transcript (duration 120): Datadog 1.00-1.50, agents 1.60-2.00,
  collect. 2.10-2.60, Traces 30.00-30.50, connect 30.60-31.00,
  services. 31.10-31.70, Logs 70.00-70.40, explain 70.50-71.00,
  errors. 71.10-71.60, Done. 110.00-110.50.
  Storyboard: canvas 1920x1080; sections s1 0-29.8, s2 29.8-69.8,
  s3 69.8-120. Every beat enters 0.2s before its anchor, speaker
  visible, layer overlay:
    b1 s1 anchor 0 "Datadog", camera W1, new A/element/"Agent", plant
    b2 s2 anchor 3 "Traces", camera W1, new T/element/"Traces", reshow
    b3 s3 anchor 6 "Logs", camera W1, new L/element/"Logs", reshow
    b4 s3 anchor 9 "Done.", camera W2, no new elements, close
  Overlays: inset_rect [1440,600,1860,1020];
    o1 card, card lt-headline, s2, anchor 4 "connect" 30.60, start
       30.40, end 52.00, headline "Service map", subline "every hop
       timed", placement [160,700,1300,980], answers structure
    o2 takeover, card to-statement, s3, anchor 7 "explain" 70.50, start
       70.30, end 78.30, headline "Why it failed", answers emphasis
  Expected coverage, storyboard only: events 0.8, 29.8, 69.8, 109.8;
    flags EARLY 0.8-29.8 (29.0s), EARLY 29.8-69.8 (40.0s),
    STRICT 69.8-109.8 (40.0s).
  Expected coverage with overlays: 6 events; flags EARLY 0.8 (29.0s),
    EARLY 30.4 (39.4s), STRICT 70.3 (39.5s). With --max 35: EARLY 0.8,
    MAX 30.4, MAX 70.3.
  Expected check: 0 errors, 0 warnings; words s1 = 1, s2 = 6, s3 = 4;
    speaker on screen 93.3%.
  Broken copy: o1 anchor text "connects"; o1 placement
    [160,700,1700,980]; o1 subline "Every hop is timed, end to end.";
    o2 headline "Why the checkout failed"; o2 end 84.30; o2 card
    lt-list; add o3 card, card lt-headline, s2, anchor 5 "services."
    31.10, start 30.90, end 40.00, headline "Hops", placement
    [160,700,1300,980], answers structure; add o4 card, card
    lt-equation, s1, anchor 1 "agents" 1.60, start 1.40, end 12.00,
    headline "Signals", items ["Agents", "Metrics", "Insight"],
    operators ["+"], placement [160,700,1300,980], answers structure.
  Expected: exactly 7 errors (anchor text mismatch, subline reads as a
    sentence, o1 overlaps the inset, headline over 3 words, o1 and o3 on
    screen at the same time, o2's card lt-list is a card type on a
    takeover, o4 has 1 operator for 3 items) and exactly 2 warnings (o1
    is 1540px wide, o2 takeover lasts 14.00s).
  Show expected vs actual.

=== PHASE 1: COVERAGE AND PROPOSALS (no plan files) ===
Run the self-test and pre-flight. Report:
- Self-test result and pre-flight results.
- The storyboard coverage map: every visual-change event, and every
  flagged gap at the default thresholds and at your proposed ones.
- Topic spans from the narration (not from timestamps): start and end
  word index and time, and what the topic is.
- A proposal table, one row per topic span: overlay or none, kind, card
  type, answers, anchor word (index, time), start, end, builds,
  headline / subline / items, placement, what it sits over in the
  storyboard, and why. Include the spans you chose "none" for and why.
- Projected words per section and speaker-on-screen % with the
  proposals.
- Conflicts with the storyboard you see (covered on-screen text, a card
  doubling a world element, budget pressure), each with a fix.
- Ask which thresholds to use and which proposals to keep, as
  decisions in the orchestrator's format: a recommended choice for the
  thresholds and for each proposal row (keep / drop), each with a
  one-sentence reason. Skip any choice already recorded in the ledger.

Stop and wait for my choices.

=== PHASE 2: WRITE THE OVERLAY PLAN (only after I choose) ===
Build the overlays in /tmp/overlays/, run check until 0 errors, fix or
justify every warning, and re-run coverage with the overlays. Then write
(mode "x"):
- plan/overlay-beats.json (schema above).
- plan/overlay-beats.md: the same as a readable table grouped by
  section, with each overlay's card type and reason.
- plan/OVERLAYS.md: the build rules for overlays, so the build step can
  follow them without this prompt:
  - the style, placement, motion and writing rules above, with this
    video's values (inset rect, card area, thresholds);
  - the card types used, with their slots and limits;
  - each overlay is an instance of its card type from the build step's
    card library (film/cards/), with slots filled from this plan:
    compositions/beats/NNN-short-name.html, mounted in index.html on its
    own overlay track above the world and section hosts, with
    data-start, data-duration and data-track-index and the project's
    clip class;
  - each overlay composition registers one paused GSAP timeline on
    window.__timelines and pads it to its slot (tl.to({}, {duration:
    SLOT}, 0) or tl.set({}, {}, SLOT)), where SLOT equals the mounted
    duration;
  - deterministic logic only; no animating video dimensions or media
    properties; no same-track overlaps; HyperFrames check after every
    edit;
  - follow the build step's seek-safety rules (paused timelines,
    immediateRender:false defaults, initial states via gsap.set outside
    the timeline).
Run both:
  beats_tools.py check plan/overlay-beats.json --beatsheet plan/beat-sheet.json --transcript <transcript>
  beats_tools.py coverage plan/beat-sheet.json --transcript <transcript> --overlays plan/overlay-beats.json <approved thresholds>

Report:
- The overlay table, both outputs and each warning's resolution.
- Remaining flagged gaps and why each has no supportable concept.
- Judgment calls the checker can't see (on-screen text under a card,
  face clearance, takeovers near payoff beats).
- Input md5s unchanged.

Stop. No compositions until I approve the overlay plan. The build step
comes next: the open loop's shared geometry first, then one section end
to end, rendered and reviewed muted, before the rest.
```
