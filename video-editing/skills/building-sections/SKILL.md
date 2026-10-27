---
name: building-sections
description: >-
  This skill should be used when the user wants to build one section of an
  approved video plan (plan/STORY.md, plan/DESIGN.md, plan/beat-sheet.json and
  optionally plan/overlay-beats.json) end to end as HyperFrames compositions
  with GSAP, render it, and review it muted. It applies when the user says
  "build section s2", "run building-sections", "build the next section", "build
  the first section of the plan", "render and review this section", or "build
  the cards and overlays for this section", even if they don't name the skill.
  It is agent 5 of the editing pipeline and usually follows planning-overlays.
  The skill reads the HyperFrames and GSAP skills first, creates or reuses the
  film/ project, localizes every asset, builds the persistent world, the
  section's footage and speaker inset, and its overlays from a reusable card
  library, then runs check, timeline-duration, no-network, snapshot, render,
  muted frame review and luma checks, writes film/REVIEW.md and film/LESSONS.md,
  and stops after that one section.
version: "0.1.0"
author: productivity-plugins
---

# Building Sections

This is agent 5 (building-sections) of the video editing pipeline.

Follow this tested prompt exactly as written; do not reinterpret or simplify it.

```
Build one section of the approved plan end to end, then render it and
review it muted. Stop after that section; do not build others.

Run settings (fill in before each run)
- Section: <SECTION_ID> (its title and times come from
  plan/beat-sheet.json)
- First run for this video: <yes | no>
- Decisions already made: <list each, or "none">
- History author: <claude | codex | your name> (default claude)

Inputs (read-only)
- plan/STORY.md, plan/DESIGN.md, plan/beat-sheet.json,
  plan/beat-sheet.md, and plan/overlay-beats.json + plan/OVERLAYS.md if
  they exist.
- Locked cut: raw.clean.mp4 + raw.mistakes-transcript.json if both
  exist, otherwise raw.silenced.mp4 + raw.silence-transcript.json.
  Take resolution, fps, layout (e.g. split halves), footage crop and
  speaker-inset crop from plan/STORY.md; never assume them.
- film/LESSONS.md if it exists: lessons from earlier sections of this
  video. Read it before building.
- Never modify raw.mp4, the locked pair, earlier steps' files or
  anything in plan/. Record md5s before starting and confirm at the end.

Skills (read before authoring)
- HyperFrames (HeyGen): start with /hyperframes, then read the domain
  skills it points to for this work (the core composition contract,
  animation, media and CLI). Where they conflict with this prompt, they
  win; say what conflicted.
- GSAP (GreenSock): gsap-core and gsap-timeline; gsap-plugins,
  gsap-utils or gsap-performance only if you use them.
- If either skill set is missing, stop and tell me how to install it.
  Don't rebuild the contract from memory.
- Run `npx hyperframes usage --json` and report it ("unknown" if so).
- Never send frames, renders or transcripts to an external service. If
  a HyperFrames command offers an AI describe, upload or share option,
  leave it off.
- Scratch files (generators, frame grabs, measurements) go to
  /tmp/building/.

HTML or GSAP: decide per object, record it in film/SPEC.md (OBJECTS)
- HTML/CSS/SVG for structure and static look: the world plane, labels,
  plates, cards, the inset frame. Write it as static, editable markup;
  where geometry is computed, generate it from a scratch script and
  extend that script per section.
- GSAP for every change over time: camera, spotlight, label print-ins,
  wipes, card entrances and builds, counters. One paused timeline per
  composition, registered on window.__timelines under its composition id.
- Video and audio are framework-owned media (<video class="clip" muted>,
  <audio>) timed with data-* attributes. Never call play() or set
  currentTime from JavaScript; never tween media except opacity.
- No CSS animations or transitions for timed motion unless the
  HyperFrames animation skill says the renderer can seek them.

Project (film/, created on the first run, reused after)
- First run: `npx hyperframes init film --example blank --resolution
  <landscape | the canvas from plan/STORY.md> --non-interactive --skill
  hyperframes`, then write film/SPEC.md (GOAL, OUTPUT, TIME, LOOK,
  OBJECTS with html|gsap per object, MOTION, SHOTS with absolute times
  per beat, BANNED, QA times).
- Later runs: read film/SPEC.md, film/REVIEW.md and film/LESSONS.md
  first, run `npx hyperframes history --since mine --who <history author>`, and build on what
  changed.

Localize every asset (nothing loads from the network at render)
- Media into film/assets/, once: the screen footage (screen.mp4) and
  speaker inset (cam.mp4) cropped per plan/STORY.md, no audio, a
  keyframe every 0.5s (-g = fps/2); the voice audio copied. Check one
  inset frame shows the whole head. Keep these file names: the finish
  step's lip-sync check reads film/assets/cam.mp4.
- Fonts as local files with @font-face; no Google Fonts or other CDN.
- GSAP from a local copy in the project, not a CDN.
- No logos or brand marks. This is a personal learning video, not
  official content.
- Before rendering, search every file under film/ that the root loads
  for http:// and https:// URLs; any outside a comment is an error.

Architecture
- compositions/world.html: the one persistent world, hosted from 0 for
  the whole built span on the ABSOLUTE timeline. An SVG plane at the
  world size in plan/STORY.md inside a camera wrapper (transform-origin
  0 0); the camera is GSAP x/y/scale from the exact STORY.md window
  rects (scale = canvas width / window width).
- compositions/<section>.html: that section's footage beats and
  speaker inset, mounted at the section start with LOCAL times.
  Footage = an untimed wipe wrapper > untimed window div (CSS transform
  for the footage rect) > timed <video class="clip" muted> with
  data-media-start = absolute source time. Inset = a timed
  <video class="clip"> per beat, data-media-start = that beat's absolute
  time so it stays lip-synced, styled per plan/DESIGN.md.
- Overlays (if plan/overlay-beats.json exists): build every overlay
  whose start falls inside this section as an instance of the card type
  named in its card field, from the card library below, following
  plan/OVERLAYS.md.
- index.html: the root with the world host, section hosts above it, an
  overlay track above those, and <audio id="voice" data-volume="1">
  from 0. Set the root data-duration to the end of the last built
  section for now.
- Host ids: the host's data-composition-id, the inner composition's id
  and its window.__timelines key are identical; no -host or -mount
  suffixes.
- Check the nesting of timed media against HyperFrames' sub-composition
  rules (no <video data-start> under an ancestor that also carries
  data-start) and report how the section hosts satisfy them.
- Prefix every SVG def id (gradients, filters, masks, clip paths) with
  its composition id.

Seek and render safety
- Every timeline: gsap.timeline({paused:true,
  defaults:{immediateRender:false}}). Never call the global
  gsap.defaults(). Initial states via gsap.set() outside the timeline,
  never tl.set at 0. The earliest fromTo on a repeatedly tweened element
  gets immediateRender:true. Camera moves use fromTo with explicit
  from-values.
- Every timeline fills its slot: end it with
  tl.to({}, {duration: SLOT}, 0) (or tl.set({}, {}, SLOT)), where SLOT
  is the mounted data-duration. A timeline shorter than its slot hides
  the composition and flashes black.
- Snap every tween's end time to a multiple of 1/fps.
- Deterministic only: no Math.random(), Date.now() or unseeded noise;
  use a seeded hash if you need variation.
- A footage clip that starts or ends while visible gets poster and
  last-frame stills (extracted from the derived clip) bracketing it, or
  runs 0.3s past its exit wipe.
- Render with one worker.

Motion (plan/DESIGN.md and the storytelling rules win)
- One idea per beat. Every transition uses motion; never a hard cut or
  cross-fade between layers. Each colour carries its DESIGN.md meaning.
- Hold the opening title 1.5-2s and the final frame 4s or more.
- Explicit data-volume on every audio element (voice 1.0; any bed at
  0.15 or less, and only if I approved one).
- Seam convention: every entry or exit tween's comment names the
  matching tween across the seam. If you can't name it, the seam isn't
  designed yet.
- Eases: label reveal expo.out 0.2-0.33s; generic enter power2.out
  0.2-0.5s; generic exit power2.in 0.2-0.33s; camera power2.inOut at
  the durations the plan implies (scale with distance); slow drift
  sine.inOut.
- Don't use: gradient or glowing type; more than one typeface; fast
  1-2s scene cutting; a grid, crosshairs, vignette or grain on every
  scene (only a texture DESIGN.md names); light-streak or blur whips as
  the default transition; elastic or back overshoot beyond the
  storyboard's one back.out per section; HyperFrames registry blocks
  unless I approve them.

=== CARD LIBRARY ===
Cards are reusable HTML templates for overlays and takeovers, built from
plan/DESIGN.md's tokens and nothing else.

Where they live
- film/cards/<card-id>.html, one file per card type, plus
  film/cards/registry.json listing each card: {id, kind card|takeover,
  purpose, slots {name: limit}, size, notes}.
- Reuse film/cards/ from <PATH TO PREVIOUS FOLDER>/film/cards if it
  exists: copy it in, then re-token it against this video's
  plan/DESIGN.md. Otherwise build the cards this section needs from the
  catalogue below, and only those.

Catalogue (slot limits match planning-overlays)
- lt-headline (card): headline 1-3 words + optional subline up to 7
  words, no closing full stop. For topic labels and "what this means".
- lt-list (card): headline 1-3 words + 1-4 items of up to 3 words;
  items build in at their spoken phrases.
- lt-equation (card): 2-3 terms of up to 3 words, joined by + = or ->;
  only the result term may use Signal ink. The joiners come from the
  overlay's operators list (one between each pair of terms) and fill
  operator slots between the term slots; never pick them yourself.
- to-statement (takeover): headline 1-3 words at type 60 or 84 +
  optional source line up to 7 words at 30.
- to-stat (takeover): number and unit as one token (Signal ink; 40ms,
  3x, 99.9%) + a short label, 3 words in total; a counter rolls as an odometer (same start, duration and
  ease for every digit).
- to-overview (takeover): headline 1-3 words + 1-4 items of up to 3
  words, for an "in this video" moment.
Add a new card type only when the overlay plan approved one; register
it with its slot limits.

How a card is built
- Cards: the frosted plate from plan/OVERLAYS.md (or plan/DESIGN.md),
  transparent outside the plate, never covering the face or the inset.
  Takeovers: opaque, on Ground, full frame.
- Slots are named data-slot elements; text goes in only through slots.
  Each slot has a fixed box sized for its limit at its type token; text
  never shrinks to fit.
- Styling comes only from DESIGN.md tokens (colour, type, stroke,
  radius, shadow, edge light) as CSS custom properties at the top of
  the file. No values outside the token set.
- Motion lives in the card's own paused timeline: entrance and exit per
  plan/OVERLAYS.md, builds at times passed in from the overlay plan,
  padded to its slot. No back.out on cards.
- Fonts and GSAP are the project's local copies.

Using a card
- Each overlay in plan/overlay-beats.json becomes
  compositions/beats/NNN-short-name.html: a copy of the card named in
  its card field with the slots filled from the plan, mounted on the
  overlay track with its start, duration and track index.
- Never edit a card inside a single overlay. If a card needs to change,
  change it in film/cards/ and re-instance every overlay that uses it.

Card QA (cards are drafts until this passes)
- On the first use of each card type, build film/cards/test.html with
  every slot at maximum length, and render it at project resolution.
  Check the hero frame (nothing clipped, overflowing or under 28px
  rendered) and its entrance and exit as a frame strip.
- On every use, snapshot the overlay at start + 0.5s and at each build.

Build rules
- Follow the beat sheet exactly: enter times, windows, active element,
  new labels, layer. Spotlight: active 1.0, quiet 0.6, retired 0
  (0.25s). Labels print in with blur 6px -> 0 plus opacity, 0.2s,
  expo.out. Footage enters and exits by clip-path wipe (0.35s in, 0.25s
  out); move the world camera only while footage covers it.
- When a label is cut by a window edge or sits within 60 rendered px of
  it, move the LABEL in world geometry, never the window. Record every
  geometry change.
- Rendered text >= 28px: world font size >= 28 / window scale. Only
  type tokens from plan/DESIGN.md.
- The speaker inset uses the positions in plan/STORY.md, never covers
  what the viewer reads at that beat, and never moves while on screen.
- Before placing a footage beat, grab frames across its whole clip
  (including the exit wipe) to confirm the intended page. If the
  recording changes page inside the clip, shift only the screen's
  data-media-start (never the inset's).
- Never label real footage with names that are only a spoken example.

Check and review (before replying)
1. `npx hyperframes check --json`: 0 errors. List every kept warning
   with the reason.
2. Timeline durations: confirm every registered timeline's duration is
   at least its composition's data-duration. Any shortfall is an error.
3. The no-network search above: 0 hits.
4. Snapshot the SPEC.md QA times, plus each overlay at start + 0.5s and
   at each build (`snapshot --at ... --no-end --describe false`; the
   describe step sends frames to an AI model, so keep it off). Check each: one element
   at full brightness, no label cut or within 60px of an edge, nothing
   the viewer must read under the inset or a card. Fix, then
   re-snapshot only what changed.
5. Render: `npx hyperframes render --fps <fps> --quality looks
   --video-frame-format png --skill hyperframes -o
   renders/build-0-<END>-v<N>.mp4` with one worker, in the background.
   Cut the section with ffmpeg (-ss START -to END, re-encode) to
   renders/<section>-review-v<N>.mp4; ffprobe it and full-decode it.
   Use a new version number on every re-render; never replace one I
   reviewed.
6. Review muted: a 2 fps contact sheet of the whole section, plus frame
   strips at -0.1/+0.1/+0.2/+0.4s around every footage seam, camera
   move and overlay entrance (look for pages flashing, pops, jumps, a
   motion that stops and a second one starts).
7. Luma on the render (Y 16-235): ffmpeg crop + signalstats YMAX on
   active labels, quiet labels, active lines, edges and card text.
   Compute each crop from world coords: canvas = (world - window
   origin) x scale. Targets from plan/DESIGN.md. Report every miss.
8. Update film/REVIEW.md (add this section's entry; keep earlier
   sections' entries and approval lines): creative calls, geometry and timing changes
   from the plan, cards built or changed (and the card QA result), what
   was measured vs only looked at (sound not heard), kept warnings, the
   weakest shot with options, P2 polish, and a line
   "<section>: awaiting approval" that I change to "approved".
9. Append to film/LESSONS.md anything the next section should do
   differently (a rule, not a story).

Report: the review file path and specs, every fix made, the check
result, the timeline-duration result, the card QA result, the luma
table, decisions needed from me, and input md5s unchanged. Then stop.
```
