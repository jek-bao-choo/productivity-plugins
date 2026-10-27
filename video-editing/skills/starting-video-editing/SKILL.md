---
name: starting-video-editing
description: >-
  This skill should be used when the user wants to start, resume, or check the
  status of editing a video project (a folder with raw.mp4) through the whole
  video-editing pipeline. It applies when the user says "edit this video",
  "start video editing", "where am I", "what's next", "continue", "next step",
  "resume the edit", "redo the silence cut", "re-plan the story", or "just cut
  the silences" in a video project folder, even if they don't name the skill.
  It is the orchestrator: it detects the project's state from files and
  PIPELINE.md, runs the next step with its own skill
  (converting-speech-to-text-elevenlabs, cutting-silences, cutting-mistakes,
  planning-storytelling, planning-overlays, building-sections, finishing-video),
  honours every stop inside those skills, keeps the PIPELINE.md ledger of
  settings, decisions, approvals and output md5s up to date, flags stale steps,
  and never edits media itself.
version: "0.1.0"
author: productivity-plugins
---

# Starting Video Editing

This is the orchestrator of the video editing pipeline. It runs the other video-editing skills in order and does no editing itself.

Follow this tested prompt exactly as written; do not reinterpret or simplify it.

```
Orchestrate the edit of the video in this folder. Work out where the
project is, run the next step with its skill, and keep PIPELINE.md up to
date. You don't edit anything yourself: every step is done by its skill,
following that skill exactly, including all of its stops.

Project
- One folder per video. The source recording is raw.mp4 in this folder.
- If raw.mp4 is missing: ask me for the source path, then copy it here
  as raw.mp4 (never move or modify the original), and record both paths
  and the md5 in PIPELINE.md.
- You never delete, move or overwrite any file yourself except
  PIPELINE.md. A skill may do what its own SKILL.md says (for example,
  cutting-silences deletes its Phase 1 files before rendering). One
  exception: when I approve a section in chat, change that section's
  "<section>: awaiting approval" line in film/REVIEW.md to
  "<section>: approved" (that line only), then mirror it in the ledger.

PIPELINE.md (the ledger; create it on the first run with mode "x")
- Project: source path, raw.mp4 md5, created date.
- Settings: tools_from (the folder whose scripts later skills reuse, for
  their <PATH TO PREVIOUS FOLDER>), overlays (run | skip),
  fresh_transcription (yes | no), auto_advance (yes | no; default yes),
  final_render_quality (default: the highest quality
  `npx hyperframes render --help` lists), privacy (default: run every
  HyperFrames snapshot and render with `env -u GEMINI_API_KEY` and
  `--describe false`; the CLI also reads GEMINI_API_KEY from .env, so
  `--describe false` is what guarantees no frames go out; never send
  media, frames or transcripts anywhere except the transcription
  call), hyperframes_cli (an exact pinned
  version, e.g. `npx --yes hyperframes@X.Y.Z`).
  Ask for every unset setting once, in one batch, on the first run
  (using the decision format below), not when a later step first needs
  it. Pass them to every skill as Run settings.
- Steps table: step, skill, status (todo | in progress | awaiting
  approval | done | skipped | stale), key outputs, md5 of each key output
  at approval, approved date.
- Sections table (after storytelling): id, title, times, status (todo |
  in progress | awaiting approval | approved), build order.
- Decisions: anything I decide that a later step needs (chosen concept,
  canvas, thresholds, card or colour choices, "decisions already made"
  for building-sections), each with its date.
- Approvals log: every approval I give, with the step and date.
Update the ledger after every step result and every approval. When a
skill asks for something already recorded under Decisions or Approvals,
answer from the ledger and tell me you did; don't ask me again.

Skills (load each by name; its SKILL.md is the authority)
  0. converting-speech-to-text-elevenlabs
  1. cutting-silences
  2. cutting-mistakes
  3. planning-storytelling
  4. planning-overlays (skippable)
  5. building-sections (once per section)
  6. finishing-video
(The numbers match the "agent N" label inside each skill.)
If a skill isn't installed, stop and tell me which one.

=== STATE DETECTION (run at the start of every turn) ===
Check files, then reconcile with the ledger; files win when they
disagree, and say so.
0. Transcribe: done when transcript.json and transcript.raw.json exist.
1. Cut silences: done when raw.silenced.mp4, raw.silence-transcript.json
   and raw.silence-edl.json exist and the video's duration is within
   0.1s of the transcript's audio_duration_secs. Awaiting approval when
   the EDL exists without raw.silenced.mp4.
2. Cut mistakes: done when raw.approved-cuts.json exists and either its
   cuts list is empty (zero cuts: the silence pair carries forward) or
   raw.clean.mp4 + raw.mistakes-transcript.json exist with matching
   durations. Awaiting approval when raw.cut-candidates.json exists
   without raw.approved-cuts.json. Stopped mid-apply when
   raw.approved-cuts.json has cuts but raw.clean.mp4 +
   raw.mistakes-transcript.json are missing or don't match: list the
   partial outputs, and with my approval archive them (and
   raw.approved-cuts.json) so Phase 2 can re-run.
3. Storytelling: done when plan/STORY.md, plan/DESIGN.md and
   plan/beat-sheet.json exist and the ledger records the plan approved.
4. Overlays: done when plan/overlay-beats.json and plan/OVERLAYS.md
   exist and are approved, or the ledger says overlays: skip.
5. Build: a section is approved when film/REVIEW.md contains the line
   "<section>: approved". Done when every section in
   plan/beat-sheet.json is approved. Mirror this into the Sections
   table.
6. Finish: done when deliver/VERIFY.md exists.
The locked cut is raw.clean.mp4 + raw.mistakes-transcript.json if both
exist, otherwise raw.silenced.mp4 + raw.silence-transcript.json.

Staleness: for each done step, compare the md5s of its upstream outputs
now with those recorded at approval. If any changed, mark every later
step stale, list exactly which files and approvals are affected, and
don't run a stale step's successors until I decide.

=== WHAT TO DO EACH TURN ===
Status ("where am I", or at the start of a session)
- Show the Steps table, the Sections table if any, the locked cut, and
  the next step with the skill that runs it. Then stop.

Next step ("continue", "next", "edit this video")
- Run the first step that isn't done, with its skill, from its current
  phase (a step awaiting approval resumes at its approval stop; it
  doesn't start over).
- Pass the skill what it needs from the ledger: tools_from as
  <PATH TO PREVIOUS FOLDER>, recorded decisions, and Run settings
  (building-sections: the next section in build order, whether it's the
  first run, decisions already made; finishing-video: fresh
  transcription, approvals already given).
- When the skill stops for approval, stop too, unless auto_advance
  auto-approves that stop (below). Record my reply in the ledger before
  acting on it.
- After a step is done: with auto_advance no, tell me the next step and
  stop. With auto_advance yes, start the next step.
- auto_advance yes means: stop ONLY for (a) an .mp4 (or audio clip) I
  must review, (b) a HyperFrames Studio review, (c) a decision only I
  can make that no recorded decision or sensible default covers, or
  (d) a paid external call not already approved in Settings (such as
  the first ElevenLabs transcription). Every
  other approval stop inside a skill counts as approved: write "auto-
  approved (auto_advance): <what>" in the Approvals log and continue.
  Phase stops that exist only to show me a plan or a table become
  report-and-continue, unless they contain a stop of type (c) or (d).

Single operation ("just cut the silences", "only plan overlays")
- Route straight to that skill. First check that its inputs exist and
  aren't stale; if not, say which earlier step it needs and stop.

Redo a step ("redo the silence cut", "re-plan the story")
- Don't delete anything. List the outputs the redo would replace and
  every later step and approval it makes stale. With my approval, move
  those outputs into archive/<step>-<date>/ (the only move allowed),
  mark the steps stale or todo, then run the step. Re-planning the story
  archives the whole plan/ folder (planning-storytelling stops if plan/
  exists), which also takes the overlay plan, so mark planning-overlays
  todo too.

=== REVIEWS AND DECISIONS (every skill, every stop) ===
Pass this section to every skill as part of its Run settings.

Review handoff (required whenever you stop for a review)
- Put every file I'm asked to review (renders, review cuts, preview and
  listen clips, A/B tests, captions drafts) in <project>/reviews/<step>/
  (e.g. reviews/cut-silences/, reviews/build/s3/, reviews/finish/),
  never in /tmp. Scratch files stay in /tmp.
- End the message with a "Review" block:
  - File: the absolute path (clickable), duration, resolution/fps.
  - Watch with: sound on or off, and why.
  - Timecodes: a table of clip time | film time | what happens | what to
    check.
  - Optional: any extra file, each with its absolute path and a one-line
    reason to look at it.
  - Reply with: the exact words that approve ("approve <step>") or ask
    for changes.
- Always give absolute paths for every output you mention (renders,
  deliver/, reports), not paths relative to a subfolder.
- A Studio review gets the same block with the running preview URL
  (start it yourself with `preview --background`; stop it when done).

Decisions
- Ask with AskUserQuestion. Put the recommended option first, labelled
  "(Recommended)", and give 1-2 sentences on why and what it costs.
  Every open option in a report ("options: a/b/c") is a decision in this
  format, never a bare list.
- Batch all decisions pending at a stop into one AskUserQuestion call.
- Never ask for anything already recorded under Decisions or Approvals;
  answer from the ledger and say you did.
- If I reply only "approve" while options are open, take the recommended
  option for each, record each one, and say so.

=== HAND-OFFS BETWEEN STEPS ===
- After transcription: confirm the transcript looks right with me
  before cutting (the skill's own stop).
- After cut mistakes with zero cuts: record "zero cuts" and carry the
  silence pair forward; don't render anything.
- After storytelling: record the chosen concept, canvas, design system
  and the recommended first section, and fill the Sections table in
  that build order.
- If storytelling's air check flagged tight sentence gaps: no skill
  fixes them yet. Ask me to accept them or fix them by hand before any
  building, and record the answer.
- Overlays: ask once whether to run or skip planning-overlays, and
  record it.
- Between sections: carry each section's open decisions and new
  film/LESSONS.md rules into the next run's "decisions already made".
- Before finishing: every section approved (the "<section>: approved"
  line in film/REVIEW.md, mirrored in the ledger).

Rules
- One skill at a time. Never skip, merge or shortcut a skill's phases or
  stops (except stops auto_advance auto-approves, which are logged), and
  never do a skill's work yourself.
- Read-only on everything except PIPELINE.md, the one-time raw.mp4 copy,
  archive moves I approve, and the section approval line in
  film/REVIEW.md when I approve a section.
- Never send media, frames or transcripts anywhere; only the skills'
  own approved service calls (transcription) leave the machine.
- When you're unsure what state something is in, say so and ask; don't
  guess from file names alone.
```
