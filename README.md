# ε-bit-ai-composer

A compact 8-bit / chip-style game music workbench. This repository is a cleaned-up, public-ready evolution of the original 8-bit AI composer idea: AI can help design and implement arrangements, but the useful artifact is deterministic Python composition code and preset cards that render locally to audio, MIDI, stems, and validation files.

The current best direction is not "ask an AI for a melody." In the Thermocline battle-BGM experiment, lead-melody attempts were weak. The strongest music came from bass, drums, harmony, arps, counters, and FX acting as the foreground engine.

## Quick Start

Requirements:

- Python 3.11+
- `ffmpeg` on PATH for MP3 export

Install and render:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_thermocline_no_lead_expanded.py
```

The generated files are written to:

```text
output/analysis/温跃层战斗BGM_v1_no_lead_expanded/
```

`output/` is ignored by Git. The checked-in `examples/` folder contains selected reference outputs and analysis packs.

## What To Listen To First

The most useful checked-in examples are:

```text
examples/thermocline_v1_reconsidered/
examples/thermocline_chatb_direct_v1/
examples/highspeed_reference_midi_v1/
examples/community_midi_analysis_v1/
```

For the current musical direction, start with:

- `examples/thermocline_v1_reconsidered/03_去掉主旋律_伴奏对比.mp3`
- `examples/thermocline_chatb_direct_v1/04_no_lead_arrangement.mp3`
- then regenerate `scripts/generate_thermocline_no_lead_expanded.py` locally for the latest no-lead draft.

## Project Layout

```text
src/ebit/       Small reusable rendering core
presets/        Creator-facing instrument and macro cards
scripts/        Reproducible composition scripts
examples/       Four curated example/reference folders
docs/           Project status, architecture, case study, release notes
output/         Generated local output; ignored by Git
```

## Creator Presets

The `presets/` layer restores a lightweight version of the old instrument-card and macro workflow without bringing back the old asset tree.

- `presets/instruments/*.json` describe reusable renderer-facing roles, such as bass drive, quiet cue arp, snare noise, and teleport chirp.
- `presets/macros/*.json` describe reusable note decorations, such as vibrato, retrigger rolls, slides, and alarm arps.
- `src/ebit/presets.py` loads, validates, and applies those cards to the same note/track dictionaries used by the composition scripts.

Try it:

```bash
python scripts/render_preset_demo.py
```

This writes a short proof render to:

```text
output/preset_demo/
```

## Core Scripts

- `scripts/generate_thermocline_v1.py`
  - Recreates the earlier Thermocline v1 arrangement.
  - Useful because its backing track is strong, even though the lead is not.

- `scripts/generate_thermocline_chatb_direct.py`
  - Chat B direct pass with delayed, quieter lead and stronger support layers.
  - Kept as process evidence, not the final recommended musical path.

- `scripts/generate_thermocline_no_lead_expanded.py`
  - Current recommended direction.
  - Removes the foreground lead role and expands bass, drums, harmony, arps, counters, and FX.

- `scripts/render_preset_demo.py`
  - Minimal card-based demo.
  - Useful as the starting point for creating new instrument and macro cards.

## Main Findings

- Deterministic arrangement code is more useful than flat AI note dumps.
- AI-written analysis is only advisory; human listening overrides it.
- Melody-only gating was a failed decision for this case.
- Bass/drums/harmony/arps can carry game BGM without a conventional lead.
- MIDI files are useful for inspection, but this project's local MP3 render is the sound reference.

## Continue The Music

Good next edits for collaborators:

- Improve the no-lead script's section transitions.
- Add 2-4 bar variants for different combat intensity states.
- Keep secondary arp/cue sounds quiet; they should not feel like loud UI prompts.
- Add manual loop-point checking for game integration.
- Tune bass/drum balance on real speakers and headphones.
- Promote repeated hard-coded roles from scripts into `presets/` cards when they become reusable.

See:

- [Project Status](docs/PROJECT_STATUS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Creator Workflow](docs/CREATOR_WORKFLOW.md)
- [Thermocline Case Study](docs/THERMOCLINE_CASE_STUDY.md)
- [Data And License Notes](docs/DATA_AND_LICENSE_NOTES.md)
- [GitHub Release Checklist](docs/GITHUB_RELEASE_CHECKLIST.md)

## License

MIT. See [LICENSE](LICENSE).
