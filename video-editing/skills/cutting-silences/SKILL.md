---
name: cutting-silences
description: >-
  This skill should be used when the user wants to cut silences, pauses, or dead
  air out of a recording (typically raw.mp4) using a word-timestamped
  transcript.json, render the tightened video, and verify lip sync and render
  quality. It applies when the user says "cut the silences", "run
  cut-silences", "remove the pauses from raw.mp4", "tighten my recording",
  "make raw.silenced.mp4", or "check lip sync after the cut", even if they don't
  name the skill. It is agent 1 of the editing pipeline and usually follows
  converting-speech-to-text-elevenlabs. The skill runs read-only pre-flight checks, builds or reuses cut_silences.py,
  produces an EDL, re-timed transcript, and decisions report, stops for
  approval, then renders with ffmpeg, verifies with ffprobe, measures lip sync
  with check_sync.py, and runs render QA before stopping ahead of cut-mistakes.
version: "0.1.0"
author: productivity-plugins
---

# Cutting Silences

This is agent 1 (cut-silences) of the video editing pipeline.

Follow this tested prompt exactly as written; do not reinterpret or simplify it.

```
Cut the silences from raw.mp4 using transcript.json, render the result,
then check lip sync and render quality. Work in two phases and stop
between them for my approval.

Scripts
- cut_silences.py (in this folder): reuse it from
  <PATH TO PREVIOUS FOLDER>/cut_silences.py and copy it in if it isn't
  already here. Only write a new one if it's missing, implementing the
  cut-silences algorithm below in Python with only the standard library.
  Required CLI: transcript (default transcript.json), --gap, --head-pad,
  --tail-pad, --audio-events cut|protect, --video, --apply (needs
  --video), --prefix raw, --dry-run (computes and prints, writes
  nothing), --self-test.
- check_sync.py: write it to /tmp/lipsync/check_sync.py (not this
  folder) from the lip-sync algorithm below. Frame grabs go to
  /tmp/lipsync/ too.
- numpy isn't installed: use plain Python (standard library only) plus
  ffmpeg and /opt/homebrew/bin/ffprobe. Run Python with -I.

Safety
- Never overwrite raw.mp4 or transcript.json.
- cut_silences.py must refuse existing outputs (open files with mode
  "x", run ffmpeg with -n).
- The QA step is read-only for this folder: it must not modify or create
  files here, except review clips in reviews/cut-silences/.

Pre-flight (read-only, report results)
- raw.mp4 and transcript.json exist in this folder.
- ffmpeg and /opt/homebrew/bin/ffprobe exist. Report the ffmpeg version.
- Report codec, resolution, fps, start_time, duration and nb_frames for
  every stream in raw.mp4. Note the fps; one frame = 1/fps.
- If any cut-silences output file listed below already exists, stop and
  tell me.
- Face crop for lip sync: grab one frame of raw.mp4 at about 2/3 of its
  length, scaled to 1600px wide, and look at it. Find the face (webcam
  overlay) and choose a crop box covering the face and mouth, in
  full-resolution pixels (W:H:X:Y). Report it. If there's no face, say so;
  the lip-sync part will be skipped. (Previous OBS layout at 5120x1440:
  crop=960:1120:3360:320.)

=== CUT-SILENCES ALGORITHM ===

Inputs
- transcript.json: { language_code, audio_duration_secs, text,
  words: [ {text, start, end, type} ] }, times in seconds.
- Use only entries with type "word" (or no type) that have numeric start
  and end, in transcript order. Treat type "audio_event" entries as
  events.
- Duration = audio_duration_secs if numeric, else ffprobe duration of
  raw.mp4, else last word end + tail_pad.

Parameters (defaults)
- --gap 0.55        minimum pause treated as trimmable silence
- --head-pad 0.22   silence kept before the first word
- --tail-pad 0.34   silence kept after the last word
- --audio-events cut   "cut" treats audio events as silence; "protect"
                       never deletes time overlapping an audio_event

Algorithm
1. Head trim: head_end = first_word.start - head_pad. If head_end > 0,
   delete [0, head_end], reason "head trim before first word".
2. Tail trim: tail_start = last_word.end + tail_pad. If duration >
   tail_start, delete [tail_start, duration], reason "tail trim after
   final word".
3. Pauses: for each consecutive pair (prev, next):
   gap = next.start - prev.end. If gap < --gap, skip.
   keep = 0.24 if gap >= 2.0
          else 0.20 if prev.text ends with . ! or ?
          else 0.14
   del_start = prev.end + keep * 0.55
   del_end   = next.start - keep * 0.45
   If del_end > del_start, delete [del_start, del_end], reason
   "pause {gap:.2f}s -> {keep:.2f}s".
4. If --audio-events protect: subtract every audio_event's [start, end]
   from the delete ranges (splitting ranges where needed).
5. Merge: drop ranges where end <= start, sort by start, and merge any
   range whose start <= the previous range's end. Collect all reasons.
6. Keep ranges = complement of the merged deletes over [0, duration].
   Any keep range shorter than 0.04s becomes a delete: fold it in and
   re-merge, repeating until none remain.
7. removed = sum of delete lengths; edited_duration = duration - removed,
   rounded to 3 decimals.
8. Re-time words. removed_before(t) = sum over deletes in order:
   if del.end <= t, add the full length; elif del.start < t, add
   t - del.start; else stop. Drop any word overlapping a delete range
   (report it). For each kept word, output text, source_start,
   source_end, start = start - removed_before(start),
   end = end - removed_before(end), rounded to 3 decimals.

Self-test (run first; fix the script if anything differs)
  words: "Hello" 0.50-0.90, "world." 1.00-1.40, "Again" 2.40-2.80;
  duration 3.50, default parameters
Expected:
  deletes [0, 0.28], [1.51, 2.31], [3.14, 3.50]; removed 1.44;
  edited_duration 2.06; keeps [0.28, 1.51], [2.31, 3.14];
  re-timed: Hello 0.22-0.62, world. 0.72-1.12, Again 1.32-1.72
Show expected vs actual.

Outputs (in this folder)
- raw.silence-edl.json: { agent: "cut-silences", params, source_duration,
  edited_duration, removed, delete_ranges: [{start, end, reasons}],
  keep_ranges: [{start, end}] }
- raw.silence-transcript.json: { language_code, source_audio_duration_secs,
  audio_duration_secs (edited), produced_by: "cut-silences",
  words: [{text, source_start, source_end, start, end}] }
- raw.silence-decisions.md: source and edited duration as mm:ss.ss and
  seconds, total removed across N ranges, params, and the top 15 pause
  deletes by length (mm:ss.ss-mm:ss.ss removed X.XXs).
- raw.silence-filter.txt (only with --video): for each keep range i,
    [0:v]trim=start=S:end=E,setpts=PTS-STARTPTS[vi];
    [0:a]atrim=start=S:end=E,asetpts=PTS-STARTPTS[ai];
  then a final line: [v0][a0][v1][a1]...concat=n=N:v=1:a=1[v][a]
  (S and E to 3 decimals).
- raw.silenced.mp4 (only with --apply):
    ffmpeg -n -i raw.mp4 -/filter_complex raw.silence-filter.txt
      -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 18
      -c:a aac -b:a 192k -movflags +faststart raw.silenced.mp4
  If ffmpeg is older than 7.0, use -filter_complex_script instead.

=== LIP-SYNC ALGORITHM (check_sync.py) ===

Inputs: SRC=raw.mp4, OUT=raw.silenced.mp4, EDL=raw.silence-edl.json,
CROP from pre-flight, and render test times as CLI arguments.

1. Edited timeline: walk keep_ranges in order with o = 0. For each keep
   (S, E): the segment covers render [o, o + (E - S)) and maps to source
   S. Then o += E - S.
   source_time(t) = S_i + (t - o_i) for the segment i containing t.

2. Exact extraction (avoids seek error): always use
     ffmpeg -copyts -ss max(A-2, 0) -i FILE
   then trim with absolute timestamps:
   - Audio(FILE, A, D): -vn -af "atrim=start=A:end=A+D,aresample=8000"
     -ac 1 -f s16le -   -> list of int16 samples at 8 kHz.
   - Frames(FILE, A, D): -an -vf "trim=start=A:end=A+D,crop=CROP,
     scale=48:56,format=gray,showinfo" -fps_mode passthrough
     -f rawvideo -   -> frames of 48*56 bytes. Parse each frame's
     pts_time from showinfo on stderr; never infer it from frame counts.
   Use 4 decimals for A and D.

3. Audio offset at render time t (s = source_time(t)):
   r = Audio(OUT, t - 0.4, 0.8)      (6400 samples)
   w = Audio(SRC, s - 0.55, 1.1)     (8800 samples, +-150 ms search)
   Subtract r's mean from r. For each lag L in 0..len(w)-len(r), take the
   window w[L:L+len(r)] and compute the normalized correlation
     corr(L) = sum(r*win - mean(win)*r) / (|r| * |win - mean(win)|)
   Pick the L with the largest corr.
   audio_off = (s - 0.55 + L/8000) - (t - 0.4)
   Also report corr at the best L (expect >= 0.95).

4. Video offset at render time t:
   rp, rf = Frames(OUT, t - 0.2, 0.4)    (about 0.4 s of render frames)
   sp, sf = Frames(SRC, s - 0.35, 0.7)   (+-150 ms search)
   For each j in 0..len(sf)-len(rf), compute
     MAD(j) = mean over all frames and pixels of |rf[k] - sf[j+k]|
   Pick the j with the smallest MAD.
   video_off = sp[j] - rp[0]
   Also report the MAD at the best j (expect a small value, about < 1 on
   a 0-255 scale, because render frames are re-encoded source frames).

5. sync_ms = (video_off - audio_off) * 1000
   0 = same A/V alignment as the source; positive = picture leads sound.

6. Print one row per test time: render_t, segment, audio_off (ms), corr,
   video_off (ms), MAD, sync_ms.

Self-check (run first; fix the script if it fails)
- At a test time inside segment 0, audio_off must equal
  keep_ranges[0].start within 1 ms, and video_off must be within one
  frame of it. Show expected vs actual.

Test points
- About 11 render times: one in each of about 6 segments spread across
  the video, 2 in the second-to-last segment, and 3 in the last segment
  (the last one before the final word ends).
- Each render window [t - 0.4, t + 0.4] must sit inside a single keep
  segment. Print the segment table (render range -> source range) and
  pick times from it.

=== PHASE 1: NO RENDER ===
Run the cut-silences self-test, then run cut_silences.py on
transcript.json without --video. Also --dry-run it at --gap 0.55, 0.8,
1.0 and 1.5. Report:
- Pre-flight results, including the face crop.
- Self-test result. Show the full script only if it is new or changed.
- Source and edited duration, removed seconds and %, delete and keep
  range counts.
- Word check: type "word" count in transcript.json vs words in
  raw.silence-transcript.json. They must match; list any dropped word.
- Audio events overlapping a delete range, with timestamps.
- Consistency: deletes + keeps sum to the source duration; re-timed
  words are in order and end within edited_duration.
- The contents of raw.silence-decisions.md.
- A table of removed % and edited length by --gap, and whether the
  default is far outside 15-20%.
- Every pause over 2s with the words on each side. In a screen recording
  these may be on-screen demo moments, and they get cut at any --gap.

Stop and wait for my approval or new parameters.

=== PHASE 2: RENDER, VERIFY AND QA (only after I approve) ===
Render
- Delete only the three Phase 1 files (raw.silence-edl.json,
  raw.silence-transcript.json, raw.silence-decisions.md), because the
  script refuses to overwrite.
- Re-run with --video raw.mp4 --apply, plus any parameter changes.

Verify with /opt/homebrew/bin/ffprobe
- raw.silenced.mp4 duration is within 0.1s of edited_duration.
- Video and audio stream durations match each other within 0.1s.
- Report codec, resolution, fps, start_time, duration and nb_frames for
  every stream in the render, the file size, and that raw.mp4 and
  transcript.json are unchanged.

Lip sync (skip if pre-flight found no face)
- Write check_sync.py, run its self-check, then measure at the test
  points.
- Report the segment table and the results table.
- Verdict: pass if |sync_ms| < one frame (16.7 ms at 60 fps) at every
  point, and points in the same segment show the same value (no drift
  within a segment) with no growing trend across segments.
- Compare the end (last segment) with the start.
- Mention the usual detectability thresholds (about +45 ms with sound
  early, about -125 ms with sound late).
- State the limit: this is relative to raw.mp4, so sync already off in
  the original recording won't show up.

Render checks
- Full decode: ffmpeg -v error -i raw.silenced.mp4 -f null - ; report
  any errors and the exit code.
- silencedetect=n=-35dB:d=0.5 on the render audio: list any silences.
- On a 320px proxy: blackdetect=d=0.2:pix_th=0.10 and
  freezedetect=n=-60dB:d=2. List any hits.
- volumedetect on both files: compare mean and max volume. The peak
  should match; the mean rises because silence was removed.
- Tail: -sseof -0.7, fps=4, scale=800, tile=1x3 into one image. Look at
  it and confirm the video ends after the final word, not mid-word.
- List the cuts around source pauses over 2s (source time and render
  time) for me to check by eye.

Review files: cut a 2s clip (1s either side) around each cut at a
source pause over 2s into <project>/reviews/cut-silences/ (the only
files this step writes outside its outputs), and list them, with
absolute paths, in the orchestrator's Review block.

Stop after the report. Do not start cut-mistakes until I confirm the
cut looks right.
```
