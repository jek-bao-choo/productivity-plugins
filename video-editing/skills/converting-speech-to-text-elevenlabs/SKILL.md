---
name: converting-speech-to-text-elevenlabs
description: >-
  This skill should be used when the user wants to transcribe a video or audio
  recording (typically raw.mp4) with the ElevenLabs speech-to-text API (Scribe
  v2) and produce transcript.raw.json and transcript.json with word-level
  timestamps. It applies when the user says "transcribe my recording",
  "transcribe raw.mp4", "run ElevenLabs STT", "make transcript.json", "get word
  timestamps for my video", or "prepare the transcript before cut-silences or
  cut-mistakes", even if they don't mention ElevenLabs by name. It is agent 0
  of the editing pipeline, the first step before cutting-silences. The skill runs
  read-only pre-flight checks, extracts the audio so only audio is uploaded,
  calls the API with curl using glossary.txt keyterms, converts the response to the herk-edit-kit source.json schema,
  validates timings, and stops for confirmation before any editing step.
version: "0.1.0"
author: productivity-plugins
---

# Converting Speech to Text with ElevenLabs

This is agent 0 (transcription) of the video editing pipeline.

Follow this tested prompt exactly as written; do not reinterpret or simplify it.

```
Transcribe my recording raw.mp4 using the ElevenLabs speech-to-text API.
Plan first, then run after I approve.

Pre-flight (read-only, report results)
- If transcript.json or transcript.raw.json already exists in this folder,
  stop and tell me. Do not re-transcribe.
- Check that ELEVENLABS_API_KEY is set (environment or .env). Never print it.
- Get the media duration with /opt/homebrew/bin/ffprobe and report it,
  and confirm the audio stream's start_time is 0.
- Extract the audio only: ffmpeg -n -i raw.mp4 -vn -ac 1 -c:a flac
  /tmp/transcribe/raw-audio.flac (WAV if the API rejects FLAC). Before
  the call, tell me what will be uploaded (audio only, its size) and
  that this is a paid API call.
- Read glossary.txt: trim whitespace, skip blank lines, skip any term over
  50 characters (tell me which). If glossary.txt doesn't exist, continue
  without keyterms and say so.

API call (curl, no SDK)
  POST https://api.elevenlabs.io/v1/speech-to-text
  header xi-api-key: $ELEVENLABS_API_KEY
  multipart: -F file=@/tmp/transcribe/raw-audio.flac
  --form-string model_id=scribe_v2  --form-string language_code=en
  --form-string timestamps_granularity=word
  --form-string no_verbatim=false   (keep fillers, false starts, repeats,
                                     stutters; cut-mistakes needs them)
  --form-string diarize=false       (single speaker)
  --form-string tag_audio_events=true
  --form-string keyterms=<term>     (one field per glossary term, built
                                     from a bash array)
  Text fields use --form-string so a value starting with @ or <, or
  containing ;, is sent as text. -F is only for the file.
Confirm in your report that each field was sent, plus the keyterms count.

Outputs
1. Write the response to transcript.raw.tmp.json. Only if the HTTP status is
   200 and `jq empty` passes, rename it to transcript.raw.json. Otherwise
   delete the temp file and show me the status and error body.
2. Convert to transcript.json with exactly this schema (herk-edit-kit
   examples/editing/source.json):
   { language_code, audio_duration_secs, text, words: [ {text, start, end, type} ] }
   - language_code: "eng" -> "en"
   - audio_duration_secs: from the raw response if present, else ffprobe
     (report both values if they differ)
   - text: unchanged
   - words: keep type "word" and "audio_event", drop "spacing"; copy only
     text/start/end/type (drop speaker_id, logprob, everything else)
   Tell me how you mapped each field.

Validation (run before reporting)
- Every entry has a numeric start and end, and end >= start.
- Type "word" only: in order and no overlaps. Report overlaps, don't fix them.
  Report audio events that overlap words separately (that can be normal).
- The last entry's end is within the media duration.
- Report: word count, audio-event count, media duration, total speech time
  (sum of word durations), lead-in and tail silence, and the 5 longest gaps
  between consecutive words (with timestamps and the words on each side).
- Flag it if the transcript has no filler words or false starts at all, in
  case Scribe smoothed them out despite no_verbatim=false.
- Show the full text.

Stop after validation. Do not start cut-silences or cut-mistakes until I
confirm the transcript looks right.
```
