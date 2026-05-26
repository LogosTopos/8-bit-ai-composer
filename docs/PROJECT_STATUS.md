# Project Status

This is a cleaned public snapshot of the project after a destructive cleanup. Most failed attempts, old demos, prompt drafts, and multi-GB generated output were removed.

## Current Mainline

The recommended path is:

```bash
python scripts/generate_thermocline_no_lead_expanded.py
```

This generates a Thermocline battle-BGM draft where bass, drums, harmony, arps, counters, and FX carry the loop without a foreground lead melody.

## Kept Examples

Only four example/reference folders are intentionally kept:

- `examples/highspeed_reference_midi_v1/`
- `examples/community_midi_analysis_v1/`
- `examples/thermocline_chatb_direct_v1/`
- `examples/thermocline_v1_reconsidered/`

They are kept because they explain the successful direction and the failure boundary around lead writing.

## Stable Components

- `src/ebit/renderer.py`
  - Offline renderer for pulse, triangle, sawtooth, sine, wavetable, noise, and FM tones.
  - Stereo rendering, per-track pan, simple note FX, WAV/MP3 export.

- `src/ebit/audio/constants.py`
  - Waveform names, note frequencies, FM presets.

- `src/ebit/audio/envelope.py`
  - Tick-based volume envelope helper.

- `scripts/`
  - Three reproducible Thermocline composition scripts.

## Main Findings

- The AI-produced melody-only branch was a failure.
- The v1 backing track was more valuable than its lead.
- Lower-frequency drive, drums, chord stabs, arps, and quiet cue layers can produce a viable game loop.
- Loud lead and loud prompt-like arps damage the mix quickly.
- The local renderer output is authoritative; MIDI playback is only a secondary reference.

## Known Defects

- The renderer is useful but not a full DAW or tracker.
- No formal test suite exists yet.
- The current best no-lead output is generated, not checked in as a full output folder.
- Some kept reference MIDI files may have third-party licensing constraints; see `DATA_AND_LICENSE_NOTES.md`.
- Human listening is still the real quality gate.

## Good Next Steps

1. Add a small pytest suite for renderer duration, non-NaN audio, and script validation.
2. Turn the no-lead script into a parameterized generator for intensity variants.
3. Add release assets for the current no-lead MP3s.
4. Clean up example licensing before broad public promotion.
