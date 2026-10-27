---
name: cutting-mistakes
description: >-
  This skill should be used when the user wants to cut spoken mistakes
  (stutters, repeats, false starts, retakes, fillers) out of a recording
  (typically raw.silenced.mp4) using a word-timestamped transcript
  (raw.silence-transcript.json), then render and QA the result. It applies when
  the user says "cut the mistakes", "run cut-mistakes", "remove my stutters and
  retakes", "find the flubs", "clean up the false starts", or "make
  raw.clean.mp4", even if they don't name the skill. It is agent 2 of the
  editing pipeline and usually follows cutting-silences. The skill runs read-only pre-flight checks, builds or
  reuses cut_mistakes.py to propose candidates, runs a hidden-flub check,
  reviews every candidate in context with preview clips, stops for approval,
  then applies only the approved cuts, renders with ffmpeg, verifies with
  ffprobe, checks cut points and lip sync, and stops after the report.
version: "0.1.0"
author: productivity-plugins
---

# Cutting Mistakes

This is agent 2 (cut-mistakes) of the video editing pipeline.

Follow this tested prompt exactly as written; do not reinterpret or simplify it.

```
Cut spoken mistakes (stutters, repeats, false starts, retakes) from
raw.silenced.mp4 using raw.silence-transcript.json. Work in two phases
and stop between them for my approval. Deciding what is a mistake is
judgment, not a formula: the script only proposes candidates, and
nothing is cut until I approve it.

Scripts
- cut_mistakes.py (in this folder): reuse it from
  <PATH TO PREVIOUS FOLDER>/cut_mistakes.py and copy it in if it isn't
  already here. Only write a new one if it's missing, implementing the
  find and apply algorithms below in Python with only the standard
  library. Show the full script only if it is new or changed.
  - find CLI: transcript (default raw.silence-transcript.json),
    --prefix raw, --segment-gaps edited|source (default edited),
    --fillers, --dry-run (computes and prints, writes nothing),
    --self-test.
  - apply CLI: transcript (default raw.silence-transcript.json),
    --cuts raw.approved-cuts.json, --prefix raw, --video, --apply (needs
    --video), --output raw.clean.mp4, --dry-run, --self-test.
- check_sync_mistakes.py (only needed if cuts are rendered): write it to
  /tmp/lipsync/check_sync_mistakes.py from the lip-sync algorithm below.
- numpy isn't installed: use plain Python plus ffmpeg and
  /opt/homebrew/bin/ffprobe. Run Python with -I.

Safety
- Never modify raw.mp4, raw.silenced.mp4, or any raw.silence-* file.
  Record their md5 checksums before starting and confirm them at the end.
- cut_mistakes.py must refuse existing outputs (open files with mode
  "x", run ffmpeg with -n), refuse an --output equal to the --video
  path, and refuse any output path that resolves to an input.
- Preview clips and frame grabs go to /tmp/cut-mistakes/, not this
  folder.

Pre-flight (read-only, report results)
- raw.silence-transcript.json, raw.silence-edl.json, raw.silenced.mp4
  and transcript.raw.json exist in this folder.
- ffmpeg and /opt/homebrew/bin/ffprobe exist. Report the ffmpeg version.
- Report codec, resolution, fps and duration for every stream in
  raw.silenced.mp4.
- raw.silenced.mp4 duration is within 0.1s of audio_duration_secs in
  raw.silence-transcript.json. If not, stop: the two steps are out of
  step.
- If any output file listed below already exists, stop and tell me.

=== FIND ALGORITHM (cut_mistakes.py find) ===

Inputs
- Transcript words: entries with type "word" (or no type) that have
  numeric start and end, in order, indexed 0..n-1. All times are on the
  silenced (edited) timeline. Keep each word's source_start/source_end
  (raw.mp4 timeline) if present.
- token(text) = lowercase text with leading and trailing characters
  outside [a-z0-9$%] stripped.
- display(words) = texts joined by single spaces, then remove any
  whitespace before , . ! ? ; :
- ctx(i) = display(words[max(0, i-6) : min(n, i+6)])
- fmt(s) = mm:ss.ss (minutes zero-padded to 2, seconds to 2 decimals,
  padded to 5 chars).
- Each candidate stores its range as cut: {start, end}.

1. Stutters. For i in 1..n-1, with a = words[i-1], b = words[i]:
   skip if token(b) is empty. If token(a) == token(b) and
   b.start - a.end < 0.5, add a candidate:
     type "stutter", confidence "high", recommend "cut",
     cut [a.start, b.start] (3 decimals), removes a.text, keeps b.text,
     context ctx(i), note: repeated "<token>".

2. Fillers (only with --fillers). For each word whose token is in
   {um, uh, erm, er, ah, hmm, mm, mhm}, add:
     type "filler", confidence "low", recommend "review",
     cut [w.start, next_word.start] (or [w.start, w.end] for the last
     word), removes w.text, context ctx(i).

3. Segments. seg_start = 0. For i in 1..n-1, with prev = words[i-1],
   cur = words[i]:
     gap = cur.start - prev.end
       (with --segment-gaps source: cur.source_start - prev.source_end,
        falling back to edited times if those fields are missing)
     elapsed = cur.end - words[seg_start].start   (always edited times)
     sentence_end = prev.text ends with . ! or ?
   If gap > 0.85 or (sentence_end and elapsed >= 7.5) or elapsed >= 16:
     close a segment: words seg_start..i-1, start =
     words[seg_start].start, end = prev.end, text =
     display(words[seg_start:i]); then seg_start = i.
   After the loop, close the final segment the same way through the
   last word. Segments are indexed from 0 internally; ids shown to me
   are 1-based.

4. Signatures. sig(seg) = seg.text lowercased, every character not in
   [a-z0-9], whitespace, $ or % replaced with a space, split on
   whitespace, keep tokens longer than 2 characters that are not in
   this stop list, first 18 tokens (duplicates kept, order kept):
     a an and are as at be but by for from i if in is it of on or so
     that this to was we with you your they their there what when where
     why how like um uh
   ("the" is deliberately not in the list.)
   jaccard(x, y) = |set(x) & set(y)| / max(1, |set(x) | set(y)|)

5. Retakes and false starts. For each segment index i (0-based), for j
   in range(i+1, min(segment_count, i+9)):
     if seg[j].start - seg[i].end > 75, stop this inner loop.
     score = jaccard(sig_i, sig_j)
     same_opening = (number of idx in 0, 1, 2, 3 where idx < len(sig_i),
       idx < len(sig_j) and sig_i[idx] == sig_j[idx]) >= 2
     If score >= 0.34 or (score >= 0.24 and same_opening):
       first_len = seg[i].end - seg[i].start
       false_start = same_opening and first_len < 6 and
                     seg[j].start - seg[i].end < 12
       add a candidate (no context field):
         type "false_start" if false_start else "retake",
         confidence "high" if score >= 0.45, "medium" if >= 0.34,
           else "low",
         recommend "cut" if score >= 0.34 else "review",
         score (3 decimals),
         cut [seg[i].start, seg[j].start],
         removes seg[i].text, keeps seg[j].text,
         gap_between = seg[j].start - seg[i].end (2 decimals),
         spans_segments = j - i,
         note: "seg <i+1> ~ seg <j+1> (jaccard <score 2dp>[, same opening])"

6. Ids are assigned in detection order (stutters, then fillers, then
   retakes: c001, c002, ...). Then sort all candidates by cut.start. Do
   not de-duplicate. raw_start = source_start of the first word with
   start >= cut.start; raw_end = source_start of the first word with
   start >= cut.end (omit either if there's no such word or field).
   Also compute: counts by type; proposed_cut_seconds = sum of cut
   lengths where recommend is "cut"; and the same total after merging
   overlaps.

Find outputs (in this folder)
- raw.cut-candidates.json: { agent: "cut-mistakes", source_transcript,
  word_count, segment_count, counts, proposed_cut_seconds,
  proposed_cut_seconds_merged, options, candidates }.
- raw.cut-candidates.md: header (words, segments, counts, proposed
  total, "Review before applying."), then per candidate:
    ## <id> · <type> · <confidence> · recommend: <recommend>
    cut <fmt(start)>-<fmt(end)> (<len 2dp>s) — <note>
    - removes: ... / - keeps: ... / - context: ... (lines present only)
- The find run also prints the segment table (id, start, end, text).

Find self-test (run first; fix the script if anything differs)
  words (no type): "The" 0.00-0.20, "datadog" 0.30-0.70,
  "agent" 0.80-1.10, "The" 2.10-2.30, "datadog" 2.40-2.80,
  "agent" 2.90-3.20, "collects" 3.30-3.70, "metrics" 3.80-4.20,
  "metrics." 4.30-4.80; audio_duration_secs 5.00; default options
Expected:
  word_count 9, segment_count 2
  seg 1: 0.00-1.10 "The datadog agent"
  seg 2: 2.10-4.80 "The datadog agent collects metrics metrics."
  candidates in order:
    c002 false_start, high, cut, score 0.6, cut [0.00, 2.10],
      gap_between 1.0, note "seg 1 ~ seg 2 (jaccard 0.60, same opening)"
    c001 stutter, high, cut, cut [3.80, 4.30], removes "metrics",
      keeps "metrics.",
      context "agent The datadog agent collects metrics metrics."
  counts {stutter: 1, false_start: 1}, proposed_cut_seconds 2.6
Show expected vs actual.

=== HIDDEN-FLUB CHECK (not part of the script) ===
The transcription can smooth over real flubs, so check the raw
transcription data too. From transcript.raw.json (type "word" entries):
- List the 8 lowest-logprob words and the 8 longest words by duration
  per character, each with its edited time (match source_start in
  raw.silence-transcript.json) and 3 words of context on each side.
- Listen-check spots: any word with logprob < -0.3, and any word lasting
  >= 0.6s that doesn't end with . ! ? or ,
- For each spot, cut /tmp/cut-mistakes/check-<n>-<word>.mp4 from
  raw.silenced.mp4, 1.0s before the word's start to 1.0s after its end.
  These are not candidates and never pre-approved.

=== APPLY ALGORITHM (cut_mistakes.py apply) ===

1. Load the approved cuts file { cuts: [ {id, start, end, reason} ] }.
   An empty list is valid: print "no approved cuts; nothing to apply"
   and exit without writing anything. Reject the file if any cut has a
   non-numeric start or end, end <= start, start < 0, or end > duration.
2. Duration = audio_duration_secs of the transcript if numeric, else
   the ffprobe duration of --video, else last word end + 0.2.
3. Boundary check: report any cut whose start or end falls strictly
   inside a word (word.start < t < word.end). Do not apply those; stop
   and show them.
4. Merge: sort by start, merge any cut whose start <= the previous
   range's end, and collect all reasons ("<id>: <reason>").
5. Keep ranges = complement of the merged deletes over [0, duration].
   Any keep range shorter than 0.04s becomes a delete: fold it in and
   re-merge, repeating until none remain. If no keep range is left,
   stop with an error.
6. removed = sum of delete lengths; edited_duration = duration -
   removed, rounded to 3 decimals.
7. Re-time words. removed_before(t) = sum over deletes in order:
   if del.end <= t, add the full length; elif del.start < t, add
   t - del.start; else stop. Drop every word overlapping a delete range
   (word.start < del.end and del.start < word.end); list them per
   merged cut, with 3 words on each side. For each kept word output
   text, source_start, source_end (its times on the silenced timeline),
   raw_start, raw_end (its source_start/source_end from the input, if
   present), start = start - removed_before(start),
   end = end - removed_before(end), rounded to 3 decimals.

Apply outputs (in this folder)
- raw.approved-cuts.json (written by you from my approvals, not by the
  script).
- raw.mistakes-edl.json: { agent: "cut-mistakes", source_duration,
  edited_duration, removed, delete_ranges: [{start, end, reasons}],
  keep_ranges: [{start, end}] }
- raw.mistakes-transcript.json: { language_code,
  source_audio_duration_secs, audio_duration_secs (edited),
  produced_by: "cut-mistakes", words: [{text, source_start, source_end,
  raw_start, raw_end, start, end}] }
- raw.mistakes-decisions.md: input and output duration (mm:ss.ss and
  seconds), total removed across N cuts, then one line per merged cut:
  "- mm:ss.ss-mm:ss.ss (X.XXs): <reasons>".
- raw.mistakes-filter.txt (only with --video): for each keep range i,
    [0:v]trim=start=S:end=E,setpts=PTS-STARTPTS[vi];
    [0:a]atrim=start=S:end=E,asetpts=PTS-STARTPTS[ai];
  then a final line: [v0][a0][v1][a1]...concat=n=N:v=1:a=1[v][a]
  (S and E to 3 decimals).
- raw.clean.mp4 (only with --apply):
    ffmpeg -n -i raw.silenced.mp4 -/filter_complex raw.mistakes-filter.txt
      -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 18
      -c:a aac -b:a 192k -movflags +faststart raw.clean.mp4
  If ffmpeg is older than 7.0, use -filter_complex_script instead.

Apply self-test (run first; fix the script if anything differs)
  Same 9 words and duration 5.00. Cuts: [0.00, 2.10] and [3.80, 4.30].
Expected:
  deletes [0.00, 2.10], [3.80, 4.30]; keeps [2.10, 3.80], [4.30, 5.00];
  removed 2.6; edited_duration 2.4
  dropped: The, datadog, agent (first take), metrics
  re-timed: The 0.00-0.20, datadog 0.30-0.70, agent 0.80-1.10,
            collects 1.20-1.60, metrics. 1.70-2.20
Show expected vs actual.

=== LIP-SYNC ALGORITHM (check_sync_mistakes.py, only if cuts are rendered) ===
CLI: --src raw.silenced.mp4 --out raw.clean.mp4 --edl
raw.mistakes-edl.json --crop W:H:X:Y, then render test times.
Face crop: grab one frame of the source at about 2/3 of its length,
scaled to 1600px wide, look at it, and choose a crop box covering the
face and mouth in full-resolution pixels. (Previous OBS layout at
5120x1440: crop=960:1120:3360:320.) No face: skip lip sync.

1. Edited timeline: walk keep_ranges in order with o = 0. For each keep
   (S, E): the segment covers render [o, o + (E - S)) and maps to
   source S. Then o += E - S.
   source_time(t) = S_i + (t - o_i) for the segment i containing t.
2. Exact extraction: ffmpeg -copyts -ss max(A-2, 0) -i FILE, then trim
   with absolute timestamps (4 decimals):
   - Audio(FILE, A, D): -vn -af "atrim=start=A:end=A+D,aresample=8000"
     -ac 1 -f s16le -   -> int16 samples at 8 kHz.
   - Frames(FILE, A, D): -an -vf "trim=start=A:end=A+D,crop=CROP,
     scale=48:56,format=gray,showinfo" -fps_mode passthrough
     -f rawvideo -   -> 48*56-byte frames. Take each frame's pts_time
     from showinfo on stderr; never infer it from frame counts.
3. Audio offset (s = source_time(t)): r = Audio(OUT, t-0.4, 0.8),
   w = Audio(SRC, s-0.55, 1.1). Subtract r's mean. For each lag L in
   0..len(w)-len(r), with win = w[L:L+len(r)]:
     corr(L) = sum(r*win - mean(win)*r) / (|r| * |win - mean(win)|)
   Best L = largest corr. audio_off = (s-0.55 + L/8000) - (t-0.4).
4. Video offset: rp, rf = Frames(OUT, t-0.2, 0.4); sp, sf =
   Frames(SRC, s-0.35, 0.7). For each j in 0..len(sf)-len(rf):
   MAD(j) = mean |rf[k] - sf[j+k]| over all frames and pixels.
   Best j = smallest MAD. video_off = sp[j] - rp[0].
5. sync_ms = (video_off - audio_off) * 1000 (positive = picture leads).
6. Print per test time: render_t, segment, audio_off, corr, video_off,
   MAD, sync_ms. Expect corr >= 0.95 and MAD < 1.
Self-check: at a time inside segment 0, audio_off must equal
keep_ranges[0].start within 1 ms and video_off must be within one frame.
Test points: one per keep segment that is at least 0.9s long, plus 2
right after each cut (each render window [t-0.4, t+0.4] inside one
segment).
Verdict: pass if |sync_ms| < one frame at every point with no drift.
Mention the detectability thresholds (about +45 ms with sound early,
about -125 ms with sound late) and that this is relative to the source.

=== PHASE 1: FIND AND REVIEW (no cuts) ===
Run both self-tests, then run find on raw.silence-transcript.json.
Also --dry-run find with --segment-gaps source, and with --fillers, and
report how the candidates differ from the default run. Run the
hidden-flub check.

For every candidate, cut a preview clip to /tmp/cut-mistakes/<id>.mp4
from raw.silenced.mp4, 1.0s before cut.start to 1.0s after cut.end,
scaled to 1920px wide, so I can listen.

Then review each candidate yourself, in context. Read removes, keeps
and context; don't trust recommend blindly. Common false positives:
- emphatic repetition ("it's never, never hands-off")
- copula then question ("the piece is, is this...")
- lists and parallel phrasing
- in a tech demo, a product name, command or number said twice on
  purpose (e.g. re-running a command)
For retakes and false starts, check that the kept take is complete and
cleaner. Flag any candidate with spans_segments > 1: its default cut
also removes the segments in between, which may be good content. Prefer
narrowing the cut to just the botched take. Every range you propose
must start at a word's start and end at the start of the next kept
word. You may add your own candidates for flubs the detector missed;
label them "manual" and never pre-approve them.

Report:
- Pre-flight results and both self-test results.
- Word count, segment count, counts by type, proposed total (raw and
  merged), and proposed % of the silenced duration, for all three runs.
- One table row per candidate: id, type, confidence, script recommend,
  your recommendation (cut / keep / narrow / widen) with the exact range
  if changed, edited-timeline range, raw.mp4 range, removes, keeps, and
  a one-line reason.
- Overlapping candidates, grouped.
- The segment table (id, start, end, text), so I can sanity-check
  retake pairing.
- The hidden-flub check results and listen-check clips.
- A very clean delivery may have few or no real mistakes. That's a
  valid result; don't cut natural speech to hit a quota.

Stop and wait. I'll reply with approve / keep / changed ranges per id,
or "approve zero cuts".

=== PHASE 2: APPLY, RENDER AND QA (only after I approve) ===
- Write raw.approved-cuts.json from my reply exactly (id, start, end,
  reason). Show it.
- If I approved zero cuts: write { "cuts": [] }, run apply --dry-run to
  confirm it's a no-op, confirm no raw.mistakes-* or raw.clean.mp4 was
  created, confirm the input md5 checksums are unchanged, and say
  raw.silenced.mp4 and raw.silence-transcript.json are the final outputs
  of this step. Do not render. Stop.
- Run apply --dry-run. Show each merged cut with the words it removes
  and the words on each side. Stop if the boundary check fails or any
  dropped word wasn't meant to go.
- Run apply --video raw.silenced.mp4 --apply.

Verify with /opt/homebrew/bin/ffprobe
- raw.clean.mp4 duration is within 0.1s of edited_duration.
- Video and audio stream durations match each other within 0.1s.
- Codec, resolution and fps match raw.silenced.mp4. Report file size.
- Full decode: ffmpeg -v error -i raw.clean.mp4 -f null - ; report any
  errors and the exit code.
- Text check: the word sequence in raw.mistakes-transcript.json equals
  the input word sequence minus exactly the dropped words.
- Re-timed words are in order, don't overlap, and end within
  edited_duration.
- raw.mp4, raw.silenced.mp4 and the raw.silence-* files are unchanged
  (md5).

Cut-point QA
- For each merged cut, give its render time and the words on each side,
  and cut a preview to /tmp/cut-mistakes/join-<n>.mp4 (0.8s before to
  0.8s after the join in raw.clean.mp4).
- These are hard joins between words. If any join is likely to click,
  say which; a 20-30 ms audio fade can be added later.
- Lip sync: write check_sync_mistakes.py, run its self-check, then measure and
  report the verdict.

Stop after the report. The hand-off to the next step is raw.clean.mp4
and raw.mistakes-transcript.json, or raw.silenced.mp4 and
raw.silence-transcript.json if no cuts were made.
```
