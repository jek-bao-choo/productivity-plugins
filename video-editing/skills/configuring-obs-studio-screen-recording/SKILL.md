---
name: configuring-obs-studio-screen-recording
description: >-
  This skill should be used when the user wants to set up or verify OBS Studio
  and their Mac for screen recording that matches the video-editing pipeline's
  reference spec (5120x1440 canvas with a 2560x1440 screen pane and camera
  pane, HEVC Hybrid MP4, one mic track, global hotkeys). It applies when the
  user says "set up OBS", "configure OBS for screen recording", "check my OBS
  settings", "verify my recording setup", "is my machine ready for the
  video-editing pipeline", or "do a test recording", even if they don't name
  the skill. It is a one-time setup step that runs before the pipeline
  (before converting-speech-to-text-elevenlabs); the orchestrator doesn't run
  it. The skill works in three phases with a stop after each: a read-only
  machine and tools check with install commands to approve, a panel-by-panel
  OBS walkthrough verified against OBS's saved config files without editing
  them, and a 30-second test recording checked with ffprobe and ffmpeg for
  streams, keyframes, panes, camera rate, audio and clap sync.
version: "0.1.0"
author: productivity-plugins
---

# Configuring OBS Studio Screen Recording

This is a one-time setup step that runs before the video editing pipeline (before agent 0). The orchestrator doesn't run it.

Follow this tested prompt exactly as written; do not reinterpret or simplify it.

```
Guide me through setting up OBS Studio and this Mac for screen recording
so the recordings match the reference spec below, then verify everything.
You can't click in OBS: tell me exactly what to set, one panel at a time,
and check what you can yourself. Work in three phases and stop between
them for my approval.

Rules
- Read-only. Never edit OBS's config files (OBS overwrites them, and a
  hand edit can corrupt a profile); every OBS change is made by me in
  the OBS interface.
- Never install or update anything without my approval. Show the exact
  command first.
- Never print API keys or secrets; only say whether they're set.
- Menu names can differ slightly between OBS versions. If what you
  describe doesn't match what I see, adapt and say so.
- Scratch files go to /tmp/obs-setup/.

=== REFERENCE SPEC ===
Machine: 14-inch MacBook Pro (M4), OBS Studio 32.2.2.
Profile: my-custom-screencasting-profile. Scene: My Custom Screen Recording.

Layout: one 5120x1440 canvas, two 2560x1440 panes side by side, one
clock, one mic track. The 1440p screen pane lets any zoom up to 1.33x
stay a crop, never an upscale, in a 1080p output.
  Screen pane  x 0,    y 0, 2560x1440  macOS Screen Capture
  Camera pane  x 2560, y 0, 2560x1440  1080p30 camera, scaled 1.33x

Sources (scene My Custom Screen Recording)
- macOS Screen Capture: display capture of a 16:9 2560x1440 screen.
  Transform X 0, Y 0, 2560x1440, no crop. Not Window Capture (it loses
  app switches).
- Video Capture Device: MacBook Pro Camera. Use Preset off, 1920x1080,
  NV12 (420v), 30 fps fixed, buffering off. Transform X 2560, Y 0,
  2560x1440, no crop. Center Stage off. (30 fps on a 60 fps canvas: each
  camera frame shows twice; expected.)
- Mic/Aux: the dedicated mic, on Track 1 only.
Audio
- Global Mic/Auxiliary device disabled, so the mic isn't captured twice.
- Desktop Audio and any camera audio off Track 1 (Advanced Audio
  Properties).
- No noise gate, suppression or other filters in OBS; cleanup happens
  later in the pipeline.
Video settings
- Base and output canvas 5120x1440 (32:9), no rescale. 60 fps.
- Renderer OpenGL. Colour format NV12 (8-bit 4:2:0), space Rec. 709,
  range Limited.
- macOS V-Sync disabled while OBS runs, reset on exit.
Recording output (Output mode Advanced)
- Format Hybrid MP4 (crash-resilient, no remux step).
- Video encoder Apple VT HEVC hardware (H.264 hardware can't encode 5120
  wide). Rate control CRF, quality 75, no bitrate limit. Keyframe
  interval 2 s. Profile main, B-frames on, Spatial AQ automatic.
- Audio encoder CoreAudio AAC 320 kbps, Track 1 only.
- Rescale output disabled (panes stay pixel-exact).
- File name %CCYY-%MM-%DD %hh-%mm-%ss, no spaces. Path ~/Movies. (The
  absolute path lives in the profile; never commit it anywhere.)
Hotkeys (global: OBS doesn't swallow them, so they also reach VS Code,
Chrome or Terminal)
- Start recording ⌃⌥⌘R (or F13). Stop recording ⌃⌥⌘S (or F14).
  Pause/unpause ⌃⌥⌘P (or F15); one key must toggle cleanly.
- OBS has Accessibility permission. Hotkey focus behaviour: Never
  disable hotkeys.
Machine tools
- FFmpeg and FFprobe, Chromium (or Chrome), Node.js 22 or newer,
  Python 3, jq, Claude Code.
- Agent skills: HyperFrames (HeyGen), GSAP (GreenSock), ElevenLabs, and
  the video-editing plugin from the productivity-plugins marketplace
  (https://github.com/jek-bao-choo/productivity-plugins).
- ELEVENLABS_API_KEY set (environment or .env).

=== PHASE 1: MACHINE CHECK (read-only) ===
Check and report each item as present (with version or path), missing,
or unknown:
- sw_vers and the chip (sysctl -n machdep.cpu.brand_string).
- ffmpeg and ffprobe (which, -version; note if they're Homebrew's under
  /opt/homebrew/bin), node --version (needs 22+), python3 --version, jq,
  Chromium or Google Chrome (in /Applications or on PATH), claude
  --version.
- OBS: /Applications/OBS.app and its version.
- Agent skills: list the installed skills and plugins you can see and
  whether HyperFrames, GSAP, ElevenLabs and the video-editing plugin's
  skills (starting-video-editing, converting-speech-to-text-elevenlabs,
  cutting-silences, cutting-mistakes, planning-storytelling,
  planning-overlays, building-sections, finishing-video) are available.
- ELEVENLABS_API_KEY: set or not set (never its value).
- The main display: its resolution and whether it's 16:9 (screen
  capture expects 2560x1440; if it's the built-in screen at a different
  size, say so and list the options, e.g. an external 1440p display or
  the closest 16:9 scaled resolution).
For everything missing, give the install command or link: Homebrew
for ffmpeg, node, jq and chromium; for agent skills, the commands from
each vendor (HyperFrames: npx skills add heygen-com/hyperframes; GSAP:
/plugin marketplace add greensock/gsap-skills; ElevenLabs: npx skills
add elevenlabs/skills; video-editing: /plugin marketplace add
jek-bao-choo/productivity-plugins, then install the video-editing
plugin from it, checking the exact plugin name in its marketplace.json).

Report, then stop and wait. Install nothing until I approve each command.

=== PHASE 2: CONFIGURE OBS (one panel at a time) ===
First find OBS's settings folder (normally ~/Library/Application
Support/obs-studio/): list the profiles under basic/profiles/ and the
scene collections under basic/scenes/. Say whether
my-custom-screencasting-profile and a collection holding the scene My
Custom Screen Recording already exist. If they do, offer to verify
instead of re-creating them.

Then walk me through these panels in order. For each: tell me where to
go, what to set (from the spec), and what to leave alone; wait for me to
say "done"; then move on.
1. Profile and scene collection: create or select
   my-custom-screencasting-profile and the scene My Custom Screen
   Recording.
2. Settings > Video: canvas and output 5120x1440, 60 fps.
3. Settings > Advanced: renderer, colour format, space, range, macOS
   V-Sync options, recording filename format with no spaces.
4. Settings > Audio: global Mic/Auxiliary and Desktop Audio devices.
5. Scene sources: macOS Screen Capture, Video Capture Device and Mic/Aux
   with the spec's properties; Edit Transform for each pane (the exact
   X, Y, size and no crop). Remind me to turn off Center Stage (and
   other camera video effects, such as Reactions, which can add
   animations to the feed) in Control Centre while the camera is on.
6. Edit > Advanced Audio Properties: only the mic on Track 1; no filters
   on any audio source.
7. Settings > Output (Advanced) > Recording: path, format, encoders and
   every encoder setting, audio track, rescale off.
8. Settings > Hotkeys: the three hotkeys; then the hotkey focus
   behaviour. macOS: System Settings > Privacy & Security, OBS allowed
   for Screen Recording, Camera, Microphone and Accessibility (I confirm
   these; you can't read them).

After the last panel, ask me to quit OBS so it writes every setting to
disk. Then read, without changing anything:
- the profile's basic.ini and encoder settings file, and the scene
  collection's JSON;
- OBS's global or user settings file for the hotkey focus behaviour.
Compare every spec value you can find there. Key names differ between
OBS versions: locate the setting rather than assuming a key, and quote
the key and value you found. Report a table: setting, spec value, found
value, match / mismatch / not found (and what I should check by eye).

Stop and wait until every mismatch is fixed or I accept it.

=== PHASE 3: TEST RECORDING ===
Ask me to record a 30 s test with the hotkeys only:
- start; say one full sentence; clap once, visibly, in front of the
  camera; switch between two apps; pause for 3 s with the pause hotkey;
  resume; say one more sentence; stop.
Then find the newest file in ~/Movies and check (copy it to
/tmp/obs-setup/test.mp4 first; never touch the original):
- File name matches the date-stamp format with no spaces.
- ffprobe: exactly one video stream, HEVC, Main profile, 8-bit
  (yuv420p), 5120x1440, 60 fps, colour primaries / transfer / matrix
  bt709, range tv (limited); exactly one audio stream, AAC, about
  320 kb/s, start_time 0 (the transcription step requires it); no other
  streams.
- Keyframes about every 2 s (list keyframe times with ffprobe
  -skip_frame nokey).
- Full decode with ffmpeg -v error ... -f null - : no errors, exit 0.
- Pause: one recording file, no decode errors across the pause; report
  the duration (it should exclude the paused time).
- Panes: grab one frame and look at it. Screen content fills x 0-2560;
  the camera fills x 2560-5120 at full height, no black bars, no crop
  of the head; no window-only capture (the app switch shows in the
  screen pane).
- Camera rate: within the camera pane, consecutive canvas frames repeat
  in pairs (30 fps on a 60 fps canvas).
- Audio: the mic is present and not doubled (no echo or comb filtering
  from a second capture); report peak and mean levels (volumedetect).
- Sync: find the clap's audio peak, grab camera-pane frames from 0.2 s
  before to 0.2 s after it, look for the frame where the hands meet,
  and report the offset (within one camera frame, ~33 ms, is a pass).

Report a pass / fail table with what to fix for each fail, and whether
this setup is ready for the video-editing pipeline (the recording is
copied into a project folder as raw.mp4). Then stop.
```
