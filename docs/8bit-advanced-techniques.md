# Advanced 8-Bit / Chiptune Music Theory

> Complements `music-theory-for-ai.md`. Assumes familiarity with the NES 2A03 APU (2 pulse, 1 triangle, 1 noise, 1 DPCM), basic scales, chord progressions, and standard song structures. This document goes deeper: composer analysis, advanced hardware tricks, genre-specific patterns, counterpoint, emotion mapping, and real transcriptions.

---

## Table of Contents

1. [Famous 8-Bit Composer Analysis](#1-famous-8-bit-composer-analysis)
2. [Advanced NES Composition Tricks](#2-advanced-nes-composition-tricks)
3. [Genre/Style-Specific 8-Bit Patterns](#3-genrestyle-specific-8-bit-patterns)
4. [Counterpoint in Chiptune](#4-counterpoint-in-chiptune)
5. [Emotion-to-Music Mapping](#5-emotion-to-music-mapping)
6. [Real NES Game Music Transcriptions](#6-real-nes-game-music-transcriptions)

---

## 1. Famous 8-Bit Composer Analysis

### 1.1 Koji Kondo (Super Mario Bros., The Legend of Zelda)

**Career context:** Nintendo's first in-house composer. Self-taught on electric organ from age 5; never classically trained. Background in jazz-rock fusion (influenced by Sadao Watanabe, T-SQUARE).

#### Key Compositional Techniques

| Technique | Description | Example |
|-----------|-------------|---------|
| **Open voicing** | Square waves have rich harmonic content; tight voicings sound muddy. Kondo spaces chord tones across all 3 melodic channels with wide intervals (octaves, 10ths) so each tone is distinct. | SMB Overworld: Pulse 1 = C4, Pulse 2 = E4, Triangle = G3 -- a C major triad spread across ~5 semitones between adjacent voices |
| **Mode mixture (borrowed chords)** | Freely borrows bVI, bVII, and minor v from the parallel minor key. Creates emotional depth without losing the tonic. | SMB uses Ab and Bb (bVI-bVII) chords against C major tonic; Zelda overworld uses Fm/Ab, Gb, Db against Bb major |
| **Two-against-three rhythm** | Straight 8th notes on melodic channels rub against swung/clave percussion in the noise channel. Creates the signature "off-kilter" groove. | SMB Overworld: Pulse channels play straight eighths, noise channel plays a Latin/swing pattern |
| **Triadic melody** | Melodies built almost entirely from chord tones (root, 3rd, 5th). Makes themes instantly singable and harmonically clear. | SMB Overworld melody: C-E-G-C, E-G-C-E, G-C-E-G -- all chord tones |
| **Accumulative form** | Builds larger pieces from smaller loops to conserve ROM. Each section recycles the same cadential rhythmic cell. | SMB Overworld: Sections A-B-C-D all derive from the same rhythmic-motivic kernel |
| **Kinetic anaphones** | Music that represents movement. The rhythm of the music mirrors the rhythm of gameplay (jumping, swimming, falling). | Underwater theme uses 3/4 waltz time to mimic floating/swimming |
| **Ritardando as game mechanic** | Slowing tempo signals failure and lets the player's internal rhythm reset after death. | SMB Game Over theme: 4-second theme uses gradual ritardando |

#### Kondo's Core Principle

> "The music is inspired by the game controls, and its purpose is to heighten the feeling of how the game controls."

Every compositional choice serves the gameplay first, musical autonomy second.

#### Hallmark Harmonic Moves

| Move | Description | Where Heard |
|------|-------------|-------------|
| I -> bVI -> bVII -> I | Chromatic mediant shift into borrowed major chords | SMB flagpole fanfare, Zelda overworld bridge |
| I -> V7sus4 | Suspended dominant for forward momentum | SMB Overworld A section |
| I -> IV -> I -> IV(9) -> I -> IV -> bVI -> bVII -> I | Gradual introduction of borrowed chords | SMB Overworld B section |
| Descending bass by whole step | Creates harmonic "descent into unknown" | Zelda overworld: Bb -> Ab -> Gb -> Db -> Cb -> Bbm |

---

### 1.2 Nobuo Uematsu (Final Fantasy I-III NES)

**Career context:** Self-taught composer, no formal music education. Joined Square in 1986. NES-era Final Fantasy music was composed under extreme technical constraints (3 melodic channels maximum).

#### NES-Era Harmonic Language

| Era | Harmonic Style | Example Tracks |
|-----|---------------|----------------|
| FFI (1987) | Tense, experimental. Uses ascending melodic minor, altered modes. Unconventional scales for dungeon themes. | "Dungeon", "Chaos Shrine" |
| FFII (1988) | Harmonic minor with bb7 (doubly-flat seventh). Chromatic bass movement. | "Dungeon", "Rebel Army Theme" |
| FFIII (1990) | Toward atonality in dungeon themes. No stable tonal center. Modal stasis. | "The Dungeon", "Crystal Cave" |
| All NES-era | Avoidance of perfect authentic cadences. Half cadences dominate. Tonic resolution is constantly delayed. | Battle themes end on V or half-cadence, never full I |

#### Key Uematsu Techniques

| Technique | Description | Example |
|-----------|-------------|---------|
| **Modal mixture** | Borrows bII, bVII, iv from parallel modes constantly. | FFI battle theme uses bII and bVII against minor tonic |
| **Delayed resolution** | Refuses to give structural resolution to tonic until the very end of a piece. Maintains tension across loops. | FFI "Prelude": the famous arpeggiated sequence never resolves cleanly until the final repeat |
| **Linear voice-leading (S-lines/H-lines)** | Every note on every channel carries structural weight. Uses Schenkerian-style structural lines and harmonic support lines within 3-channel polyphony. | FFI "Overworld Theme": each channel follows its own contrapuntal line |
| **Tonal ambiguity for dungeons** | Deliberately discomforting through unstable key centers. Moves toward modal stasis. | FFIII "The Dungeon": no clear tonic for the entire piece |
| **i -> iio -> VI -> VII** | The looping minor progression that underpins many FF battle themes | FFI "Battle Scene": Am -> Bdim -> F -> G -- looping |

#### Progression Template: NES-Era Final Fantasy Battle

```
BPM: 140-150
Key: Typically E minor or A minor
Structure: 16-bar loop
  Intro (4 bars): Triangle bass + percussion, establishing groove
  A section (8 bars): Pulse 1 melody enters on i chord
  B section (4 bars): Rising sequence, ends on V (half cadence)
  Loop back to bar 5

Characteristic chord loop:
| i . . . | iio . . . | VI . . . | VII . . . |
| i . . . | iv . . . | VII . . . | V . . . |
```

---

### 1.3 Hirokazu Tanaka (Metroid, Kid Icarus, EarthBound)

**Career context:** Known as "Hip" Tanaka. Engineer who wrote his own audio drivers in 6502 assembly. Co-founded Creatures Inc. (Pokemon). Radical minimalist who rejected the "upbeat game music" convention.

#### Core Philosophy: "Sound Without Distinctions"

Tanaka deliberately blurred the line between music and sound effects. His Metroid score was designed to make players feel "as if they were encountering a living creature." He wanted sound to be an extension of the game world, not a separate musical layer.

#### Key Stylistic Traits

| Technique | Description | Application |
|-----------|-------------|-------------|
| **Minimalism and silence** | Uses negative space as a compositional tool. Trusts atmosphere over constant melody. | Metroid: long pauses between phrase groups; sparse arpeggios with rests |
| **Dub/reggae foundation** | Heavily influenced by dub reggae (Linval Thompson, Sly Dunbar, Jah Wobble). Drums and bass are the foundation; melodic elements drop in and out. | Wrecking Crew (1985) used dub structure: "play melody, cut it off, insert section with just drums and bass, then vice versa" |
| **Dark ambient texture** | Minor chords, dissonant textures, subdued themes. Was initially rejected internally for being "too dark." | Metroid Brinstar theme: sparse bass, slow arpeggios, no strong melodic presence |
| **Melodic contrast** | Despite Metroid's darkness, Kid Icarus uses melodic, youthful, upbeat style -- demonstrating range. | Kid Icarus Underworld: bright pulse channel melodies |
| **Pacing changes** | Radical tempo and density shifts within a single piece. | Metroid Escape theme: slow build to frantic finale |

#### Tanaka's NES Channel Strategy

```
Metroid "Brinstar" (approximate texture):
  Pulse 1: Sparse melody notes, 2-4 seconds apart
  Pulse 2: Slow arpeggio cycling through minor chord tones
  Triangle: Pedal bass on E2, held for bars at a time
  Noise: Occasional accents, not a steady beat

Key insight: The player's own footsteps and weapon sounds 
become the rhythmic element against this sparse backdrop.
```

#### Tanaka's Influence on Chiptune

- Pioneer of ambient game scoring
- First to use dub structure in video games (call-and-response between bass/drums and melody)
- Proved that minimalism could be more effective than constant melodic activity
- His assembly-level audio programming gave him control most composers lacked

---

### 1.4 Tim Follin (Solstice, Silver Surfer, Pictionary)

**Career context:** British composer (born 1970). Worked at Software Creations. Widely considered the most technically virtuosic NES composer. Composed directly in 6502 assembly -- no keyboard, no instruments. His work sounds like it uses expansion chips but does not.

#### The Follin Sound: Technical Hallmarks

| Technique | Description | Example |
|-----------|-------------|---------|
| **Hyper-fast arpeggios** | Extremely rapid note cycling (faster than standard 16th notes) to simulate fully voiced chords. Creates lush, multi-voice harmony from a single channel. | Silver Surfer Stage 1: constant 32nd-note arpeggios across all pulse channels |
| **Wide-span arpeggios (2-3 octaves)** | Arpeggios that span multiple octaves, often ascending and descending in a single beat. Creates the illusion of more notes than physically possible. | Solstice title theme: C3 E3 G3 C4 E4 G4 C5 G4 E4 C4 G3 E3 -- full cycle in one beat |
| **No DPCM samples** | Silver Surfer soundtrack famously uses zero DPCM samples. All richness comes from the pulse + triangle + noise channels only. | Silver Surfer: pulse 1 melody, pulse 2 arpeggio, triangle bass, noise drums -- no DPCM |
| **Dense texture** | Perceived complexity so high that listeners routinely disbelieve it is NES hardware. | Silver Surfer Stage 1: sounds like 8+ channels from 4 channels |
| **Custom sound driver** | Worked with Stephen Ruddy's custom NES sound driver for complete low-level hardware control. | Enabled frame-by-frame control of all APU registers |
| **Assembly-level composition** | Composed by "thinking along the lines of the computer and not a keyboard." Wrote note values and effects directly in 6502. | Solstice score was written entirely as assembly data tables |

#### Follin's Drum Programming

Follin used the noise channel in conjunction with the triangle channel to produce unusually realistic percussion for the NES:

```
Typical Follin drum programming (per-frame register writes):
  Frame 1: Noise mode 0, period 3, volume 15 (kick attack)
  Frame 2: Noise mode 0, period 8, volume 12 (snare body)
  Frame 3: Noise mode 1, period 2, volume 8 (hi-hat)
  Frame 4-6: Rapid noise period changes for snare roll
```

#### Comparison: Follin vs Typical NES Composers

| Aspect | Typical NES | Tim Follin |
|--------|-------------|------------|
| Arpeggio speed | 16th notes at 120-150 BPM | 32nd notes, sometimes faster |
| Chord voicing | Root position triads | Wide voicings spanning 2-3 octaves |
| Channel utilization | Clear melody/harmony/bass roles | Roles blur; channels trade functions rapidly |
| Sample usage | Common DPCM usage | Avoids DPCM entirely |
| Perceived density | 3-4 voices | 6-8 voices |

---

## 2. Advanced NES Composition Tricks

### 2.1 Multi-Channel Echo / Delay Simulation

Since the NES has no hardware reverb or delay, echo must be simulated manually. There are several approaches:

#### Technique A: One-Voice Echo (Pulse Channel Only)

Duplicate a melodic line on the same channel at lower volume, delayed by a fixed number of frames. Works best with staccato notes.

```
Original melody (Pulse 1):
| C4 . . E4 . . G4 . . . . . . . . |

Echo pattern (Pulse 1, 6-frame delay, volume 8 instead of 15):
| . . C4 . . E4 . . G4 . . . . . . |
| vol 15    vol 15 | vol 15         |

Each note is followed by a quieter copy 6 frames later.
Max volume = 15, echo at volume 8-10 for a natural decay.
```

#### Technique B: Two-Voice Echo (Cross-Channel)

Use Pulse 2 as a dedicated echo channel. Pulse 1 plays the melody; Pulse 2 plays the same line delayed by 3-12 frames at lower volume.

```
FamiTracker-style echo implementation:

Effect column: set delay = 6 frames on Pulse 1 row
Pulse 2: reads delayed notes from Pulse 1, plays at volume 8

Or manually:
Bar 1, Pulse 1: C4 E4 G4 C5  (volume 15)
Bar 1, Pulse 2: --- C4 E4 G4  (volume 10, delay = 2 notes)

The human ear perceives this as reverb.
```

#### Technique C: Pitch-Shifted Echo

Same as Technique B, but the echo channel plays the delayed notes transposed up or down an octave (or a 5th). Creates a "cathedral" effect.

```
Pulse 1 (melody, volume 15): C4 . E4 . G4 . C5 .
Pulse 2 (echo +1 octave, vol 9): . C5 . E5 . G5 . C6
                                   (delayed by 1 quarter note)
```

#### Technique D: Triangle "Verb" (Quantization Echo)

Uses the triangle channel's binary on/off state to create a gated reverb-like effect. The triangle rapidly toggles on/off at decreasing frequency after a note attack, simulating a decay tail.

```
Triangle echo (FamiTracker volume column workaround):
Note C2 at volume on, then quickly alternate:
  C2 (on) . . . C2 (on) . . . C2 (off) . . .
Creates a pseudo-decay that sounds like reverb on bass.
```

### 2.2 Pseudo-Reverb Techniques

#### Manual Reverb via Rapid Note Repetition

Simulates reverb by playing the same note multiple times in rapid succession at decreasing volume:

```
"Reverb" on a held note C4:
Frame:  1   2   3   4   5   6   7   8
Note:   C4  C4  C4  C4  C4  C4  C4  C4
Vol:    15  13  11  9   7   5   3   1
Duration: each frame = 1/60 second (NTSC)

Total reverb tail: ~133ms -- short but effective.
```

#### Detuning / Chorus Effect

Play the same part on Pulse 1 and Pulse 2 with one channel slightly detuned. On the NES, this is done by using different frequency values that are 1-2 semitone steps apart (not microtonal, since the NES has no fine pitch control -- but alternating rapidly between two close pitches works).

```
Chorus simulation:
Pulse 1: C4 E4 G4 C5  (exact pitches)
Pulse 2: C#4 F4 G#4 C#5 (sharp by one semitone, volume 8)

Played simultaneously, the slight pitch difference
creates a beating effect that sounds thicker.
```

### 2.3 Simulating More Than 4 Channels

#### Out-of-Phase Arpeggios

Play two slow arpeggios on Pulse 1 and Pulse 2, but out of phase with each other. The ear perceives overlapping chords rather than sequential notes.

```
Standard: both arpeggios in phase (sounds like one chord):
  Pulse 1: C4 E4 G4 E4 | C4 E4 G4 E4
  Pulse 2: C4 E4 G4 E4 | C4 E4 G4 E4

Out of phase (sounds like two independent chords):
  Pulse 1: C4 . E4 . G4 . E4 . | C4 . E4 . G4 . E4 .
  Pulse 2: . C4 . E4 . G4 . E4 | . C4 . E4 . G4 . E4

Each arpeggio is offset by one 16th note. The ear
hears: C4 C4 E4 E4 G4 G4 E4 E4 -- a fuller texture.
```

#### Rapid Channel Role Switching

Trade roles between Pulse 1 and Pulse 2 every 1-2 bars. The ear perceives each channel as having a distinct function (melody vs harmony), so when they switch, it sounds like two new voices entered.

```
Bar 1-2:
  Pulse 1: Melody (C4-E4-G4-C5)
  Pulse 2: Arpeggio (C3-G3-C4-G3)

Bar 3-4 (roles swap):
  Pulse 1: Arpeggio (C3-G3-C4-G3)  -- now harmony
  Pulse 2: Melody (C4-E4-G4-C5)   -- now lead

Listener perceives: 4 distinct voices across 2 bars,
even though only 2 channels exist.
```

#### Three-Channel Chord Spread

For a single sustained chord, spread the three notes across all three melodic channels. The chord sounds simultaneously (as close as the NES gets):

```
C major triad:
  Pulse 1: C4 (root, 50% duty)
  Pulse 2: E4 (3rd, 25% duty)
  Triangle: G3 (5th, triangle wave)

This sounds like a full chord, not an arpeggio.
Kondo used this constantly -- see Section 1.1.
```

### 2.4 Volume Envelope Tricks

The NES pulse channels have 16 volume levels (0-15). Frame-by-frame volume manipulation creates expressive effects.

#### Exponential Volume Decay (Plucked String)

Decrease volume in a decaying curve for a plucked/pizzicato sound:

```
Frame:  1   2   3   4   5   6   7   8   9   10
Volume: 15  14  12  10  8   6   4   3   2   1

This approximates a natural exponential decay.
Use on pulse channels to simulate a guitar/harp pluck.
```

#### Tremolo via Volume Envelope Loop

Rapid volume cycling creates a tremolo effect perfect for sustained notes:

```
FamiTracker volume envelope:
| f e d c b c d e |
(write as hex: 15 14 13 12 11 12 13 14)

Cycle length: 8 frames (~133ms)
Applied to a held C4, this produces a shimmering tremolo.
```

#### Hardware Decay Envelope (NES APU Built-in)

The NES APU has a built-in decay envelope unit. When enabled, it decrements volume automatically every N frames:

```
Register: $4000 (Pulse 1 control)
Bit 4 = 1: Enable decay envelope
Bits 0-3: Period of decay (N = value + 1 frames per decrement)

Example: $1E = enable envelope, decay period = 15
  Volume starts at 15, decrements by 1 every 15 frames
  (every 250ms at 60fps). Reaches 0 after ~3.75 seconds.

Used in: Super Mario Bros. coin sound for the "ping" decay.
```

#### Volume Swell (Crescendo)

Ramp volume up over time to simulate a note "swelling in":

```
Frame:   1  2  3  4  5  6  7  8  9  10 11 12
Volume:  0  1  2  4  6  8  10 11 12 13 14 15

Used on sustained melody notes for dramatic emphasis.
Common in Castlevania and Final Fantasy intros.
```

### 2.5 Pitch Bending and Vibrato

#### Hardware Sweep Unit (NES APU)

The NES pulse channels have a built-in frequency sweep unit that automatically changes pitch over time:

```
Register: $4001 (Pulse 1 sweep)
Bits 6-7: Sweep shift amount
Bit 3:   Direction (0 = up, 1 = down)
Bits 0-2: Sweep period (in frames)

Example sweep (downward pitch bend):
  $88 = sweep enabled, down, shift=1, period=0
  Result: pitch decreases by 1 unit every 2 frames
  Creates a classic "coin collect" or "jump" sound.
```

#### Manual Pitch Bend (FamiTracker)

Use pitch envelope sequences for controlled bends:

```
Pitch envelope (bend down):
| 0 -1 -2 -3 -4 -5 -6 -7 |

Pitch envelope (bend up):
| 0 1 2 3 4 5 6 7 |

Apply to triangle for kick drum:
  Note: E3
  Pitch envelope: | 0 -3 -6 -10 -15 -20 -28 -40
  Result: rapid downward bend -> kick drum "thump"
```

#### Vibrato Envelope

```
Vibrato via pitch envelope loop:
| -2 -1 0 1 2 1 0 -1 -2 |
(cycle length: 9 frames, ~150ms)

Gentle vibrato (slower, shallower):
| -1 0 1 0 -1 |
(cycle length: 5 frames, ~83ms)

Fast vibrato (for "trembling" tension effect):
| -3 -2 -1 0 1 2 3 2 1 0 -1 -2 -3 |
(cycle length: 13 frames)
```

#### Hardware Click Avoidance

On real NES hardware, rewriting the high frequency byte during a note can cause audible clicks. Best practices:

1. Only write to the high byte when the value actually changes
2. Use the sweep unit when crossing a period multiple of 256
3. XOR the frequency with 1 for subtle vibrato without register resets
4. For smooth slides, avoid rewriting `$4003`/$4007` every frame

---

### 2.6 FamiTracker Advanced Techniques

| Technique | FamiTracker Implementation |
|-----------|---------------------------|
| **Arpeggio chord simulation** | Instrument arpeggio envelope: `| 0 4 7 4` for C major (root, major 3rd, perfect 5th, back to 3rd). Use 1-3 frame speed for fastest arpeggiation |
| **Pitch bend on triangle kick** | Instrument pitch envelope: single note (C-3 or E-3) with pitch envelope `| 0 -5 -12 -20 -30 -45`. Use on triangle channel |
| **Multi-instrument switching** | Create multiple instruments with different peak volume envelopes (one at F, one at C, one at 8). Switch between them to simulate volume changes when Famitone2 lacks a volume column |
| **Duty cycle animation** | Instrument duty cycle envelope: `| 0 1 2 1` cycles through 12.5%, 25%, 50%, 25% duty cycles. Creates a dynamic, evolving timbre |
| **Noise drum programming** | Use the noise channel with rapid volume changes: volume envelope `| f 0` (hex) triggers a single noise burst. Different noise periods = different drum sounds |
| **DPCM delta counter** | The DPCM delta counter affects noise and triangle volume. Use `Zxx` effect to control this value. Higher DPCM activity = quieter noise/triangle |
| **Echo/delay** | Duplicate notes on a second channel with a 3-12 frame offset. Use lower volume or different octave |

---

## 3. Genre/Style-Specific 8-Bit Patterns

### 3.1 Mega Man Style (Fast Rock-Influenced)

**Composers:** Manami Matsumae (MM1), Takashi Tateishi (MM2), Yasuaki Fujita (MM3)

| Parameter | Value |
|-----------|-------|
| Typical BPM | 120-160 (stage themes), 140-180 (boss/Wily) |
| Common keys | C major, A minor, E minor, G major |
| Time signature | 4/4 |
| Feel | Straight 8ths, rock-band imitation |
| Form | Binary (A-B) or verse/chorus/bridge |

#### Channel Allocation (Mega Man Standard)

```
Pulse 1: Lead melody (50% duty, aggressive attack)
Pulse 2: Arpeggio harmony (25% duty, 16th notes)
Triangle: Root-5th bass pattern (8th notes)
Noise: Rock drum beat (kick on 1+3, snare on 2+4)

Rock drum pattern (standard):
| 1  &  2  &  3  &  4  & |
| K  .  S  .  K  .  S  . |
| .  H  .  H  .  H  .  H | (8th note hi-hats)
```

#### Melodic Characteristics

- Strong hook within first 2 bars
- Heavy use of pentatonic and blues scales
- Rapid ascending/descending scale runs (16th notes)
- Call-and-response between channels
- Frequent key changes between sections (Wily stages modulate upward)

#### Typical Chord Loop (Stage Theme)

```
| i . . . | VII . . . | VI . . . | V . . . |
| i . . . | iv . . . | VII . . . | V . . . |
```

Example in A minor: `| Am | G | F | E | Am | Dm | G | E |`

#### Bass Pattern (Mega Man Style)

```
Triangle (8th notes, driving):
| A1 A1 A1 A1 E1 E1 E1 E1 | (root, root, root, root, fifth, fifth, fifth, fifth)
| A1 A1 A1 A1 G1 G1 G1 G1 | (descending stepwise)
| F1 F1 F1 F1 E1 E1 E1 E1 |
| A1 A1 A1 A1 E1 E1 E1 E1 |

The relentless 8th-note pattern is key to Mega Man's "driving" feel.
```

---

### 3.2 Castlevania Style (Gothic/Classical Chiptune)

**Composers:** Kinuyo Yamashita (CV1), Kenichi Matsubara (CV2), Hidenori Maezawa (CV3)

| Parameter | Value |
|-----------|-------|
| Typical BPM | 100-140 (stage themes), 130-160 (boss) |
| Common keys | D minor, E Phrygian, A harmonic minor |
| Time signature | 4/4, also uses 6/8 and 3/4 |
| Feel | Classical/baroque influence, gothic arpeggios |
| Form | Through-composed with contrasting sections |

#### Gothic Harmonic Techniques

| Technique | Description | Example |
|-----------|-------------|---------|
| **Baroque voice leading** | 4-voice contrapuntal movement within 3 NES channels. Each channel is an independent voice. | Castlevania III "Clockwork" |
| **Pedal point** | A repeated bass note under a moving melodic/arpeggio pattern. Creates tension through harmonic dissonance over a static bass. | "Bloody Tears": pedal E under F-E-D-C-Bb-C motion |
| **Diminished chords** | Diminished triads and dim7 for gothic tension. The diminished chord over a pedal creates maximum unease. | CV1 "Wicked Child": Bdim -> Cdim -> Dm |
| **Secondary dominants** | V-of-vi, V-of-IV, etc. for chromatic color without modulation. | CV1 "Vampire Killer": uses A7 (V/iii) against D minor |
| **Suspensions** | Suspended 4th-3rd and 2nd-3rd resolutions, borrowed from baroque organ style. | CV3 "Beginning": chain suspensions in the harmony |
| **Toccata influence** | Direct references to Bach's Toccata and Fugue in D Minor. Runs, diminished arpeggios, pedal points. | CV1 title screen: descending D minor arpeggios |

#### "Bloody Tears" Harmonic Framework

```
Key: G minor (original NES version)

Intro (4 bars): Pedal D in bass, arpeggiated Gm chord
A section (8 bars):
  | Gm . . . | D7 . . . | Gm . . . | D7 . . . |
  | Gm . . . | Cm . . . | Gm . D7 . | Gm . . . |
B section (8 bars):
  | Bb . . . | F . . . | Bb . . . | F . . . |
  | Eb . . . | Bb . . . | D7 . . . | D7 . . . |

The pedal point on D throughout A section creates tension.
The D7 (V of Gm) pulls back to Gm every 4 bars.
B section modulates to relative major (Bb) for contrast.
```

#### Castlevania Drum Pattern (Gothic Rock)

```
| 1  e  &  a  2  e  &  a  3  e  &  a  4  e  &  a |
| K  .  S  .  K  .  S  .  K  .  S  .  K  .  S  . |
| K  .  .  .  S  .  .  .  K  .  .  .  S  .  .  . | (half-time feel)
| .  H  H  H  .  H  H  H  .  H  H  H  .  H  H  H | (galloping hi-hat)

The gallop (eighth + two sixteenths) is signature Castlevania:
| 1  e  &  a  2  e  &  a |
| K  .  .  .  S  .  S  . |
```

---

### 3.3 Kirby Style (Cheerful, Bouncy)

**Composer:** Jun Ishikawa (Kirby's Adventure, 1993), Hirokazu Ando

| Parameter | Value |
|-----------|-------|
| Typical BPM | 120-150 |
| Common keys | C major, G major, F major (avoid minor keys) |
| Time signature | 4/4 |
| Feel | Bouncy, playful, syncopated but cheerful |
| Form | A-B-A with short loops |

#### Kirby Style Techniques

| Technique | Description | Example |
|-----------|-------------|---------|
| **Major pentatonic dominance** | Melodies heavily use the major pentatonic scale. No half steps = guaranteed consonant. | "Vegetable Valley": pentatonic-based melody |
| **"Bouncing" rhythms** | Off-beat accents and dotted rhythms create a skipping/bouncing feel. | Syncopated 8th rests between melodic phrases |
| **Sparkling arpeggios** | Fast, high-register arpeggios (octave 5-6) on Pulse 2 using 12.5% duty for a "sparkle" sound. | "Green Greens" style: C5 E5 G5 C6 arpeggios |
| **Techno-style beats** | Four-on-the-floor kick with syncopated snare accents. | Kick on every quarter note, snare on 2 and 4 + occasional 8th notes |
| **Consonant harmony only** | Avoids diminished, augmented, and suspended chords. All chords are major or minor. | I-IV-V-vi progression blocks |
| **Bass on beats 1 and 3 only** | Triangle plays roots on strong beats only. Leaves space for the bouncy feel. | Contrasts with Mega Man's relentless 8th-note bass |

#### Melody Construction (Kirby Bouncy)

```
Melody uses short motifs (2-4 notes) with rests between them:
Bar 1: C4 E4 G4 . | C4 E4 G4 . | (motif, rest, repeat)
Bar 2: A4 G4 E4 C4 | (descending run)
Bar 3: D4 F4 A4 . | D4 F4 A4 . | (motif on IV chord)
Bar 4: G4 G4 G4 . | (held note leading back)

Key: frequent use of rests between phrases creates the "bouncy" feel.
Compare to Mega Man: continuous motion vs. Kirby's stop-and-go bounce.
```

#### Kirby Drum Pattern

```
| 1  e  &  a  2  e  &  a  3  e  &  a  4  e  &  a |
| K  .  .  .  S  .  .  .  K  .  .  .  S  .  .  . | (kick 1+3, snare 2+4)
| .  .  H  .  .  .  H  .  .  .  H  .  .  .  H  . | (hi-hat on 8th note offbeats)
| K  K  .  .  S  .  .  S  K  .  K  .  S  .  .  . | (occasional double kick for bounce)
```

---

### 3.4 Metroid Style (Atmospheric, Minimal)

**Composer:** Hirokazu Tanaka

| Parameter | Value |
|-----------|-------|
| Typical BPM | 80-110 (exploration), 120-140 (action/escape) |
| Common keys | E Phrygian, B natural minor, A minor |
| Time signature | 4/4, occasionally 5/4 or irregular |
| Feel | Sparse, atmospheric, ambient |
| Form | Open, through-composed, no strong sectional demarcation |

#### Metroid Style Techniques

| Technique | Description | Example |
|-----------|-------------|---------|
| **Extreme sparseness** | Notes may be 2-4 seconds apart. Silence is a compositional element. | Brinstar: melody notes separated by full rests |
| **Pedal bass drones** | Triangle holds a single note for 4-8 bars at a time. Creates a meditative/frantic atmosphere. | Brinstar: E2 held for entire section |
| **Slow arpeggios** | Arpeggios at half or quarter speed (compared to standard). Creates texture, not harmonic filler. | 8th-note arpeggios at 80 BPM = slow, deliberate |
| **Noise as texture, not beat** | Noise channel used for ambient hiss, wind effects, or irregular percussion rather than a steady beat. | Norfair: noise as "fire crackle" ambience |
| **Blurred music/SFX line** | Tanaka deliberately made music sound like sound effects. Metroid's music/sound design is continuous. | Item room "beeps" blend into the musical texture |
| **Minor/modal dissonance** | Phrygian mode (flat 2nd), chromatic bass, diminished intervals. | E Phrygian: E-F-E-B-C-B repeated creates "alien" feel |

#### Metroid Brinstar (Approximate Texture)

```
Pulse 1: Sparse notes, 2-4 second gaps
  | E4 . . . . . . . | F4 . . . E4 . . . |
  | F4 . . . . . . . | E4 . . . . . . . |

Pulse 2: Slow arpeggio, very quiet
  | E3 G3 B3 G3 E3 G3 B3 G3 | (repeating)

Triangle: Pedal drone
  | E2 . . . . . . . | E2 . . . . . . . |

Noise: Irregular, quiet accents
  | . . . s . . . . | . s . . . . . . | (s = soft noise burst)
```

#### Escaping the Planet (Action Variation)

When Samus escapes, the same themes shift to:

```
BPM: 140 (was 90)
Pulse 1: Rapid 16th-note version of the melody
Pulse 2: Fast arpeggio, higher register
Triangle: 8th-note bass (was whole notes)
Noise: Driving beat (was ambient)
```

---

### 3.5 RPG Battle Themes (Urgent, Looping)

**Composers:** Nobuo Uematsu (Final Fantasy I-III), Koichi Sugiyama (Dragon Quest)

| Parameter | Value |
|-----------|-------|
| Typical BPM | 130-150 (standard battle), 155-180 (boss) |
| Common keys | E minor, A minor, D minor |
| Time signature | 4/4 |
| Feel | Urgent, driving, constantly looping |
| Form | 16-bar loop: Intro (4) + A (8) + A' (4, variation + loop back) |

#### Battle Theme Structural Template

```
INTRO (4 bars):
  Triangle + Noise only. Establish groove.
  Bars 1-2: Bass plays i -> V pattern
  Bars 3-4: Noise enters with full drum pattern

A SECTION (8 bars):
  Pulse 1 enters with battle melody (aggressive, short notes)
  Pulse 2: Fast arpeggio (16th notes) playing chord tones
  Triangle: Relentless 8th-note bass
  Noise: Full drum beat

A' SECTION (4 bars, variation leading to loop):
  Slight melodic variation or sequence
  Ends on V chord (half cadence) to create looping tension
  No resolution to i until player wins the battle

LOOP back to bar 5 (A section)
```

#### Bass Pattern (RPG Battle Urgent)

```
The driving 8th-note bass is essential:
| E1 E1 E1 E1 B0 B0 B0 B0 | E1 E1 E1 E1 B0 B0 B0 B0 |
| C1 C1 C1 C1 D1 D1 D1 D1 | G1 G1 G1 G1 G1 G1 G1 G1 |

Descending chromatic walks add urgency:
| E1 E1 E1 E1 Eb1 Eb1 Eb1 Eb1 | D1 D1 D1 D1 Db1 Db1 Db1 Db1 |
| C1 C1 C1 C1 B0 B0 B0 B0 | B0 B0 B0 B0 B0 B0 B0 B0 |
```

#### RPG Battle Drum Patterns

Standard battle:
```
| 1  &  2  &  3  &  4  & |
| K  .  S  .  K  .  S  . |
| .  H  H  H  .  H  H  H | (gallop hi-hat or crash on 1)
```

Boss battle (more intense):
```
| 1  e  &  a  2  e  &  a  3  e  &  a  4  e  &  a |
| K  .  S  .  K  .  S  .  K  .  S  .  K  .  S  . |
| .  .  .  .  .  .  .  .  K  .  .  .  S  .  S  . | (double kick fill)

Double bass feel: K on every quarter AND 8th note.
```

---

### 3.6 Genre Comparison Table

| Parameter | Mega Man | Castlevania | Kirby | Metroid | RPG Battle |
|-----------|----------|-------------|-------|---------|------------|
| **BPM** | 120-160 | 100-140 | 120-150 | 80-140 | 130-180 |
| **Primary key(s)** | C major, A minor | D minor, E Phrygian | C major, G major | E Phrygian, B minor | E minor, A minor |
| **Scale** | Major, blues | Harmonic minor, Phrygian | Major pentatonic | Phrygian, natural minor | Natural minor, harmonic minor |
| **Melody density** | Continuous 8th/16th | Moderate, with rests | Bouncy, with rests | Very sparse | Aggressive, dense |
| **Bass pattern** | 8th notes, root-5th | Half notes, pedal | Quarter notes, sparse | Whole notes, drone | 8th notes, driving |
| **Arpeggio speed** | 16th notes | 8th notes | 16th notes | 8th notes (slow) | 16th notes |
| **Drum style** | Rock beat | Gothic gallop | Bouncy rock | Ambient/irregular | Heavy rock |
| **Harmonic complexity** | Moderate | High (Baroque) | Low | Low | Moderate |
| **Primary emotion** | Energetic | Dark/gothic | Cheerful | Atmospheric | Urgent |

---

## 4. Counterpoint in Chiptune

### 4.1 The Constraint: 2-Voice Counterpoint on NES

The NES has 2 monophonic pulse channels plus a monotimbral triangle. True counterpoint is limited to 2 independent voices (Pulse 1 and Pulse 2), with the triangle providing harmonic foundation.

The triangle channel cannot participate actively in counterpoint because:
- No volume control (always on)
- Slow attack (bass notes speak slowly)
- Narrow melodic range (best below C3)
- Must stay in low register to leave space for pulse channels

**Practical result:** Chiptune counterpoint is almost always **2-voice (Pulse 1 + Pulse 2)** with **triangle pedal/harmonic support**.

### 4.2 First Species (Note-Against-Note)

Both pulse channels move in the same rhythm (e.g., quarter notes). The intervals between them should be consonant (3rds, 5ths, 6ths, octaves) on strong beats.

```
Cantus firmus:        C4  D4  E4  F4  G4  A4  G4  F4  E4  D4  C4
Counterpoint (3rds):  E4  F4  G4  A4  B4  C5  B4  A4  G4  F4  E4
Intervals:            M3  m3  M3  M3  M3  M3  M3  M3  m3  m3  M3

All intervals are 3rds -- guaranteed consonant.
The counterpoint provides simple harmonization.
```

### 4.3 Second Species (2:1 Rhythm)

Pulse 1 moves in half notes, Pulse 2 moves in quarter notes. Passing tones (dissonant notes on weak beats) are allowed.

```
Pulse 1 (half notes): C4 . . . E4 . . . G4 . . . C5 . . .
Pulse 2 (quarter):    C4 D4 E4 F4 | G4 F4 E4 D4 | E4 F4 G4 A4 | B4 C5 D5 C5

Intervals on strong beats (beat 1, 3):
  Beat 1: C4+C4  = unison (consonant)
  Beat 3: E4+F4  = 2nd (dissonant -- passing tone)
  Beat 5: G4+E4  = 3rd (consonant)
  Beat 7: C5+E4  = 10th (consonant)

Dissonances on weak beats are acceptable if approached and
left by step (passing tones).
```

### 4.4 Third Species (4:1 Rhythm)

Pulse 1 moves in whole notes, Pulse 2 in quarter notes (or vice versa). Maximum rhythmic activity:

```
Pulse 1 (held):        C4 . . . . . . . | E4 . . . . . . .
Pulse 2 (16th notes):  C4 E4 G4 E4 C4 E4 G4 E4 | (arpeggiating the chord)

This is the standard chiptune arrangement:
  Pulse 1 melody (slow)
  Pulse 2 arpeggio (fast)
  Triangle bass (slow)

The counterpoint is between the held melody notes and
the arpeggio's structural tones (the 1st and 3rd of each group).
```

### 4.5 Call-and-Response Between Pulse Channels

The most idiomatic chiptune counterpoint technique. One channel "calls," the other "responds":

```
Pulse 1 (call): C4 E4 G4 C5 . . . . | . . . . . . . .
Pulse 2 (response): . . . . G3 B3 D4 G4 | G3 B3 D4 G4 . . . .

Bar 3 (call): D4 F4 A4 D5 . . . . |
Bar 4 (response): . . . . A3 C4 E4 A4 |

The response is typically at a lower octave and transposed
to fit the current chord. Common response intervals:
  Response at the 5th (most common for "question/answer")
  Response at the 3rd (for closer harmony)
  Response at the octave (for stronger contrast)
```

### 4.6 Voice Leading Rules for 3-Channel Chiptune

When writing for Pulse 1 + Pulse 2 + Triangle, follow these voice-leading rules:

```
Rule 1: No voice crossing.
  Triangle must always be below Pulse 2, which must always
  be below Pulse 1. Crossing creates muddiness.

  Correct:  Triangle = C2, Pulse 2 = E3, Pulse 1 = G4
  Incorrect: Triangle = C3, Pulse 2 = C2, Pulse 1 = E4

Rule 2: Shared tones between chords should stay on the same channel.
  C major -> G major:
    Pulse 1: E4 -> D4  (step)
    Pulse 2: G3 -> G3  (shared tone, stays)
    Triangle: C2 -> B1 (step down)
  The shared G stays on Pulse 2. Minimal movement = clean voice leading.

Rule 3: Triangle should move in contrary motion to Pulse 1 when possible.
  Pulse 1 ascends -> Triangle descends. This opens the texture.

  C major -> F major:
    Pulse 1: C4 -> F4 (ascending)
    Triangle: C2 -> F1 (descending by octave, but same direction avoided)
    Better: Triangle: C2 -> A1 (descending)

Rule 4: Avoid parallel 5ths and octaves between Pulse channels.
  BAD:
    Pulse 1: C4 -> G4 (parallel 5th)
    Pulse 2: C3 -> G3 (parallel 5th -- both channels move same interval)
  GOOD:
    Pulse 1: C4 -> E4 (move to 3rd)
    Pulse 2: E3 -> C4 (move to root -- contrary motion)
```

### 4.7 Complete 2-Voice Counterpoint Example (8 bars)

```
Key: A minor. Two independent voices on Pulse 1 and Pulse 2.
Triangle provides bass roots.

Bar 1:
  Pulse 1: A4 . . C5 . . . . | (melody)
  Pulse 2: . . E4 . . C4 . . | (counter-melody, 3rds and 6ths)
  Triangle: A2 . . . . . . . | (bass root)

Bar 2:
  Pulse 1: E5 . . D5 . . C5 . | (descending)
  Pulse 2: . . G4 . . A4 . . | (ascending -- contrary motion)
  Triangle: E2 . . . . . . . |

Bar 3:
  Pulse 1: B4 . . . . . . C5 | (suspension-like)
  Pulse 2: G4 . . A4 . . . . |
  Triangle: G2 . . . . . . . |

Bar 4:
  Pulse 1: D5 . . C5 . . . . | (cadence)
  Pulse 2: . . E4 . . . . . . |
  Triangle: G2 . . C3 . . . . | (V -> I cadence)

Note how the voices maintain independence:
- Each has its own rhythm
- They don't move in parallel
- The triangle provides bass foundation
- The counter-melody (Pulse 2) fills the gaps in the melody (Pulse 1)
```

---

## 5. Emotion-to-Music Mapping

### 5.1 Emotion Parameter Table

Each emotion is defined by a combination of musical parameters. Changing one parameter shifts the perceived emotion.

| Parameter | Happy | Tense/Danger | Sad/Melancholy | Heroic | Mysterious |
|-----------|-------|-------------|---------------|--------|------------|
| **Mode** | Major | Minor, Phrygian | Minor | Major, Mixolydian | Dorian, Phrygian, Whole Tone |
| **BPM** | 120-150 | 140-180 | 60-90 | 100-130 | 80-110 |
| **Pulse 1 duty** | 50% (full) | 12.5% (thin, piercing) | 25% (warm) | 50% (full) | 25% (mellow) |
| **Arpeggio speed** | 16th notes | 16th/32nd notes | 8th notes (slow) | Quarter/8th | Slow, irregular |
| **Arpeggio type** | Major triads | Dim/aug, tritone jumps | Minor triads | Major, power chords | Open 5ths, sus chords |
| **Bass pattern** | Root-5th, quarter | Chromatic, 8th notes | Half/whole notes | March rhythm | Pedal tones |
| **Melody shape** | Ascending, small leaps | Chromatic, narrow range | Descending, stepwise | Ascending leaps | Sparse, wide leaps |
| **Articulation** | Staccato | Staccato, accented | Legato, held | Marcato | Legato |
| **Noise usage** | Steady beat | Aggressive, fills | Sparse or absent | March snare | Ambient, irregular |
| **Dynamics** | Even | Loud, accented | Soft | Building | Soft, varied |
| **Harmony** | I-IV-V | i-iio-VII-VI | i-iv-VII | I-bVI-bVII-I | i-bII-bIII |
| **Loop length** | 16-32 bars | 8-16 bars (short) | 16-32 bars | 8-16 bars | 16+ bars |

### 5.2 Happy/Upbeat

**NES recipe for happy:**

```
Key: C major
BPM: 136
Pulse 1 duty: 50%
Melody: Pentatonic-based, ascending leaps, staccato
Pulse 2: 16th-note major arpeggios (12.5% duty for sparkle)
Triangle: Root-5th, quarter notes
Noise: Kick on 1+3, snare on 2+4, open hat on offbeats
Chord loop: | C . . . | G . . . | Am . . . | F . . . |

Example melody phrase:
C4 E4 G4 G4 | A4 G4 E4 C4 | D4 F4 A4 A4 | G4 G4 E4 C4
```

### 5.3 Tense/Danger

**NES recipe for tension:**

```
Key: E Phrygian or A harmonic minor
BPM: 160
Pulse 1 duty: 12.5% (thin, cutting)
Melody: Narrow range (4th-5th), chromatic motion, accented
Pulse 2: Diminished arpeggios at 32nd note speed
Triangle: Chromatic bass, 8th notes
Noise: Snare on every offbeat, 16th note fills
Chord loop: | Am . . . | Bdim . . . | F . . . | E7 . . . |

Example tense phrase:
A4 A4 Bb4 Bb4 | C5 C5 Bb4 Bb4 | A4 A4 G#4 G#4 | A4 A4 . . |
```

### 5.4 Sad/Melancholy

**NES recipe for sadness:**

```
Key: A minor (natural minor)
BPM: 70
Pulse 1 duty: 25% (warm, flute-like)
Melody: Descending stepwise, long held notes, legato
Pulse 2: Slow arpeggio, 8th notes, minor chords
Triangle: Whole notes, root emphasis
Noise: Very sparse or absent (hi-hat on 2 and 4, quiet)
Chord loop: | Am . . . | F . . . | C . . . | G . . . |

Example sad phrase:
A4 . . C5 . . . | E5 . . . . . . | D5 . . C5 . . . | A4 . . . . . .
```

### 5.5 Heroic

**NES recipe for heroism:**

```
Key: C major or G Mixolydian
BPM: 120
Pulse 1 duty: 50% (full, trumpet-like)
Melody: Ascending arpeggios, wide leaps (octaves, 5ths), fanfare rhythms
Pulse 2: Sustained chords (not arpeggiated -- spread across triangle)
Triangle: March rhythm (dotted quarter + 8th)
Noise: March snare (16th note rolls on accented beats)
Chord loop: | C . . . | F . . . | G . . . | C . . . |
Special cadence: | Ab . . . | Bb . . . | C . . . | C . . . |
  (bVI-bVII-I "Mario Cadence")

Example heroic phrase:
C4 E4 G4 C5 | C5 . . . . . . | G4 B4 D5 G5 | G5 . . . . . .
```

### 5.6 Mysterious

**NES recipe for mystery:**

```
Key: D Dorian or E Phrygian
BPM: 90
Pulse 1 duty: 25% (mellow)
Melody: Sparse, wide leaps (7ths, 9ths), long rests between phrases
Pulse 2: Open 5th arpeggios (no 3rd -- ambiguous tonality)
Triangle: Pedal drone (single note held for 4+ bars)
Noise: Irregular, quiet -- wind-like texture
Chord loop: | Dm . . . | . . . . | G . . . | . . . . |
  (minimal chord movement, long pedals)

Example mysterious phrase:
D4 . . . . . . . | . . G4 . . . . . | B4 . . . . . . . | A4 . . . . . . .
```

### 5.7 Emotion Transition Diagram

How to shift emotion gradually:

```
HAPPY (C major, 136 BPM)
  |-- Slow down to 100 BPM
  |-- Shift to A minor
  |-- Lengthen note values
  v
SAD (A minor, 70 BPM)
  |-- Speed up to 140 BPM
  |-- Switch to 12.5% duty
  |-- Add chromatic bass
  |-- Shorten note values
  v
TENSE (A harmonic minor, 160 BPM)
  |-- Add bVI-bVII chords
  |-- Switch to 50% duty
  |-- March rhythm on bass
  |-- Ascending melody
  v
HEROIC (C major / G Mixolydian, 120 BPM)
  |-- Remove percussion
  |-- Slow arpeggios
  |-- Add pedal drone
  |-- Sparse melody
  v
MYSTERIOUS (D Dorian, 90 BPM)
  |-- Brighten to major
  |-- Speed up
  |-- Add percussion
  v
HAPPY (back to start)
```

---

## 6. Real NES Game Music Transcriptions

### 6.1 Super Mario Bros. - Overworld Theme (Koji Kondo, 1985)

**Key:** C major (with mode mixture)
**BPM:** ~136 (cut time, notated here in 4/4 for clarity)
**Structure:** 32-bar loop (A-A-B-B-C-D)

#### Pulse 1 (Melody) - First 4 Bars

```
Bar 1: C4 E4 G4 C5 | E5 C5 G4 E4 |
Bar 2: C4 E4 G4 C5 | G4 G4 E4 . |
Bar 3: C4 F4 A4 C5 | F5 C5 A4 F4 |
Bar 4: C4 F4 A4 C5 | C5 C5 A4 . |
```

#### Pulse 2 (Harmony/Arpeggio)

```
Bar 1: C3 E3 G3 E3 | C3 E3 G3 E3 |
Bar 2: C3 E3 G3 E3 | C3 E3 G3 . |
Bar 3: C3 F3 A3 F3 | C3 F3 A3 F3 |
Bar 4: C3 F3 A3 F3 | C3 F3 A3 . |

16th-note arpeggios cycling root-3rd-5th-3rd.
```

#### Triangle (Bass) - Full 8-Bar Phrase

```
Bar 1: C2 . G1 . | C2 . G1 . |
Bar 2: C2 . G1 . | C2 . C2 . |
Bar 3: C2 . A1 . | F1 . C2 . |
Bar 4: F1 . D1 . | G1 . . . |

Quarter-note root/fifth alternation. The last bar
of each 4-bar phrase ends on a held G (dominant) to lead
back to C.
```

#### Noise (Percussion)

```
Standard pattern across all bars:
| 1  &  2  &  3  &  4  & |
| K  .  S  .  K  .  S  . |

K = noise mode 0, period 2 (short bass burst)
S = noise mode 1, period 4 (snare-like)
```

#### Important Chord Changes (B Section)

The B section introduces the famous borrowed chords:

```
Pulse 1 melody:
Bar 9:  C4 C4 E4 E4 | G4 G4 . . |
Bar 10: C4 C4 E4 E4 | G4 G4 . . |
Bar 11: C4 C4 E4 E4 | Ab4 Ab4 . . |
Bar 12: Bb4 Bb4 G4 G4 | C4 . . . |

Triangle bass:
Bar 9:  C2 . G1 . | C2 . G1 . |
Bar 10: C2 . G1 . | C2 . . . |
Bar 11: Ab1 . . . | Ab1 . . . |
Bar 12: Bb1 . . . | C2 . . . |

Bar 12's bass notes: Ab1 - Bb1 - C2 (the "Mario Cadence").
This is the bVI-bVII-I progression in action.
```

### 6.2 The Legend of Zelda - Overworld Theme (Koji Kondo, 1986)

**Key:** Bb major (with heavy mode mixture)
**BPM:** ~120
**Structure:** 8-bar phrase, repeated with variations

#### Pulse 1 (Melody) - Main 8-Bar Phrase

```
Bar 1: F4 F4 G4 F4 | Eb4 F4 Bb3 . |
Bar 2: F4 F4 G4 F4 | D4 F4 Bb3 . |
Bar 3: Eb4 Eb4 F4 Eb4 | C4 Eb4 Bb3 . |
Bar 4: D4 D4 Eb4 D4 | C4 . Bb3 . |
Bar 5: Bb3 Bb3 C4 Bb3 | Ab3 Bb3 F3 . |
Bar 6: Bb3 Bb3 C4 Bb3 | G3 Bb3 F3 . |
Bar 7: Bb3 Bb3 C4 Bb3 | D4 C4 Bb3 . |
Bar 8: F4 . Bb4 F4 | D4 Bb3 F3 . |
```

#### Triangle (Bass) - Descending Whole-Step Pattern

```
Bar 1: Bb1 . . . | Bb1 . . . |
Bar 2: A1 . . . | A1 . . . |
Bar 3: G1 . . . | G1 . . . |
Bar 4: F1 . . . | F1 . . . |
Bar 5: Eb1 . . . | Eb1 . . . |
Bar 6: D1 . . . | D1 . . . |
Bar 7: C1 . . . | C1 . . . |
Bar 8: F1 . . . | F1 . . . |

The bass descends by whole step: Bb -> Ab -> Gb -> F -> Eb -> D -> C -> F.
This descending bass is the harmonic foundation of the entire theme.
The borrowed chords come from the bass movement through the parallel minor.
```

#### Harmony (Implied Chords from the Voice Leading)

```
Bar 1: Bb major (I)
Bar 2: Fm/Ab (v6 -- borrowed from Bb minor)
Bar 3: Gb major (bVI -- borrowed)
Bar 4: Db major (bIII -- borrowed, tonicization)
Bar 5: Cb major (bVII -- dark, far from home)
Bar 6: Bbm (vi -- the emotional low point)
Bar 7: C major (V/V -- secondary dominant, the turnaround)
Bar 8: F major (V -- dominant, leading back to Bb)
```

### 6.3 Mega Man 2 - Flash Man Stage (Takashi Tateishi, 1988)

**Key:** F# minor (rock battle in a minor key)
**BPM:** ~140
**Structure:** 16-bar loop

#### Pulse 1 (Melody) - Main Hook (First 4 Bars)

```
Bar 1: C#5 D5 E5 D5 | C#5 B4 A4 B4 |
Bar 2: C#5 D5 E5 D5 | C#5 E5 . . |
Bar 3: D5 E5 F#5 E5 | D5 C#5 B4 C#5 |
Bar 4: D5 E5 F#5 E5 | D5 . . . |
```

#### Pulse 2 (Arpeggio Harmony)

```
Arpeggiating the F#m chord (F#, A, C#) in 16th notes:
Bar 1-2: F#4 A4 C#5 A4 | repeating
Bar 3-4: D5 pattern (D major arpeggio for IV chord)

When the harmony moves to D major (bar 3-4):
| D4 F#4 A4 F#4 | D4 F#4 A4 F#4 |
```

#### Triangle (Bass)

```
Driving 8th-note rock bass:
| F#2 . F#2 . A2 . A2 . | C#2 . C#2 . E2 . E2 . |
| F#2 . F#2 . A2 . A2 . | C#2 . C#2 . . . . . |
| D2 . D2 . F#2 . F#2 . | A2 . A2 . C#2 . C#2 . |
| D2 . D2 . F#2 . F#2 . | . . . . . . . . |
```

#### Noise (Drums)

```
Standard Mega Man rock beat:
| 1  &  2  &  3  &  4  & |
| K  .  S  .  K  .  S  . |
| .  H  .  H  .  H  .  H |

K = triangle kick (E2 with pitch bend down)
S = noise mode 0, period 4-5
H = noise mode 1, period 2 (short, quiet)
```

### 6.4 Castlevania - "Vampire Killer" (Kinuyo Yamashita, 1986)

**Key:** D minor
**BPM:** ~130
**Structure:** 16-bar loop (A-B)

#### Pulse 1 (Melody) - Main Hook

```
Bar 1: D5 . . . | A4 . . . |
Bar 2: Bb4 . C5 . | D5 . . . |
Bar 3: D5 . . . | E5 . . . |
Bar 4: F5 . E5 . | D5 . . . |
Bar 5: F5 F5 F5 F5 | E5 E5 E5 E5 |
Bar 6: D5 D5 D5 D5 | C5 C5 C5 C5 |
Bar 7: Bb4 . Bb4 . | Bb4 . . . |
Bar 8: A4 . . . | . . . . |
```

#### Pulse 2 (Harmony - Baroque Voice Leading)

```
Bar 1: D4 F4 | A3 E4 |
Bar 2: D4 F4 | F4 G4 A4 |
Bar 3: D4 F4 | A3 E4 |
Bar 4: Bb3 D4 | A3 F4 |
Bar 5: A3 D4 F4 | G3 C4 E4 |
Bar 6: F3 Bb3 D4 | E3 A3 C4 |
Bar 7: D3 G3 Bb3 | D3 G3 Bb3 |
Bar 8: C#3 E3 A3 | (leading to D minor cadence)
```

#### Triangle (Bass)

```
Bar 1: D2 . A1 . | D2 . A1 . |
Bar 2: D2 . A1 . | D2 . A1 . |
Bar 3: D2 . A1 . | D2 . A1 . |
Bar 4: D2 . A1 . | D2 . A1 . |
Bar 5: D2 . C2 . | Bb1 . A1 . |
Bar 6: G1 . F1 . | E1 . D1 . |
Bar 7: G1 . G1 . | G1 . G1 . |
Bar 8: A1 . A1 . | A1 . . . |
```

### 6.5 Final Fantasy I - "Battle Scene" (Nobuo Uematsu, 1987)

**Key:** E minor
**BPM:** ~145
**Structure:** 16-bar loop

#### Pulse 1 (Melody) - Battle Theme

```
Bar 1: E4 . . . | B4 B4 . . |
Bar 2: D5 . C5 . | B4 . . . |
Bar 3: E4 . . . | G4 G4 . . |
Bar 4: A4 . G4 . | E4 . . . |
Bar 5: G4 G4 G4 G4 | A4 A4 A4 A4 |
Bar 6: B4 B4 B4 B4 | C5 C5 C5 C5 |
Bar 7: D5 D5 D5 D5 | C5 C5 C5 C5 |
Bar 8: B4 . . . | B4 . . . |
```

#### Pulse 2 (Arpeggio Harmony)

```
Bar 1-2: E4 G4 B4 G4 | (Em arpeggio loop)
Bar 3-4: E4 G4 B4 G4 | (same)
Bar 5-6: G4 B4 D5 B4 | (G major - bIII)
Bar 7-8: A4 C5 E5 C5 | (A major - IV, with raised 3rd)

The harmony stays on Em for the first phrase (bars 1-4),
then jumps to G major (bIII) and A major (IV) for contrast.
```

#### Triangle (Bass - Driving 8th Notes)

```
Bar 1: E1 E1 E1 E1 | B0 B0 B0 B0 |
Bar 2: E1 E1 E1 E1 | B0 B0 B0 B0 |
Bar 3: E1 E1 E1 E1 | B0 B0 B0 B0 |
Bar 4: E1 E1 E1 E1 | B0 B0 B0 B0 |
Bar 5: G1 G1 G1 G1 | G1 G1 G1 G1 |
Bar 6: A1 A1 A1 A1 | A1 A1 A1 A1 |
Bar 7: B1 B1 B1 B1 | B1 B1 B1 B1 |
Bar 8: B1 B1 B1 B1 | B1 B1 B1 B1 |
```

### 6.6 Transcription Summary Table

| Game | Track | Key | BPM | Structure | Notable Technique |
|------|-------|-----|-----|-----------|-------------------|
| Super Mario Bros. | Overworld | C major (+ borrowed) | 136 | ABCD 32-bar | Mode mixture, open voicing, two-against-three |
| Legend of Zelda | Overworld | Bb major (+ borrowed) | 120 | 8-bar phrase | Descending whole-step bass, modal mixture |
| Mega Man 2 | Flash Man | F# minor | 140 | 16-bar AB | Driving 8th-note bass, rock beat, blues tinges |
| Castlevania | Vampire Killer | D minor | 130 | 16-bar AB | Baroque voice leading, gothic arpeggios |
| Final Fantasy I | Battle Scene | E minor | 145 | 16-bar loop | Half-cadence loop, arpeggio harmony, driving bass |

---

## References

- Schartmann, Andrew. *33 1/3: Koji Kondo's Super Mario Bros. Soundtrack*. Bloomsbury, 2015.
- Schartmann, Andrew. *Analyzing NES Music: Harmony, Form, and the Art of Technological Constraint*. Intellect Books, 2025.
- Anatone, Richard (ed.). *The Music of Nobuo Uematsu in the Final Fantasy Series*. 2022.
- Fox, James Anthony. "It's a-me, Mario!" University of Huddersfield, 2016.
- "Song Forms, Rock Tropes, and Metaphors for Listening to the Mega Man Series 1987-1993." University of Michigan, 2018.
- Tanaka, Hirokazu. Interviews and writings on NES sound design. Nintendo World Report, nintendoworldreport.com.
- NESdev Wiki (nesdev.org) -- 2A03 APU technical documentation.
- FamiTracker documentation and community forums (famitracker.com).
- Splice Blog -- "How the Overworld Theme of The Legend of Zelda Takes Us On a Harmonic Adventure."
- Hardcore Gaming 101 -- "A Look at the Music of Castlevania" by Paul Esch.
- Video Game Music Shrine -- "Inside the Score: Super Mario All-Stars Ground Theme."
- NESdev BBS -- "Techniques You've Found on Your Own" (forum thread, 2010).
- ChipMusic.org forums -- Community chiptune knowledge base.
- Video Game Music Preservation Foundation (vgmpf.com) -- Track analysis and technical details.
- NinSheetMusic.org -- NES game sheet music transcriptions.
- MelodicNotes.com -- Chiptune melody transcriptions.
- Library of Congress. National Recording Registry essay on Super Mario Bros. theme, 2023.
