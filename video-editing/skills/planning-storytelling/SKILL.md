---
name: planning-storytelling
description: >-
  This skill should be used when the user wants to plan the visual story for an
  edited video (typically raw.clean.mp4 or raw.silenced.mp4 with its re-timed
  transcript) before any compositions are built. It applies when the user says
  "plan the visual story", "run planning-storytelling", "make a beat sheet", "storyboard
  this video", "propose world concepts", "plan the open loop and camera
  windows", or "write STORY.md and DESIGN.md", even if they don't name the
  skill. It is agent 3 of the editing pipeline and usually follows
  cutting-mistakes. Use it for the planning step
  only, not for building HyperFrames compositions or rendering. The skill runs
  read-only pre-flight checks and a contact sheet, builds or reuses
  story_tools.py, proposes 2-3 world concepts and canvas options using the
  Datadog design system by default, stops for the user's choice, then writes
  plan/STORY.md, plan/DESIGN.md and a checked beat sheet, and stops before
  planning-overlays.
version: "0.1.0"
author: productivity-plugins
---

# Planning Storytelling

This is agent 3 (planning-storytelling) of the video editing pipeline.

Follow this tested prompt exactly as written; do not reinterpret or simplify it.

```
Plan the visual story for this video. Planning only: no compositions,
no HyperFrames, no rendering. Work in two phases and stop between them
for my approval.

Locked cut
- Use raw.clean.mp4 + raw.mistakes-transcript.json if both exist;
  otherwise raw.silenced.mp4 + raw.silence-transcript.json. All plan
  times are on this timeline.
- The video duration must be within 0.1s of the transcript's
  audio_duration_secs. If not, stop: the pair doesn't match.

Script
- story_tools.py (in this folder): reuse it from
  <PATH TO PREVIOUS FOLDER>/story_tools.py and copy it in if it isn't
  already here. Only write a new one if it's missing, from the spec
  below, in Python with only the standard library. Show the full script
  only if it is new or changed. Run Python with -I.

Safety
- Never modify the locked video, its transcript, raw.mp4 or any earlier
  step's files. Record md5s before starting (raw.mp4, raw.silenced.mp4,
  raw.silence-*, transcript*.json, cut_*.py, raw.cut-*,
  raw.approved-cuts.json, plus raw.clean.mp4 and raw.mistakes-* if they
  exist) and confirm them at the end.
- Plan files go to ./plan/ (create it). Never overwrite a plan file:
  open with mode "x"; if plan/ or a plan file exists, stop and tell me.
- Scratch files go to /tmp/storytelling/. Build and iterate the beat
  sheet there (a generator script that computes enter = anchor start -
  0.20 from the transcript), run check on the scratch copy until it's
  clean, and only then write it into plan/.

Pre-flight (read-only, report results)
- ffmpeg and /opt/homebrew/bin/ffprobe exist. Report codec, resolution,
  fps, duration and aspect ratio of every stream in the locked video.
- Contact sheet: one frame every 5s, scaled to 640px wide, tiled 2x4
  with padding into /tmp/storytelling/contact-*.png (frames run left to
  right, top to bottom, 5s apart; this ffmpeg build has no drawtext, so
  don't try to stamp timestamps). Look at every tile. Describe the
  layout: screen content, webcam position, what changes over time, and
  whether the frame is a split (e.g. two 16:9 halves) that changes the
  canvas options.
- Also grab full-resolution crops of the screen at 3-4 key moments (the
  live product, any docs or code) to locate real on-screen subjects and
  footage windows in source pixels.
- story_tools.py index <transcript> --out /tmp/storytelling/transcript-indexed.txt
- story_tools.py air <transcript>

=== STORYTELLING RULES ===

One persistent world
- The video lives in one space that never resets. Anything drawn stays
  where the viewer left it; new material is added, never redrawn, moved
  or relabelled.
- Decide the spatial grammar first (e.g. left to right = toward the
  outcome, up = toward a human) and hold it for the whole runtime. Break
  it exactly once, deliberately, for meaning.

The camera is the edit
- Prefer moving through the world over cutting to new graphics.
  Altitudes: World (orient, payoff), Region (most of the runtime), Detail
  (one number, state change or decision). Move between adjacent
  altitudes; World<->Detail only as a deliberate payoff.
- Name framings as exact windows (x0,y0,x1,y1), never scale factors.
  World windows are in world px on a declared world plane (e.g.
  3840x2160); footage windows are in source px of the full recording.
  Window edges fall between labels. One window, one purpose; near-
  identical windows read as drift.
- Move duration scales with distance. Camera and full-frame wipes are
  sequenced (camera first), never concurrent; a cover layer is opaque
  before the camera moves under it. Two sequential moves on one subject
  become one gesture with a shared symmetric ease (power2.inOut).
- No label within 60px of the frame edge (rendered pixels, after the
  window's scale).

Attention is a spotlight
- Exactly one element at full brightness at any moment; everything else
  drawn stays quiet but legible. Hierarchy comes from the active/quiet
  ratio, never from making everything dark. A label inherits its
  element's state. A finished prop retires to opacity 0, not 0.3.

Open loops are spatial
- Never say "we'll come back to this"; leave something visibly
  incomplete. Plant it in the hook, re-show it at every section boundary
  (~2s), advance it visibly, close on the opening image.
- Shapes:
    N parallel items        -> N sockets on a spine; empty slots
    One process, deep       -> the full pipeline; a broken link
    Levels or tiers         -> a stack building up; the top is a ghost
    Comparison              -> two columns, one axis; one column empty
    News or announcement    -> timeline or map; the future is blank
    Tutorial or build-along -> finished architecture ghosted
    Product demo            -> end-state dashboard ghosted; panels light
                               up as the demo reaches them
- Filling the loop is a live ~1.4s camera move, never a cut to a
  pre-made picture. A counter needs a 1-2 word name, not just a number.

Discipline
- If it doesn't get a word, it doesn't get drawn. Every shape is a
  labelled element, a connector between labelled elements, the
  travelling subject, or ambient ground. Nothing decorative.
- ~20 on-screen words per section. No sentences. Labels 1-2 words.
- An anti-pattern visual never overlays the recommendation.
- One travelling subject whose state visibly changes; it moves along
  drawn connectors at constant speed and never teleports.
- Motion: entrances cubic-bezier(0.16,1,0.3,1); exits faster; duration
  by mass; back.out exactly once per section; no cross-fade ever (full-
  bleed layers enter and exit by clip).
- Timing: every beat anchors to a word start and enters 0.15-0.25s ahead
  of it. Never divide a section evenly. A full-bleed screen that doesn't
  change for over 1.5s is a dead screen, so full-bleed stretches need a
  beat at least every 1.5s.
- Layers: overlay = the drawn world with the live speaker inset (the
  inset keeps the frame alive); full-bleed = the drawn world alone;
  footage = the recording (screen footage keeps the inset).
- Presence: aim for ~40% speaker on screen; long absences are fine at
  payoff beats.
- Type floor per window: rendered text must be at least 28px, so for
  every camera window, (canvas width / window width) x the smallest
  type token used by labels visible in it must be >= 28. A world-wide
  orientation or payoff window usually fails this; plan a tighter
  window instead of shrinking type. Record each window's min_type.
- End hold: the final frame holds for 4s or more. If the last beat is
  closer than 4s to the end of the audio, plan a tail_hold (seconds of
  silent hold after the audio) instead of cutting the hold short; the
  film's length is then duration + tail_hold.
- The close shows the planted loop element (the filled sockets, the
  completed pipeline) inside the close window at a legible size; if it
  can't, say so in STORY.md and plan a re-show just before the close.

Screen recordings (most Datadog videos)
- The screen is part of the world: zooms and pans into screen regions
  are camera moves (windows in source pixels). Overlays annotate what's
  on screen and never cover what the viewer must read at that moment.
- Prefer a real on-screen travelling subject (a request, trace, log
  line, alert) over a drawn stand-in. Show Datadog UI as it is; don't
  redraw product screens.
- Never label real footage with names that are only a spoken example
  (e.g. regions the speaker says "say..." about); those labels belong on
  drawn elements only.
- For every footage window, confirm from frames that the content is on
  screen at that beat's time; note any timing that needs checking during
  the build.
- Decide the delivery canvas explicitly. If the source isn't 16:9,
  propose options with costs (native, a 16:9 reframe following the
  action, or a 16:9 layout that re-places the webcam). If the recording
  is two 16:9 halves, say so: the screen half maps cleanly to 16:9.

=== DESIGN SYSTEM ===
Default: the Datadog design system below. Use it unless I specify a
different brand or design system; if I do, keep the same structure (one
token set, five colours with one meaning each, luma targets) and swap in
those values.

Tokens (nothing else): stroke 1.5 / 2.5 / 4 / 7; type 22 / 30 / 42 / 60 /
84; radius 10 / 22 / 40, always superellipse. One arrowhead size. Curved
connectors only. One typeface: the Datadog brand face if licensed,
otherwise one neutral grotesque.

Five colours, one meaning each:
  Ground        #140A22 (derived)      the canvas
  Structure     #C2BCD6 (derived)      structure, edges, quiet state
  Signal        #632CA6 fill, #8000FF accent (official press kit),
                #D3A6FF ink (derived)  Datadog doing the work: the
                                       active path. Nothing else purple.
  Human         #FFB454 / #FFD98F      a human is involved; nothing else
                                       is warm
  Type          #ECEAF2 / #CFCADB      text; never #FFFFFF
The brand purples are too dark for thin lines on dark ground (about Y=71
and Y=55), so they carry areas (plates, fills, glows); #D3A6FF carries
active lines; active labels use the Type colour. No cyan, no gradient
text. Replace derived values if internal brand values are available.
Luma targets (Y 16-235): active 200-235, context 120-150, spent 85-105,
labels never below 90. Verify on the render, not the hex.
No logos or brand marks: this is a personal learning video, not
official content. In text, "Datadog" is one word, capital D.
Material: three-layer shadow stack (contact, key, ambient), neutral
tones; top-lit edge light on plates; the video inset follows the same
corners, shadow and edge light.

=== story_tools.py SPEC ===
Words = transcript entries with type "word" (or no type) and numeric
start/end, indexed 0..n-1 in order. Sentence end = text ends with . ! ?
Exit codes: 0 ok (warnings allowed), 1 errors, 2 bad input (unreadable
JSON, missing words/sections/beats lists, no duration, or an existing
--out file).

index TRANSCRIPT [--out FILE]
  One line per word: "index  start  end  text" (3 decimals). --out opens
  with mode "x".

air TRANSCRIPT [--ratio 10]
  gap = max(0, word[i].start - word[i-1].end). Report the median gap,
  the number of sentence boundaries (prev word ends a sentence), and
  every sentence boundary with gap <= median/ratio, with its time (the
  previous word's end) and 3 words each side. Report only; the cut is
  locked.

check BEATSHEET --transcript T [--budget 20] [--dead 1.5]
  Beat sheet: { canvas {width, height, fps}, duration (optional, else
  audio_duration_secs), open_loop {shape, description} or null,
  camera_windows [{id, rect [x0,y0,x1,y1], purpose}],
  sections [{id, title, start, end}],
  beats [{id, section, anchor {index, text, start}, enter, hold_until,
  altitude world|region|detail|footage, camera_window (id or null),
  visual, active [ids], new_elements [{id, kind element|connector|
  subject|ground, label}], captions [strings] (optional),
  loop_role plant|reshow|advance|close|none, speaker_visible bool,
  layer overlay|full-bleed|footage, back_out bool (optional),
  notes (optional)}] }
  Errors:
  - missing beat fields; duplicate beat, section or window ids; empty
    window rects; unknown section or camera_window; bad enum values
  - anchor index out of range, anchor text != transcript text, or anchor
    start off by more than 0.0015s
  - lead (anchor start - enter) outside 0.15-0.25s (+-0.0015)
  - beats out of time order; hold_until <= enter
  - an element id drawn twice; an active id lit before it's drawn
    (elements in the same beat's new_elements count as drawn)
  - a label over 2 words; otherwise, kind "element" without a label
    (count each bad label once, never both errors)
  - back_out more than once in a section
  - open loop defined but no plant, or no close, or close before plant
  - a camera window with min_type set where (canvas width / window
    width) x min_type < 28 (type below the 28px floor)
  - tail_hold present but not a number >= 0
  Warnings:
  - sections not contiguous, not starting at 0, or not ending at the
    duration (+-0.05s); beat enter outside its section (allowing the
    0.25s lead)
  - two camera windows within 2% of canvas size on every edge
  - a beat lighting more than one element
  - section words (label words of elements first drawn there + caption
    words) over --budget
  - World<->Detail between consecutive beats, unless the first is a
    close or its notes contain "payoff"
  - full-bleed beat held longer than --dead, measured from its enter to
    the next beat's enter (or the end), not to hold_until
  - no open_loop; loop closes outside the last section; never advanced;
    for each section after the planting section, no reshow beat entering
    within [section start - 0.25s, section start + 3s]
  Report: presence % overall and per section (each beat's
  speaker_visible applies from its enter to the next beat's enter; the
  speaker counts as visible before the first beat), the 5 longest
  absences (consecutive hidden beats merged into one) with their beats,
  and words per section.

self-test (run first; fix the script if anything differs)
  Transcript (duration 5.5): The 0.50-0.70, agent 0.80-1.10, collects
  1.20-1.60, metrics. 1.70-2.20, Then 2.40-2.60, traces 2.70-3.10, flow
  3.20-3.50, in. 3.60-3.90, Finally 4.10-4.50, logs. 4.60-5.00.
  Air: median 0.1, 2 sentence boundaries, 0 flagged. With "Then" moved
  to start 2.205: 1 flagged, at 2.2.
  Sheet: canvas 1920x1080 @ 60; open_loop set; windows W_ORIENT
  [0,24,1920,1080], W_SLOT1 [160,300,800,700]; sections s1 0-2.3,
  s2 2.3-5.5.
    b1 s1 anchor 0 "The" 0.50, enter 0.30, hold 1.0, world, W_ORIENT,
       active [slots], new slots/element/"Signals", plant, visible,
       overlay, back_out
    b2 s1 anchor 2 "collects" 1.20, enter 1.00, hold 2.2, region,
       W_SLOT1, active [m], new m/element/"Metrics", advance, visible,
       overlay
    b3 s2 anchor 4 "Then" 2.40, enter 2.20, hold 3.0, region, W_ORIENT,
       active [slots], no new elements, reshow, not visible, full-bleed
    b4 s2 anchor 9 "logs." 4.60, enter 4.40, hold 5.4, world, W_ORIENT,
       active [payoff], new payoff/connector/no label, close, visible,
       overlay
  Expected: 0 errors; exactly 1 warning (b3 holds full-bleed 2.20s);
  presence 60.0% (s1 95.7, s2 34.4); words s1 = 2, s2 = 0.
  Broken copy: b2 anchor text "collect"; b2 enter 1.10; b2 back_out;
  b3 new element m/element/"Metrics"; b3 active [ghost]; b4 new element
  payoff/element/"All three signals now"; b4 loop_role none.
  Expected: exactly 7 errors (text mismatch, lead 0.10s, back.out twice
  in s1, m drawn again, ghost lit before drawn, label over 2 words, no
  close beat).
  Type copy: the good sheet with min_type 22 on both windows and
  tail_hold 4. Expected: exactly 1 error (W_ORIENT renders
  1920/1920 x 22 = 22px < 28; W_SLOT1 renders 1920/640 x 22 = 66px,
  fine) and the same 1 warning as the good sheet.
  Show expected vs actual.

=== PHASE 1: UNDERSTAND AND PROPOSE (no plan files) ===
Run the self-test and pre-flight. Report:
- Self-test result, pre-flight results and the contact-sheet
  description, including a time-ordered table of what's on screen.
- The transcript as readable paragraphs, with an edited timestamp at
  each sentence.
- Video type, audience and the one takeaway, a sentence each. Mark
  anything uncertain.
- The script shape and why, and the section boundaries (anchored on
  signpost words where the script has them).
- 2-3 world concepts. For each: the world; the spatial grammar and its
  one break; the travelling subject (real on-screen subject where
  possible); the open-loop shape with its plant, re-show, advance and
  close moments (anchor word index and time); sections with time
  ranges; the delivery canvas it needs; its cost.
- Your recommendation and why.
- Canvas options with costs.
- Air-check results.
- Ask these as decisions (orchestrator format: recommended option
  first, with why). Ask which concept, which canvas, which design system (Datadog by
  default), whether I have brand values to replace the derived colours,
  and whether the brand typeface is licensed.

Stop and wait for my choice of concept, canvas and colours.

=== PHASE 2: WRITE THE PLAN (only after I choose) ===
Build the beat sheet in /tmp/storytelling/ and run check on it until it
has 0 errors; fix or justify every warning. Then write (mode "x"):
- plan/STORY.md: the world (world plane size, every element's id,
  label and position), grammar and its one break, travelling subject
  and its states, open-loop table (role, beat, anchor, what happens),
  altitudes, every camera window (id, exact rect, one purpose; world px
  vs source px stated), the speaker inset (source crop and canvas rect),
  and build guardrails (example-only labels, footage timing to check),
  each window's scale and min_type, and the tail_hold if any.
  Beat sheet schema additions: camera_windows[].min_type (optional,
  the smallest type token labels use in that window) and tail_hold
  (optional, seconds of silent final hold after the audio).
- plan/DESIGN.md: the locked tokens and palette for this video, what
  each colour is used for here, any retuned value and why, the no-logo
  rule, material and motion.
- plan/beat-sheet.json (schema above) and plan/beat-sheet.md (the same
  as a readable table grouped by section).
Run: story_tools.py check plan/beat-sheet.json --transcript <transcript>

Report:
- The beat-sheet table, the check output and each warning's resolution.
- Judgment calls the checker can't see (inset-only holds, payoff
  absences, footage timing, example-only labels).
- Which section to build first and why (the one that proves the
  system).
- Input md5s unchanged.

Stop. No compositions until I approve the plan. Planning overlays
(planning-overlays) comes next.
```
