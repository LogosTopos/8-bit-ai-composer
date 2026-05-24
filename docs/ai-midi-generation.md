# AI MIDI Generation for 8-Bit / Chiptune Music

> Compiled: 2026-05-24
> Focus: actionable patterns for building an AI-powered 8-bit composer

---

## Table of Contents

1. [Python MIDI Libraries: State of the Ecosystem](#1-python-midi-libraries-state-of-the-ecosystem)
2. [MIDI Format Specifics for Chiptune](#2-midi-format-specifics-for-chiptune)
3. [Practical MIDI Generation with Python](#3-practical-midi-generation-with-python)
4. [Tokenization Approaches for Music AI](#4-tokenization-approaches-for-music-ai)
5. [Existing AI MIDI Tools](#5-existing-ai-midi-tools)
6. [Building an AI 8-Bit Composer: Architecture](#6-building-an-ai-8-bit-composer-architecture)

---

## 1. Python MIDI Libraries: State of the Ecosystem

### Recommended Stack (2026)

```
PyTorch 2.4+ / HuggingFace Transformers
    |
    v
MidiTok 2.1+      (tokenization for AI training)
    |
    v
mido 1.3+         (low-level MIDI file I/O)
music21 9.9+      (music theory + composition)
    |
    v
MusPy             (optional: unified bridge between formats)
    |
    v
FluidSynth        (MIDI -> audio rendering via .sf2 SoundFonts)
```

### Library Details

| Library | Status | Purpose | Install |
|---------|--------|---------|---------|
| **mido** | Active (v1.3.3) | Low-level MIDI file creation, reading, writing. Handles ticks, messages, meta events. | `pip install mido` |
| **music21** | Active (v9.9.1) | Music theory analysis, composition, notation. Higher-level than mido. Does NOT reliably export `program_change` -- needs mido post-processing. | `pip install music21` |
| **pretty_midi** | Abandoned (no updates since 2020) | Was the go-to for easy MIDI manipulation. No Python 3.11+ support. **Avoid for new projects.** | `pip install pretty-midi` (legacy) |
| **MusPy** | Active | Unified toolkit bridging mido, music21, pretty_midi, Pypianoroll. Built for symbolic music generation research (ISMIR 2020). Supports PyTorch/TF datasets. | `pip install muspy` |
| **MidiTok** | Active (v2.1+) | Tokenization for AI/Transformer models. Supports REMI, CP Word, Octuple, MIDI-Like, TSD, MuMIDI. HuggingFace Hub integration. | `pip install miditok symusic` |
| **chippy** | Active | Pure Python chiptune waveform synthesis (square/pulse with adjustable duty cycle). Generator-based. | `pip install chippy` |
| **isobar** | Active | Algorithmic composition / pattern-based MIDI generation. Built-in loop/ping-pong patterns. | `pip install isobar` |

### When to Use What

- **Creating a MIDI file from scratch** -> `mido`
- **Composing with music theory (scales, chords, voice leading)** -> `music21`
- **Tokenizing MIDI for transformer training** -> `MidiTok`
- **Converting between formats** -> `MusPy` (has `from_mido()`, `from_music21()`, `from_pretty_midi()`)
- **Daisy-chaining AI output to audio** -> `mido` -> `fluidsynth` (or `chippy` for direct 8-bit audio)

---

## 2. MIDI Format Specifics for Chiptune

### The NES 2A03 Sound Chip

The NES APU (Audio Processing Unit) has **5 monophonic channels**:

| Voice | Waveform | MIDI Name | MIDI Note Range | Velocity/Volume | Timbre/Duty |
|-------|----------|-----------|----------------|----------------|-------------|
| Pulse 1 (P1) | Square (12.5%, 25%, 50%, 75% duty) | `P1` | 32-108 | CC11 (0-15) | CC12 (0-3) |
| Pulse 2 (P2) | Square (same duty options) | `P2` | 32-108 | CC11 (0-15) | CC12 (0-3) |
| Triangle (TR) | Triangle (no volume control) | `TR` | 21-108 | On/off only | None |
| Noise (NO) | Pseudo-random noise (16-bit shift register) | `NO` | 0-16 (non-MIDI mapping) | CC11 (0-15) | CC12 (0-1) |
| DPCM | 1-bit delta PCM samples | (excluded from most datasets) | - | - | - |

### Channel Constraints (Critical for Chiptune)

- **Monophonic**: Each channel plays ONE note at a time. Chords must be arpeggiated.
- **No velocity on triangle**: Triangle channel is on/off only -- no volume gradient.
- **Duty cycle CC12**: Pulse channels use CC12 to select duty cycle (0=12.5%, 1=25%, 2=50%, 3=75%).
- **5 channels total**: Any AI model targeting NES must output exactly 4-5 note streams (P1, P2, TR, NO, and optionally DPCM).

### MIDI-to-NES Instrument Mapping

There is no General MIDI standard for chiptune, but here is a practical convention:

```
GM Program 80-87 (Synth Lead):   Use for Pulse 1 (lead/melody)
GM Program 88-95 (Synth Pad):    Use for Pulse 2 (harmony/countermelody)
GM Program 96   (FX 1 - rain):   Use for Triangle (bass)
GM Program 124  (Telephone ring): Use for Noise (percussion)

Or, use custom track naming:
  Track name "P1" = Pulse 1 (square lead)
  Track name "P2" = Pulse 2 (square harmony)
  Track name "TR" = Triangle (bass)
  Track name "NO" = Noise (drums/percussion)
```

This follows the **nesmdb convention** where MIDI tracks are named P1/P2/TR/NO and control changes encode chiptune-specific parameters.

### Tools for MIDI <-> Chiptune Conversion

| Tool | Purpose | Notes |
|------|---------|-------|
| **FamiStudio** | DAW-like NES music editor | Supports MIDI input, NSF export, MIDI export. Cross-platform. Best modern tool. |
| **0CC-FamiTracker** | Classic tracker fork | Extended features, multichip NSF. No native MIDI export. |
| **nsf2midi** | Convert NSF to MIDI | Results lose chiptune character; useful for analysis/visualization. |
| **mmlx** | Python NES chiptune language | Define instrument patches, ADSR, arpeggio patterns. Generates NSF. Install: `pip install mmlx` |
| **nesmdb** | NES Music Database | 5,278 songs from 397 games. MIDI + expressive formats. Python package for rendering. |

---

## 3. Practical MIDI Generation with Python

### 3.1 Creating a MIDI File from Scratch with `mido`

```python
from mido import Message, MidiFile, MidiTrack, MetaMessage

def create_chiptune_midi(filepath: str, bpm: int = 150):
    """Create a multi-track MIDI file with NES-like channel mapping."""
    mid = MidiFile(type=1)
    ticks_per_beat = 480
    mid.ticks_per_beat = ticks_per_beat
    tempo = mido.bpm2tempo(bpm)

    # --- Track 1: Pulse 1 (Lead / Square Wave) ---
    track_p1 = MidiTrack()
    mid.tracks.append(track_p1)
    track_p1.append(MetaMessage('track_name', name='P1'))
    track_p1.append(MetaMessage('set_tempo', tempo=tempo))
    # GM Synth Lead 1 (square wave approximation)
    track_p1.append(Message('program_change', program=80, time=0))

    # Simple ascending scale
    for note in [60, 62, 64, 65, 67, 69, 71, 72]:
        track_p1.append(Message('note_on', note=note, velocity=100, time=0))
        track_p1.append(Message('note_off', note=note, velocity=64,
                                time=ticks_per_beat // 2))

    # --- Track 2: Pulse 2 (Harmony / Square Wave) ---
    track_p2 = MidiTrack()
    mid.tracks.append(track_p2)
    track_p2.append(MetaMessage('track_name', name='P2'))
    track_p2.append(Message('program_change', program=81, time=0))

    # C major triad arpeggiated
    for note in [60, 64, 67]:  # C E G
        track_p2.append(Message('note_on', note=note, velocity=80, time=0))
        track_p2.append(Message('note_off', note=note, velocity=64,
                                time=ticks_per_beat * 2))

    # --- Track 3: Triangle (Bass) ---
    track_tr = MidiTrack()
    mid.tracks.append(track_tr)
    track_tr.append(MetaMessage('track_name', name='TR'))
    track_tr.append(Message('program_change', program=96, time=0))

    for note in [36, 40, 43]:  # C2, E2, G2
        track_tr.append(Message('note_on', note=note, velocity=80, time=0))
        track_tr.append(Message('note_off', note=note, velocity=64,
                                time=ticks_per_beat * 2))

    # --- Track 4: Noise (Drums) ---
    track_no = MidiTrack()
    mid.tracks.append(track_no)
    track_no.append(MetaMessage('track_name', name='NO'))
    track_no.append(Message('program_change', program=124, time=0))

    # Simple kick-snare pattern (MIDI note 36 = kick, 38 = snare)
    for i in range(8):
        if i % 2 == 0:
            track_no.append(Message('note_on', note=36, velocity=90, time=0))
            track_no.append(Message('note_off', note=36, velocity=64,
                                    time=ticks_per_beat // 2))
        else:
            track_no.append(Message('note_on', note=38, velocity=70, time=0))
            track_no.append(Message('note_off', note=38, velocity=64,
                                    time=ticks_per_beat // 2))

    mid.save(filepath)
    return filepath

# Usage
create_chiptune_midi('chiptune_demo.mid', bpm=150)
```

### 3.2 Generating Arpeggio Patterns (Essential for Chiptune)

Arpeggios are the heart of chiptune -- since NES channels are monophonic, chords are faked by rapidly cycling through notes.

```python
from mido import Message, MidiFile, MidiTrack, MetaMessage
import mido

def add_arpeggio(track, chord_notes, start_note, duration_ticks,
                 arp_rate=6, velocity=80):
    """
    Add an arpeggiated chord to a track.
    
    Args:
        track: MidiTrack object
        chord_notes: list of MIDI note numbers (e.g., [60, 64, 67] for C major)
        start_note: starting note offset (transposition)
        duration_ticks: total duration of the arpeggio
        arp_rate: ticks per individual note in the arpeggio
        velocity: note velocity
    """
    notes = [n + start_note for n in chord_notes]
    elapsed = 0
    while elapsed < duration_ticks:
        for note in notes:
            if elapsed >= duration_ticks:
                break
            track.append(Message('note_on', note=note, velocity=velocity, time=0))
            track.append(Message('note_off', note=note, velocity=64,
                                 time=min(arp_rate, duration_ticks - elapsed)))
            elapsed += arp_rate

# Usage example
mid = MidiFile(type=1)
mid.ticks_per_beat = 480
track = MidiTrack()
mid.tracks.append(track)
track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(140)))
track.append(Message('program_change', program=80, time=0))

# C major arpeggio over 4 beats
add_arpeggio(track, [0, 4, 7], start_note=60,
             duration_ticks=480 * 4, arp_rate=80)
mid.save('arpeggio_test.mid')
```

### 3.3 Creating Loopable Game Music

Game music needs seamless loops. The key is ensuring the total duration of all tracks is identical.

```python
def create_loopable_section(track, notes_pattern, bars, ticks_per_bar):
    """
    Create a loopable musical section.
    All tracks must have the same total tick count.
    """
    total_ticks = bars * ticks_per_bar
    current_tick = 0

    for note, duration_beats in notes_pattern:
        duration_ticks = int(duration_beats * ticks_per_bar / 4)
        track.append(Message('note_on', note=note, velocity=80, time=0))
        track.append(Message('note_off', note=note, velocity=64,
                             time=duration_ticks))

    # Verify total duration matches
    # (In practice, you'd sum up durations and pad if needed)
```

### 3.4 Higher-Level Composition with `music21`

```python
from music21 import stream, note, chord, tempo, instrument, key, metadata

def compose_chiptune_loop():
    """Create a loopable 4-bar chiptune phrase with music21."""
    score = stream.Score()
    score.append(metadata.Metadata(title='Chiptune Loop'))
    score.append(tempo.MetronomeMark(number=140))

    # --- Lead (Pulse 1) ---
    lead = stream.Part()
    lead.insert(0, instrument.SynthLead())
    lead.partName = 'P1'

    # Pentatonic melody
    melody_notes = [72, 69, 71, 67, 64, 67, 69, 72]
    for n in melody_notes:
        mel_note = note.Note(n, quarterLength=0.5)
        lead.append(mel_note)

    # --- Bass (Triangle) ---
    bass = stream.Part()
    bass.insert(0, instrument.ElectricBass())
    bass.partName = 'TR'

    bass_notes = [36, 43, 40, 48]  # C2, G2, E2, C3
    for n in bass_notes:
        bass_note = note.Note(n, quarterLength=1.0)
        bass.append(bass_note)

    score.append(lead)
    score.append(bass)

    score.write('midi', fp='chiptune_loop.mid')
    return score
```

### 3.5 Post-Processing: mido Pass-Through for Program Changes

`music21` doesn't reliably emit `program_change` messages. Fix with a post-processing step:

```python
from mido import MidiFile, Message

def fix_program_changes(input_midi: str, output_midi: str,
                        program_map: dict = None):
    """
    Add program_change messages to a music21-generated MIDI file.
    
    program_map: {track_index: program_number}
    """
    if program_map is None:
        program_map = {0: 80, 1: 81, 2: 96, 3: 124}

    mid = MidiFile(input_midi)
    for i, track in enumerate(mid.tracks):
        if i in program_map:
            # Insert program change after the first meta message
            prog = Message('program_change', program=program_map[i], time=0)
            # Insert at position 1 (after track name/time signature)
            track.insert(1, prog)

    mid.save(output_midi)
```

---

## 4. Tokenization Approaches for Music AI

### Overview: Why Tokenize?

Transformers need flat token sequences. Raw MIDI bytes are not ideal. The music AI community has developed several tokenization strategies that convert MIDI events into discrete tokens.

### 4.1 REMI (Revamped MIDI-derived Events)

**Origin**: Huang & Yang, "Pop Music Transformer" (2020)

**Concept**: Decompose each note into a sequence of attribute tokens: Bar, Position (within bar), Pitch, Duration, Velocity.

```
[Bar_1] [Position_0] [Pitch_60] [Duration_2] [Velocity_80]
[Position_4] [Pitch_64] [Duration_2] [Velocity_80] ...
```

**Pros**: Fine-grained temporal control, musically coherent.
**Cons**: Long sequences (~19 tokens/beat), memory-intensive.

### 4.2 CP Word (Compound Word)

**Origin**: Hsiao et al., "Compound Word Transformer" (AAAI 2021)

**Concept**: Group all attributes of a musical event into a SINGLE compound token with multiple sub-attributes predicted in parallel.

```
CompoundToken: {
    Family: Note_Family,
    Pitch: 60,
    Duration: 0.25,
    Velocity: 80,
    Program: 0
}
```

**Pros**: ~55% shorter sequences (~8.6 tokens/beat), enables full-song attention windows, faster training/inference.
**Cons**: Parallel prediction can miss intra-token dependencies (pitch-duration correlations).

**Architecture**: K+1 Feed-Forward heads predict each attribute in parallel + a "Family Token" (Note Family or Metric Family). Uses adaptive sampling (different temperature per attribute type).

### 4.3 Comparison

| Method | Vocab Size | Tokens/Beat | Inference Speed | Training Time |
|--------|-----------|-------------|----------------|---------------|
| REMI | ~338 | ~19.1 | ~88-140 sec/song | ~3-7 days |
| CP Word | ~341 | ~8.6 | ~19-29 sec/song | ~0.6-1.3 days |
| Octuple | ~241 | ~5.2 | Fastest | Fastest |
| MIDI-Like | ~395 | ~31.2 | Slowest | Slowest |

### 4.4 Tokenizing for 3-4 Channel NES Music

For chiptune, you want each of the 4 NES channels predicted independently:

**Approach A: Multi-track REMI**
- Tokenize each track (P1, P2, TR, NO) separately with REMI
- Train a model that generates 4 parallel token sequences
- Use a special "channel" token or separate embedding per track

**Approach B: Channel-annotated CP Word**
- Add a `Channel` attribute (P1/P2/TR/NO) to each compound word
- Single token stream interleaves all 4 channels
- Model learns to switch between channels

**Approach C: Track-specific fine-tuning**
- Train 4 separate small models (one per channel)
- Synchronize via shared bar/position tokens

### 4.5 Using MidiTok in Practice

```python
from miditok import REMI, TokenizerConfig, CPWord
from symusic import Score

# --- Configure for chiptune constraints ---
config = TokenizerConfig(
    num_velocities=8,              # NES has ~16 velocity levels max
    use_chords=False,              # Chiptune rarely uses chords
    use_programs=True,             # Track instrument assignments
    use_tempos=True,
    use_time_signatures=True,
    one_token_stream_for_programs=False,  # Keep tracks separate
)

# REMI tokenizer
tokenizer = REMI(config)

# Tokenize a MIDI file
midi = Score("chiptune_demo.mid")
tokens = tokenizer(midi)

# tokens.ids -> list of ints, ready for transformer training
print(f"Sequence length: {len(tokens.ids)}")

# Detokenize back to MIDI (for listening to generated output)
midi_reconstructed = tokenizer(tokens)
midi_reconstructed.dump_midi("reconstructed.mid")

# Train BPE for further compression (optional)
files = ["chiptune_demo.mid", "another_song.mid"]
tokenizer.train(vocab_size=30000, files_paths=files)

# For PyTorch training:
from miditok.pytorch_data import DatasetMIDI, DataCollator
from torch.utils.data import DataLoader

dataset = DatasetMIDI(
    files_paths=["chiptune_demo.mid"],
    tokenizer=tokenizer,
    max_seq_len=1024,
    bos_token_id=tokenizer["BOS_None"],
    eos_token_id=tokenizer["EOS_None"],
)
collator = DataCollator(pad_token_id=tokenizer.pad_token_id,
                        copy_inputs_as_labels=True)
loader = DataLoader(dataset, batch_size=8, collate_fn=collator)
```

### 4.6 Byte-Pair Encoding for Music

Both REMI and CP Word sequences can be further compressed with BPE:

- **REMI + BPE**: Reduced from ~19 to ~12 tokens/beat with minimal quality loss
- **CP + BPE**: Reduced from ~8.6 to ~6 tokens/beat
- Implemented directly in MidiTok via `tokenizer.train(vocab_size=N, files_paths=...)`

---

## 5. Existing AI MIDI Tools

### 5.1 Google Magenta

| Model | Type | Input/Output | Status |
|-------|------|-------------|--------|
| **MusicVAE** | VAE | MIDI in/out, interpolation, sampling | TensorFlow legacy. PyTorch ports available. |
| **Music Transformer** | Transformer (relative self-attention) | Event-based MIDI tokens | Original TF. PyTorch ports: `pno-ai`, `MusicTransformer-Pytorch` |
| **GrooVAE** | VAE | Drum pattern generation | Legacy (TF dependency hell) |
| **Magenta.js** | Browser runtime | MusicRNN, MusicVAE in browser | Still functional for demos |

**Python example (MusicVAE - legacy approach):**
```python
# NOTE: Requires TensorFlow 1.x / Python 3.7 environment
from magenta.models.music_vae import configs
from magenta.models.music_vae.trained_model import TrainedModel

config = configs.CONFIG_MAP['cat-mel_2bar_big']
model = TrainedModel(config, batch_size=4,
                     checkpoint_dir_or_path='path/to/checkpoint')
samples = model.sample(n=1, length=80)  # 2 bars
```

### 5.2 OpenAI MuseNet

- GPT-2-like architecture trained on MIDI
- Generates up to 4-minute compositions with 10 instruments
- Predicts next token in MIDI event stream
- **Not open source** (no public weights or code)
- Useful as a reference architecture: GPT-2 + event-based MIDI tokens

### 5.3 Meta MusicGen / AudioCraft

- Generates RAW AUDIO (not MIDI) from text prompts
- Uses EnCodec tokens + Transformer language model
- **Not suitable for MIDI output directly**
- Could be used to generate reference audio for style transfer into MIDI

### 5.4 LakhNES (The Most Relevant Project)

**GitHub**: https://github.com/phaschwazzi/LakhNES

**What**: Transformer-XL trained on 5,278 NES songs (NES-MDB), pre-trained on 170k Lakh MIDI files.

**Key aspects**:
- Uses TX1 (notes/timing) and TX2 (expressive: dynamics + timbre) event representations
- 4-channel output (P1, P2, TR, NO)
- Pre-trained PyTorch checkpoints available (~147 MB each)
- Paper: ISMIR 2019

**Architecture insight for your own build**:
```
Lakh MIDI Dataset (170k songs)
        |
    Pre-training (Transformer-XL)
        |
    Fine-tune on NES-MDB (5,278 songs)
        |
    Generate TX1 events -> Convert to MIDI -> Render to audio (nesmdb)
```

**What's missing**: LakhNES generation quality is basic. It demonstrates the transfer-learning approach works but the results are not production-quality. A modern replacement would use:
- MidiTok (REMI/CP Word) instead of TX1/TX2
- Modern decoder-only transformer (LLaMA-style) instead of Transformer-XL
- Better dataset curation

### 5.5 Other Projects

| Project | Description | Approach |
|---------|-------------|----------|
| **NES-Music-Maker** | LSTM/VAE for NES music | LSTM + VAE, same NES-MDB dataset |
| **chiptune-ai** | GPT-Neo based chiptune | GPT-Neo fine-tuned on MIDI |
| **MMLX** | Python NES programming language | Rule-based, not AI. Generates NSF from Python DSL. |
| **MusPy** | Unified symbolic music toolkit | Dataset management, format conversion, PyTorch/TF datasets |

---

## 6. Building an AI 8-Bit Composer: Architecture

### Recommended Architecture

```
+---------------------------+
|   LLM / Transformer       |  <- Receives text prompt + optional MIDI seed
|   (e.g., fine-tuned       |
|    CodeLLaMA or GPT-2)    |
+-------------+-------------+
              |
              | Generates structured output
              v
+---------------------------+
|   MIDI Generation Layer   |  <- Python code that converts AI output to MIDI
|   (mido / music21)        |
+-------------+-------------+
              |
              | 4 tracks: P1, P2, TR, NO
              v
+---------------------------+
|   Chiptune MIDI File      |  <- Standard MIDI with NES channel conventions
+-------------+-------------+
              |
              v
+---------------------------+
|   Audio Rendering         |  <- FluidSynth + custom .sf2, or chippy
|   FluidSynth / chippy     |
+---------------------------+
```

### Option A: LLM Outputs Structured Note Data

The LLM generates structured text (JSON or tabular) that a Python script converts to MIDI:

```
Prompt: "Generate an 8-bit boss battle theme in C minor"

LLM Output:
{
  "bpm": 160,
  "time_signature": "4/4",
  "key": "C minor",
  "tracks": {
    "P1": {  // Pulse 1 - Lead melody
      "duty": "12.5%",
      "pattern": [
        {"note": 60, "duration": 0.25, "rest": 0},
        {"note": 63, "duration": 0.25, "rest": 0},
        ...
      ]
    },
    "P2": {  // Pulse 2 - Harmony/arpeggio
      "duty": "50%",
      "pattern": [
        {"notes": [60, 63, 67], "type": "arpeggio", "duration": 2.0}
      ]
    },
    "TR": {  // Triangle - Bass
      "pattern": [
        {"note": 48, "duration": 1.0}
      ]
    },
    "NO": {  // Noise - Percussion
      "pattern": [
        {"type": "kick", "position": 0},
        {"type": "snare", "position": 2},
        {"type": "hihat", "position": [0, 1, 2, 3]}
      ]
    }
  }
}
```

Then `json_to_midi.py` converts this JSON to a proper `.mid` file using `mido`.

### Option B: LLM Generates Python Code That Creates MIDI

The LLM writes the MIDI-generation code itself, which is then executed:

```
Prompt: "Write a Python script using mido to create a chiptune
         with an ascending bassline on triangle and square lead"

LLM -> generates runnable Python -> execute -> .mid file
```

This is already feasible with current LLMs (GPT-4, Claude, DeepSeek) for simple patterns.

### Option C: Fine-tune a Model on MidiTok Tokens

For a dedicated model (not relying on a general LLM prompt):

```
1. Collect NES MIDI dataset (NES-MDB, or rip your own)
2. Tokenize with MidiTok (REMI or CP Word)
3. Fine-tune a small transformer (e.g., GPT-2 124M) on token sequences
4. At inference:
   a. Seed with a prompt sequence
   b. Generate autoregressively
   c. Detokenize with MidiTok
   d. Convert to MIDI with mido
```

### Dataset Sources

| Dataset | Size | Format | Access |
|---------|------|--------|--------|
| **NES-MDB** | 5,278 songs, 397 games | MIDI (4 tracks P1/P2/TR/NO) + TX1/TX2 | `pip install nesmdb` |
| **Lakh MIDI** | ~170k songs | MIDI | https://colinraffel.com/projects/lmd/ |
| **MAESTRO** | 1,276 hours of piano | MIDI + aligned audio | Google Magenta |
| **VGMusic** | Thousands of game MIDIs | MIDI | https://www.vgmusic.com/ |

### Practical Roadmap

```
Phase 1: MIDI Generation Toolkit (weeks 1-2)
  - Set up mido pipeline for 4-track NES MIDI creation
  - Implement arpeggio, drum pattern, and bass generators
  - Build JSON-to-MIDI converter for LLM output
  - Verify output with FluidSynth + chiptune SoundFont

Phase 2: LLM Prompting (weeks 3-4)
  - Craft system prompts for chiptune generation
  - Test current LLMs (Claude, GPT-4) on structured note output
  - Build a few-shot example library
  - Iterate on prompt engineering

Phase 3: Fine-tuned Model (months 2-3+)
  - Curate NES-MDB dataset
  - Tokenize with MidiTok
  - Fine-tune small transformer (GPT-2 124M or similar)
  - Compare: general LLM prompting vs. fine-tuned model
```

### Quick-Start Template

```python
#!/usr/bin/env python3
"""
Minimal AI chiptune composer.
Accepts structured note data from an LLM and produces a MIDI file.
"""

import json
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

def llm_to_midi(composition: dict, output_path: str):
    """Convert LLM-generated composition dict to MIDI file."""
    mid = MidiFile(type=1)
    mid.ticks_per_beat = 480
    tempo = bpm2tempo(composition.get('bpm', 140))

    track_templates = {
        'P1': 80,   # Synth Lead (square)
        'P2': 81,   # Synth Lead (square 2)
        'TR': 96,   # FX 1 (triangle bass)
        'NO': 124,  # Telephone (noise drums)
    }

    for track_name, program in track_templates.items():
        track = MidiTrack()
        mid.tracks.append(track)
        track.append(MetaMessage('track_name', name=track_name))
        track.append(MetaMessage('set_tempo', tempo=tempo))
        track.append(Message('program_change', program=program, time=0))

        pattern = composition.get('tracks', {}).get(track_name, {}).get('pattern', [])
        for event in pattern:
            note = event.get('note', 60)
            dur = event.get('duration', 0.5)
            vel = event.get('velocity', 80)
            ticks = int(mid.ticks_per_beat * dur)

            track.append(Message('note_on', note=note, velocity=vel, time=0))
            track.append(Message('note_off', note=note, velocity=64, time=ticks))

    mid.save(output_path)
    print(f"Saved: {output_path}")
    return output_path

# Example input (what an LLM would generate)
example = {
    "bpm": 150,
    "tracks": {
        "P1": {"pattern": [
            {"note": 72, "duration": 0.25, "velocity": 100},
            {"note": 71, "duration": 0.25},
            {"note": 69, "duration": 0.5},
            {"note": 67, "duration": 0.5},
            {"note": 72, "duration": 1.0},
        ]},
        "TR": {"pattern": [
            {"note": 36, "duration": 2.0},
            {"note": 43, "duration": 2.0},
        ]},
    }
}

if __name__ == '__main__':
    llm_to_midi(example, 'ai_chiptune.mid')
```

---

## References

- MidiTok: https://github.com/Natooz/MidiTok
- mido: https://github.com/mido/mido
- music21: https://github.com/cuthbertLab/music21
- MusPy: https://github.com/salu133445/muspy
- NES-MDB / nesmdb: https://github.com/chrisdonahue/nesmdb
- LakhNES: https://github.com/phaschwazzi/LakhNES
- FamiStudio: https://famistudio.org/
- MMLX: https://github.com/ccampbell/mmlx
- chippy: https://github.com/benmoran56/chippy
- isobar: https://github.com/ideoforms/isobar
- Pop Music Transformer (REMI): https://arxiv.org/abs/2002.00212
- Compound Word Transformer: https://arxiv.org/abs/2101.02402
- Magenta: https://magenta.tensorflow.org/
- PyMusicLooper: https://github.com/arkrow/PyMusicLooper
