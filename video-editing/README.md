# video-editing

Edit a talking-head or screen recording from raw footage to a delivered video: transcribe it, cut silences and spoken mistakes, plan the visual story and overlays, build it section by section in HyperFrames, then assemble, check and render the final.

Every step is a tested prompt kept word for word in its skill. Each step plans first and stops for your approval before it changes anything.

## Prerequisites

- **ffmpeg** and **ffprobe**. The skills call `/opt/homebrew/bin/ffprobe`, so they assume a Homebrew install on macOS.
- **Python 3**. The helper scripts use only the standard library.
- **ElevenLabs API key** in `ELEVENLABS_API_KEY` (environment or `.env`). Only transcription uses it, plus one optional fresh transcription in finishing-video. Both are paid calls.
- **HyperFrames** and **GSAP** skills, for building-sections and finishing-video. Install them with `/plugin marketplace add greensock/gsap-skills` for GSAP, and the HyperFrames plugin from its marketplace.
- **Node.js**, for `npx hyperframes`.

## How to start

Put the recording in its own folder as `raw.mp4`, open Claude Code there, and say **"edit this video"**. The orchestrator (`starting-video-editing`) works out where the project is, runs the next step with its skill, and records settings, decisions, approvals and output checksums in `PIPELINE.md`.

Other things to say:
- "where am I": show the steps, sections and next step.
- "continue" or "next": run the next step.
- "just cut the silences" or "only plan overlays": run one step, if its inputs are ready.
- "redo the silence cut": archive that step's outputs and run it again, after showing what becomes stale.

## Skills

| # | Skill | What it does | Main outputs |
|---|-------|--------------|--------------|
| | `starting-video-editing` | Orchestrator: detects state, runs the next skill, keeps the ledger | `PIPELINE.md` |
| 0 | `converting-speech-to-text-elevenlabs` | Transcribes `raw.mp4` with ElevenLabs Scribe v2 (word timestamps, fillers kept) | `transcript.raw.json`, `transcript.json` |
| 1 | `cutting-silences` | Trims pauses, renders, checks lip sync and render quality | `raw.silenced.mp4`, `raw.silence-*` |
| 2 | `cutting-mistakes` | Proposes stutters, retakes and false starts for you to approve, then cuts them | `raw.clean.mp4`, `raw.mistakes-*` |
| 3 | `planning-storytelling` | Plans the visual story: world, camera windows, open loop, beat sheet | `plan/STORY.md`, `plan/DESIGN.md`, `plan/beat-sheet.json` |
| 4 | `planning-overlays` | Plans lower-third cards and takeovers on top of the story (optional) | `plan/overlay-beats.json`, `plan/OVERLAYS.md` |
| 5 | `building-sections` | Builds one section in HyperFrames with GSAP, renders and reviews it muted | `film/`, `film/REVIEW.md` |
| 6 | `finishing-video` | Assembles all sections, runs full QA, renders the final | `renders/final-v<N>.mp4`, `deliver/VERIFY.md` |

You can also run any skill on its own by naming it, for example "run cutting-mistakes".

## Things to know

- **Reused scripts.** Several skills reuse helper scripts (`cut_silences.py`, `cut_mistakes.py`, `story_tools.py`, `beats_tools.py`, `finish_tools.py`, `check_sync_final.py`) from a previous video's folder. The orchestrator asks once for that folder (`tools_from`) and fills in each skill's `<PATH TO PREVIOUS FOLDER>`. If a script is missing, the skill writes it from the spec in its prompt and runs its self-test first.
- **Nothing is overwritten.** Outputs open with mode `"x"`, renders get new version numbers, and inputs are checked by md5 at the end of each step.
- **Privacy.** Frames, renders and transcripts stay on your machine. The only outside calls are the ElevenLabs transcriptions. HyperFrames AI describe, upload and share options stay off.
- **No logos or brand marks.** The design system follows Datadog colours by default, but these are personal learning videos, not official content.

**Example prompts:**
- "Edit this video"
- "Where am I?"
- "Transcribe raw.mp4"
- "Cut the silences"
- "Build section s2"
- "Finish the video"
