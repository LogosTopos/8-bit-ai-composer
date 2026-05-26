# Architecture

The repository now has four layers:

```text
composition script
  -> explicit note timelines
  -> src/ebit/renderer.py
  -> stereo numpy buffers
  -> WAV/MP3 through soundfile + ffmpeg
  -> optional MIDI through mido
  -> validation JSON and stem CSV
```

## Renderer Input

The renderer accepts a small dictionary format:

```json
{
  "bpm": 192,
  "tracks": [
    {
      "name": "bass_drive",
      "instrument": "triangle",
      "pan": 0.0,
      "notes": [
        {"n": "C#2", "b": 0.0, "d": 0.5, "v": 0.8}
      ]
    }
  ]
}
```

Important note fields:

- `n`: note name, such as `C#4`.
- `b`: start beat.
- `d`: duration in beats.
- `v`: velocity.
- `fx`: optional macros, including `slide_to`, `vib`, `tremolo`, `retrigger`, and `arp`.
- `pan`: optional per-note pan override.

## Local Instruments

Supported local instrument names:

- pulse: `pulse_12`, `pulse_25`, `pulse_50`, `pulse_75`
- bass/chip: `triangle`
- bright: `sawtooth`, `wavetable`
- clean: `sine`
- noise: `noise_short`, `noise_long`, `noise_periodic`
- FM: `fm`, `fm_bass`, `fm_bell`, `fm_brass`, `fm_lead`, `fm_string`

These are not General MIDI instruments. MIDI export is for inspection and DAW handoff; external MIDI playback will not match the MP3 rendered by this project.

## Composition Script Pattern

The useful scripts follow this pattern:

1. Define sections, tempo, progression, and role constraints.
2. Build role-specific tracks: bass, drum core, drum detail, harmony, arps, FX.
3. Render each role group as a stem bus.
4. Apply simple filtering, delay, and sidechain-like ducking.
5. Mix and limit.
6. Write master MP3, comparison MP3s, stem MP3s, MIDI, score JSON, and validation files.

## Why This Shape

The project found that raw AI composition tends to fail where control matters most: melody quality, arrangement density, and mix balance. Code-based arrangement keeps those decisions inspectable. AI can still help write or revise scripts, but the musical artifact remains reproducible.
