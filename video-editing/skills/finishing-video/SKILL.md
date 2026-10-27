---
name: finishing-video
description: >-
  This skill should be used when the user wants to finish a video whose
  sections are all built and approved: assemble every section into one
  HyperFrames composition, verify the whole thing, render the final, and
  deliver it with a VERIFY.md. It applies when the user says "finish the
  video", "run finishing-video", "assemble all sections", "render the draft",
  "render the final", "do the full QA pass", or "package the deliverable",
  even if they don't name the skill. It is agent 6 of the editing pipeline and
  usually follows building-sections once every section is approved. The skill
  works in three phases with a stop after each: assemble and check (coverage,
  hyperframes check, mounts, plan anchors, no-network) and hand off to Studio;
  draft render with frame, audio-join, optional fresh transcription diff and
  lip-sync QA; then the final render and a deliver/ folder with edit
  decisions, transcript, composition manifest and VERIFY.md.
version: "0.1.0"
author: productivity-plugins
---

# Finishing Video

This is agent 6 (finishing-video) of the video editing pipeline.

Follow this tested prompt exactly as written; do not reinterpret or simplify it.

```
Finish this video: assemble every approved section into one composition,
verify the whole thing, render the final, and deliver it with a
VERIFY.md. Work in three phases and stop after each for my approval.

Run settings (fill in before each run)
- Fresh transcription of the draft: <yes (one paid ElevenLabs call) | no>
- Final render quality: <the highest quality option `npx hyperframes
  render --help` lists, unless I name one>
- Approvals already given: <list, or "none">. Don't ask again for
  anything listed here.

Inputs (read-only)
- plan/STORY.md, plan/DESIGN.md, plan/beat-sheet.json,
  plan/overlay-beats.json and plan/OVERLAYS.md if they exist.
- film/ (the built sections, film/SPEC.md, film/REVIEW.md,
  film/LESSONS.md, film/cards/, film/assets/).
- Locked cut: raw.clean.mp4 + raw.mistakes-transcript.json if both
  exist, otherwise raw.silenced.mp4 + raw.silence-transcript.json.
- Edit decisions: raw.silence-edl.json, plus raw.mistakes-edl.json and
  raw.approved-cuts.json if they exist.
- Never modify raw.mp4, the locked pair, the EDLs, earlier steps' files
  or anything in plan/. Record md5s before starting and confirm at the
  end of every phase.
- Inside film/, change only what a listed failure or my notes require.
  Make changes through the generators, never by hand-editing generated
  files, and record each change in film/REVIEW.md.

Skills (read before touching compositions)
- HyperFrames (HeyGen): /hyperframes and the domain skills it points to
  (core contract, animation, media, CLI). They win over this prompt
  where they conflict; say what conflicted.
- GSAP (GreenSock): gsap-core and gsap-timeline, others only if used.
- If either skill set is missing, stop and tell me how to install it.
- Never send frames, renders, audio or transcripts to an external
  service, except the one fresh transcription in Run settings. If a
  HyperFrames command offers an AI describe, upload or share option,
  leave it off.
- No logos or brand marks.

Scripts (Python 3, standard library only, run with -I)
- finish_tools.py (this folder): reuse it from
  <PATH TO PREVIOUS FOLDER>/finish_tools.py and copy it in if it isn't
  here. Only write a new one if it's missing, from the spec below. Show
  the full script only if it is new or changed.
- story_tools.py and beats_tools.py: use them if they're in this folder.
- check_sync_final.py: always write it fresh to
  /tmp/finishing/check_sync_final.py from the lip-sync spec below.
  Never reuse a cut step's check_sync.py: those map times through an
  EDL and crop the source, so they measure the wrong thing here.
- Scratch files go to /tmp/finishing/.

Outputs (never overwrite: open files with mode "x"; renders get a new
version number instead of replacing one)
- renders/draft-v<N>.mp4, renders/final-v<N>.mp4
- deliver/ (created in Phase 3; if it exists, stop and tell me)

=== finish_tools.py SPEC ===
Exit codes: 0 ok, 1 errors or flags, 2 bad input.

joins --silence-edl S [--mistakes-edl M]
  Joins of one EDL = positions on its output timeline where one keep
  range meets the next: the running sum of keep lengths after each keep
  except the last (4 decimals).
  Without M: the silence joins. With M: drop each silence join that
  falls strictly inside an M delete range; map the rest with
  t - removed_before(t) over M's deletes (removed_before(t) = sum over
  deletes in order: full length if del.end <= t; t - del.start if
  del.start < t; else stop); add M's own joins. Sort, drop duplicates
  within 1 ms. Print {"joins": [{t, from: silence|mistakes}]}.

mounts MOUNTS --beatsheet B [--overlays O] --duration D --fps F
  MOUNTS = {root_duration, mounts: [{id, start, duration}]} on the final
  timeline. Every section in B and every overlay in O must be mounted
  under its own id, with start and duration each within one frame
  (1/F + 0.0015s) of the plan (section: start, end - start; overlay:
  start, end - start). Errors: a planned id not mounted, a mount listed
  twice, start or duration off by more than one frame, root_duration
  more than one frame from D. Also print mounted ids not in the plan.

audio WAV --joins J [--zero-ms 5] [--jump-db 18]
  WAV = 16-bit PCM (first channel if stereo). Dead spans = runs of
  samples exactly 0 lasting at least --zero-ms; mark a span within 50 ms
  of either file end as "edge". For each join t: 1 ms windows from
  t - 10 ms to t + 10 ms, each window's RMS in dBFS (floor -120); flag
  the join if the largest jump between adjacent windows exceeds
  --jump-db, or a dead span lies within 10 ms of t. Print every dead
  span and every join (time, source, max jump, digital zero nearby).
  Exit 1 if any join is flagged or any non-edge dead span exists.

diff EXPECTED FRESH
  Tokens = word entries (type "word" or no type), lowercased, keeping
  only a-z 0-9 $ % '. Word error rate = word-level edit distance /
  expected token count. Differences = difflib SequenceMatcher (no
  autojunk) non-equal opcodes, each with the expected start time, the
  expected words and the heard words.

self-test (run first; fix the script if anything differs)
  joins: silence keeps [0.28,1.51], [2.31,3.14], [4.00,6.00] -> joins
    1.23, 2.06. With mistakes deletes [1.00,1.50] and keeps [0,1.00],
    [1.50,4.06] -> 1.0 (mistakes), 1.56 (silence); 1.23 is cut away.
  mounts: sections s1 0-10, s2 10-20; overlay o1 3.0-8.0; fps 60,
    duration 20. Mounts s1 0/10, s2 10.01/9.99, o1 3.0/5.0, world 0/20,
    root_duration 20.0 -> 0 errors, extra [world]. Broken copy: s2
    start 10.05, o1 removed, root_duration 19.9 -> exactly 3 errors
    (s2 off 50 ms, o1 not mounted, root duration).
  audio: a 3.0s, 16 kHz mono 16-bit WAV: sample i =
    round(A * sin(2*pi*2000*i/16000 + pi/8)), A = 33 for i < 32000 and
    3277 after; samples 16000-16159 set to 0. Joins 0.5, 1.0, 2.0.
    Expected: one dead span 1.000-1.010 (10.0 ms); join 0.5 not flagged
    (max jump 0.0 dB); join 1.0 flagged, digital zero nearby, max jump
    57.0 dB; join 2.0 flagged, no digital zero, max jump 40.0 dB.
  diff: expected "The agent collects metrics." (starts 0.5, 0.8, 1.2,
    1.7) vs heard "The agents collects metric data." -> WER 0.75;
    exactly 2 differences: agent -> agents at 0.8, metrics -> metric
    data at 1.7.
  Show expected vs actual.

=== LIP-SYNC SPEC (check_sync_final.py) ===
The inset plays film/assets/cam.mp4 at the same absolute time as the
locked cut, so render time t maps to source time t.
- Exact extraction: ffmpeg -copyts -ss max(A-2, 0) -i FILE, then trim
  with absolute timestamps (4 decimals).
  - Audio(FILE, A, D): -vn -af "atrim=start=A:end=A+D,aresample=8000"
    -ac 1 -f s16le -  -> int16 samples at 8 kHz.
  - Frames(FILE, A, D, CROP): -an -vf "trim=start=A:end=A+D,CROP,
    scale=48:56,format=gray,showinfo" -fps_mode passthrough -f rawvideo -
    Take each frame's pts_time from showinfo on stderr; never infer it
    from frame counts.
- Audio offset at t: r = Audio(final, t-0.4, 0.8), w = Audio(locked
  video, t-0.55, 1.1). Subtract r's mean; for each lag L, with
  win = w[L:L+len(r)]: corr(L) = sum(r*win - mean(win)*r) /
  (|r| * |win - mean(win)|). Best L = largest corr.
  audio_off = (t-0.55 + L/8000) - (t-0.4).
- Video offset at t: rf = Frames(final, t-0.2, 0.4, crop = the inset's
  canvas rect from plan/STORY.md, inside its rounded corners);
  sf = Frames(film/assets/cam.mp4, t-0.35, 0.7, no crop). Best j =
  smallest mean |rf[k] - sf[j+k]|. video_off = sp[j] - rp[0].
- sync_ms = (video_off - audio_off) * 1000 (positive = picture leads).
  Expect corr >= 0.95.
- Self-check: at one time inside a visible inset, audio_off must be
  0 within 1 ms and video_off within one frame.
- Verdict: pass if |sync_ms| < one frame at every point, with no drift
  across the video. Usual detectability: about +45 ms (sound early),
  about -125 ms (sound late). The check is relative to the locked cut,
  so sync already off in the recording won't show.

=== PHASE 1: ASSEMBLE AND CHECK (no render) ===
Run all self-tests, then:
1. Coverage: list every section in plan/beat-sheet.json and whether it's
   built and approved (the "<section>: approved" line in
   film/REVIEW.md; PIPELINE.md's Sections table mirrors it). If any
   isn't, stop and tell me.
2. Assemble index.html: the world host, every section host, every
   overlay on the overlay track, <audio id="voice" data-volume="1"> from
   0, and the root data-duration = the locked video's duration.
3. Project checks:
   - `npx hyperframes check --json`: 0 errors; list kept warnings with
     reasons.
   - Every registered timeline's duration >= its composition's
     data-duration.
   - `npx hyperframes timeline --json` -> write /tmp/finishing/mounts.json ->
     finish_tools.py mounts ... (0 errors; explain every extra id).
   - story_tools.py check and beats_tools.py check against the locked
     transcript (if present): the plan's anchors still match it.
   - SVG def ids: no id defined in more than one composition.
   - No http:// or https:// URL outside comments in any file the root
     loads; fonts and GSAP are local files.
4. List every seam to look at: section boundaries, camera moves,
   footage wipes, overlay entrances and exits, with times.
5. Tell me to open the Studio (`npx hyperframes preview` from film/)
   and scrub those seams before any draft render.

Report: self-tests, coverage, every check result, the seam list, input
md5s unchanged. Stop and wait for "Studio OK" or my notes.

=== PHASE 2: DRAFT RENDER AND FULL QA (after Studio OK) ===
Fix my Studio notes first (through the generators), re-run the Phase 1
checks on what changed, then:
1. Render the draft with one worker (same command as the section
   builds) to renders/draft-v<N>.mp4. ffprobe it: duration within one
   frame of the locked video, video and audio stream durations within
   0.1s of each other. Full decode (ffmpeg -v error -i ... -f null -)
   with exit code 0.
2. Frames:
   - A 1 fps contact sheet of the whole video.
   - For every seam in the Phase 1 list, a strip of contiguous frames
     (about 24, tiled) across it. Look for pops, flashes, a motion that
     stops and a second one starts, and pages changing under footage.
   - blackdetect=d=0.2:pix_th=0.10 and freezedetect=n=-60dB:d=2 on a
     320px proxy. Check each freeze against the plan: a planned hold is
     fine, anything else is a failure.
   - Face framing: one frame at the start of every inset appearance;
     the whole head is in frame and nothing covers it.
   - Legibility: a 960x540 downscale of every major beat, read by eye,
     plus luma (signalstats YMAX, Y 16-235) on one active label, one
     quiet label and one card per section against plan/DESIGN.md.
3. Audio:
   - Decode the draft audio to /tmp/finishing/draft.wav (16 kHz mono
     16-bit) and the locked video's audio to /tmp/finishing/locked.wav.
   - finish_tools.py joins (with the mistakes EDL if it exists) ->
     /tmp/finishing/joins.json; finish_tools.py audio on draft.wav. For
     every flagged join and dead span, cut a listen clip (1s either
     side) to /tmp/finishing/listen-<t>.wav.
   - The voice is copied, not mixed: volumedetect on both WAVs (mean and
     max within 0.5 dB) and an audio offset of 0 within 1 ms at 3 points
     using the lip-sync audio method. If an approved music bed exists,
     check the voice level instead and say so.
   - If Run settings say yes: transcribe draft.wav with the same API
     call and fields as the transcription step (upload
     /tmp/finishing/draft.wav; tell me its size and that it's a paid
     call first), writing the response to /tmp/finishing/fresh.raw.json
     and converting it to /tmp/finishing/fresh.json with the same
     schema. Don't run the transcription skill itself: it stops because
     transcript.json exists and it writes into this folder. Then
     finish_tools.py diff <locked transcript> /tmp/finishing/fresh.json. Treat differences at or near a join as high
     priority.
4. Lip sync: run check_sync_final.py's self-check, then measure one point in
   every inset appearance of at least 0.9s, plus 2 points just after
   each join that falls inside a visible inset.
5. A listening list for me: every join on the final timeline with the
   words on each side and its listen clip. I listen; you can't.

Report: the draft path and specs, every check with its result (measured
/ looked at / not done), every failure with a proposed fix, the
listening list, and input md5s unchanged. Stop and wait for my approval
or notes.

=== PHASE 3: FINAL RENDER AND DELIVERY (after approval) ===
1. Fix the approved failures through the generators and re-run the
   checks they touch.
2. Render the final with one worker at the Run settings quality to
   renders/final-v<N>.mp4. Re-verify: ffprobe (duration, stream
   durations), full decode, a 1 fps contact sheet compared with the
   draft's, the audio check on its WAV, and lip sync at 3 points.
3. Create deliver/ with:
   - the final MP4;
   - edit-decisions/: raw.silence-edl.json, raw.approved-cuts.json and
     raw.mistakes-edl.json if they exist, plan/beat-sheet.json, and
     plan/overlay-beats.json if it exists;
   - transcript.json: a copy of the locked transcript, which is on the
     final timeline;
   - composition.txt: the film/ path and every file the root loads, with
     its md5;
   - VERIFY.md: every check run in Phases 1-3 and its result, marked
     measured, looked at, or not done; what you couldn't check (sound
     quality is only heard by me; lip sync is relative to the recording;
     the fresh transcription if skipped); remaining known issues; and
     the note that automated checks propose, but editorial judgement
     decided.
4. Confirm input md5s unchanged.

Report: the deliver/ contents, VERIFY.md, and anything left for me to
decide. Stop.
```
