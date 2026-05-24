# Music AI: Datasets, Training, and Research Landscape

A comprehensive reference for building AI music generation systems, from 8-bit/chiptune to multi-instrumental music.

---

## Table of Contents

1. [Music Datasets for AI Training](#1-music-datasets-for-ai-training)
2. [Data Preprocessing for Music AI](#2-data-preprocessing-for-music-ai)
3. [Training Approaches](#3-training-approaches)
4. [Evaluation Metrics](#4-evaluation-metrics)
5. [Open Source Models](#5-open-source-models)
6. [Music Representation Formats](#6-music-representation-formats)
7. [Python Code Examples](#7-python-code-examples)
8. [Recommendations for 8-Bit System](#8-recommendations-for-8-bit-system)

---

## 1. Music Datasets for AI Training

### 1.1 NES-MDB (NES Music Database)

| Property | Value |
|----------|-------|
| **Size** | 5,278 songs from 397 NES games |
| **Notes** | 2+ million, 296 unique composers |
| **Channels** | 4 NES voices (Pulse 1, Pulse 2, Triangle, Noise) |
| **Format** | MIDI, VGM, music score |
| **Year** | 2018 |
| **License** | CC-BY |
| **URL** | https://github.com/chrisdonahue/nesmdb |

**Notes:** The foundational dataset for chiptune AI. MIDIs extracted directly from NES assembly code. Each song maps to the original NES hardware channels, making it the ideal dataset for 8-bit generation. NES-VMDB (2024) extends it with 98,940 paired gameplay video clips from 389 games: https://github.com/rubensolv/NES-VMDB

### 1.2 Lakh MIDI Dataset (LMD)

| Property | Value |
|----------|-------|
| **Size** | 176,581 unique MIDI files |
| **Aligned to MSD** | 45,129 files matched to Million Song Dataset |
| **Genres** | Pop, rock, classical, jazz, electronic, soundtracks |
| **Format** | MIDI |
| **Year** | 2016 |
| **License** | CC-BY 4.0 |
| **URL** | https://colinraffel.com/projects/lmd/ |

**Notes:** The most widely-used symbolic music dataset. Covers diverse instrumentation (solo piano to full orchestral). The LMD-matched subset (45k files) provides audio alignment via the Million Song Dataset. Key derivatives: Lakh Pianoroll Dataset (LPD), Slakh2100 (source separation), LMD-clean (15k curated files).

### 1.3 MAESTRO

| Property | Value |
|----------|-------|
| **Version** | v3.0.0 (latest) |
| **Performances** | 1,276 |
| **Duration** | 198.7 hours |
| **Notes** | 7.04 million |
| **Alignment** | ~3 ms accuracy MIDI-to-audio |
| **Format** | MIDI + audio (WAV) |
| **Year** | 2022 (v3.0.0) |
| **URL** | https://magenta.tensorflow.org/datasets/maestro |

**Notes:** Gold standard for piano transcription and generation. Recorded on Yamaha Disklavier concert grand pianos (simultaneous MIDI + audio). Split: Train 962 perf. (159.2 hrs), Validation 137 (19.4 hrs), Test 177 (20.0 hrs). MIDI-only zip is ~56 MB; full with audio is ~101 GB.

### 1.4 ADL Piano MIDI

| Property | Value |
|----------|-------|
| **Size** | 11,086 piano pieces |
| **Format** | MIDI |
| **Organization** | By genres, sub-genres, artists |
| **URL** | https://github.com/lucasnfe/adl-piano-midi |

**Notes:** 9,021 files extracted from LMD (Piano Family only, MIDI program 1-8) + 2,065 scraped from internet. Deduplicated via MD5. Good for solo piano training.

### 1.5 POP909

| Property | Value |
|----------|-------|
| **Size** | 909 popular songs |
| **Duration** | ~60 hours |
| **Artists** | 462 |
| **Tracks per song** | 3 (Melody, Bridge, Piano accompaniment) |
| **Annotations** | Tempo curves, beats, chords, key changes |
| **Format** | MIDI + audio alignment |
| **Year** | 2020 |
| **URL** | https://github.com/music-x-lab/POP909-Dataset |

**Notes:** ISMIR 2020 dataset. Professionally arranged by teams of musicians. Ideal for studying melody-accompaniment relationships and arrangement generation. Includes preprocessed Magenta-compatible tokens.

### 1.6 MetaMIDI Dataset (MMD)

| Property | Value |
|----------|-------|
| **Size** | 436,631 MIDI files |
| **With metadata** | 221,504 (artist + title), 143,868 (genre) |
| **Audio-MIDI matches** | 10,796,557 (237k MIDI to Spotify) |
| **Format** | MIDI |
| **Year** | 2021 (ISMIR) |
| **URL** | https://github.com/Metacreation-Lab/MetaMIDI-Dataset |

**Notes:** 10x more metadata than LMD. Links MIDI to Spotify 30-second previews and MusicBrainz. Requires application for access. Successor: GigaMIDI (even larger).

### 1.7 IrishMAN / The Session

| Property | Value |
|----------|-------|
| **IrishMAN** | 216,284 tunes (ABC notation) |
| **MABCD** | 285,449 tunes (ABC notation) |
| **Format** | ABC, MIDI, MusicXML |
| **Source** | thesession.org, abcnotation.com |
| **URL** | https://huggingface.co/datasets/sander-wood/irishman |

**Notes:** Public domain Irish folk music. Used to train TunesFormer. IrishMAN includes control codes for structured generation and ~34k lead sheets with chord annotations. Excellent monophonic/melodic training data.

### 1.8 Chiptune & Game Music Collections

| Dataset | Size | URL |
|---------|------|-----|
| **VGMusic (Kaggle)** | 30,000+ game MIDI files (~110 MB) | https://www.kaggle.com/datasets/hansespinosa2/40000-video-game-midi-files |
| **VGMIDI** | 95 pieces with emotion labels | https://service.tib.eu/ldmservice/dataset/dublincore/vgmidi.xml |
| **NES-MDB** | 5,278 NES songs (see 1.1) | https://github.com/chrisdonahue/nesmdb |

**VGMusic notes:** Scraped from vgmusic.com. Covers nearly every console and computer platform. Includes CSV with credits, game titles, composers, consoles, companies. Wide instrument variety.

### 1.9 Additional Datasets

| Dataset | Size | Format | Description | URL |
|---------|------|--------|-------------|-----|
| **JSB Chorales** | 382 chorales | MIDI/MusicXML | J.S. Bach 4-part chorales | music21 built-in |
| **SymphonyNet** | ~100k+ | MIDI | Orchestral/ensemble MIDI | https://github.com/symphony-net |
| **MidiCaps** | 168k | MIDI + captions | MIDI-caption pairs for text-to-MIDI | https://huggingface.co/amaai-lab/text2midi |
| **Amadeus MIDI** | 9M pretrain + 320k finetune | MIDI | Large-scale for Amadeus model | https://arxiv.org/abs/2508.20665 |
| **Bach Doodle** | Millions | MIDI | User-contributed 2-part harmonizations | https://magenta.tensorflow.org/datasets/bach-doodle |
| **GuitarSet** | 360 | MIDI + audio | Guitar performances with tab | https://guitarset.weebly.com/ |

---

## 2. Data Preprocessing for Music AI

### 2.1 Cleaning & Filtering Pipeline

```python
# Typical MIDI cleaning pipeline
# Steps applied in order:

# 1. Parse MIDI
import pretty_midi

midi = pretty_midi.PrettyMIDI('file.mid')

# 2. Remove percussion channels (channel 9 / 10)
midi.instruments = [i for i in midi.instruments if not i.is_drum]

# 3. Remove metadata-only tracks (fewer than 2 notes)
midi.instruments = [i for i in midi.instruments if len(i.notes) >= 2]

# 4. Remove overlapping duplicate notes (same pitch, same time)
def remove_overlapping_duplicates(notes):
    notes.sort(key=lambda n: (n.pitch, n.start))
    cleaned = []
    for note in notes:
        if cleaned and cleaned[-1].pitch == note.pitch and cleaned[-1].end > note.start:
            continue  # skip duplicate
        cleaned.append(note)
    return cleaned

for inst in midi.instruments:
    inst.notes = remove_overlapping_duplicates(inst.notes)

# 5. Sustain pedal merging (CC64 sustain → note extension)
def merge_sustain(notes, pedal_events, tick_resolution=240):
    # Extend note offsets while sustain pedal is held
    # Standard technique from "Symbolic Music Data Version 1.0" (Walder, 2016)
    pass

# 6. Filter by duration (remove very short files < 5 seconds)
total_duration = max(n.end for i in midi.instruments for n in i.notes) \
    if midi.instruments else 0
if total_duration < 5.0:
    raise ValueError("File too short")
```

### 2.2 Format Conversion

```
ABC Notation  ───► music21 ───► MIDI
MusicXML      ───► music21 ───► MIDI
MIDI          ───► pretty_midi ───► numpy array (piano roll)
MIDI          ───► MidiTok ───► token sequence (REMI/CPWord)
MIDI          ───► MusPy ───► Music object (unified format)
```

**Key conversion libraries:**
- **music21** – Converts between MIDI, MusicXML, ABC, **kern, Humdrum. Handles music theory analysis
- **pretty_midi** – MIDI ↔ numpy piano roll, note-level manipulation
- **mido** – Low-level MIDI message I/O
- **MusPy** – Unified `Music` object with I/O for MIDI, MusicXML, ABC, JSON
- **MidiTok** – MIDI ↔ token sequences for transformer models

```python
# music21 conversion example
from music21 import converter

# ABC to MIDI
abc_score = converter.parse("abc_file.abc")
abc_score.write('midi', 'output.mid')

# MIDI to MusicXML
midi_score = converter.parse("input.mid")
midi_score.write('musicxml', 'output.xml')
```

### 2.3 Data Augmentation Techniques

| Technique | Description | Implementation |
|-----------|-------------|----------------|
| **Pitch Shift** | Transpose by -3 to +3 semitones | `notes[:, 2] += shift` |
| **Time Stretch** | Multiply onset/offset by 0.95-1.05 | `notes[:, :2] *= factor` |
| **Velocity Noise** | Add ±10% random velocity | `notes[:, 3] += randint(-12, 12)` |
| **Note Deletion** | Remove random 5-15% of notes | Random mask on note array |
| **Duration Shift** | Modify note lengths | `notes[:, 1] += delta` |
| **Tempo Change** | Change global tempo | Scale all time values |
| **Octave Shift** | Transpose by ±12 | `notes[:, 2] += 12` |
| **Track Dropout** | Randomly remove a track/channel | Per-track mask |

**Library:** MIDIOgre (https://github.com/a-pillay/MIDIOgre) provides on-the-fly augmentation:

```python
from midiogre import PitchShift, TimeStretch, VelocityShift, Compose

augment = Compose([
    PitchShift(max_shift=3, p=0.8),
    TimeStretch(factors=[0.95, 1.0, 1.05], p=0.5),
    VelocityShift(max_shift=10, p=0.3),
])

augmented_notes = augment(original_notes)
```

### 2.4 Train/Validation/Test Split Strategies

**Problem:** Data leakage when the same song appears in both train and test (common in multi-file MIDI datasets like LMD).

**Strategies:**

1. **Random split (80/10/10)** – Simple, but risks leakage with multi-file songs
2. **Artist-based split** – Group by composer/artist before splitting
3. **Clustering-based split** – Cluster by musical signatures (pitch histograms + duration profiles) to minimize similarity leakage. *Used in Walder (2016), "Symbolic Music Data Version 1.0"*
4. **Temporal split** – Chronological (train on older, test on newer)

```python
# Clustering-based split example (from Walder 2016)
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist
import numpy as np

def create_splits(feature_vectors, train_ratio=0.8, val_ratio=0.1):
    """Hierarchical clustering to avoid data leakage."""
    # feature_vectors: (n_files, n_features) where features = pitch histogram + duration histogram
    distance_matrix = pdist(feature_vectors, metric='cosine')
    linkage_matrix = linkage(distance_matrix, method='average')
    n_clusters = int(len(feature_vectors) * 0.2)  # ~20% of files as clusters
    cluster_labels = fcluster(linkage_matrix, n_clusters, criterion='maxclust')
    
    # Assign clusters to splits
    unique_clusters = np.unique(cluster_labels)
    np.random.shuffle(unique_clusters)
    n_train = int(len(unique_clusters) * train_ratio)
    n_val = int(len(unique_clusters) * val_ratio)
    
    train_idx = np.isin(cluster_labels, unique_clusters[:n_train])
    val_idx = np.isin(cluster_labels, unique_clusters[n_train:n_train + n_val])
    test_idx = ~train_idx & ~val_idx
    
    return train_idx, val_idx, test_idx
```

---

## 3. Training Approaches

### 3.1 Autoregressive Generation (Event-by-Event)

**How it works:** Treat music as a sequence of tokens (like language). Predict next token given previous tokens.

**Architecture:** Transformer decoder (GPT-style), LSTM, Transformer-XL

**Pros:**
- Simple and proven (works well for single-track)
- State-of-the-art for symbolic music (Music Transformer, LakhNES)
- Easy to condition on prompt/continuation

**Cons:**
- Quadratic attention cost for long sequences
- No explicit structure or repetition pattern
- Multi-track correlation is challenging

**Key papers:**
- Music Transformer (Huang et al., 2018) – Relative attention for longer context
- LakhNES (Donahue et al., 2019) – Transformer-XL, pretrain on LMD then finetune on NES-MDB
- Performance RNN (Magenta) – LSTM-based event generation
- MuseNet (OpenAI, 2019) – GPT-2 style for multi-instrumental MIDI

### 3.2 Encoder-Decoder Architectures

**How it works:** Encoder processes input (melody, chords, text), decoder generates output arrangement.

**Architecture:** T5, BART, or custom encoder-decoder transformer

**Pros:**
- Natural for arrangement/melody-to-full generation
- Text conditioning works well (Text2MIDI, MuseCoco)
- Controllable generation

**Cons:**
- More parameters than pure decoder
- Requires paired data (input → output)

**Key papers:**
- Text2MIDI (AMAAI-Lab, 2024/AAAI 2025) – T5 encoder + autoregressive decoder for text-to-MIDI
- Pop2Piano (ICLR 2023) – Audio-to-piano-cover
- MuseCoco (2023) – Text-to-symbolic-music

### 3.3 Diffusion Models for Symbolic Music

**How it works:** Gradually add noise to music data, then learn to denoise. Applied in latent space.

**Pros:**
- High quality samples
- Good for modeling complex distributions
- Can be conditioned for controllable generation

**Cons:**
- Slower generation (many denoising steps)
- Less explored for symbolic vs. audio music
- Harder to enforce note-level constraints

**Key papers (2024-2025):**
- **Amadeus** (2025) – Autoregressive + bidirectional discrete diffusion for attributes. 4x speedup vs SOTA. 9M pretraining samples. https://arxiv.org/abs/2508.20665
- **ERLD-HC** (2025) – VAE + latent diffusion + CRF for harmony-constrained generation. 2.35% fewer harmony violations. https://www.mdpi.com/1099-4300/27/9/901
- **FGG** (2024-2025) – Fine-Grained Guidance for diffusion models, real-time pitch/harmony control. https://github.com/huajianduzhuo-code/FGG-music-code
- **LZMidi** (2025) – Compression-based alternative. 30x faster training, 300x faster generation than diffusion, runs on CPU. https://arxiv.org/abs/2503.17654

### 3.4 GANs for Music Generation

**How it works:** Generator creates music, discriminator judges real vs. fake.

**Pros:**
- Fast generation (single forward pass)
- Good for piano-roll representations

**Cons:**
- Mode collapse (generates similar patterns)
- Hard to train, unstable convergence
- Lower quality than autoregressive/diffusion

**Key papers:**
- MuseGAN (2018) – Multi-track piano roll GAN
- C-RNN-GAN (2016) – Continuous RNN-GAN for sequential data
- BachGAN (2019) – GAN for chorale generation

### 3.5 Reinforcement Learning for Music

**How it works:** Train a music generation policy, reward with human preferences or music theory rules.

**Key papers:**
- **MusicRL** (Google DeepMind, ICML 2024) – First RLHF system for music. Fine-tunes MusicLM with 300k pairwise human preferences + text-adherence reward. Shows RL + human feedback improves alignment. https://arxiv.org/abs/2402.04229
- **ReaLchords** (ICML 2024) – RL for adaptive chord accompaniment with harmonic/temporal coherence rewards.

**Reward design ideas:**
- Text adherence score (CLAP similarity)
- Audio quality classifier score
- Music theory rule compliance (scale consistency, voice leading)
- Human preference (RLHF pairwise comparisons)
- Novelty penalty (KL from training distribution)

### 3.6 What Works Best for Multi-Track/Channel Music

| Approach | Single Track | Multi-Track (2-4) | Multi-Instrument (8+) |
|----------|-------------|-------------------|----------------------|
| Autoregressive (event) | Excellent | Good (with track tokens) | Challenging (long sequences) |
| Piano Roll (image-like) | Good | Good (multi-channel) | Very Good (3D conv) |
| Hierarchical (bar-level) | Good | Very Good | Good |
| Diffusion (latent) | Good | Very Good | Very Good |

**Recommendations for multi-track:**
- **2-4 tracks (e.g., NES 4-channel):** Autoregressive with track tokens works well. LakhNES proved this for 4-channel NES.
- **8+ instruments:** Hierarchical approaches (generate structure first, then fill notes) or piano-roll CNN/GAN architectures.
- **Key technique:** Cross-domain pretraining. LakhNES showed that pretraining on general MIDI (LMD) before finetuning on domain-specific data (NES-MDB) significantly improves quality on limited-channel music.

---

## 4. Evaluation Metrics

### 4.1 Objective (Quantitative) Metrics

#### MusPy Metrics Suite

The MusPy library (https://muspy.readthedocs.io) provides standard objective metrics:

| Metric | Description | Range |
|--------|-------------|-------|
| `pitch_range()` | Range between lowest/highest pitch | 0-127 |
| `n_pitches_used()` | Number of unique pitches | 0-128 |
| `n_pitch_classes_used()` | Unique pitch classes (octave-independent) | 0-12 |
| `polyphony()` | Avg simultaneous notes | 0+ |
| `polyphony_rate()` | Ratio of time steps with multiple notes | 0-1 |
| `pitch_in_scale_rate()` | Ratio of notes in key | 0-1 |
| `scale_consistency()` | Best scale fit across all keys | 0-1 |
| `pitch_entropy()` | Shannon entropy of pitch distribution | 0-~7 |
| `pitch_class_entropy()` | Shannon entropy of pitch class dist. | 0-~3.6 |
| `empty_beat_rate()` | Ratio of empty beats | 0-1 |
| `drum_pattern_consistency()` | Drum pattern regularity | 0-1 |
| `groove_consistency()` | Pattern repetition across measures | 0-1 |

**Usage:** Compare distribution of metrics between training data and generated samples. Significant deviation = poor style matching.

#### Audio-Level Metrics

| Metric | Description | Best For |
|--------|-------------|----------|
| **FAD** (Frechet Audio Distance) | Distribution distance between reference and generated audio embeddings | Overall quality (CLAP embeddings best) |
| **FAD-inf** | FAD extrapolated to infinite samples | Removing sample-size bias |
| **KL Divergence** | Distribution difference over classifier predictions | Prompt adherence |
| **CLAP Score** | Cosine similarity of audio-text embeddings | Text-to-music alignment |
| **KAD** (Kernel Audio Distance) | MMD-based distribution-free metric | When Gaussian assumption fails |
| **MAD** (Mauve Audio Divergence) | Distribution overlap quantification | Comparing generated vs reference |

**Important:** FAD has sample-size bias (decreases as sample count increases). Use FAD-inf or consistent sample sizes. CLAP embeddings outperform VGGish for both acoustic and musical quality prediction.

### 4.2 Human Evaluation Methods

| Method | Description | Pros | Cons |
|--------|-------------|------|------|
| **MOS** (Mean Opinion Score) | 5-point Likert scale rating | Standard, comparable | Expensive, subjective |
| **AB Test** | Which sample is better? | Simple, reliable | Binary only |
| **ABX Test** | Which is closer to reference? | Good for style similarity | Requires reference |
| **MUSHRA** | Multi-stimulus rating with hidden reference | High resolution | Complex setup |
| **Preference Elicitation** | Pairwise comparisons → ranking | Captures nuance | Needs aggregation |

**Best practice:** Combine MOS + AB tests. Use at least 10-20 participants. Include reference samples from training data. Recent work (2025, "From Aesthetics to Human Preferences") shows significant inconsistencies across metrics, advocating for human-centered evaluation.

### 4.3 Music Theory Rule Compliance

Automated rule-checking for generated music:

```python
# Example checks for tonal music
def check_rule_compliance(music: "MusPy Music object"):
    violations = {}
    
    # 1. Scale consistency (notes should mostly fit one key)
    violations['scale_violation_rate'] = 1.0 - muspy.scale_consistency(music)
    
    # 2. Voice leading (no leaps > octave in inner voices)
    violations['large_leap_rate'] = compute_large_leaps(music, max_interval=12)
    
    # 3. Parallel fifths/octaves (for polyphonic music)
    violations['parallel_fifth_rate'] = compute_parallel_intervals(music, interval=7)
    
    # 4. Note density (reasonable number of notes per beat)
    violations['density_outlier'] = check_note_density(music)
    
    # 5. Chord voicing (no note overlaps on same pitch)
    violations['note_overlap_rate'] = compute_note_overlaps(music)
    
    return violations
```

### 4.4 Style Similarity Metrics

- **Pitch histogram KL divergence** – How well does the generated pitch distribution match the training domain?
- **Duration histogram KL divergence** – How well do note lengths match?
- **Groove similarity** – Hamming distance of onset patterns between neighboring measures
- **Embedding distance** – Use a pretrained music encoder (MERT, CLAP) to embed generated and reference, then compare with cosine distance
- **n-gram overlap** – Fraction of common melodic n-grams (too high = plagiarism, too low = unrelated)

### 4.5 Novelty vs. Plagiarism

| Check | Method | Threshold |
|-------|--------|-----------|
| **Exact match** | Check generated sequence against training corpus | >4 consecutive identical bars = plagiarism |
| **Edit distance** | Levenshtein distance to nearest training sample | <0.1 normalized = suspicious |
| **n-gram coverage** | Fraction of n-grams found in training | >80% = low novelty |
| **Embedding nearest neighbor** | Find closest training sample in embedding space | Distance < threshold = derivative |

**Plagiarism check implementation:**
```python
def plagiarism_score(generated_notes, training_notes, ngram_size=4):
    """
    Compute plagiarism risk as fraction of generated n-grams
    that appear in the training set.
    """
    def to_ngrams(notes, n):
        pitches = tuple(n.pitch for n in notes)
        return set(zip(*[pitches[i:] for i in range(n)]))
    
    gen_ngrams = to_ngrams(generated_notes, ngram_size)
    train_ngrams = to_ngrams(training_notes, ngram_size)
    
    overlap = len(gen_ngrams & train_ngrams)
    total = len(gen_ngrams)
    return overlap / total if total > 0 else 0.0
```

---

## 5. Open Source Models

### 5.1 Pretrained Models on HuggingFace

| Model | Params | Type | Output | Year | HF Link |
|-------|--------|------|--------|------|---------|
| **Text2MIDI** | ~770M | T5 + Transformer Decoder | MIDI (REMI tokens) | 2024/2025 | https://huggingface.co/amaai-lab/text2midi |
| **Giant Music Transformer** | 786M | Custom Transformer | MIDI | 2024 | https://huggingface.co/asigalov61/Giant-Music-Transformer |
| **MusicGen (Medium)** | 1.5B | EnCodec + AR LM | Audio (WAV) | 2023 | https://huggingface.co/facebook/musicgen-medium |
| **MusicGen (Small)** | 300M | EnCodec + AR LM | Audio (WAV) | 2023 | https://huggingface.co/facebook/musicgen-small |
| **MIDI Gen AI** | 117M | GPT-2 finetuned | MIDI (text-encoded) | 2024 | https://huggingface.co/nicholasbien/midi-gen-ai |
| **MusicLang 4K** | ~85M | GPT-2 | MIDI | 2024 | https://huggingface.co/musiclang/musiclang-4k-onnx |
| **MIDI Model** | ~200M | Transformer Decoder | MIDI | 2024 | https://huggingface.co/SkyTNT/midi-model |

### 5.2 Models Fine-Tuned on Game Music

| Model | Base | Game Music Data | Notes |
|-------|------|-----------------|-------|
| **LakhNES** | Transformer-XL | NES-MDB (pretrained on LMD) | 4-channel NES chiptune generation. Checkpoints available. https://github.com/chrisdonahue/LakhNES |
| **Chiptune.app / Chiptune AI** | GPT-Neo | Lakh MIDI + NES-MDB | Flask server frontend. https://github.com/pickles976/chiptune-ai |

**Note:** No existing models on HuggingFace are specifically tagged for "game music" or "chiptune" finetuning as of mid-2024. LakhNES is the only known pretrained chiptune model. A custom finetune would need to be created.

### 5.3 Small/Lightweight Models for Desktop

| Model | Params | VRAM | CPU Inference | Notes |
|-------|--------|------|---------------|-------|
| **MusicLang 4K ONNX** | ~85M | ~340 MB | Yes (ONNX Runtime) | Quantized version available |
| **MIDI Gen AI (GPT-2)** | 117M | ~470 MB | Yes (CPU OK) | Simple text-encoded MIDI |
| **LZMidi** | N/A (compression) | Minimal | Yes (CPU, 300x faster than diffusion) | No GPU needed |
| **MusicGen Small** | 300M | ~1.2 GB | With OpenVINO | Needs quantization for desktop |

**ONNX/TensorRT Deployment:**
- MusicLang 4K already has ONNX export: https://huggingface.co/musiclang/musiclang-4k-onnx
- MusicGen can be converted via OpenVINO: https://docs.openvino.ai/archive/2023.2/notebooks/250-music-generation-with-output.html
- General ONNX export flow: PyTorch model → torch.onnx.export() → ONNX Runtime inference
- INT8 quantization can reduce size by ~4x and improve latency by ~4.5x (proven on Raspberry Pi 5 for audio models)

### 5.4 Key Repositories

| Repository | Stars | Focus | URL |
|------------|-------|-------|-----|
| **MidiTok** | 2k+ | MIDI tokenization | https://github.com/Natooz/MidiTok |
| **MusPy** | 400+ | Symbolic music toolkit | https://github.com/salu133445/muspy |
| **music21** | 2k+ | Music theory + analysis | https://github.com/cuthbertLab/music21 |
| **pretty_midi** | 1k+ | MIDI manipulation | https://github.com/craffel/pretty-midi |
| **AudioCraft** | 10k+ | Meta's audio generation | https://github.com/facebookresearch/audiocraft |
| **MIDIOgre** | New | On-the-fly MIDI augmentation | https://github.com/a-pillay/MIDIOgre |

---

## 6. Music Representation Formats

### 6.1 REMI (Revamped MIDI-derived Events)

**Description:** Flattened token sequence of musical events. Each token represents one attribute (e.g., Bar, Position, Pitch, Velocity, Duration).

**Token sequence example:**
```
[Bar, Position=0, Pitch=60, Velocity=80, Duration=4,
 Position=4, Pitch=64, Velocity=80, Duration=4,
 ...]
```

**Pros:**
- Well-studied, many papers use it
- Good temporal resolution
- Easy to implement with MidiTok
- Strong coherence in generated music

**Cons:**
- Very long sequences (can exceed transformer context)
- Repeated Position tokens waste tokens
- No explicit note grouping

**Best for:** Single-track or few-track generation where timing detail matters.

**Library:** `from miditok import REMI`

### 6.2 CP Word (Compound Word)

**Description:** Groups all attributes of a note into a single compound token. Multiple sub-tokens (pitch, velocity, duration, etc.) predicted simultaneously via separate linear heads.

**Token example:**
```python
# REMI: [Pitch=60, Velocity=80, Duration=4]  -- 3 tokens
# CPWord: [Pitch_60|Velocity_80|Duration_4]  -- 1 compound token
```

**Pros:**
- Much shorter sequences (3-4x shorter than REMI)
- Faster training and inference
- Natural note grouping

**Cons:**
- Possible dependency loss between attributes (pitch-duration correlation)
- Fixed vocabulary per attribute
- Needs careful head design

**Best for:** Multi-track music where sequence length is a bottleneck.

**Library:** `from miditok import CPWord`

### 6.3 Structured (JSON-Based Note Sequences)

**Description:** Each "event" is a structured JSON/hash with fields. Common in Magenta's NoteSequence format.

```json
{
  "notes": [
    {"pitch": 60, "velocity": 80, "start_time": 0.0, "end_time": 0.5, "instrument": 0},
    {"pitch": 64, "velocity": 80, "start_time": 0.5, "end_time": 1.0, "instrument": 0}
  ],
  "tempo_changes": [{"time": 0.0, "bpm": 120}],
  "time_signatures": [{"time": 0.0, "numerator": 4, "denominator": 4}]
}
```

**Pros:**
- Human-readable, debuggable
- Flexible, extensible
- Direct MusicJSON format

**Cons:**
- Verbose, large file sizes
- Not sequence-friendly (needs flattening for transformers)
- No standard for tensor representation

**Best for:** Data analysis, debugging, intermediate storage.

### 6.4 Piano Roll (Image-Like)

**Description:** 2D matrix: time steps × pitch. Value = velocity (or binary on/off). Multi-track = 3D tensor (tracks × time × pitch).

```
       C4 C#4 D4 D#4 E4 F4 F#4 G4
beat0: [0, 0, 80, 0, 0, 0, 0, 0]
beat1: [0, 0, 0, 0, 80, 0, 0, 0]
beat2: [0, 0, 0, 0, 0, 0, 80, 0]
```

**Pros:**
- Natural for CNN architectures
- Good for multi-track (as channels)
- Easy visualization
- Direct audio-like processing

**Cons:**
- Coarse time resolution (fixed grid)
- Lossy (exact note durations quantized)
- Memory-hungry for high resolution

**Best for:** GANs and CNN-based models, multi-track with many instruments.

**Libraries:** `pypianoroll` (https://github.com/salu133445/pypianoroll), `pretty_midi.get_piano_roll()`

### 6.5 ABC Notation as Training Format

**Description:** Text-based music notation from the folk music community. Terse ASCII format.

```
X:1
M:4/4
L:1/8
K:C
| C D E F | G A B c |]
```

**Pros:**
- Extremely compact
- Human-writable
- Large existing corpora (IrishMAN: 216k+ tunes)
- Natural for character-level LM training

**Cons:**
- Limited to monophonic / simple polyphony
- No velocity/dynamics in standard ABC
- Non-standard extensions for chords
- Limited instrument support

**Best for:** Melodic generation, folk music, monophonic training. Used in MIT intro-to-deep-learning course for RNN music generation.

### 6.6 Comparison for Chiptune / Limited-Channel Music

| Format | Seq Length | Temporal Detail | Multi-Track | Best For |
|--------|-----------|-----------------|-------------|----------|
| **REMI** | Very long | High | Good (track tokens) | Timing-critical generation |
| **CP Word** | Short | Medium | Good | General multi-track |
| **Structured** | N/A | High | Excellent | Data pipeline, preprocessing |
| **Piano Roll** | N/A (image) | Medium-Fixed | Excellent | GANs, multi-channel (NES 4-ch) |
| **ABC** | Short (chars) | Low | Poor | Melody-only, folk |
| **MIDI-Like** | Medium | High | Good | Streaming generation |
| **Octuple** | Medium | High | Very Good | Multi-track transformers |

**Recommendation for 4-channel NES music:** CP Word or Octuple for transformer models (good balance of sequence length and multi-track support). Piano roll for GAN/CNN approaches. REMI for timing-precise generation.

---

## 7. Python Code Examples

### 7.1 Loading and Exploring NES-MDB

```python
import pretty_midi
import glob
import os
from collections import Counter

# Assuming NES-MDB is downloaded and extracted
nesmdb_path = "path/to/nesmdb/midi/"
files = glob.glob(os.path.join(nesmdb_path, "**/*.mid"), recursive=True)
print(f"Total NES-MDB files: {len(files)}")

# Analyze channel usage
channel_counts = Counter()
for f in files[:100]:  # Sample first 100
    midi = pretty_midi.PrettyMIDI(f)
    for inst in midi.instruments:
        channel_counts[inst.program] += 1

print("Instrument program usage:", channel_counts.most_common(10))
```

### 7.2 Loading and Using the Lakh MIDI Dataset with MusPy

```python
import muspy

# Download and load LMD-matched subset
lmd = muspy.LakhMIDIDataset('matched', download_and_extract=True)
print(f"Dataset size: {len(lmd)} files")

# Access a specific file
music = lmd[0]
print(f"Tracks: {len(music.tracks)}")
print(f"Resolution: {music.resolution}")
print(f"Total notes: {sum(len(track.notes) for track in music.tracks)}")

# Convert to numpy piano roll
piano_roll = muspy.to_piano_roll(music)
print(f"Piano roll shape: {piano_roll.shape}")

# Evaluate metrics
print(f"Pitch range: {muspy.pitch_range(music)}")
print(f"Polyphony: {muspy.polyphony(music):.2f}")
print(f"Scale consistency: {muspy.scale_consistency(music):.2f}")
```

### 7.3 Tokenizing MIDI with MidiTok

```python
from miditok import REMI, TokenizerConfig
from miditok.pytorch_data import DatasetMIDI, DataCollator
from miditok.utils import split_files_for_training
from pathlib import Path
from torch.utils.data import DataLoader

# Configuration
config = TokenizerConfig(
    num_velocities=16,           # Quantize 128 velocities to 16 bins
    use_chords=True,             # Include chord tokens
    use_programs=True,           # Include instrument program tokens
    use_tempos=True,             # Include tempo tokens
    beat_res={(0, 1): 8, (1, 2): 4, (2, 4): 2, (4, 8): 1},  # Sub-beat resolution
)

# Create tokenizer
tokenizer = REMI(config)
print(f"REMI tokenizer created, special tokens: {tokenizer.special_tokens}")

# Tokenize a single MIDI file
from symusic import Score
midi = Score("example.mid")
tokens = tokenizer(midi)  # List of List[int]
print(f"Tokenized to {sum(len(t) for t in tokens)} tokens")

# Convert back
restored_midi = tokenizer(tokens, midi)
restored_midi.dump_midi("restored.mid")

# Prepare dataset for training
midi_dir = Path("path/to/midis")
chunk_dir = Path("path/to/chunks")
split_files_for_training(
    files_paths=list(midi_dir.glob("**/*.mid")),
    tokenizer=tokenizer,
    save_dir=chunk_dir,
    max_seq_len=1024,           # Maximum token sequence length
    chunk_overlap=0,            # No overlap between chunks
)

# Create PyTorch DataLoader
dataset = DatasetMIDI(
    files_paths=list(chunk_dir.glob("**/*.mid")),
    tokenizer=tokenizer,
    max_seq_len=1024,
    bos_token_id=tokenizer["BOS_None"],
    eos_token_id=tokenizer["EOS_None"],
)
collator = DataCollator(tokenizer.pad_token_id, copy_inputs_as_labels=True)
dataloader = DataLoader(dataset, batch_size=32, collate_fn=collator)
```

### 7.4 MIDI Cleaning and Filtering Pipeline

```python
import pretty_midi
import numpy as np

def clean_midi_file(filepath, min_duration=5.0, max_polyphony=8):
    """
    Clean a single MIDI file for training.
    Returns cleaned PrettyMIDI object or None if file should be filtered out.
    """
    try:
        midi = pretty_midi.PrettyMIDI(filepath)
    except Exception as e:
        print(f"Parse error: {filepath} - {e}")
        return None
    
    # Remove drum tracks (channel 9)
    midi.instruments = [i for i in midi.instruments if not i.is_drum]
    
    if not midi.instruments:
        return None
    
    # Remove tracks with too few notes
    midi.instruments = [i for i in midi.instruments if len(i.notes) >= 4]
    
    if not midi.instruments:
        return None
    
    # Check minimum duration
    all_notes = [n for i in midi.instruments for n in i.notes]
    if not all_notes:
        return None
    duration = max(n.end for n in all_notes)
    if duration < min_duration:
        return None
    
    # Check maximum polyphony (filter out orchestral files for chiptune)
    max_notes_at_once = 0
    times = sorted(set(n.start for n in all_notes))
    for t in times:
        active = sum(1 for n in all_notes if n.start <= t < n.end)
        max_notes_at_once = max(max_notes_at_once, active)
    
    # Remove overlapping duplicate notes (same pitch, same channel, overlapping time)
    for inst in midi.instruments:
        cleaned_notes = []
        inst.notes.sort(key=lambda n: (n.pitch, n.start))
        for note in inst.notes:
            if cleaned_notes and cleaned_notes[-1].pitch == note.pitch:
                if cleaned_notes[-1].end > note.start:
                    # Merge or skip
                    cleaned_notes[-1].end = max(cleaned_notes[-1].end, note.end)
                    continue
            cleaned_notes.append(note)
        inst.notes = cleaned_notes
    
    return midi

# Batch process a directory
def filter_dataset(input_dir, output_dir):
    import os, glob
    os.makedirs(output_dir, exist_ok=True)
    
    files = glob.glob(os.path.join(input_dir, "**/*.mid"), recursive=True)
    original_count = len(files)
    passed = 0
    
    for f in files:
        midi = clean_midi_file(f)
        if midi is not None:
            rel_path = os.path.relpath(f, input_dir)
            out_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            midi.write(out_path)
            passed += 1
    
    print(f"Filtered: {passed}/{original_count} files kept ({100*passed/original_count:.1f}%)")
```

### 7.5 Training a Minimal Autoregressive Music Transformer

```python
import torch
import torch.nn as nn
import math

class MusicTransformer(nn.Module):
    """
    Minimal GPT-style transformer for symbolic music generation.
    """
    def __init__(self, vocab_size, d_model=256, nhead=8, num_layers=6, max_len=2048):
        super().__init__()
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.pos_embedding = nn.Embedding(max_len, d_model)
        
        decoder_layer = nn.TransformerDecoderLayer(d_model, nhead, dim_feedforward=1024, 
                                                    dropout=0.1, batch_first=True)
        self.decoder = nn.TransformerDecoder(decoder_layer, num_layers)
        self.lm_head = nn.Linear(d_model, vocab_size)
        self.max_len = max_len
        
    def forward(self, x):
        # x: (batch, seq_len)
        seq_len = x.size(1)
        positions = torch.arange(seq_len, device=x.device).unsqueeze(0)
        
        x = self.token_embedding(x) + self.pos_embedding(positions)
        causal_mask = nn.Transformer.generate_square_subsequent_mask(seq_len, device=x.device)
        
        x = self.decoder(x, x, tgt_mask=causal_mask)
        logits = self.lm_head(x)
        return logits
    
    def generate(self, prompt, max_new_tokens=512, temperature=1.0, top_k=40):
        self.eval()
        with torch.no_grad():
            for _ in range(max_new_tokens):
                if prompt.size(1) > self.max_len:
                    prompt = prompt[:, -self.max_len:]
                logits = self.forward(prompt)
                logits = logits[:, -1, :] / temperature
                
                if top_k > 0:
                    values, _ = torch.topk(logits, top_k)
                    logits[logits < values[:, -1:]] = float('-inf')
                
                probs = torch.softmax(logits, dim=-1)
                next_token = torch.multinomial(probs, 1)
                prompt = torch.cat([prompt, next_token], dim=1)
                
                # Stop at EOS token
                if next_token.item() == 0:  # Assuming 0 = EOS
                    break
        return prompt

# Training loop
def train_music_transformer(model, dataloader, epochs=10, lr=1e-4):
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()
    
    for epoch in range(epochs):
        total_loss = 0
        for batch in dataloader:
            input_ids = batch['input_ids']  # (batch, seq_len)
            labels = batch['labels']
            
            logits = model(input_ids)
            loss = criterion(logits.view(-1, logits.size(-1)), labels.view(-1))
            
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            
            total_loss += loss.item()
        
        print(f"Epoch {epoch+1}: loss = {total_loss/len(dataloader):.4f}")
    
    return model
```

### 7.6 Evaluating Generated Music with MusPy

```python
import muspy
import numpy as np

def evaluate_generated(music, reference_stats=None):
    """
    Comprehensive evaluation of generated symbolic music.
    
    Args:
        music: MusPy Music object
        reference_stats: dict of stats from training data for comparison
    
    Returns:
        dict of evaluation metrics
    """
    metrics = {}
    
    # Basic musicality
    metrics['pitch_range'] = muspy.pitch_range(music)
    metrics['n_pitches'] = muspy.n_pitches_used(music)
    metrics['polyphony'] = muspy.polyphony(music)
    metrics['polyphony_rate'] = muspy.polyphony_rate(music)
    metrics['scale_consistency'] = muspy.scale_consistency(music)
    metrics['empty_beat_rate'] = muspy.empty_beat_rate(music)
    
    # Entropy metrics
    metrics['pitch_entropy'] = muspy.pitch_entropy(music)
    metrics['pitch_class_entropy'] = muspy.pitch_class_entropy(music)
    
    # Groove
    if len(music.tracks) > 0 and len(music.tracks[0].notes) > 0:
        metrics['groove_consistency'] = muspy.groove_consistency(music, measure_resolution=8)
    
    # Compare to reference if available
    if reference_stats:
        for key in metrics:
            if key in reference_stats:
                ref_val = reference_stats[key]
                gen_val = metrics[key]
                # Normalized absolute difference
                if ref_val != 0:
                    metrics[f'{key}_diff'] = abs(gen_val - ref_val) / abs(ref_val)
                else:
                    metrics[f'{key}_diff'] = abs(gen_val)
    
    return metrics

def compute_reference_stats(dataset_path):
    """Compute reference statistics from training data."""
    import glob, os
    files = glob.glob(os.path.join(dataset_path, "**/*.mid"), recursive=True)
    
    all_metrics = []
    for f in files[:500]:  # Sample 500 files
        try:
            music = muspy.read_midi(f)
            m = evaluate_generated(music)
            all_metrics.append(m)
        except:
            continue
    
    # Average stats
    avg_stats = {}
    for key in all_metrics[0]:
        values = [m[key] for m in all_metrics if not np.isnan(m.get(key, np.nan))]
        avg_stats[key] = np.mean(values) if values else 0
        avg_stats[f'{key}_std'] = np.std(values) if values else 0
    
    return avg_stats
```

### 7.7 Converting Between Formats

```python
# ABC to MIDI using music21
from music21 import converter

def abc_to_midi(abc_string, output_path="output.mid"):
    score = converter.parse(abc_string, format='abc')
    score.write('midi', output_path)
    return score

# MIDI to ABC
def midi_to_abc(midi_path):
    score = converter.parse(midi_path)
    abc_data = score.write('abc')  # Returns ABC string
    return abc_data

# MIDI to piano roll (numpy)
import pretty_midi

def midi_to_pianoroll(midi_path, fs=100, track_idx=0):
    """
    Convert MIDI to piano roll numpy array.
    
    Args:
        midi_path: Path to MIDI file
        fs: Frame rate (frames per second)
        track_idx: Which instrument track to use
    
    Returns:
        (time_frames, 128) numpy array
    """
    midi = pretty_midi.PrettyMIDI(midi_path)
    if track_idx < len(midi.instruments):
        piano_roll = midi.instruments[track_idx].get_piano_roll(fs=fs)
        return piano_roll.T  # Transpose to (time, pitch)
    return None

# REMI tokens to MIDI
from miditok import REMI
from symusic import Score

def remi_tokens_to_midi(tokens, tokenizer, output_path="output.mid"):
    midi = tokenizer(tokens)  # tokens → Score
    midi.dump_midi(output_path)
```

### 7.8 Data Augmentation Pipeline

```python
import random
import numpy as np

class MidiAugmenter:
    """Augmentation pipeline for symbolic MIDI data."""
    
    def __init__(self, pitch_shift_range=(-3, 3), 
                 time_stretch_range=(0.95, 1.05),
                 velocity_noise=10,
                 note_dropout=0.05):
        self.pitch_range = pitch_shift_range
        self.time_range = time_stretch_range
        self.velocity_noise = velocity_noise
        self.note_dropout = note_dropout
    
    def augment_notes(self, note_array):
        """
        note_array: (n, 4) array of [start, end, pitch, velocity]
        Returns augmented array.
        """
        notes = note_array.copy()
        
        # 1. Pitch shift
        if random.random() < 0.5:
            shift = random.randint(*self.pitch_range)
            notes[:, 2] = np.clip(notes[:, 2] + shift, 0, 127)
        
        # 2. Time stretch
        if random.random() < 0.3:
            factor = random.uniform(*self.time_range)
            notes[:, :2] *= factor
        
        # 3. Velocity noise
        if random.random() < 0.3:
            noise = np.random.randint(-self.velocity_noise, self.velocity_noise + 1, 
                                       size=len(notes))
            notes[:, 3] = np.clip(notes[:, 3] + noise, 0, 127)
        
        # 4. Note dropout
        if random.random() < 0.3:
            mask = np.random.random(len(notes)) > self.note_dropout
            notes = notes[mask]
        
        # 5. octave shift (more extreme augmentation)
        if random.random() < 0.2:
            octave = random.choice([-12, 0, 12])
            notes[:, 2] = np.clip(notes[:, 2] + octave, 0, 127)
        
        return notes
    
    def __call__(self, note_array):
        return self.augment_notes(note_array)
```

---

## 8. Recommendations for 8-Bit System

### Starting Datasets (Priority Order)

| Priority | Dataset | Justification |
|----------|---------|---------------|
| 1 | **NES-MDB** | Native 4-channel NES format. 5,278 songs. Perfect for 8-bit. |
| 2 | **Lakh MIDI (LMD-clean)** | Cross-domain pretraining (LakhNES showed this helps chiptune quality). 15k curated files. |
| 3 | **VGMusic 30k** | General game music MIDI. Expands to non-NES game styles. |
| 4 | **MetaMIDI** | If access granted, 436k files with genre metadata. Filter for electronic/game genres. |

### Recommended Training Approach

**Phase 1: Autoregressive pretraining on LMD**
- Use REMI or CP Word tokenization via MidiTok
- Train GPT-style transformer (6-12 layers, d_model=512)
- Target: General musical understanding

**Phase 2: Finetune on NES-MDB**
- Same architecture, continued training on NES-MDB
- Target: 4-channel NES style
- This is the LakhNES approach, proven effective

**Phase 3: RLHF / Reward optimization (optional)**
- Use MusicRL-style reward modeling
- Reward for: scale consistency, 4-channel constraint satisfaction, user preference

### Architecture Sizing

| Target | Params | VRAM | CPU Inference | Model |
|--------|--------|------|---------------|-------|
| Desktop (no GPU) | < 200M | ~800 MB | Yes | GPT-2 Medium scale (LZMidi or MIDI Gen AI approach) |
| Desktop (GPU) | 300-500M | 2-4 GB | Possible | MusicGen Small or custom transformer |
| Server | 700M+ | 4-8 GB | Heavy | Giant Music Transformer or Text2MIDI |

### Key Libraries to Install

```bash
# Core MIDI processing
pip install pretty_midi mido music21

# Tokenization for transformers
pip install miditok symusic

# Evaluation and dataset management
pip install muspy pypianoroll

# Deep learning
pip install torch torchaudio

# Audio playback and analysis
pip install librosa soundfile

# Augmentation
pip install midiogre

# Model deployment (optional)
pip install onnx onnxruntime
```

---

## References

1. Donahue, C., et al. "LakhNES: Improving Multi-instrumental Music Generation with Cross-domain Pre-training." ISMIR 2019. https://arxiv.org/abs/1907.04868
2. Raffel, C. "Learning-Based Methods for Comparing Sequences." PhD Thesis, 2016. https://colinraffel.com/projects/lmd/
3. Hawthorne, C., et al. "Enabling Factorized Piano Music Modeling and Generation with the MAESTRO Dataset." ICLR 2019. https://magenta.tensorflow.org/datasets/maestro
4. Wang, Z., et al. "POP909: A Pop-song Dataset for Music Arrangement Generation." ISMIR 2020. https://arxiv.org/abs/2008.07142
5. Ens, J., Pasquier, P. "Building the MetaMIDI Dataset." ISMIR 2021. https://github.com/Metacreation-Lab/MetaMIDI-Dataset
6. Huang, C.Z., et al. "Music Transformer." ICLR 2019. https://arxiv.org/abs/1809.04281
7. Cideron, G., et al. "MusicRL: Aligning Music Generation to Human Preferences." ICML 2024. https://arxiv.org/abs/2402.04229
8. Copet, J., et al. "Simple and Controllable Music Generation (MusicGen)." NeurIPS 2023. https://arxiv.org/abs/2306.05284
9. Fradet, N., et al. "MidiTok: A Python Package for MIDI File Tokenization." ISMIR 2021 LBD. https://github.com/Natooz/MidiTok
10. Dong, H.W., et al. "MusPy: A Toolkit for Symbolic Music Generation." ISMIR 2020. https://arxiv.org/abs/2008.01951
11. Cardoso, Moraes, Ferreira. "The NES Video-Music Database." FDG 2024. https://arxiv.org/abs/2404.04420
12. Walder, C. "Symbolic Music Data Version 1.0." 2016. https://arxiv.org/abs/1606.02542
13. Gui, A., et al. "Adapting Frechet Audio Distance for Generative Music Evaluation." 2023. https://arxiv.org/abs/2311.01616
14. Li, Y. "ERLD-HC: Entropy-Regularized Latent Diffusion for Harmony-Constrained Symbolic Music Generation." MDPI Entropy, 2025. https://www.mdpi.com/1099-4300/27/9/901
15. Amadeus: "Autoregressive Model with Bidirectional Attribute Modelling for Symbolic Music." 2025. https://arxiv.org/abs/2508.20665
