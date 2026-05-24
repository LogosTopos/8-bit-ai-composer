# LLM Music Composition Guide: 8-Bit / Chiptune Focus

> **Target audience:** AI engineer building an LLM-powered 8-bit music composer.
> Last updated: 2026-05-24

---

## Table of Contents

1. [Overview of Approaches](#1-overview-of-approaches)
2. [Music Representations for LLMs](#2-music-representations-for-llms)
3. [Prompt Engineering for Music Generation](#3-prompt-engineering-for-music-generation)
4. [Fine-Tuning LLMs on Music Data](#4-fine-tuning-llms-on-music-data)
5. [Key GitHub Projects & Repos](#5-key-github-projects--repos)
6. [Tokenization Strategies](#6-tokenization-strategies)
7. [Multi-Track & Constraint-Based Generation](#7-multi-track--constraint-based-generation)
8. [The 8-Bit / Chiptune Pipeline](#8-the-8-bit--chiptune-pipeline)
9. [Audio Generation Models (MusicGen, AudioCraft, etc.)](#9-audio-generation-models)
10. [Real-World Examples & Demos](#10-real-world-examples--demos)
11. [Best Practices & Prompt Templates](#11-best-practices--prompt-templates)
12. [Tooling & Libraries Reference](#12-tooling--libraries-reference)
13. [References & Further Reading](#13-references--further-reading)

---

## 1. Overview of Approaches

There are three broad strategies for using LLMs in music composition:

### A. Prompt-Based Generation (Zero-Shot / Few-Shot)
Use a general-purpose LLM (ChatGPT, Claude, Gemini) to generate music directly through prompt engineering. The LLM outputs symbolic music notation (ABC notation, JSON with MIDI pitches, or chord sequences) which is then converted to audio.

**Pros:** No training required, works with existing APIs, fast iteration.
**Cons:** Limited control, output quality varies, struggles with long-form structure, no guarantee of musical coherence.

### B. Fine-Tuned LLMs
Take an open-source LLM (LLaMA, Mistral, GPT-2) and continue pre-training/fine-tuning on music data (ABC notation, MIDI tokens). This produces a model that natively "understands" music.

**Pros:** Deep musical understanding, can generate complete compositions, controllable via conditioning.
**Cons:** Requires compute (GPUs), needs curated datasets, risk of overfitting to specific genres.

### C. Hybrid Systems (LLM + Constraint Solver + Audio Model)
Use an LLM as a high-level orchestrator that generates structural plans, then feed those plans to specialized music generation models (MusicGen, MuseNet) or constraint solvers.

**Pros:** Best of both worlds -- LLM handles structure/creativity, constraints ensure musicality.
**Cons:** Complex architecture, multiple points of failure, latency.

---

## 2. Music Representations for LLMs

Choosing the right representation is critical. LLMs are text models, so the music representation must be text-compatible.

### 2.1 ABC Notation (Recommended for LLMs)

ABC notation is a text-based music notation language. It is the **most LLM-friendly** format because:
- It is purely ASCII text that tokenizes naturally with standard tokenizers
- It is compact -- a full composition fits in 512-2048 tokens
- It is well-established in the folk music community with abundant training data
- Multiple conversion tools exist (abc2midi, abc2wav, music21)

**Basic ABC format:**
```
X:1                    % Reference number
T:Example Tune         % Title
M:4/4                  % Meter (time signature)
L:1/8                  % Default note length
K:C                    % Key signature
| C D E F | G A B c |  % Notes (lowercase = octave up)
```

**Headers reference:**
| Header | Meaning | Example |
|--------|---------|---------|
| `X:` | Reference number | `X:1` |
| `T:` | Title | `T:My Song` |
| `M:` | Meter | `M:4/4`, `M:3/4`, `M:6/8` |
| `L:` | Default note length | `L:1/8`, `L:1/4` |
| `K:` | Key signature | `K:C`, `K:Am`, `K:Dmaj` |
| `Q:` | Tempo | `Q:1/4=120` |
| `%%MIDI program` | Instrument | `%%MIDI program 1` |

**Multi-voice ABC:**
```
X:1
M:4/4
L:1/8
K:C
%%score P1 P2
V:P1 name="Melody"
| C E G c | c B A G |
V:P2 name="Bass"
| C,2 C,2 | F,2 F,2 |
```

### 2.2 MIDI Event Tokens (for Training)

MIDI events can be serialized as token sequences. This is the standard approach for training custom music transformers (e.g., Music Transformer, MuseNet).

**Common MIDI token types:**
- `NOTE_ON` -- pitch + velocity
- `NOTE_OFF` -- pitch (+ velocity)
- `TIME_SHIFT` -- advance time by X ticks
- `VELOCITY` -- set velocity
- `PROGRAM` -- change instrument

**REMI (Revamped MIDI) encoding adds musical structure:**
- `Bar` -- bar boundary
- `Position` -- position within a bar (in beats/16ths)
- `Pitch` -- MIDI note number (0-127)
- `Velocity` -- velocity class (0-127, usually quantized to 16 or 32 bins)
- `Duration` -- note duration in time units
- `Chord` -- chord label (optional)
- `Tempo` -- tempo change (optional)
- `Program` -- instrument program (optional)

### 2.3 YNote / HNote (Compact Tokenization)

YNote (2025) uses only **4 characters per note**: pitch class + octave + accidental + duration, arranged in 32-unit measure frames.

Example: `C4Q` = middle C, quarter note; `D#5E` = D#5, eighth note.

HNote extends this with hexadecimal encoding for transformer efficiency.

### 2.4 JSON with MIDI Pitches

Simple structured format suitable for zero-shot LLM prompts:
```json
{
  "tempo": 120,
  "time_signature": [4, 4],
  "key": "C",
  "tracks": [
    {
      "instrument": "piano",
      "notes": [
        {"pitch": 60, "start": 0.0, "duration": 0.5, "velocity": 100},
        {"pitch": 64, "start": 0.5, "duration": 0.5, "velocity": 100}
      ]
    }
  ]
}
```

### Comparison of Representations

| Format | LLM-Friendly | Compact | Multi-Track | Convertible | Best For |
|--------|-------------|---------|-------------|-------------|----------|
| **ABC Notation** | Excellent | Good | Good | Excellent | Zero-shot & fine-tuning |
| **MIDI Tokens (REMI)** | Poor (needs custom tokenizer) | Good | Excellent | Native | Training custom models |
| **YNote/HNote** | Good (text chars) | Excellent | Limited | Good | Fine-tuning small LLMs |
| **JSON Pitches** | Good | Poor | Good | Good | Zero-shot API calls |
| **MusicXML** | Poor (verbose) | Poor | Excellent | Excellent | Interchange format |

---

## 3. Prompt Engineering for Music Generation

### 3.1 Core Principles

1. **Specify the output format explicitly.** LLMs will default to poor formats if not told what to use.
2. **Provide few-shot examples.** Show 1-3 bars of correct ABC notation before asking for generation.
3. **Use chain-of-thought for structure.** Ask the LLM to plan (structure, key, chord progression) before writing notes.
4. **Constraint injection.** State explicit constraints: note range, max polyphony, rhythmic density.
5. **Iterative refinement.** Generate, validate, feed errors back, regenerate.

### 3.2 ABC Notation Prompt Template

```
You are a music composition AI. Always respond with valid ABC notation.

Generate an 8-bit style melody in the style of a video game overworld theme.

Requirements:
- Key: C major
- Time signature: 4/4
- Tempo: 120 BPM
- Instrument: Square wave (MIDI program 80)
- Length: 8 bars
- Note range: C4 to C6 (MIDI 60-84)
- Single track melody only
- Use 8th and 16th notes for an energetic feel

Use this exact format:
X:1
T:8-Bit Overworld Theme
M:4/4
L:1/8
Q:1/4=120
K:C
%%MIDI program 80
[NOTES HERE]
```

### 3.3 Multi-Instrument Prompt Template

```
Generate a complete NES-style chiptune track with 4 voices:

**Voice 1: Pulse 1 (Lead Melody)**
- MIDI program: 80 (square wave)
- Range: C4-C6
- Primary melody, 8th/16th notes

**Voice 2: Pulse 2 (Harmony/Arpeggio)**
- MIDI program: 80 (square wave)  
- Range: C3-C5
- Chord arpeggios, sustained notes

**Voice 3: Triangle (Bass)**
- MIDI program: 81 (triangle wave)
- Range: C2-C4
- Root notes on beat 1 and 3

**Voice 4: Noise (Percussion)**
- MIDI program: 82 (noise)
- 16 noise patterns for hi-hat/snare feel

Key: C minor
Tempo: 140
Structure: 16 bars total
- Bars 1-4: Intro (melody + bass only)
- Bars 5-8: Verse (add harmony)
- Bars 9-12: Chorus (full, more energetic)
- Bars 13-16: Outro (fade, return to intro theme)

Use %%score and V: markers for multi-voice ABC notation.
```

### 3.4 JSON Pitch Output Prompt Template

```
Output a 4-bar melody as a JSON array of notes.

Format:
{
  "tempo": 120,
  "time_signature": [4, 4],
  "notes": [
    {"pitch": <MIDI note 0-127>, "start": <beat position float>, "duration": <beats float>, "velocity": <1-127>}
  ]
}

Constraints:
- Key: C major (use notes C4-B4, MIDI 60-71)
- 4/4 time, 4 bars total
- Beat 0 = first beat of bar 1
- 16 notes total, feel free to use rests
- Vary durations between 0.25 and 1.0 beats
- End on the tonic (C4, MIDI 60)

Example:
{"tempo": 120, "time_signature": [4, 4], "notes": [
  {"pitch": 60, "start": 0.0, "duration": 0.5, "velocity": 100},
  {"pitch": 62, "start": 0.5, "duration": 0.5, "velocity": 90}
]}

Now generate:
```

### 3.5 Chord Progression -> Full Arrangement

```
Generate a chord progression and then a full arrangement.

Step 1 (Plan): Suggest a chord progression for a C major pop/rock song.
Step 2 (Arrange): Using this progression, write a multi-instrument ABC notation score for:
- Piano (chords, MIDI program 1)
- Bass (root notes, MIDI program 34)
- Lead synth (melody, MIDI program 80)
- Drums (basic beat, MIDI program 118)

Key: C major, 4/4, 120 BPM, 8 bars.
```

### 3.6 Style Conditioning via Prompts

Use descriptive text to control style:

```
Compose an 8-bit chiptune in the style of:
- Komiku (French chiptune artist)
- Influences: classic NES RPG overworld themes
- Energy: upbeat, adventurous
- Texture: arpeggiated chords, steady bass, syncopated lead

Key structural elements:
- Call-and-response between lead and harmony
- Key change from C to G at bar 9
- Percussion uses noise channel for snare on beats 2 and 4
```

### 3.7 LLM Comparison for Music Tasks

From practical experiments (2025):

| Model | Best At | Weakness |
|-------|---------|----------|
| **ChatGPT (GPT-4)** | Technically correct output, clean JSON, good pitch range | Rhythmically rigid (all quarter notes), lacks groove |
| **Claude (Sonnet 3.7)** | Best phrasing, natural velocity shaping, syncopation | Melodic range can be narrow, JSON inline comments break parsers |
| **Gemini** | Best structural architecture, clear cadence points | Emotionally flat, barline overflow bugs |
| **Grok** | Most commercially viable, best energy arc, clear verse/chorus | Minor barline overflow issues |

---

## 4. Fine-Tuning LLMs on Music Data

### 4.1 ChatMusician (The Gold Standard Reference)

**Paper:** *ChatMusician: Understanding and Generating Music Intrinsically with LLM* (ACL 2024)
**Base model:** LLaMA2-7B
**Representation:** ABC notation as a "second language"

**Training pipeline:**
1. **Continual pre-training** on MusicPile (4B tokens of ABC notation + music-text pairs)
   - 1 epoch, 16x80GB A800 GPUs
2. **Supervised fine-tuning** on 1.1M instruction samples
   - 2:1 ratio of music knowledge + summaries to music scores
   - 2 epochs, 8x32GB V100 GPUs
3. **LoRA configuration:** dim=64, alpha=16, dropout=0.1, applied to attention & MLP

**Capabilities after fine-tuning:**
- Text-to-music composition
- Melody harmonization (add chords to a melody)
- Chord-conditioned generation
- Musical form generation (ternary, verse/chorus/bridge)
- Motif development
- Music understanding and analysis

**Limitations noted:**
- Biased toward Irish/folk music style (training data distribution)
- Supports strict format instructions better than open-ended ones
- Can hallucinate -- not suitable for music education use
- Weak in-context learning and chain-of-thought abilities

### 4.2 Data Preparation for Fine-Tuning

**ABC notation training data format (ChatMusician style):**
```
{
  "instruction": "Compose a piece in C major, 4/4 time.",
  "input": "",
  "output": "X:1\nM:4/4\nL:1/8\nK:C\n| C E G c | c B A G |\n..."
}
```

**Multi-task training mixture:**
```
Human: Compose a melody using the chords C, F, G, Am.
Assistant: X:1\nM:4/4\nL:1/8\nK:C\n| \"C\" C E G c | \"F\" F A c' f' | \"G\" G B d g | \"Am\" A c e a |

Human: Harmonize this melody: | C D E F | G A B c |
Assistant: X:1\nM:4/4\nL:1/8\nK:C\n%%score V0 V1\nV:V0\n| C D E F | G A B c |\nV:V1\n| C E G A | G B d e |
```

### 4.3 Fine-Tuning Recipe (LoRA)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model

model_name = "meta-llama/Llama-2-7b-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)

lora_config = LoraConfig(
    r=64,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)

model = AutoModelForCausalLM.from_pretrained(model_name)
model = get_peft_model(model, lora_config)

training_args = TrainingArguments(
    output_dir="./music-llm",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=8,
    learning_rate=1e-4,
    num_train_epochs=2,
    logging_steps=10,
    save_steps=500,
    fp16=True,
    max_seq_length=2048,
)
```

### 4.4 Available Open-Source Music Models

| Model | Base | Size | Format | Training Data | Availability |
|-------|------|------|--------|---------------|-------------|
| **ChatMusician** | LLaMA2 | 7B | ABC | MusicPile (4B tokens) | HuggingFace: `m-a-p/ChatMusician` |
| **ChatMusician-Base** | LLaMA2 | 7B | ABC | MusicPile (pre-train only) | HuggingFace: `m-a-p/ChatMusician-Base` |
| **MuPT** | Custom | Various | ABC (SMT-ABC) | Large symbolic corpus | HuggingFace |
| **NotaGen** | Custom | Various | ABC | Classical music corpus | Weights available |
| **GPT-2 (fine-tuned)** | GPT-2 | 124M | ABC/YNote | Custom | Self-trainable |
| **MuseNet** | GPT-3 | Custom | MIDI | Proprietary | Not open (OpenAI) |
| **MusicGen** | T5-based | 300M-3.3B | Audio tokens | 20K hrs licensed | MIT code, CC-NC weights |

---

## 5. Key GitHub Projects & Repos

### 5.1 Chiptune-Specific Projects

| Project | Description | Tech | Stars | Link |
|---------|-------------|------|-------|------|
| **LakhNES** | Transformer-XL for 8-bit chiptune generation. Pre-trained on Lakh MIDI, fine-tuned on NES-MDB | PyTorch, Transformer-XL | ~353 | [github.com/chrisdonahue/LakhNES](https://github.com/chrisdonahue/LakhNES) |
| **nesmdb** | NES Music Database - 5,278 songs from 397 NES games, 2M+ notes | MIDI dataset | ~495 | [github.com/chrisdonahue/nesmdb](https://github.com/chrisdonahue/nesmdb) |
| **chiptune-ai** | GPT-based chiptune via ABC notation. Uses aitextgen (GPT-2) | GPT, Flask, Docker | - | [github.com/pickles976/chiptune-ai](https://github.com/pickles976/chiptune-ai) |
| **8bit-VAE** | MusicVAE for NES-MDB in PyTorch | PyTorch, VAE | ~22 | [github.com/xgarcia238/8bit-VAE](https://github.com/xgarcia238/8bit-VAE) |
| **NES-Music-Maker** | LSTM + VAE for NES music generation | PyTorch | Active | [github.com/youngmg1995/NES-Music-Maker](https://github.com/youngmg1995/NES-Music-Maker) |

### 5.2 General AI Music Projects

| Project | Description | Tech | Link |
|---------|-------------|------|------|
| **ChatMusician** | LLaMA2 fine-tuned on ABC notation | LLaMA2, HuggingFace | [github.com/hf-lin/ChatMusician](https://github.com/hf-lin/ChatMusician) |
| **AudioCraft (MusicGen)** | Meta's text-to-music generation | PyTorch, EnCodec | [github.com/facebookresearch/audiocraft](https://github.com/facebookresearch/audiocraft) |
| **MidiTok** | MIDI tokenization library (REMI, etc.) | Python, HuggingFace | [github.com/Natooz/MidiTok](https://github.com/Natooz/MidiTok) |
| **REMI-z** | Track-aware REMI tokenizer | Python | [github.com/Sonata165/REMI-z](https://github.com/Sonata165/REMI-z) |
| **mediocre** | LLM-generated ABC music for synthetic datasets | Node.js, Claude API | [github.com/agrathwohl/mediocre](https://github.com/agrathwohl/mediocre) |
| **JAMMIN-GPT** | Text-based MIDI in Ableton Live | ChatGPT, ABC, MIDI | Paper only |
| **survey-music-nlp** | Survey of NLP methods for symbolic music | Reference | [github.com/dinhviettoanle/survey-music-nlp](https://github.com/dinhviettoanle/survey-music-nlp) |

### 5.3 Datasets

| Dataset | Size | Format | Content | Link |
|---------|------|--------|---------|------|
| **NES-MDB** | 5,278 songs | MIDI | NES game music, 4-voice ensemble | [github.com/chrisdonahue/nesmdb](https://github.com/chrisdonahue/nesmdb) |
| **Lakh MIDI** | 175K songs | MIDI | Multi-genre MIDI, 9K+ hours | [colinraffel.com/projects/lmd](https://colinraffel.com/projects/lmd/) |
| **MusicPile** | 4B tokens | ABC + text | ABC notation + music knowledge | HuggingFace: `m-a-p/MusicPile` |
| **MusicTheoryBench** | ~1,200 questions | ABC + text | College-level music theory | HuggingFace: `m-a-p/MusicTheoryBench` |

---

## 6. Tokenization Strategies

### 6.1 Overview of Approaches

| Tokenization | Vocabulary Size | Musical Structure | Complexity |
|-------------|----------------|-------------------|------------|
| **MIDI-like** | ~388 tokens | No bar/beat awareness | Simple |
| **REMI** | ~332 tokens | Bar, position, chord, tempo | Moderate |
| **Octuple/MusicBERT** | ~10K+ composite tokens | Full structural embedding | High |
| **ABC (character)** | ~95 chars | Inherits ABC structure | Simple |
| **ABC (BPE)** | ~50K tokens | Inherits ABC structure | Moderate |
| **Bar-stream patching** | N/A (fixed patches) | Bar-aligned patches | Moderate |

### 6.2 REMI Tokenization Example (MidiTok)

```python
from miditok import REMI, TokenizerConfig
from symusic import Score

# Configure tokenizer
config = TokenizerConfig(
    num_velocities=16,       # Quantize velocity to 16 bins
    use_chords=True,         # Include chord tokens
    use_programs=True,       # Include instrument program tokens
    use_tempos=True,         # Include tempo tokens
    use_time_signatures=True,# Include time signature tokens
    use_rests=True,          # Include rest tokens
)

tokenizer = REMI(config)

# MIDI -> tokens
midi = Score("song.mid")
tokens = tokenizer(midi)  # List[List[int]] (batched sequences)

# Tokens -> MIDI
reconstructed = tokenizer(tokens)
```

**REMI token sequence example:**
```
[Bar] [Position=0] [Pitch=60] [Velocity=80] [Duration=0.25] [Position=4] [Pitch=64] ...
```

### 6.3 ABC Character Tokenization

ABC notation tokenizes naturally with standard LLM tokenizers:

```
Raw ABC:   | C4 D4 E4 F4 | G4 A4 B4 C5 |
Tokens:    [124, 67, 52, 32, 68, 52, ...]  (GPT-2 tokenizer)
```

Most LLM tokenizers handle ABC well because it uses standard ASCII characters, numbers, and bar lines -- all common in text.

### 6.4 Comparison: REMI vs. ABC for Training

| Factor | REMI Tokens | ABC Notation |
|--------|-------------|--------------|
| Tokenizer complexity | Custom (MidiTok) | Built into LLM tokenizer |
| Sequence length (4 bars) | ~200 tokens | ~80 characters |
| Musical structure awareness | Explicit (Bar, Position) | Implicit (bar lines `|`) |
| Human readability | Poor | Good |
| Multi-track handling | Per-track concatenation | `%%score` + `V:` markers |
| Best for | Training from scratch | Fine-tuning existing LLMs |

---

## 7. Multi-Track & Constraint-Based Generation

### 7.1 Approaches to Multi-Track

**A. Per-Track Concatenation (MIDI-GPT approach)**
Each track is an independent sequence; tracks are concatenated with separator tokens.

```
[Track=0] NOTE_ON(60) TIME_SHIFT(120) NOTE_OFF(60) [SEP]
[Track=1] NOTE_ON(36) TIME_SHIFT(240) NOTE_OFF(36) [SEP]
[Track=2] DRUM(hi-hat) TIME_SHIFT(60) DRUM(snare) ...
```

**B. Interleaved Multi-Track (MuPT SMT-ABC)**
Voices are interleaved per bar to maintain alignment, using `%%score` and `V:` markers in ABC.

```
%%score P1 P2
V:P1 | C E G c |
V:P2 | C,2 C,2 |
```

**C. Hierarchical (TOMI approach)**
A 4D representation: clips -> transformations -> sections -> tracks. An LLM (GPT-4o) fills in a structured composition graph using in-context learning.

### 7.2 Constraint-Based Generation

**Finite State Machines (SymPAC, ISMIR 2024)**

SymPAC uses FSMs during autoregressive inference to constrain which tokens can be sampled next. Two constraint types:

1. **Grammar constraints** -- enforce valid encoding format (e.g., bar token must be followed by a genre token)
2. **User input constraints** -- enforce user specifications (e.g., only allow "rock" genre tokens)

```python
# Simplified FSM constraint example
def get_allowed_tokens(current_token, state, grammar_rules, user_constraints):
    """Return subset of vocabulary that is valid given current state."""
    allowed = set(range(vocab_size))

    # Grammar rules
    if current_token == BAR_TOKEN:
        allowed &= GENRE_TOKENS | TEMPO_TOKENS

    # User constraints
    if user_constraints.get("genre") == "rock":
        allowed &= ROCK_GENRE_TOKENS

    return allowed
```

**NeuralConstraints (2025)**

Combines a feedforward neural network with a backtracking constraint solver (Cluster-Engine). The NN provides heuristic predictions (weighted by mean absolute error), while the solver enforces:
- Allowed intervals (e.g., no tritones)
- Pitch ranges per voice
- Chord constraints (e.g., no parallel fifths)
- Repetition patterns

**MIDI-GPT conditioning attributes:**
- Instrument type
- Musical style
- Note density (notes per bar)
- Polyphony level
- Note duration range

### 7.3 Music Theory Rule Enforcement

Common theory rules that can be programmatically enforced:

| Rule | Description | Implementation |
|------|-------------|----------------|
| **Voice range** | Each voice stays within valid range | Post-generation filter |
| **No parallel fifths** | Consecutive perfect fifths between voices | Constraint solver |
| **Chord tones on strong beats** | Beat 1 should be chord root or third | Post-generation correction |
| **Cadence structure** | End phrases with V-I or IV-V-I | Structural template |
| **Stepwise motion** | Prefer stepwise motion in melodies | Heuristic scoring |
| **Note density limits** | Max N notes per bar per voice | FSM constraint |

---

## 8. The 8-Bit / Chiptune Pipeline

### 8.1 NES Sound Architecture

The NES audio processing unit (APU) has 4 voices:

| Channel | Waveform | Usage | Pitch Range |
|---------|----------|-------|-------------|
| **Pulse 1** | Square (12.5%/25%/50%/75% duty) | Lead melody | 33-108 (MIDI) |
| **Pulse 2** | Square (variable duty) | Harmony, arpeggios | 33-108 |
| **Triangle** | Triangle wave | Bass line | 21-108 |
| **Noise** | Pseudo-random | Percussion | 16 noise types |

### 8.2 End-to-End Pipeline Architecture

```
                    +-------------------+
                    |   User Prompt     |
                    |  (style, tempo,   |
                    |   key, length)    |
                    +--------+----------+
                             |
                             v
                    +-------------------+
                    |    LLM (Prompt    |
                    |    or Fine-Tuned) |
                    +--------+----------+
                             |
                     ABC Notation
                             |
                             v
                    +-------------------+
                    |    Validation     |
                    |  (abc2midi test,  |
                    |   music21 parse)  |
                    +--------+----------+
                             |
                    (fix errors, retry if needed)
                             |
                             v
                    +-------------------+
                    |   MIDI Conversion |
                    |  (abc2midi or     |
                    |   music21)        |
                    +--------+----------+
                             |
                             v
                    +-------------------+
                    |   Chiptune Synth  |
                    |  (NES VST, fami-  |
                    |   tracker, etc.)  |
                    +--------+----------+
                             |
                             v
                    +-------------------+
                    |   Audio Output    |
                    |  (WAV/MP3/OGG)    |
                    +-------------------+
```

### 8.3 Python Pipeline Implementation

```python
"""
End-to-end pipeline: LLM -> ABC -> MIDI -> 8-bit audio
"""

import subprocess
import music21
from pathlib import Path

# === Step 1: Get ABC from LLM ===
def generate_abc_from_llm(prompt: str, model="gpt-4") -> str:
    """Send prompt to LLM and get back ABC notation."""
    # This is a placeholder -- use your LLM API of choice
    # For OpenAI:
    # response = openai.chat.completions.create(
    #     model=model,
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # return response.choices[0].message.content
    pass

# === Step 2: Validate ABC ===
def validate_abc(abc_text: str) -> bool:
    """Try to parse with music21, return True if valid."""
    try:
        score = music21.converter.parse(abc_text, format="abc")
        return True
    except Exception as e:
        print(f"ABC validation error: {e}")
        return False

# === Step 3: ABC to MIDI ===
def abc_to_midi(abc_text: str, output_path: str):
    """Convert ABC notation to MIDI file."""
    # Write ABC to temp file
    abc_path = Path(output_path).with_suffix(".abc")
    abc_path.write_text(abc_text)

    # Option A: Use abc2midi
    subprocess.run([
        "abc2midi", str(abc_path), "-o", output_path
    ], check=True)

    # Option B: Use music21
    # score = music21.converter.parse(abc_text, format="abc")
    # score.write("midi", fp=output_path)

# === Step 4: MIDI to 8-bit audio ===
def midi_to_8bit(midi_path: str, output_path: str, soundfont: str = "nes.sf2"):
    """Convert MIDI to 8-bit WAV using FluidSynth with NES soundfont."""
    subprocess.run([
        "fluidsynth", "-ni", soundfont, midi_path, "-F", output_path, "-r", 44100
    ], check=True)

# === Step 5: Full pipeline ===
def compose_8bit(prompt: str, output_dir: str = "./output"):
    """Complete pipeline from prompt to 8-bit audio."""
    Path(output_dir).mkdir(exist_ok=True)

    abc = generate_abc_from_llm(prompt)
    if not validate_abc(abc):
        print("ABC validation failed, attempting fix...")
        # Re-prompt LLM with error
        # ...

    abc_path = Path(output_dir) / "composition.abc"
    abc_path.write_text(abc)

    midi_path = Path(output_dir) / "composition.mid"
    abc_to_midi(str(abc_path), str(midi_path))

    wav_path = Path(output_dir) / "composition_8bit.wav"
    midi_to_8bit(str(midi_path), str(wav_path))

    return {
        "abc": abc_path,
        "midi": midi_path,
        "audio": wav_path,
    }
```

### 8.4 NES SoundFonts for Chiptune Audio

| SoundFont | Description | Link |
|-----------|-------------|------|
| **NES.sf2** | NES APU soundfont | Various |
| **C64.sf2** | Commodore 64 SID soundfont | Various |
| **Famicom.sf2** | Famicom/NES soundfont | Various |
| **chiptune.sf2** | General chiptune instruments | Various |

Alternatively, use dedicated chiptune trackers:
- **Famitracker** (Windows, NES-focused)
- **Deflemask** (Multi-system, cross-platform)
- **LSDJ** (Game Boy, but NES-compatible techniques)

### 8.5 Using the NES-MDB Dataset

```python
# Install: pip install nesmdb
from nesmdb import NESMusicDB

db = NESMusicDB()

# List available songs
songs = db.list_songs()  # Returns list of (game, song_id, title)

# Load a song
song = db.load_song("Zelda II - The Adventure of Link", 0)
midi_data = song.to_midi()  # MIDI file object
abc_data = song.to_abc()    # ABC notation string
```

---

## 9. Audio Generation Models

For engineers who want to skip symbolic music and generate audio directly:

### 9.1 MusicGen (Meta / AudioCraft)

**Architecture:** Single-stage autoregressive Transformer + EnCodec audio tokenizer.
**Sizes:** 300M, 1.5B, 3.3B parameters (musicgen-small/medium/large).
**Input:** Text prompt (e.g., "8-bit chiptune video game music, upbeat, retro").
**Output:** 32kHz stereo audio.

**Key facts:**
- Trained on 20,000 hours of licensed music
- Code is MIT licensed, model weights are CC-BY-NC 4.0 (non-commercial)
- Cannot generate realistic vocals
- Best results with English text prompts

**Usage example:**
```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained("facebook/musicgen-medium")
model.set_generation_params(duration=8)  # 8 seconds

wav = model.generate([
    "8-bit chiptune video game overworld music, retro NES style",
    "dark ambient dungeon music for a RPG game"
])

torchaudio.save("output.wav", wav[0].cpu(), 32000)
```

### 9.2 MAGNeT (Non-Autoregressive)

Masked Audio Generation using a Single Non-Autoregressive Transformer.
- **7x faster** than MusicGen
- Comparable quality
- Supports hybrid AR/non-AR mode
- Available in the same AudioCraft codebase

### 9.3 Comparison: Symbolic (LLM + MIDI) vs. Audio (MusicGen)

| Dimension | Symbolic (ABC/MIDI) | Audio (MusicGen) |
|-----------|--------------------|-------------------|
| **Control** | Note-perfect, editable | Prompt-level only |
| **Length** | Arbitrary (just generate more tokens) | Limited by model context (typically 30s-2min) |
| **Instruments** | Explicit per-track | Learned from data |
| **8-bit feel** | Guaranteed (NES soundfont) | Must be learned from training data |
| **File size** | Small (KB) | Large (MB) |
| **Post-processing** | MIDI editing, human refinement | Limited |
| **Fine-tuning** | Easy (LoRA on LLM) | Requires GPU cluster |
| **Latency** | Fast (seconds) | Slower (minutes for long clips) |

---

## 10. Real-World Examples & Demos

### 10.1 LakhNES Examples

- **Project page with audio:** [chrisdonahue.com/LakhNES/](https://chrisdonahue.com/LakhNES/)
- **Capabilities:** Unconditional generation, continuations, rhythm-conditioned generation
- **Result:** Human judges preferred LakhNES over real NES music ~6% of the time (LSTM got 0%)

### 10.2 JAMMIN-GPT + Ableton Live

Workflow: Name MIDI clips descriptively in Ableton -> ChatGPT generates ABC/chords/drum notation -> converted to MIDI -> played back in Live.

### 10.3 mediocre (Synthetic Dataset Generation)

CLI tool that uses Claude 3.7 Sonnet to generate ABC notation for synthetic music datasets:
```bash
mediocre generate \
  -s "8-bit forest temple theme" \
  -C "koji_kondo,yuzo_koshiro" \
  -M "chipzel,anamanaguchi" \
  --producer "Brian Eno" \
  --record-label "Warp"
```

**Key finding from mediocre project:** Later Claude models (3.5, 4.0, Opus) have regressed in ABC notation capabilities; **Claude 3.7 Sonnet** is recommended.

### 10.4 ChatMusician Demo

Online demo at [shanghaicannon.github.io/ChatMusician/](https://shanghaicannon.github.io/ChatMusician/) with examples of:
- Text-to-music
- Chord-conditioned composition
- Melody harmonization

### 10.5 NotaGen WebUI

Classical music generation with style conditioning (112 composer/period/instrument combinations). Generates ABC -> MusicXML -> audio.

---

## 11. Best Practices & Prompt Templates

### 11.1 Prompt Structure Cheat Sheet

```
[ROLE]         You are a chiptune composer AI.
[FORMAT]       Always respond in ABC notation.
[CONSTRAINTS]  Key: C, Tempo: 120, Length: 8 bars.
[STYLE]        NES overworld theme, upbeat, arpeggiated.
[STRUCTURE]    Intro (2 bars) -> Verse (4 bars) -> Outro (2 bars).
[EXAMPLE]      X:1\nM:4/4\n... (1-2 bar example of correct format).
[OUTPUT]       Generate the full composition.
```

### 11.2 Validation Loop

Always validate LLM output before using it:

```python
import re
import subprocess

def validate_and_fix(abc_text: str, max_retries: int = 3) -> str:
    """Validate ABC output and re-prompt LLM if invalid."""
    for attempt in range(max_retries):
        try:
            # Test with music21
            import music21
            score = music21.converter.parse(abc_text, format="abc")
            return abc_text
        except Exception as e:
            error_msg = str(e)
            print(f"Attempt {attempt + 1} failed: {error_msg}")

            # Common fixes
            if "M:4/4" not in abc_text and "M:" not in abc_text:
                abc_text = "M:4/4\nL:1/8\nK:C\n" + abc_text
            elif "K:" not in abc_text:
                abc_text = abc_text.replace("M:", "K:C\nM:")
            elif "X:" not in abc_text:
                abc_text = "X:1\n" + abc_text

            # If still failing, would re-prompt LLM with error
            break

    raise RuntimeError(f"Failed to validate ABC after {max_retries} attempts")
```

### 11.3 Multi-Voice ABC Format for 4-Voice NES

```
X:1
T:8-Bit Composition
M:4/4
L:1/8
Q:1/4=150
K:C
%%score P1 | P2 | TR | NO
%%MIDI program 80
%%MIDI channel 1
V:P1 name="Pulse1"
| C4 E4 G4 c4 | c4 B4 A4 G4 | F4 E4 D4 C4 | C2 C2 C4 z4 |
V:P2 name="Pulse2"  
| E4 G4 B4 e4 | e4 d4 c4 B4 | A4 G4 F4 E4 | E2 E2 E4 z4 |
V:TR name="Triangle"
| C,2 C,2 G,2 G,2 | A,2 A,2 F,2 F,2 | C,2 C,2 G,2 G,2 | C,4 C,4 |
V:NO name="Noise"
%%MIDI program 82
| z C z C | z C z C | C C C C | z C C z |
```

### 11.4 Genre-Specific Prompting

**8-bit/Chiptune:**
```
Compose an 8-bit chiptune with:
- Fast arpeggiated chords (16th note triplets in Pulse 2)
- Syncopated lead melody (Pulse 1)
- Simple root-note bass on beats 1 and 3 (Triangle)
- Noise channel for hi-hat feel on off-beats
- Frequent key changes every 4 bars
- Call-and-response structure between bars 1-2 and 3-4
```

**Game Music (Overworld):**
```
Compose a video game overworld theme:
- Key: C major (bright, adventurous)
- Tempo: 120 BPM
- 16 bars total
- ABA structure: A is the main theme, B is a bridge with different harmony
- Strong, recognizable melody in the first 4 bars
- Bass follows root-fifth pattern
- Percussion: steady eighth-note hi-hat, snare on 2 and 4
```

**Game Music (Boss Fight):**
```
Compose an intense boss battle theme:
- Key: E minor (dark, aggressive)
- Tempo: 160 BPM
- Aggressive, chromatic melody lines
- Heavy use of percussion
- Syncopated bass
- Sudden stops and tempo changes
- 32 bars with 4 distinct sections
```

### 11.5 Avoiding Common LLM Music Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Barline overflow** | Notes extend beyond bar boundary | Post-process: truncate or shift notes |
| **Missing headers** | No X:, M:, or K: | Prepend default headers |
| **Wrong octave** | Notes outside instrument range | Clamp pitch values (NES: 33-108) |
| **Too many simultaneous notes** | >4 notes at once (NES limit) | Post-process: keep loudest N notes |
| **Invalid ABC syntax** | abc2midi parse error | Validate and re-prompt with error |
| **Repetition** | Same bar repeated 16x | Temperature > 0.7, diversity penalty |
| **Rhythmically flat** | All quarter notes | Prompt for "syncopation", "16th notes" |
| **No clear cadence** | Doesn't end on tonic | Prompt "end on C" or add structural constraint |

### 11.6 Temperature and Sampling Settings

For LLM music generation:
- **Temperature:** 0.7-0.9 (higher = more creative, risk of errors)
- **Top-p:** 0.9
- **Frequency penalty:** 0.1-0.3 (discourages repetition)
- **Presence penalty:** 0.0-0.2

---

## 12. Tooling & Libraries Reference

### Essential Libraries

| Library | Purpose | Install |
|---------|---------|---------|
| **music21** | Music analysis, ABC/MIDI/MusicXML conversion | `pip install music21` |
| **MidiTok** | MIDI tokenization (REMI, MIDI-Like, etc.) | `pip install miditok` |
| **symusic** | Fast MIDI I/O (used by MidiTok) | `pip install symusic` |
| **audiocraft** | MusicGen + AudioGen (Meta) | `pip install audiocraft` |
| **nesmdb** | NES Music Database tools | `pip install nesmdb` |
| **fluidsynth** | MIDI-to-audio with SoundFonts | `apt install fluidsynth` or `pip install pyfluidsynth` |
| **pretty_midi** | MIDI file manipulation | `pip install pretty_midi` |

### Command-Line Tools

| Tool | Purpose | URL |
|------|---------|-----|
| **abc2midi** | ABC -> MIDI conversion | Part of `abcMIDI` package |
| **abc2wav** | ABC -> WAV conversion | Part of `abcMIDI` package |
| **timidity** | MIDI -> WAV with SoundFonts | `apt install timidity` |
| **ffmpeg** | Audio format conversion | `apt install ffmpeg` |

### ABC Notation Resources

- **abcnotation.com** -- Comprehensive ABC reference
- **abc2midi** -- Command-line converter (part of abcMIDI)
- **music21** -- Python library with ABC support (`music21.converter.parse(abc_string, format="abc")`)
- **abc2svg** -- Render ABC as sheet music in browser

---

## 13. References & Further Reading

### Papers

| Title | Year | Venue | Key Insight |
|-------|------|-------|-------------|
| [Text2Score](https://arxiv.org/abs/2605.13431) | 2026 | arXiv | LLM orchestrator + generative model for sheet music |
| [Teaching LLMs Music Theory](https://arxiv.org/abs/2503.22853) | 2025 | arXiv | CoT prompting improves music theory; Claude + MEI best |
| [YNote](https://arxiv.org/abs/2502.10467) | 2025 | arXiv | 4-char per note encoding for fine-tuning |
| [MuPT](https://iclr.cc/virtual/2025/poster/28712) | 2025 | ICLR | SMT-ABC for multi-track alignment, BPE tokenization |
| [ChatMusician](https://arxiv.org/abs/2402.16153) | 2024 | ACL | ABC as second language for LLMs |
| [SymPAC](https://arxiv.org/abs/2409.03055) | 2024 | ISMIR | FSM constraints during generation |
| [MIDI-GPT](https://arxiv.org/abs/2501.17011) | 2025 | AAAI | Controllable multi-track MIDI infilling |
| [TOMI](https://arxiv.org/abs/2506.23094) | 2025 | ISMIR | Concept hierarchy for full-song generation |
| [MuseNet](https://openai.com/index/musenet/) | 2019 | OpenAI Blog | Sparse Transformer for MIDI |
| [MusicGen](https://arxiv.org/abs/2306.05284) | 2023 | arXiv | Single-stage audio token generation |
| [LakhNES](https://arxiv.org/abs/1907.04868) | 2019 | ISMIR | Transfer learning for chiptune |
| [NeuralConstraints](https://doi.org/10.3389/fcomp.2025.1543074) | 2025 | Frontiers | NN + constraint solver hybrid |
| [M6GPT3](https://arxiv.org/abs/2409.12638) | 2024 | arXiv | GPT + genetic algorithm for arrangement |
| [JAMMIN-GPT](https://arxiv.org/abs/2312.03479) | 2023 | arXiv | ChatGPT in Ableton Live workflow |
| [Tokenization Survey](https://arxiv.org/abs/2410.17584) | 2024 | arXiv | Bar-stream patching best for ABC |
| [Structural Embeddings](https://arxiv.org/abs/2407.19900) | 2024 | arXiv | Part/Type/Time/PC embeddings for MIDI |

### Projects

| Name | Type | Link |
|------|------|------|
| LakhNES | Chiptune generation | [github.com/chrisdonahue/LakhNES](https://github.com/chrisdonahue/LakhNES) |
| NES-MDB | Dataset | [github.com/chrisdonahue/nesmdb](https://github.com/chrisdonahue/nesmdb) |
| chiptune-ai | GPT chiptune | [github.com/pickles976/chiptune-ai](https://github.com/pickles976/chiptune-ai) |
| ChatMusician | Music LLM | [github.com/hf-lin/ChatMusician](https://github.com/hf-lin/ChatMusician) |
| AudioCraft | Audio generation | [github.com/facebookresearch/audiocraft](https://github.com/facebookresearch/audiocraft) |
| MidiTok | MIDI tokens | [github.com/Natooz/MidiTok](https://github.com/Natooz/MidiTok) |
| mediocre | Synthetic data | [github.com/agrathwohl/mediocre](https://github.com/agrathwohl/mediocre) |
| survey-music-nlp | Survey | [github.com/dinhviettoanle/survey-music-nlp](https://github.com/dinhviettoanle/survey-music-nlp) |

---

## Quick Start: 8-Bit Composer Workflow

```python
# Minimal example: LLM -> ABC -> MIDI -> 8-bit audio

import subprocess, music21
from pathlib import Path

# 1. Get ABC from an LLM (paste this as a prompt)
prompt = """
Compose an 8-bar NES-style chiptune melody in C major, 4/4 time, 120 BPM.
Output valid ABC notation with X:, M:, L:, Q:, K: headers.
Use MIDI program 80 (square wave).
"""

# 2. Save ABC and convert (assuming you have abc2midi)
abc_text = """
X:1
T:8-Bit Theme
M:4/4
L:1/8
Q:1/4=120
K:C
%%MIDI program 80
| C4 E4 G4 c4 | B4 A4 G4 F4 | E4 F4 G4 A4 | B4 c4 d4 e4 |
| f4 e4 d4 c4 | B4 A4 G4 F4 | E4 D4 C4 z4 | C4 C4 C4 z4 |
"""

abc_path = Path("theme.abc")
abc_path.write_text(abc_text)

# Convert ABC -> MIDI
subprocess.run(["abc2midi", "theme.abc", "-o", "theme.mid"], check=True)

# Convert MIDI -> 8-bit WAV (requires NES soundfont)
subprocess.run([
    "fluidsynth", "-ni", "nes.sf2", "theme.mid",
    "-F", "theme_8bit.wav", "-r", 44100
], check=True)

print("Done! Listen to theme_8bit.wav")
```

> **Next steps for building your own LLM-powered composer:** Start with zero-shot prompting using the templates above, validate with music21/abc2midi, then iterate. If you need deeper quality, fine-tune a LLaMA- or GPT-2-scale model on ABC notation using ChatMusician's recipe. For maximum control, add a constraint layer (FSM or rule-based) between the LLM and the audio renderer.
