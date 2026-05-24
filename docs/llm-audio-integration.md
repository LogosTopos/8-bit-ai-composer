# LLM + Audio Generation Integration: A Landscape Survey (2024-2026)

> Written: 2026-05-24
> Scope: AI audio/music generation, LLM-guided synthesis, spatial audio, browser-based music AI

---

## Table of Contents

1. [How LLMs Integrate with Audio Generation Models](#1-how-llms-integrate-with-audio-generation-models)
2. [Audio Generation Models Survey](#2-audio-generation-models-survey)
3. [Symbolic vs Audio Generation Tradeoffs](#3-symbolic-vs-audio-generation-tradeoffs)
4. [Code and API Availability](#4-code-and-api-availability)
5. [LLM as Music Arranger](#5-llm-as-music-arranger)
6. [Spatial Audio and Game Audio](#6-spatial-audio-and-game-audio)
7. [Web Audio API and Browser-Based Music AI](#7-web-audio-api-and-browser-based-music-ai)
8. [Practical Integration Patterns](#8-practical-integration-patterns)
9. [Model Comparison Matrix](#9-model-comparison-matrix)
10. [References](#10-references)

---

## 1. How LLMs Integrate with Audio Generation Models

### 1.1 The Orchestrator Pattern

The most common pattern for LLM + audio model integration is the **orchestrator pattern**: an LLM serves as a "conductor" that plans musical structure, generates parameters, and then delegates rendering to a specialized audio model.

```
User Prompt
    |
    v
+-----------------+
|   LLM           |  <-- Planning: structure, lyrics, arrangement
|  (GPT-4 /       |
|   Claude /      |
|   local model)  |
+-----------------+
    |
    | Structured output (JSON, ABC notation, token sequences)
    v
+-----------------+
|   Audio Model   |  <-- Rendering: MusicGen, AudioLDM, Stable Audio
|  (diffusion /   |
|   autoregressive)|
+-----------------+
    |
    v
  Audio file
```

### 1.2 Deep Fusion: LLM as Central Backbone

**MuMu-LLaMA** (2025) is the first system to unify music comprehension + generation in a single LLM backend. Architecture:

- **LLaMA** acts as central reasoning backbone
- Multi-modal adapters fuse vision (ViT, ViViT) and audio (MERT) features into LLM layers
- Generation requests routed to **MusicGen** (autoregressive) or **AudioLDM 2** (diffusion-based)
- Deep fusion (injecting modality tokens into last few LLM layers) outperforms shallow concatenation

Key insight: The deep fusion approach yields better cross-modal reasoning than routing raw embeddings through a single projection layer.

### 1.3 LLM-as-Judge for Audio Evaluation

Recent competitions (ICME 2026 ATTM Grand Challenge) use LLM-as-judge evaluation alongside human MOS:
- LLM evaluates audio quality against prompt adherence
- Provides automated scoring at scale
- Combined with human raters for calibration

### 1.4 Prompt Chaining: Plan-Then-Render

The most practical pattern for production systems:

```
Step 1: LLM generates structure
   "Create a 4-minute chiptune in A minor, 120 BPM.
    Structure: Intro(8 bars) -> Verse(16) -> Chorus(16) -> Verse(16) -> Chorus(16) -> Bridge(8) -> Chorus(16) -> Outro(8)"

Step 2: LLM generates per-section descriptions
   "Intro: Arpeggiated pulse wave chords, no percussion
    Verse: Pulse wave melody + square wave harmony, simple kick/snare
    Chorus: Full texture, lead saw wave, hi-hat + crash cymbal"

Step 3: Audio model renders each section
   -> Audio segment 1 (intro.wav)
   -> Audio segment 2 (verse.wav)
   -> Audio segment 3 (chorus.wav)

Step 4: LLM reviews and suggests revisions
   "The chorus needs more energy. Increase the tempo to 128 BPM and add a sub-bass layer."
```

**SegTune** (2025) and **ACE-Step** (2025) both implement variants of this pattern, using LLM-generated segment-level descriptions to control musical form.

### 1.5 Two-Stage Token Pipelines

**YuE** (HKUST, 2025) uses a two-stage pipeline:
- **Stage 1**: 7B LLM generates audio tokens using Chain-of-Thought or In-Context Learning
- **Stage 2**: 1B model refines tokens
- Output structured via JSON-like token management (SOA/EOA markers, stage markers, separator tokens)
- Includes xcodec decoding, Vocos upsampling, multi-track processing

**InspireMusic** (Alibaba, 2025): Unified framework using autoregressive transformer -> flow matching -> vocoder pipeline.

---

## 2. Audio Generation Models Survey

### 2.1 MusicGen / MAGNeT (Meta)

| Attribute | Detail |
|-----------|--------|
| **Developer** | Meta / Facebook Research |
| **Released** | June 2023 (MusicGen), Oct 2023 (MAGNeT) |
| **Architecture** | Single-stage auto-regressive Transformer |
| **Tokenization** | EnCodec (32kHz), 4 codebooks at 50 Hz |
| **Conditioning** | T5 text encoder (text-to-music) + chromagram (melody conditioning) |
| **Code** | MIT License on GitHub (AudioCraft) |
| **Weights** | CC-BY-NC 4.0 (non-commercial) |
| **HF Integration** | Full HuggingFace Transformers support (v4.31+) |

**Model Variants:**

| Model | Parameters | Type |
|-------|-----------|------|
| musicgen-small | 300M | Text-to-music |
| musicgen-medium | 1.5B | Text-to-music |
| musicgen-large | 3.3B | Text-to-music |
| musicgen-melody | 1.5B | Text + melody conditioning |
| musicgen-melody-large | 3.3B | Text + melody conditioning |
| musicgen-stereo-* (all sizes) | — | Stereo fine-tuned versions |

**Key Innovation (MAGNeT):** Masked generative audio transformer. Non-autoregressive -- generates multiple tokens in parallel, then iteratively refines. Faster inference than pure autoregressive models.

**Key Limitations:**
- Cannot generate realistic vocals
- English descriptions only in training
- May collapse to silence at song endings
- Uneven performance across music styles

**Evaluation (MusicCaps):**

| Model | FAD | KLD | Text Consistency | Chroma Cosine Sim |
|-------|-----|-----|------------------|-------------------|
| small | 4.88 | 1.42 | 0.27 | — |
| medium | 5.14 | 1.38 | 0.28 | — |
| large | 5.48 | 1.37 | 0.28 | — |
| melody | 4.93 | 1.41 | 0.27 | 0.44 |

### 2.2 Stable Audio / Stable Audio 2.5 (Stability AI)

| Attribute | Detail |
|-----------|--------|
| **Latest Version** | Stable Audio 2.5 (2025) |
| **Architecture** | Diffusion Transformer (DiT) -- same lineage as Stable Diffusion 3 |
| **Max Duration** | 3 minutes (190 seconds) |
| **Sample Rate** | 44.1 kHz stereo |
| **Speed** | <2 seconds to generate 3 minutes on GPU |
| **License** | Proprietary (commercial via subscription) |
| **API** | Stability AI API, Replicate, fal, ComfyUI |

**Key Features:**
- Text-to-audio, audio-to-audio, audio inpainting
- Multi-section composition (intro -> development -> ending)
- Enterprise-grade sound production
- Trained on AudioSparx licensed data (commercial clean)

**API Parameters (Replicate):**

| Parameter | Type | Range | Default |
|-----------|------|-------|---------|
| prompt | string | 1-10,000 chars | Required |
| duration | integer | 1-190 sec | 190 |
| steps | integer | 4-8 (2.5) | 8 |
| cfg_scale | number | — | 1.0 (2.5) |
| seed | integer | — | Random |
| output_format | string | mp3/wav | mp3 |

**Pricing:**
- Free: limited generations on stableaudio.com
- Pro: $11.99/mo
- Studio: $29.99/mo
- Max: $89.99/mo
- Replicate: ~$0.20 per generation

### 2.3 AudioLDM / AudioLDM 2

| Attribute | Detail |
|-----------|--------|
| **Developer** | CVS/Surrey (Haohe Liu et al.) |
| **Released** | 2023 (AudioLDM 2: Aug 2023) |
| **Architecture** | Dual text encoder + GPT-2 LOA + Latent Diffusion + UNet |
| **Checkpoints** | Base (350M UNet, 1.1B total), Large (750M UNet, 1.5B total) |
| **License** | Open source |
| **HF Integration** | Full Diffusers pipeline support |

**Architecture Details:**
1. Two frozen text encoders: CLAP (audio-text joint) + Flan-T5 (language understanding)
2. Projection model projects into shared space
3. GPT-2 predicts 8 new embedding vectors (Language of Audio bridge)
4. LDM with UNet -- takes two cross-attention embeddings
5. VAE decoder -> Mel spectrogram
6. Vocoder (SpeechT5HiFiGAN) -> waveform

**Available Checkpoints on HuggingFace:**

| Checkpoint | Task | Size |
|-----------|------|------|
| cvssp/audioldm2 | Text-to-audio | 1.1B |
| cvssp/audioldm2-large | Text-to-audio | 1.5B |
| cvssp/audioldm2-music | Text-to-music | 1.1B |
| anhnct/audioldm2_gigaspeech | Text-to-speech | 1.1B |

**Usage (Python):**
```python
from diffusers import AudioLDM2Pipeline
import torch
import scipy

pipe = AudioLDM2Pipeline.from_pretrained("cvssp/audioldm2-music", torch_dtype=torch.float16)
pipe = pipe.to("cuda")

prompt = "A catchy chiptune melody with pulse wave lead and square wave harmony"
audio = pipe(prompt, num_inference_steps=200, audio_length_in_s=10.0).audios[0]

scipy.io.wavfile.write("output.wav", rate=16000, data=audio)
```

### 2.4 Bark (Suno AI)

| Attribute | Detail |
|-----------|--------|
| **Developer** | Suno AI |
| **Released** | April 2023 |
| **Architecture** | 3-stage autoregressive Transformer pipeline |
| **Tokenization** | EnCodec (8 codebooks) |
| **Output** | ~13-14 sec of audio per generation |
| **License** | MIT |
| **Commercial** | Yes (MIT license) |

**Three-Stage Architecture:**

1. BarkSemanticModel (80M/300M): Text -> semantic tokens (vocab 10,000)
2. BarkCoarseModel (80M/300M): Semantic -> coarse EnCodec tokens (2 codebooks)
3. BarkFineModel (80M/300M): Coarse -> fine EnCodec tokens (remaining 6 codebooks)
4. EnCodec decoder -> waveform

**Key Strengths:**
- Natural speech with emotion, pauses, non-speech sounds (laughter, sighs)
- 100+ speaker presets
- Multi-language support (13 languages)
- Can generate simple music and sound effects

**Key Limitations:**
- Short output (14 sec max)
- Occasional hallucinations (noise, background voices)
- Slow inference (autoregressive)
- Music quality far below purpose-built music models

### 2.5 Riffusion

| Attribute | Detail |
|-----------|--------|
| **Developer** | Seth Forsgren, Hayk Martiros |
| **Architecture** | Stable Diffusion v1.5 on mel-spectrogram images |
| **Output** | Audio via Griffin-Lim reconstruction from spectrogram |
| **License** | Open source |
| **Status** | Active hobbyist community |

**Approach:**
- Audio represented as mel-spectrogram image
- Stable Diffusion generates spectrogram from text prompt
- Griffin-Lim algorithm reconstructs audio phase
- Supports interpolation between prompts

**Capabilities:**
- Text-to-audio, audio-to-audio, audio interpolation
- Real-time generation on GPU (NVIDIA 3090+)
- OpenVINO support for Intel hardware

**Relevance for Chiptune:**
- Limitation: Griffin-Lim reconstruction adds artifacts
- Not ideal for clean chiptune waveforms
- Better suited for texture/soundscape generation

### 2.6 ACE-Step 1.5 (2025)

| Attribute | Detail |
|-----------|--------|
| **Developer** | ACEMusic Community |
| **Architecture** | Hybrid LM + Diffusion Transformer (DiT) |
| **Max Duration** | 10 minutes |
| **Speed** | <2s on A100, <10s on RTX 3090 |
| **VRAM** | <4 GB |
| **Languages** | 50+ |
| **License** | Open source |

**Key Features:**
- Lyric editing, voice cloning, remixing, cover generation
- Versions: Base, SFT, Turbo; XL (4B) variants
- LM models: 0.6B / 1.7B / 4B
- Runs on consumer hardware

### 2.7 Suno v5.5 (2026)

| Attribute | Detail |
|-----------|--------|
| **Latest Version** | v5.5 (March 2026) |
| **Max Duration** | ~8 min (extendable to 12+) |
| **Audio Quality** | 44.1 kHz |
| **Stem Export** | Up to 12 tracks |
| **Voice Clone** | Yes (Voices + Custom Models) |
| **Free Tier** | 50 credits/day |
| **Pro Price** | $8-10/month |
| **API** | Third-party via CometAPI |

**Key Features:**
- Custom Models: upload 30 min of audio to fine-tune
- My Taste: learns your style preferences
- 50+ languages
- Lyric consistency improved in v5

### 2.8 Udio

| Attribute | Detail |
|-----------|--------|
| **Latest Version** | V4 |
| **Max Duration** | 2:10 (paid, can extend to 10 min) |
| **Audio Quality** | 48 kHz (studio quality) |
| **Stem Export** | Professional tier |
| **Inpainting** | Yes (precise segment repair) |
| **License** | Subscription |
| **API** | No official API |

**Strengths:**
- Best vocal realism
- Superior instrument texture and mixing
- Better at niche genres (jazz, folk, indie)
- Professional DAW workflow integration (Ableton/Logic Pro)

### 2.9 Google MusicFX / Lyria

| Attribute | Detail |
|-----------|--------|
| **Developer** | Google DeepMind |
| **Latest** | Lyria 3 Pro (2026) |
| **Max Duration** | 3 minutes |
| **Architecture** | Proprietary (based on MusicLM research) |
| **Real-time** | Lyria RealTime API available |
| **Features** | Precise section control, SynthID watermarking |
| **Access** | Google AI Studio / API |

**Space DJ:** Google Magenta's Space DJ uses Lyria RealTime API for real-time 3D music generation -- fly through a 3D genre galaxy where position determines the music.

### 2.10 Magenta RealTime (Open Weight, 2025)

| Attribute | Detail |
|-----------|--------|
| **Developer** | Google Research |
| **Architecture** | 800M Transformer on audio tokens |
| **Sample Rate** | 48 kHz stereo |
| **Streaming** | 2-second chunks, real-time (RTF 0.625) |
| **License** | Apache 2.0 |
| **Hardware** | Free-tier Colab TPU |

**Significance for this project:** First truly open-weight real-time streaming music generation model. Ideal starting point for browser-based or game-integrated AI music.

---

## 3. Symbolic vs Audio Generation Tradeoffs

### 3.1 Core Comparison

| Aspect | Symbolic (MIDI/ABC) | Raw Audio |
|--------|-------------------|-----------|
| **Data size** | Small, structured (tokens: 228-3,440) | Large, dense (spectrograms/waveforms) |
| **Expressiveness** | Limited (no timbre, articulation) | Full acoustic detail |
| **Model complexity** | Small models excel (20M params can compete) | Typically needs large models |
| **Controllability** | High (modify notes, instruments, structure) | Low (black-box generations) |
| **Interpretability** | High (visible notes, chords, structure) | Low (waveform is opaque) |
| **Reproduction** | Easy (MIDI files, standard formats) | Hard (requires full regeneration) |
| **Sound quality** | Depends on synthesizer | Can be photorealistic |
| **Training cost** | Low (web-scale MIDI data available) | High (needs audio + captions) |

### 3.2 Why Symbolic for Chiptune

For chiptune music generation specifically, symbolic approaches are ideal:

1. **Chiptune IS symbolic by nature:** NES/Famicom sound hardware uses pulse waves, triangle waves, noise -- these are all definable as parameters, not audio samples
2. **Compact representation:** A chiptune piece can be fully described in a few KB of MIDI/Famitracker data
3. **Perfect rendering:** Given the right parameters, the output sound is deterministic and perfect -- no "hallucinations" or artifacts
4. **Editability:** Each note, instrument, and effect can be independently modified
5. **Small model footprint:** A 20M-parameter model can match larger systems for structured music generation (MIREX 2025 findings)

### 3.3 Hybrid Approaches

The most practical systems combine both:

```
LLM (symbolic planning)
    |
    |--- MIDI/ABC structure (controllable, editable)
    |
    v
Symbolic renderer (software synth / tracker)
    |--- Audio stems (clean, deterministic)
    |
    v
Neural post-processor (optional)
    |--- Style transfer, timbre enhancement, mixing
    |
    v
Final mix
```

**Key research systems:**
- **CoComposer** (2025): ABC notation from LLM -> MIDI -> evaluation
- **ComposerX** (2024): Multi-agent ABC notation generation
- **MEDIOCRE-MUSIC** (2025): LLM -> ABC notation -> MIDI -> WAV -> WebM pipeline

### 3.4 MIREX 2025 Key Finding

A 20M-parameter RWKV-7 model trained on tokenized raw MIDI **performed on par or better** than MuseCoco (1.2B) and Anticipatory Transformer (780M) for symbolic music generation -- demonstrating that specialized symbolic models remain highly competitive for structured music tasks.

---

## 4. Code and API Availability

### 4.1 Open Source Models (Self-Hostable)

| Model | Code License | Weights License | Hardware Required | HF Integration |
|-------|-------------|-----------------|-------------------|----------------|
| **MusicGen** | MIT | CC-BY-NC 4.0 | 4-12 GB VRAM | Full (transformers) |
| **AudioLDM 2** | MIT | Open | 4-8 GB VRAM | Full (diffusers) |
| **Bark** | MIT | MIT | 8-12 GB VRAM | Full (transformers) |
| **ACE-Step 1.5** | Open | Open | <4 GB VRAM | Yes |
| **YuE** | Apache 2.0 | Apache 2.0 | 8-16 GB VRAM | Yes |
| **InspireMusic** | Open | Open | ~8 GB VRAM | Yes |
| **Magenta RealTime** | Apache 2.0 | Apache 2.0 | Low (TPU/GPU) | Yes |
| **Riffusion** | Open | Open | 4-8 GB VRAM | Diffusers |
| **SongGeneration (Tencent)** | Open | Open | 10-28 GB VRAM | Yes |

### 4.2 API-Only / Proprietary Models

| Model | API Access | Pricing | Commercial Terms |
|-------|-----------|---------|-----------------|
| **Stable Audio 2.5** | Stability AI API, Replicate, fal | $0.20/gen (Replicate) | Licensed data |
| **Suno v5.5** | Web + CometAPI (3rd party) | $8-10/mo Pro | Legal gray area |
| **Udio** | Web only | $10-30/mo | Legal gray area |
| **MusicFX / Lyria** | Google AI Studio / API | TBD | TBD |
| **ChatGPT/GPT-4** | OpenAI API | Standard API pricing | Can output ABC/MIDI |

### 4.3 Local Deployment Requirements

**Minimum (CPU-only):**
- AudioLDM 2 (small): 4 GB RAM, ~30 sec for 10-sec audio
- Bark (small models): 8 GB RAM, ~20 sec for 10-sec audio
- MusicGen (small): Not practical on CPU

**Recommended (Consumer GPU, 8-16 GB):**
- MusicGen-medium: ~5 sec for 30-sec audio
- AudioLDM 2-music: ~10 sec for 10-sec audio
- ACE-Step 1.5: <10 sec for full song
- Bark: ~15 sec for 13-sec audio

**Production (24+ GB GPU):**
- MusicGen-large/stereo
- YuE 7B
- Stable Audio 2.5 (via API recommended)

### 4.4 HuggingFace Music Models Collection

Key HF collections to monitor:
- Music Generation: https://huggingface.co/collections?p=3045&sort=trending
- Text-to-music models
- Audio-to-audio models
- Tags: `music-generation`, `text-to-music`, `song-generation`, `audio-generation`

---

## 5. LLM as Music Arranger

### 5.1 Multi-Agent Architecture (Dominant 2024-2025 Trend)

The multi-agent pattern has proven most effective for LLM-based music composition:

**ComposerX** (ISMIR 2024):
```
User Request ("Create a retro game soundtrack")
    |
    v
+------------------+
| Orchestrator     |  <-- Decomposes task, assigns agents
| Agent            |
+------------------+
    |        |        |        |
    v        v        v        v
+------+ +------+ +------+ +------+
|Melody| |Harmony| |Bass  | |Drum |
|Agent | |Agent  | |Agent | |Agent |
+------+ +------+ +------+ +------+
    |        |        |        |
    +--------+--------+--------+
    |
    v
+------------------+
| Review Agent     |  <-- Critiques, suggests revisions
+------------------+
    |
    v
+------------------+
| Revision Agent   |  <-- Applies fixes
+------------------+
    |
    v
  Final ABC notation -> MIDI -> Audio
```

**Results:** 98.2% generation success rate, 77% human preference over single-agent systems.

**CoComposer** (2025) improved on this with 5 agents (vs ComposerX's 6):
- Higher Production Complexity scores
- 100% generation success rate across GPT-4o, DeepSeek-V3, Gemini-2.5-Flash
- GPT-4o performed best overall
- ABC notation output for full editability

### 5.2 Iterative Refinement

The standard pattern for quality improvement:

```
1. Initial generation
   LLM: "Write a chiptune melody in C major"

2. Self-critique
   LLM: "The melody lacks rhythmic variation and
         doesn't use the upper register enough"

3. Refined generation
   LLM: "Revised melody with syncopated rhythms,
         exploring notes from C4 to C5"

4. Layer addition
   LLM: "Add a bass line following the root notes
         of the implied chord progression"

5. Final review
   LLM: "The bass conflicts with the melody in bar 12.
         Move bass to non-chord tones for that bar"
```

### 6.3 Style Transfer via LLM

LLMs excel at style description and transfer:

```
Prompt: "Take this MIDI melody and rewrite it in the
         style of a Mega Man 2 NES soundtrack.
         Use fast arpeggios, square wave lead,
         and a driving bass line. Keep the key and tempo."
```

The LLM can output transformed ABC notation with style-appropriate:
- Ornamentation patterns (trills, arpeggios)
- Instrument selection (pulse/square/triangle/noise)
- Rhythm patterns (driving 8-bit percussion)
- Harmonic density (thin for NES, rich for SNES)

### 5.4 SongComposer (ACL 2025)

Specialized LLM for structured lyric and melody generation:
- Tuple format for word-level alignment
- Multi-stage pipeline: motif -> phrase -> full song
- Extended tokenizer for song notes
- Demonstrates that domain-specific LLMs outperform general-purpose models for music tasks

### 5.5 M6(GPT)3 (2024-2025)

Uses genetic algorithms + Markov chains + GPT for multi-track MIDI:
- Maps text to composition parameters (JSON): time signature, scales, chord progressions, valence-arousal
- Generates accompaniment, melody, bass, motif, and percussion
- Genetic algorithm for melody evolution
- Markov chains for percussion

### 5.6 Creating a Chiptune Arranger Agent

Based on the research, a practical chiptune arranger would have:

```
System Prompt:
  "You are a chiptune music arranger. You output structured
   ABC notation with NES-style constraints:
   - 4 channels max (2 pulse, 1 triangle, 1 noise)
   - No reverb or effects (pure waveforms)
   - Percussion via noise channel + pitch sweeps"

Agent Roles:
  1. Structure Agent: Defines sections, key, tempo, chord progression
  2. Channel Agent 1: Pulse wave lead melody
  3. Channel Agent 2: Pulse wave harmony/arpeggio
  4. Channel Agent 3: Triangle wave bass line
  5. Channel Agent 4: Noise channel percussion
  6. Review Agent: Checks channel conflicts, NES hardware limitations
```

---

## 6. Spatial Audio and Game Audio

### 6.1 AI-Generated Game Audio Landscape

| Project | Year | Description | Relevance |
|---------|------|-------------|-----------|
| **ThinkSound (Alibaba)** | 2025 | CoT-based spatial audio generation. 3-stage: scene -> object -> edit. Open source. | Most advanced AI spatial audio model |
| **Space DJ (Google)** | 2024-25 | Real-time music from 3D navigation. Lyria RealTime API. | Interactive music from spatial input |
| **SHAC** | 2025 | Interactive spatial audio format, 6DOF, MIT license | Open standard for game spatial audio |
| **NVIDIA Fugatto** | 2024 | 2.5B param text-to-audio. Novel sounds. <4GB VRAM. | Game sound design |
| **Within (Viverse)** | 2025 | Procedural maze game. Every collectible adds musical layer. Tone.js. | Best example of AI procedural game music |
| **SynthCity** | 2025 | City builder where buildings generate music patterns. Gemini API + Web Audio API. | Player-interaction-driven music |
| **CosmicNexus** | 2025 | AI-powered exploration game with procedural audio + Gemini NPC dialogue. Web Audio API. | Full AI game audio in browser |

### 6.2 ThinkSound: Chain-of-Thought Spatial Audio

3-stage architecture:
1. Global scene understanding (analyze full audio context)
2. Object-level focus (extract/place specific sounds in 3D space)
3. User instruction editing (modify via natural language)

Outperforms MMAudio, V2A-Mappe, Meta's MovieGenAudio on benchmarks.

### 6.3 SHAC: Interactive Spatial Audio Codec

- First open-source interactive spatial audio format
- Third-order ambisonics + prerendered binaural audio
- 8.6x real-time playback, <50ms navigation latency
- WASD/controller/touch input
- MIT license
- Built via human + Claude collaboration

### 6.4 Procedural Game Audio with AI

The Within project demonstrates the ideal pattern for game audio:
- Procedural labyrinth generates geometry
- Each collectible item adds a new musical layer (ambient drone -> bass -> arpeggio -> percussion)
- Music evolves dynamically with player progress
- Built in PlayCanvas + Tone.js (browser-based)

For a game audio AI system:
```
Game State (player position, health, enemies, items)
    |
    v
+------------------+
| LLM (edge/cloud) |  <-- Maps game state to music parameters
+------------------+
    |
    | tempo, key, intensity, instrument selection
    v
+------------------+
| Synthesizer      |  <-- Real-time audio rendering
| (WebAudio/MIDI)  |
+------------------+
    |
    v
Game audio output
```

---

## 7. Web Audio API and Browser-Based Music AI

### 7.1 Current Browser AI Music Capabilities

**Web Audio API** provides full synthesis capabilities in the browser:
- OscillatorNode (sine, square, saw, triangle, custom waveforms)
- GainNode, BiquadFilterNode, ConvolverNode
- AudioWorklet for custom DSP
- MIDI access via Web MIDI API

**Browser AI Inference:**

| Library | Capability | Status |
|---------|-----------|--------|
| **tensorflow.js** | Load TFLite models for inference | Mature, but audio models are large (>100MB) |
| **ONNX.js** / **ONNX Runtime Web** | Run ONNX models in browser | Growing ecosystem, WebGPU acceleration |
| **Transformers.js** | HuggingFace models in browser | Supports audio classification, not generation |
| **WebGPU** | GPU compute for neural networks | Available in Chrome/Edge, still maturing |

### 7.2 Practical Browser Pipeline

Most practical approach for browser-based chiptune AI:

```
LLM (cloud API or WebLLM)        Web Audio API synthesis
    |                                     |
    | Structured output (ABC/MIDI/JSON)   |
    +----------> Parser <-----------------+
                        |
                        | Note events (pitch, duration, velocity, channel)
                        v
                +------------------+
                | AudioEngine      |
                |  - PulseWave     |<-- Custom oscillator for chiptune
                |  - TriangleWave  |
                |  - NoiseGen      |
                |  - Sequencer     |
                +------------------+
                        |
                        | Audio graph
                        v
                 Browser audio output
```

### 7.3 Chiptune Synthesis in Browser

Web Audio API is ideal for chiptune because:
- Square/pulse waves are native (OscillatorNode type: "square")
- Triangle waves via custom PeriodicWave
- Noise via AudioBuffer with random samples
- Low latency (<10ms with AudioContext)
- No audio model inference needed (deterministic synth)

```javascript
// Simple pulse wave chiptune synth
const audioCtx = new AudioContext();

function playNote(frequency, duration, type = 'square', volume = 0.3) {
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();

  osc.type = type;
  osc.frequency.value = frequency;

  gain.gain.setValueAtTime(volume, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);

  osc.connect(gain);
  gain.connect(audioCtx.destination);

  osc.start();
  osc.stop(audioCtx.currentTime + duration);
}

// Play a C major arpeggio
playNote(261.63, 0.2, 'square');  // C4
setTimeout(() => playNote(329.63, 0.2, 'square'), 200);  // E4
setTimeout(() => playNote(392.00, 0.2, 'square'), 400);  // G4
setTimeout(() => playNote(523.25, 0.4, 'square'), 600);  // C5
```

### 7.4 Existing Browser-Based Music AI Demos

- **Within** (Viverse): Tone.js procedural game music
- **SynthCity** (Devpost 2025): Web Audio API + Gemini API
- **CosmicNexus** (Devpost 2025): Web Audio API + Gemini NPCs
- **Riffusion Playground**: Streamlit web app for text-to-spectrogram (runs Python backend)
- **Space DJ** (Google): Three.js + Lyria API

### 7.5 WebLLM for Fully Local Browser Inference

**WebLLM** (by MLC AI) enables running LLMs directly in the browser:
- Supports 2B-7B parameter models quantized to 4-bit
- Uses WebGPU for acceleration
- Would allow fully client-side chiptune generation

**Current limitations:**
- Large initial download (1-4 GB for quantized models)
- Slower than cloud API (token-by-token generation)
- Limited to Chrome/Edge with WebGPU
- Music-specific models not yet available in WebLLM format

---

## 8. Practical Integration Patterns

### 8.1 Recommended Architecture for Chiptune Project

Based on the survey, the most practical architecture for LLM-guided chiptune synthesis:

```
Layer 1: LLM Orchestrator
  - Input: Natural language prompt
  - Output: Structured JSON with sections, instruments, notes
  - Options: GPT-4o (cloud), Claude (cloud), local LLM (offline)
  - Format: ABC notation or custom JSON schema

Layer 2: Structure Parser
  - Converts LLM output to note events
  - Handles timing, key transposition, channel assignment
  - Validates against NES hardware constraints (4 channels, waveform types)

Layer 3: Audio Renderer
  - Option A: Web Audio API (browser, real-time)
  - Option B: MIDI file + soundfont (offline, higher quality)
  - Option C: Famitracker export (for NES accuracy)

Layer 4: Optional Neural Enhancement
  - AudioLDM 2 for sound effects
  - Style transfer via prompt engineering
```

### 8.2 API Integration Examples

**OpenAI GPT-4 for Chiptune Arrangement:**
```python
import openai
import json

def generate_chiptune_arrangement(prompt: str) -> dict:
    """Use GPT-4 to generate a structured chiptune arrangement."""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{
            "role": "system",
            "content": """You are a chiptune composer. Output a JSON arrangement with:
            - tempo (BPM)
            - key (musical key)
            - sections (array of {name, bars, channels})
            - channels: array of {type: pulse1|pulse2|triangle|noise, notes: [{note, octave, duration, beat}]}
            """
        }, {
            "role": "user",
            "content": prompt
        }],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

arrangement = generate_chiptune_arrangement(
    "A energetic boss battle theme in D minor, 140 BPM, with fast arpeggios"
)
```

**Stable Audio 2.5 API (via Replicate):**
```python
import replicate

output = replicate.run(
    "stability-ai/stable-audio-2.5:46a2601577d0e31aa99b03c9d7fd2142fa3b96a282338758f794b620e35c75b7",
    input={
        "prompt": "An 8-bit chiptune track with pulse wave melodies, triangle bass, "
                  "and noise percussion. Energetic video game music style.",
        "duration": 30,
        "steps": 8,
        "cfg_scale": 3.0,
        "output_format": "wav"
    }
)
print(f"Generated audio at: {output}")
```

**MusicGen (local):**
```python
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import torch
import scipy

processor = AutoProcessor.from_pretrained("facebook/musicgen-medium")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")

inputs = processor(
    text=["A chiptune arpeggio in C major, 120 BPM, square wave lead"],
    padding=True,
    return_tensors="pt",
)

audio_values = model.generate(**inputs, max_new_tokens=256)
sampling_rate = model.config.audio_encoder.sampling_rate

scipy.io.wavfile.write("chiptune_out.wav", rate=sampling_rate,
                       data=audio_values[0, 0].numpy())
```

**AudioLDM 2 (local, music checkpoint):**
```python
from diffusers import AudioLDM2Pipeline
import torch
import scipy

pipe = AudioLDM2Pipeline.from_pretrained(
    "cvssp/audioldm2-music", torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

prompt = "8-bit chiptune melody, square wave, video game music, high quality"
negative_prompt = "Low quality, noise, distortion"

audio = pipe(
    prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=100,
    audio_length_in_s=8.0,
    num_waveforms_per_prompt=3,  # Generate 3, select best
).audios[0]

scipy.io.wavfile.write("audioldm_chiptune.wav", rate=16000, data=audio)
```

### 8.3 Multi-Agent Composition (AutoGen)

```python
# Pseudocode for multi-agent chiptune composition using AutoGen pattern
from autogen import AssistantAgent, GroupChat, GroupChatManager

# Define specialized agents
orchestrator = AssistantAgent(
    name="Orchestrator",
    system_message="You plan the structure of a chiptune piece. "
                   "Output section layout, key, tempo, and channel allocation."
)

melody_agent = AssistantAgent(
    name="MelodyAgent",
    system_message="You compose the lead melody using pulse wave 1. "
                   "Output ABC notation for the melody track."
)

bass_agent = AssistantAgent(
    name="BassAgent",
    system_message="You compose the bass line using triangle wave. "
                   "Output ABC notation for the bass track."
)

percussion_agent = AssistantAgent(
    name="PercussionAgent",
    system_message="You compose percussion using the noise channel. "
                   "Output ABC notation for the drum track."
)

reviewer = AssistantAgent(
    name="Reviewer",
    system_message="You review all tracks for channel conflicts, "
                   "hardware constraint violations, and musical coherence."
)

# Create group chat
group_chat = GroupChat(
    agents=[orchestrator, melody_agent, bass_agent,
            percussion_agent, reviewer],
    messages=[]
)

manager = GroupChatManager(groupchat=group_chat)

# Start composition
result = manager.initiate_chat(
    "Compose a chiptune boss battle theme in D minor, 150 BPM"
)
```

### 8.4 Prompt Templates for Chiptune Generation

**LLM-guided structural prompt:**
```
Generate a chiptune arrangement with these constraints:
- 4 channels: pulse1 (lead), pulse2 (harmony), triangle (bass), noise (percussion)
- 120 BPM, key of A minor
- Structure: Intro(4 bars) -> Melody A(8) -> Melody B(8) -> Bridge(4) -> Melody A(8) -> Outro(4)
- NES hardware limitations: no release envelope, 4-voice polyphony max
- Style reference: Mega Man 2, Castlevania, or original composition

Output format: structured ABC notation with channel headers.
```

**Style transfer prompt:**
```
Take the following MIDI sequence and rewrite it as a chiptune:
[original MIDI data]

Apply these transformations:
- Convert all instruments to pulse/square/triangle/noise
- Simplify chords to 2-note voicings (NES can't do 3+ note chords on one channel)
- Add fast arpeggiation where appropriate
- Use duty cycle variation (12.5%, 25%, 50%, 75%) for timbral interest
- Add noise channel percussion on beats 2 and 4
```

---

## 9. Model Comparison Matrix

### 9.1 Full Comparison

| Model | Open Source | Vocals | Music Quality | Controllability | Speed | VRAM | Best For |
|-------|-----------|--------|---------------|-----------------|-------|------|----------|
| **MusicGen** | Yes* | No | Good | Medium | Medium | 4-12 GB | Structured music generation |
| **AudioLDM 2** | Yes | No | Good | Low | Slow | 4-8 GB | Sound effects + ambient |
| **Stable Audio 2.5** | No | No | Excellent | High | Very Fast | API | Production music |
| **Suno v5.5** | No | Yes | Excellent | Low | Fast | Cloud | Full songs with vocals |
| **Udio** | No | Yes | Excellent | Medium | Fast | Cloud | Professional production |
| **ACE-Step 1.5** | Yes | Yes | Very Good | High | Very Fast | <4 GB | All-in-one local |
| **YuE** | Yes | Yes | Very Good | Medium | Medium | 8-16 GB | Lyrics-to-song |
| **Bark** | Yes | Yes** | Low | Low | Slow | 8-12 GB | TTS + simple audio |
| **Riffusion** | Yes | No | Low | Low | Fast | 4-8 GB | Sound effects |
| **Magenta RT** | Yes | No | Good | Medium | Real-time | Low | Interactive music |

*Weights are CC-BY-NC (non-commercial), code is MIT
**Bark generates speech-quality vocals, not singing

### 9.2 Chiptune-Specific Suitability

| Model | Chiptune Quality | Controllability | Local | Recommendation |
|-------|-----------------|-----------------|-------|---------------|
| **MusicGen** | Moderate (no waveform control) | Low (text only) | Yes | OK for rough drafts |
| **AudioLDM 2** | Moderate | Low | Yes | OK for SFX |
| **Stable Audio 2.5** | Good | Medium | No | Good for prototypes |
| **ACE-Step 1.5** | Good | High | Yes | **Best local option** |
| **Magenta RT** | Good | Medium | Yes | **Best real-time option** |
| **LLM + WebAudio** | **Excellent** (deterministic) | **Complete** | Yes | **Best for chiptune** |

**Recommendation for chiptune projects:** The LLM + WebAudio/MIDI approach (symbolic generation) is superior to any audio model for chiptune, because:
1. Chiptune is inherently symbolic (parameters, not samples)
2. You can guarantee hardware-accurate output
3. Full editability and control
4. Runs on any device (even without GPU)
5. Real-time performance is achievable

---

## 10. References

### Research Papers

1. **MusicGen**: "Simple and Controllable Music Generation" (Copet et al., 2023) - https://arxiv.org/abs/2306.05284
2. **AudioLDM 2**: "Learning Holistic Audio Generation with Self-supervised Pretraining" (Liu et al., 2023) - https://arxiv.org/abs/2308.05734
3. **MuMu-LLaMA**: "Multi-modal Music Understanding and Generation via Large Language Models" (2025) - https://www.sciencedirect.com/science/article/abs/pii/S0957417425043039
4. **ComposerX**: "Multi-Agent Symbolic Music Composition with LLMs" (ISMIR 2024) - https://ismir2024program.ismir.net/poster_237.html
5. **CoComposer**: "LLM Multi-agent Collaborative Music Composition" (2025) - https://arxiv.org/abs/2509.00132
6. **ChatMusician**: "Understanding and Generating Music Intrinsically with LLM" (ACL 2024) - https://aclanthology.org/2024.findings-acl.373/
7. **M6(GPT)3**: "Generating Multitrack Modifiable Multi-Minute MIDI Music from Text" (2024) - https://arxiv.org/abs/2409.12638
8. **SongComposer**: "A Large Language Model for Lyric and Melody Generation" (ACL 2025) - https://arxiv.org/abs/2402.17645
9. **SegTune**: "Structured and Fine-Grained Control for Song Generation" (2025) - https://arxiv.org/abs/2510.18416

### Code Repositories

10. **AudioCraft (MusicGen)**: https://github.com/facebookresearch/audiocraft (MIT)
11. **AudioLDM 2**: https://github.com/haoheliu/audioldm2 (MIT)
12. **Bark**: https://github.com/suno-ai/bark (MIT)
13. **Riffusion**: https://github.com/riffusion/riffusion-hobby
14. **ACE-Step 1.5**: https://github.com/ace-step/ACE-Step-1.5
15. **YuE**: https://huggingface.co/m-a-p/YuE-s1-7B-anneal-zh-icl
16. **InspireMusic**: https://huggingface.co/FunAudioLLM/InspireMusic-1.5B
17. **AI Songwriting Assistant**: https://github.com/ghchen99/ai-songwriting-assistant
18. **MEDIOCRE-MUSIC**: https://github.com/agrathwohl/mediocre
19. **TOMI**: https://github.com/heqi201255/TOMI

### Platforms & APIs

20. **Stable Audio**: https://stableaudio.com
21. **Suno**: https://suno.com
22. **Udio**: https://udio.com
23. **Google MusicFX**: https://deepmind.google/blog/new-generative-ai-tools-open-the-doors-of-music-creation
24. **Magenta RealTime**: https://huggingface.co/google-research/magenta-realtime
25. **SHAC Spatial Audio**: https://shac.dev
26. **ThinkSound**: https://developer.aliyun.com/article/1670635

### Tools & Libraries

27. **HuggingFace Diffusers**: https://huggingface.co/docs/diffusers/en/api/pipelines/audioldm2
28. **HuggingFace Transformers**: https://huggingface.co/docs/transformers/en/model_doc/musicgen
29. **Web Audio API**: https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
30. **WebLLM**: https://github.com/mlc-ai/web-llm
31. **AutoGen**: https://github.com/microsoft/autogen

---

## Quick Start: Minimal Chiptune AI Pipeline

The fastest path to a working LLM + chiptune pipeline:

```
1. LLM (GPT-4o / Claude / local) generates ABC notation
   -> Prompt: "Write a 16-bar chiptune melody in ABC notation"

2. Parse ABC with python library (abc2midi or music21)
   -> Converts to MIDI events

3. Render with software synth (pygame.midi, FluidSynth, or custom)
   -> For chiptune accuracy: use custom pulse/triangle/noise synth

4. Output: WAV file or stream to browser via Web Audio API

Total lines of code: ~100-200
Dependencies: openai + music21 + numpy + scipy (or pygame)
```

For a browser-native version:
```
1. LLM via API (or WebLLM) generates structured JSON
2. Parse in JavaScript
3. Render via Web Audio API oscillators
4. Zero audio model dependencies
```
