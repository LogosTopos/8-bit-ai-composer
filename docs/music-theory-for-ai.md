# 8-Bit / Chiptune Music Theory Reference for AI Composition

> Compiled for an 8-bit music composition AI project.
> Target platform: NES (Ricoh 2A03 APU) and similar chiptune hardware.
> Date: 2026-05-24

---

## Table of Contents

1. [Common Scales in 8-Bit / Chiptune Music](#1-common-scales-in-8-bit--chiptune-music)
2. [Rhythm Patterns for Different Game Music Styles](#2-rhythm-patterns-for-different-game-music-styles)
3. [8-Bit Specific Techniques](#3-8-bit-specific-techniques)
4. [Chord Progressions](#4-chord-progressions)
5. [Song Structure for Game Music](#5-song-structure-for-game-music)
6. [Appendix: NES Hardware Reference](#6-appendix-nes-hardware-reference)

---

## 1. Common Scales in 8-Bit / Chiptune Music

All scales are expressed as interval patterns (W = whole step = 2 semitones, H = half step = 1 semitone) from the root, with concrete examples in the most common tuning (C as tonic).

### 1.1 Major Scale (Ionian Mode)

| Property | Value |
|----------|-------|
| Formula | R - W - W - H - W - W - W - H |
| Notes in C Major | C4, D4, E4, F4, G4, A4, B4, C5 |
| Notes in G Major (upbeat) | G3, A3, B3, C4, D4, E4, F#4, G4 |
| Typical 8-bit use | Upbeat platformer overworld themes, title screens, victory themes |

**Use case in 8-bit:** C major is the default "happy" key. Used in Super Mario Bros. overworld, Mega Man stage select, and most NES platformer level themes. The lack of sharps/flats makes it the easiest key for simple melodic writing on pulse channels.

**Example melody fragment (C major, platformer style):**
```
C4 E4 G4 G4 | A4 G4 E4 C4 | D4 F4 A4 A4 | G4 E4 C4
```

### 1.2 Natural Minor Scale (Aeolian Mode)

| Property | Value |
|----------|-------|
| Formula | R - W - H - W - W - H - W - W |
| Notes in A Minor (relative minor of C) | A3, B3, C4, D4, E4, F4, G4, A4 |
| Notes in D Minor | D3, E3, F3, G3, A3, Bb3, C4, D4 |
| Typical 8-bit use | Dungeon themes, dark forest, sad scenes, tense exploration |

**Use case in 8-bit:** A minor is the most common minor key in NES music (no sharps/flats). Used in Castlevania stage themes, Metroid exploration music, and dark dungeon areas in Zelda.

**Example melody fragment (A minor, dungeon style):**
```
A3 C4 E4 F4 | E4 C4 A3 G3 | F3 E3 D3 E3 | A3 rest
```

### 1.3 Harmonic Minor Scale

| Property | Value |
|----------|-------|
| Formula | R - W - H - W - W - H - 1.5 - H |
| Notes in A Harmonic Minor | A3, B3, C4, D4, E4, F4, G#4, A4 |
| Typical 8-bit use | Boss battles, dramatic reveals, Middle Eastern/exotic themes |

**Use case in 8-bit:** The raised 7th (G# in A minor) creates a strong pull to the tonic. Used for dramatic boss intros and tension-building sections. The augmented 2nd interval between F and G# gives an "exotic" sound.

**Example (A harmonic minor, boss intro):**
```
A3 E4 A4 G#4 | A4 G#4 F4 E4 | D4 C4 B3 G#3 | A3 rest
```

### 1.4 Major Pentatonic Scale

| Property | Value |
|----------|-------|
| Formula | R - W - W - 1.5 - W - 1.5 |
| Notes in C Major Pentatonic | C4, D4, E4, G4, A4, C5 |
| Typical 8-bit use | Overworld themes, cheerful town themes, victory fanfares |

**Use case in 8-bit:** The most "foolproof" scale for chiptune. Because there are no half-step intervals, any sequence of notes sounds consonant. Extremely common in early NES titles where composers had limited time. Can be played over most chords in the key without clashing.

**Example arpeggio pattern (C major pentatonic, ascending/descending):**
```
C4 E4 G4 A4 C5 A4 G4 E4 | D4 F4 A4 C5 D5 C5 A4 F4
```

### 1.5 Minor Pentatonic Scale

| Property | Value |
|----------|-------|
| Formula | R - 1.5 - W - W - 1.5 - W |
| Notes in A Minor Pentatonic | A3, C4, D4, E4, G4, A4 |
| Typical 8-bit use | Sneaking/stealth themes, underwater levels, melancholy scenes |

**Use case in 8-bit:** Like major pentatonic but darker. The missing 2nd and 6th degrees (B and F in A minor) remove the most tense intervals, giving a smooth, bluesy feel. Works well with minor chord arpeggios.

### 1.6 Blues Scale

| Property | Value |
|----------|-------|
| Formula | R - 1.5 - W - H - H - 1.5 - W |
| Notes in A Blues | A3, C4, D4, D#4, E4, G4, A4 |
| Typical 8-bit use | Character themes, "cool" stage themes, action sequences |

**Use case in 8-bit:** The flat 5th (D# in A blues, also called the "blue note") adds gritty tension. Used sparingly in NES music for solos and character themes. Mega Man series used blues-tinged lines in many stage themes.

### 1.7 Chromatic Scale

| Property | Value |
|----------|-------|
| Formula | H - H - H - H - H - H - H - H - H - H - H - H |
| Notes in C Chromatic | C4, C#4, D4, D#4, E4, F4, F#4, G4, G#4, A4, A#4, B4, C5 |
| Typical 8-bit use | Descending basslines, transition effects, spooky/dissonant passages |

**Use case in 8-bit:** Not typically a primary scale, but used for chromatic passing tones in basslines (e.g., walking bass: C4 B3 Bb3 A3) and tension-building slides. The famous Super Mario Bros. underground theme uses chromatic movement.

**Example chromatic bass walk:**
```
C3 B2 Bb2 A2 | G2 F#2 F2 E2 | (descending)
```

### 1.8 Whole Tone Scale

| Property | Value |
|----------|-------|
| Formula | W - W - W - W - W - W |
| Notes in C Whole Tone | C4, D4, E4, F#4, G#4, A#4, C5 |
| Typical 8-bit use | Dream sequences, magical effects, puzzle themes |

**Use case in 8-bit:** Rarely used as a primary scale in NES music due to its ambiguous tonality (no leading tone). Appears in short magical transitions or "mysterious" passages. The lack of a perfect 5th makes it feel floating/unstable.

### 1.9 Dorian Mode

| Property | Value |
|----------|-------|
| Formula | R - W - H - W - W - W - H - W |
| Notes in D Dorian (on C: same as C major starting on D) | D4, E4, F4, G4, A4, B4, C5, D5 |
| Comparison to natural minor | Dorian has a raised 6th (B instead of Bb in D Dorian vs D natural minor) |
| Typical 8-bit use | Adventure/RPG themes, town themes with a wistful feel, exploration |

**Use case in 8-bit:** The raised 6th gives Dorian a minor tonality that is less sad than natural minor. Used in many RPG overworld themes (e.g., Dragon Quest). Good for "bittersweet adventure" moods.

**Example (D Dorian, RPG overworld style):**
```
D4 F4 G4 A4 | A4 B4 C5 D5 | D5 C5 B4 A4 | G4 F4 D4
```

### 1.10 Phrygian Mode

| Property | Value |
|----------|-------|
| Formula | R - H - W - W - W - H - W - W |
| Notes in E Phrygian | E4, F4, G4, A4, B4, C5, D5, E5 |
| Comparison to natural minor | Phrygian has a flat 2nd (F instead of F# in E Phrygian vs E natural minor) |
| Typical 8-bit use | Castle/dungeon themes, dark areas, "foreign"/exotic locations |

**Use case in 8-bit:** The flat 2nd degree creates a dark, Middle Eastern/Mediterranean flavor. Used in Castlevania for castle interior themes. The half-step between root and flat 2nd (E-F) is immediately recognizable.

**Example (E Phrygian, dark castle theme):**
```
E4 F4 E4 B3 | C4 B3 A3 G3 | A3 B3 C4 D4 | E4 F4 E4 rest
```

### 1.11 Mixolydian Mode

| Property | Value |
|----------|-------|
| Formula | R - W - W - H - W - W - H - W |
| Notes in G Mixolydian | G4, A4, B4, C5, D5, E5, F5, G5 |
| Comparison to major | Mixolydian has a flat 7th (F instead of F# in G Mixolydian vs G major) |
| Typical 8-bit use | Victory fanfares, heroic themes, upbeat action sequences |

**Use case in 8-bit:** The flat 7th gives Mixolydian a "dominant" feel -- less resolved than pure major. The Final Fantasy victory fanfare is in Eb Mixolydian. Creates an energetic, slightly bluesy heroic sound.

**Example (G Mixolydian, victory fanfare):**
```
G4 B4 D5 F5 | G5 F5 D5 B4 | G5 D5 B4 G4 | F4 D4 B3 G3
```

### 1.12 Scale Selection Quick Reference

| Desired Mood | Recommended Scale(s) | Key Examples |
|---|---|---|
| Cheerful/upbeat | Major, Major Pentatonic | C Major, G Major |
| Heroic/adventurous | Mixolydian, Major | G Mixolydian, C Major |
| Sad/melancholy | Natural Minor, Minor Pentatonic | A Minor, D Minor |
| Dark/tense | Harmonic Minor, Phrygian | A Harmonic Minor, E Phrygian |
| Mysterious/magical | Whole Tone, Chromatic | C Whole Tone |
| Bittersweet/adventure | Dorian | D Dorian |
| Exotic/foreign | Phrygian, Harmonic Minor | E Phrygian, A Harmonic Minor |
| Bluesy/cool | Blues Scale, Mixolydian | A Blues, G Mixolydian |
| Sneaky/stealth | Minor Pentatonic, Chromatic | A Minor Pentatonic |

---

## 2. Rhythm Patterns for Different Game Music Styles

### 2.1 Platformer Overworld (Upbeat, Adventurous)

| Parameter | Value |
|-----------|-------|
| BPM | 120-150 (typical: 136 for Super Mario Bros.) |
| Time signature | 4/4 (almost always) |
| Feel | Straight 8th notes (not swung) |
| Typical length | 16-32 bars before loop |

**Rhythmic pattern example (pulse channel 1 - melody, 4/4):**
```
| 1  e  &  a  2  e  &  a  3  e  &  a  4  e  &  a |
| C4 .  .  C4  .  E4 .  .  G4 .  .  G4  .  .  .  |
| (8th notes with rests for rhythmic bounce)      |
```

**Pulse 2 (arpeggio/harmony) pattern:**
```
| 1  &  2  &  3  &  4  & |
| C4 E4 G4 E4 C4 G4 E4 C4 |
| (16th note arpeggio)     |
```

**Triangle (bass) pattern:**
```
| 1  .  .  .  2  .  .  .  3  .  .  .  4  .  .  . |
| C2 .  .  .  G1 .  .  .  E1 .  .  .  C2 .  .  . |
| (quarter notes, root on 1 and 3, fifth on 2, third on 3) |
```

**Noise (percussion) pattern:**
```
| 1  &  2  &  3  &  4  & |
| K  .  S  .  .  .  S  . |
| K = noise mode 15 (short burst, kick-like)
| S = noise mode 1 (longer burst, snare-like)
```

### 2.2 Dungeon / Boss Battle (Tense, Driving)

| Parameter | Value |
|-----------|-------|
| BPM | 140-180 (boss), 120-150 (dungeon) |
| Time signature | 4/4 or 6/8 |
| Feel | Straight 8ths or driving 16ths |
| Typical length | 16-32 bars with variation loops |

**Rhythmic pattern for boss (4/4, fast):**
```
Pulse 1 (melody):
| 1  e  &  a  2  e  &  a  3  e  &  a  4  e  &  a |
| A4 A4 A4 A4  G4 G4 G4 G4  F4 F4 F4 F4  E4 E4 E4 E4 |
| (steady 16th notes, aggressive)                    |

Triangle (bass, driving 8ths):
| 1  &  2  &  3  &  4  & |
| A1 A1 A1 A1 E1 E1 E1 E1 |
| (staccato 8th notes, fast root-fifth alternation)  |

Noise (driving pattern):
| 1  e  &  a  2  e  &  a  3  e  &  a  4  e  &  a |
| K  .  S  .  K  .  S  .  K  .  S  .  K  .  S  . |
| (kick on 1 and 3, snare on every 8th note offbeat) |
```

**6/8 dungeon pattern:**
```
Count: | 1  2  3  4  5  6 | 1  2  3  4  5  6 |
Pulse 1: | A . . . . . | E . . . . . |  (long notes, tense)
Triangle: | A1 A1 A1 E1 E1 E1 | (droning 8ths in groups of 3)
Noise:    | K . . S . . | K . . S . . | (kick on 1, snare on 4)
```

### 2.3 Town / Village (Relaxed, Peaceful)

| Parameter | Value |
|-----------|-------|
| BPM | 80-110 |
| Time signature | 4/4 or 3/4 |
| Feel | Relaxed, may use light swing |
| Typical length | 24-32 bars before loop |

**Rhythmic pattern (4/4, relaxed):**
```
Pulse 1 (melody - mostly half and quarter notes):
| 1  .  2  .  3  .  4  . |
| C4 .  E4 .  G4 .  .  . |
| A4 .  G4 .  E4 .  C4 . |

Pulse 2 (gentle arpeggio, slower - 8th notes):
| 1  &  2  &  3  &  4  & |
| C4 E4 G4 E4 C4 E4 G4 E4 |

Triangle (bass - half notes):
| 1  .  .  .  2  .  .  .  3  .  .  .  4  .  .  . |
| C2 .  .  .  .  .  .  .  G1 .  .  .  .  .  .  . |

Noise: sparse or absent (maybe light hi-hat on 2 and 4)
| 1  &  2  &  3  &  4  & |
| .  .  H  .  .  .  H  . |
```

### 2.4 Victory Fanfare

| Parameter | Value |
|-----------|-------|
| BPM | 120-140 |
| Time signature | 4/4 |
| Feel | Triumphant, call-to-action |
| Typical length | 4-8 bars (short) |

**Example (Final Fantasy style, C major / G Mixolydian):**
```
Triad harmonization (3 pulse channels if available, or arpeggiated):
Bar 1: C5 E5 G5  (hold)  |  G4 B4 D5  (hold)
Bar 2: A4 C5 E5  (hold)  |  G4 B4 D5  (hold)
Bar 3: C5 E5 G5  (hold)  |  F4 A4 C5  (hold)
Bar 4: G4 B4 D5  (hold)  |  C5 (long)

Triangle: roots held as whole notes: C - G - A - G - C - F - G - C
Noise: fanfare-style drum roll (16th note snare rolls on last bar)
```

**The "Mario Cadence" fanfare (bVI - bVII - I):**
```
Chords: A♭ major -> B♭ major -> C major (in C major)
Notes:  A♭4 C5 E♭5 | B♭4 D5 F5 | C5 E5 G5 (sustained)
```

### 2.5 Title Screen

| Parameter | Value |
|-----------|-------|
| BPM | 100-130 |
| Time signature | 4/4 |
| Feel | Majestic, establishing, loopable |
| Typical length | 16-32 bars, often with intro lead-in |

**Example structure:**
```
Intro (4 bars): Single pulse channel playing main melody hook
Build (4 bars): Add triangle bass
Full (8 bars): All channels, melody + arpeggios + bass + percussion
Loop back to bar 5 or bar 9
```

### 2.6 Sad / Emotional Scene

| Parameter | Value |
|-----------|-------|
| BPM | 60-80 |
| Time signature | 4/4 or 3/4 |
| Feel | Sparse, slow, breathing room |
| Typical length | 8-16 bars |

**Example (A minor, 70 BPM, 4/4):**
```
Pulse 1 (slow melody - mostly half and whole notes):
| 1  .  2  .  3  .  4  . |
| A4 .  .  .  C5 .  .  . |
| E5 .  .  .  .  .  .  . |
| D5 .  .  .  C5 .  .  . |
| A4 .  .  .  .  .  .  . |

Pulse 2 (slow arpeggio, half speed):
| 1  .  2  .  3  .  4  . |
| A3 E4 A4 E4 A3 E4 A4 E4 |

Triangle (bass - whole notes):
| 1  .  .  .  2  .  .  .  3  .  .  .  4  .  .  . |
| A1 .  .  .  .  .  .  .  E1 .  .  .  .  .  .  . |

Noise: hi-hat on 2 and 4, very quiet (low volume)
```

### 2.7 Rhythm Pattern Quick Reference

| Music Type | BPM | Time Sig | Typical Patterns |
|------------|-----|----------|-----------------|
| Platformer Overworld | 120-150 | 4/4 | Straight 8th melody, 16th arpeggios, quarter note bass |
| Dungeon | 120-150 | 4/4 or 6/8 | Driving 8ths, droning bass, sparse but tense |
| Boss Battle | 140-180 | 4/4 or 6/8 | Aggressive 16th melodies, fast bass 8ths, heavy percussion |
| Town/Village | 80-110 | 4/4 or 3/4 | Relaxed half/quarter notes, gentle arpeggios |
| Victory Fanfare | 120-140 | 4/4 | Long sustained chords, triad harmonization, trumpet-like |
| Title Screen | 100-130 | 4/4 | Majestic, building, memorable hook |
| Sad/Emotional | 60-80 | 4/4 or 3/4 | Slow sparse notes, whole/half note melodies |

---

## 3. 8-Bit Specific Techniques

### 3.1 Arpeggios (Rapid Chord Simulation)

Arpeggiation is the single most important technique in chiptune. Since the NES has only 2 monophonic pulse channels, arpeggios simulate chords by rapidly cycling through chord tones.

**Standard arpeggio speed:** 16th notes at 120-150 BPM (or faster for "tremolo" arpeggios)

**Major chord arpeggio pattern (C major: C4, E4, G4):**
```
Time:   1   e   &   a   2   e   &   a   3   e   &   a   4   e   &   a
Notes:  C4  E4  G4  E4  C4  E4  G4  E4  C4  E4  G4  E4  C4  E4  G4  E4
        (root-3rd-5th-3rd repeating = the most common pattern)
```

**Major chord arpeggio, inversion patterns:**
```
Root position: C4  E4  G4  C5  (cycle)
First inversion: E4  G4  C5  E5  (cycle - softer sound)
Second inversion: G4  C5  E5  G5  (cycle - open, less stable)
```

**Minor chord arpeggio (A minor: A3, C4, E4):**
```
Time:   1   e   &   a   2   e   &   a
Notes:  A3  C4  E4  C4  A3  C4  E4  C4
```

**Two-octave arpeggio (Tim Follin style - rapid wide arpeggios):**
```
C3  E3  G3  C4  E4  G4  C5  G4  E4  C4  G3  E3  C3
(ascending through 2+ octaves then descending back)
```

**Seventh chord arpeggio (C7: C4, E4, G4, Bb4):**
```
C4  E4  G4  Bb4  C5  Bb4  G4  E4  (cycle)
```

**Arpeggio duty cycling technique:** Change the pulse wave duty cycle during different passes through the arpeggio to simulate "different instruments" playing the chord tones.

### 3.2 Pulse Width Modulation (Duty Cycle Control)

The NES pulse channels have 4 selectable duty cycles that control the timbre:

| Duty Cycle | Waveform Shape | Sound Character | Common Use |
|------------|---------------|-----------------|------------|
| 12.5% | Narrow pulse | Thin, nasal, reedy | Lead melody, bright arpeggios, fast passages |
| 25% | Medium pulse | Balanced, flute-like | Harmony, counter-melody |
| 50% | Square wave | Full, rich, fat | Bass, power chords, main melody |
| 75% | Medium pulse (mirror of 25%) | Same as 25% (identical on NES) | Same as 25% |

**Technique: duty cycle per note.** Change the duty cycle on each successive note or phrase for timbral variation without changing pitch:

```
Phrase 1 (50% duty - full sound):
C4(50%) D4(50%) E4(50%) F4(50%) | G4(50%) A4(50%) B4(50%) C5(50%)

Phrase 2 (12.5% duty - thin, contrast):
C5(12.5%) B4(12.5%) A4(12.5%) G4(12.5%) | F4(12.5%) E4(12.5%) D4(12.5%) C4(12.5%)
```

**Technique: duty cycle sweep.** Change duty on every 4th note or every bar for a "shimmer" effect. This was used extensively in Sunsoft games.

**Technique: rapid duty switching.** Alternate between 12.5% and 50% on each 16th note within an arpeggio to create a "stereo" or "dual timbre" illusion:
```
Time: 1  e  &  a   | 2  e  &  a
Duty: 50 12 50 12 | 50 12 50 12
Note: C4 E4 G4 E4 | C4 E4 G4 E4
```

### 3.3 Noise Channel for Percussion

The NES noise channel uses a pseudo-random number generator (LFSR) to produce various noise timbres:

| Noise Mode | Period Value | Sound | 8-bit Use |
|-----------|-------------|-------|-----------|
| Long (mode 0) | Low (1-3) | Lo-fi bassy noise | Kick drum, explosions |
| Long (mode 0) | Medium (4-8) | White noise hiss | Snare drum, cymbal |
| Long (mode 0) | High (9-15) | Bright noise | Hi-hat, shaker |
| Short (mode 1) | Low (1-3) | Metallic noise | Closed hi-hat, claves |
| Short (mode 1) | Medium (4-8) | Pitched noise | Tom-tom, electronic snare |

**Standard 8-bit drum kit mapping (FamiTracker convention):**

| Drum Sound | Channel | Note | Technique |
|-----------|---------|------|-----------|
| Kick drum | Triangle | E3 (or C3) | Sharp pitch bend down from higher note |
| Snare drum | Noise | Mode 0, period ~4-6 | Loud burst, short length |
| Closed hi-hat | Noise | Mode 1, period ~1-3 | Very short burst, quiet |
| Open hi-hat | Noise | Mode 0, period ~8-12 | Longer burst with volume decay |
| Crash cymbal | Noise | Mode 0, period ~15 | Long burst |

**Common drum patterns for 8-bit:**

Standard rock beat (120 BPM, 4/4):
```
| 1  &  2  &  3  &  4  & |
| K  .  S  .  K  .  S  . |
K = triangle kick (E3, pitch bend down)
S = noise snare (mode 0, period 5)
```

Double-time (160 BPM boss):
```
| 1  e  &  a  2  e  &  a  3  e  &  a  4  e  &  a |
| K  .  S  .  K  .  S  .  K  .  S  .  K  .  S  . |
(8th note kick, 8th note snare)
```

16th note drum fill:
```
| 1  e  &  a  2  e  &  a  3  e  &  a  4  e  &  a |
| .  .  .  .  .  .  .  .  K  K  K  K  S  S  S  S |
```

### 3.4 Triangle Wave for Bass

The triangle channel is the NES bass voice. Critical constraint: **no volume control** -- the triangle is either on (full volume) or off.

**Triangle channel characteristics:**
- 32-step waveform (triangular shape)
- Fixed volume (on/off only)
- Smooth, round timbre -- blends well without overpowering
- Great for low-end support

**Bass line writing guidelines for triangle:**

1. **Root-note emphasis:** Play the root of the current chord on strong beats (1 and 3).
2. **Simple intervals:** Root-fifth movement is the most common.
3. **Avoid fast passages:** The triangle speaks more slowly than pulse waves; stick to quarter or 8th notes.
4. **Use space:** Let notes ring or insert rests to avoid constant droning.

**C major bass pattern examples:**

Root-fifth alternation (standard):
```
| C2 . G1 . | C2 . G1 . | C2 . G1 . | C2 . . . |
```

Walking bass (stepwise):
```
| C2 . D2 . | E2 . F2 . | G2 . A2 . | G2 . . . |
```

Octave jumps:
```
| C2 . C3 . | G1 . G2 . | E2 . E3 . | C2 . C3 . |
```

Dotted rhythm bass:
```
| C2 . . G1 | C2 . . G1 | C2 . . . | . . . . |
```

**Triangle kick drum trick:** Play a low triangle note (E2) with a rapid downward pitch bend to simulate a kick drum. This works because the triangle can trigger a "thump" that sounds like a bass drum when pitch-bent.

### 3.5 DPCM Channel

The DPCM (Delta Pulse Code Modulation) channel plays 1-bit encoded samples.

| Parameter | Specification |
|-----------|--------------|
| Sample rates | 16 preset rates: ~4.2 kHz to ~33.5 kHz |
| Max sample length | 4,081 bytes (automatic DMA mode) |
| Bit depth | 1-bit delta (7-bit PCM possible via $4011) |
| Common uses | Drum samples, vocal/voice clips, sound effects |

**DPCM usage tips:**
- Lower sample rates (~4.2 kHz) produce lo-fi, crunchy sounds good for kick drums
- Higher sample rates (~33.5 kHz) for intelligible speech or cleaner sounds
- Common practice: pre-encode kick, snare, and hi-hat as DPCM samples and trigger them alongside noise channel percussion for layered drums
- The DPCM channel is optional and not all NES songs use it

### 3.6 Channel Role Assignment (Standard NES Arrangement)

| Channel | Primary Role | Secondary Role | Waveform |
|---------|-------------|----------------|----------|
| Pulse 1 | Lead melody | Counter-melody | Square (switchable duty) |
| Pulse 2 | Harmony / Arpeggio | Second melody | Square (switchable duty) |
| Triangle | Bass line | Kick drum (via pitch bend) | Triangle |
| Noise | Percussion | Sound effects | Noise (LFSR) |
| DPCM | Sampled drums | Voice/samples | 1-bit delta PCM |

**Typical arrangement strategy:**
- Pulse 1 carries the main tune (12.5% or 50% duty)
- Pulse 2 provides harmonic support via arpeggios (25% duty, softer)
- Triangle holds down the bass (root notes, simple patterns)
- Noise provides rhythmic drive (kick + snare + hi-hat)
- DPCM adds accent samples or fills

---

## 4. Chord Progressions

All examples given in C major (or A minor for minor progressions). Use the interval chart to transpose.

### 4.1 I - IV - V (The Basic Rock/Blues Progression)

| Scale Degree | Notes in C | Chord Quality |
|-------------|-----------|---------------|
| I (C) | C4, E4, G4 | Major |
| IV (F) | F4, A4, C5 | Major |
| V (G) | G4, B4, D5 | Major |

**Example sequence:**
```
| C . . . | F . . . | C . . . | G . . . |
| C . . . | F . . . | C . G . | C . . . |
```

**8-bit use:** Platformer overworld themes, driving action music. The I-IV-V is rock-solid and predictable.

### 4.2 I - V - vi - IV (The Pop Progression)

| Scale Degree | Notes in C | Chord Quality |
|-------------|-----------|---------------|
| I (C) | C4, E4, G4 | Major |
| V (G) | G4, B4, D5 | Major |
| vi (Am) | A4, C5, E5 | Minor |
| IV (F) | F4, A4, C5 | Major |

**Example sequence:**
```
| C . . . | G . . . | Am . . . | F . . . |
| C . . . | G . . . | Am . . . | F . . . |
```

**8-bit use:** Town themes, overworld exploration, emotional moments. The single minor chord (vi) adds subtle bittersweetness.

### 4.3 ii - V - I (Jazz/Classical Cadence)

| Scale Degree | Notes in C | Chord Quality |
|-------------|-----------|---------------|
| ii (Dm) | D4, F4, A4 | Minor |
| V (G) | G4, B4, D5 | Major (dom. 7th: add F4) |
| I (C) | C4, E4, G4 | Major |

**Example sequence:**
```
| Dm . . . | G7 . . . | C . . . | C . . . |
| Dm . . . | G7 . . . | C . . . | Am . F . |
```

**8-bit use:** Endings, "final" cadences, RPG quest completion. The ii-V-I creates the strongest sense of resolution.

### 4.4 I - vi - IV - V (50s/Do-Wop Progression)

| Scale Degree | Notes in C | Chord Quality |
|-------------|-----------|---------------|
| I (C) | C4, E4, G4 | Major |
| vi (Am) | A4, C5, E5 | Minor |
| IV (F) | F4, A4, C5 | Major |
| V (G) | G4, B4, D5 | Major |

**Example sequence:**
```
| C . . . | Am . . . | F . . . | G . . . |
| C . . . | Am . . . | F . . . | G . C . |
```

**8-bit use:** Classic, nostalgic feel. Used in many NES title screens and ending themes.

### 4.5 vi - IV - I - V (Minor-flavored Pop)

| Scale Degree | Notes in C (relative to A minor) | Chord Quality |
|-------------|---------------------------------|---------------|
| vi (Am) | A4, C5, E5 | Minor (i in Am) |
| IV (F) | F4, A4, C5 | Major (VI in Am) |
| I (C) | C4, E4, G4 | Major (III in Am) |
| V (G) | G4, B4, D5 | Major (VII in Am) |

**Example sequence:**
```
| Am . . . | F . . . | C . . . | G . . . |
| Am . . . | F . . . | C . . . | G . C . |
```

**8-bit use:** Bittersweet themes, adventure music, forest/field exploration.

### 4.6 bVI - bVII - I (The "Mario Cadence")

This is the most famous chiptune-specific cadence. It uses borrowed chords from the parallel minor.

| Scale Degree | Notes in C | Chord Quality |
|-------------|-----------|---------------|
| bVI (Ab) | Ab4, C5, Eb5 | Major (borrowed) |
| bVII (Bb) | Bb4, D5, F5 | Major (borrowed) |
| I (C) | C5, E5, G5 | Major |

**Example sequence:**
```
| Ab . . . | Bb . . . | C . . . | C . . . |
```

**8-bit use:** Victory fanfares, flagpole/stage clear jingles. Used in Super Mario Bros. flagpole fanfare ("Mario Cadence").

### 4.7 i - iv - v (Minor Blues/Modal)

| Scale Degree | Notes in A Minor | Chord Quality |
|-------------|-----------------|---------------|
| i (Am) | A3, C4, E4 | Minor |
| iv (Dm) | D4, F4, A4 | Minor |
| v (Em) | E4, G4, B4 | Minor (or E7: add D5 for dominant) |

**Example sequence:**
```
| Am . . . | Dm . . . | Am . . . | Em . . . |
| Am . . . | Dm . . . | Am . . . | Em . Am . |
```

**8-bit use:** Dungeon themes, dark forest, Castlevania-style areas.

### 4.8 i - VI - III - VII (Minor Rock Progression)

| Scale Degree | Notes in A Minor | Chord Quality |
|-------------|-----------------|---------------|
| i (Am) | A3, C4, E4 | Minor |
| VI (F) | F4, A4, C5 | Major |
| III (C) | C4, E4, G4 | Major |
| VII (G) | G4, B4, D5 | Major |

**Example sequence:**
```
| Am . . . | F . . . | C . . . | G . . . |
| Am . . . | F . . . | C . . . | G . Am . |
```

**8-bit use:** Action themes, boss battles, dramatic sequences.

### 4.9 Chromatic Mediant / Borrowed Chords (Koji Kondo Style)

Koji Kondo frequently uses chromatic mediants and borrowed chords for harmonic interest:

```
| C . . . | Ab . . . | Bb . . . | C . . . |
(Super Mario Bros. - uses Ab and Bb borrowed from C minor)
```

```
| C . . . | D7 . . . | G . . . | C . . . |
(Secondary dominant: D7 -> G -> C)
```

```
| C . . . | Am . . . | F . . . | D7 . G7 . |
(Extended with secondary dominants)
```

### 4.10 Chord Progression Quick Reference

| Progression | Pattern in C | Mood | Game Use |
|------------|-------------|------|----------|
| I-IV-V | C-F-G | Bright, simple | Platformer overworld |
| I-V-vi-IV | C-G-Am-F | Pop, emotional | Town, exploration |
| ii-V-I | Dm-G7-C | Resolved, jazz | Endings, fanfares |
| I-vi-IV-V | C-Am-F-G | Nostalgic | Title screen, ending |
| vi-IV-I-V | Am-F-C-G | Bittersweet | Adventure overworld |
| bVI-bVII-I | Ab-Bb-C | Triumphant ("Mario Cadence") | Victory fanfare |
| i-iv-v | Am-Dm-Em | Dark, tense | Dungeon, boss |
| i-VI-III-VII | Am-F-C-G | Driving minor | Action, boss battle |
| Chromatic mediant | C-Ab-Bb-C | Surprising, colorful | Character themes |

---

## 5. Song Structure for Game Music

### 5.1 Intro-Loop Structure (Most Common in 8-Bit Games)

This is the dominant structure in NES games. Music plays an intro once, then loops the main section indefinitely.

```
[INTRO] (4-8 bars) ---> [LOOP START] ---> [SECTION A] ---> [SECTION B] ---> [LOOP: go back]
                              ^                                                |
                              |________________________________________________|
```

**Example: 32-bar loop structure**

| Section | Bars | Content | Channels Active |
|---------|------|---------|----------------|
| Intro | 1-4 | Melody teaser (solo pulse) | Pulse 1 only |
| Full intro | 5-8 | Add bass and drums | Pulse 1 + Triangle + Noise |
| A section | 9-16 | Main theme | All channels |
| B section | 17-24 | Contrasting phrase | All channels (different pattern) |
| A' section | 25-32 | Main theme variant (slight change) | All channels |
| Loop back | -> to bar 9 |

**Arpeggio management across sections:** The arpeggio patterns should change between A and B sections to keep the loop from becoming stale:
- A section: root position arpeggios (C4-E4-G4-E4)
- B section: inverted arpeggios or different rhythm (E4-G4-C5-G4)

### 5.2 A-B-A Form

```
[INTRO] ---> [A SECTION] ---> [B SECTION] ---> [A' SECTION (return)] ---> [LOOP or END]
```

**Example: 24-bar structure**

| Section | Bars | Description |
|---------|------|-------------|
| Intro | 1-4 | Sparse, establishing |
| A | 5-12 | Main theme, full arrangement |
| B | 13-20 | Contrast: different key/feel, maybe fewer channels |
| A' | 21-24 | Return to A (shortened or varied) |
| Loop | | Back to bar 5 |

**8-bit use:** Common in RPG town themes and dungeon music. The B section provides contrast (often moving to the relative major or minor).

### 5.3 A-B-A-B (Verse-Chorus Alternation)

```
[INTRO] ---> [A (verse)] ---> [B (chorus)] ---> [A' (verse)] ---> [B' (chorus)] ---> [OUTRO or LOOP]
```

**Example: 32-bar structure**

| Section | Bars |
|---------|------|
| Intro | 1-4 |
| A | 5-12 (softer, pulse 1 lead, sparse) |
| B | 13-20 (fuller, more arpeggios, louder feel) |
| A' | 21-24 (abbreviated verse) |
| B' | 25-32 (extended chorus) |
| Loop | -> bar 5 |

### 5.4 Rondo Form (A-B-A-C-A)

```
[INTRO] ---> A ---> B ---> A ---> C ---> A ---> [OUTRO]
```

**8-bit use:** Longer NES themes (e.g., Mega Man stage themes). The recurring A section provides familiarity while B and C offer variety.

### 5.5 Arcade Loop Template (Adapted from Lyric Assistant)

| Segment | Bars | Content |
|---------|------|---------|
| Intro | 8 | Signature motif, single channel or drums+bass |
| Main theme | 16 | Full groove, all channels |
| Variation | 16 | Slight variation, maybe new arpeggio pattern |
| Breakdown | 8 | Minimal channels (maybe just pulse + triangle) |
| Return | 16 | Full theme with added elements |
| Loop | | Back to main theme |

### 5.6 Structural Techniques Specific to Chiptune

**1. Channel drops:** Remove one channel (e.g., noise or arpeggio) in the B section to create contrast. This is uniquely effective in chiptune because the limited channels make each one's absence noticeable.

**2. Build-ups:** Before the A section returns, add a 2-bar drum fill or ascending arpeggio on the noise channel (rapidly increasing pitch) to signal the transition.

**3. Call-and-response:** Use Pulse 1 and Pulse 2 in a question-answer pattern across sections:
```
Pulse 1: C4 E4 G4 C5   (call)
Pulse 2: G3 B3 D4 G4   (response at lower octave)
```

**4. Key change for loop fatigue:** If the loop is long, modulate up a whole step (e.g., C major -> D major) in the B section to keep it interesting.

**5. Endings:** For non-looping music (victory, game over):
- **Victory:** End on a strong I chord with a rising arpeggio and noise roll
- **Game over:** End on a descending i chord (minor), slow and decaying
- **Continue/transition:** A held chord with a quick cutoff

### 5.7 Practical Song Template: Mega Man-style Stage Theme (32-bar loop)

```
INTRO (4 bars):
  Pulse 1: Melody hook (8th notes, 50% duty)
  Pulse 2: Silence (enters later)
  Triangle: Root notes on 1 and 3 (quarter notes)
  Noise: Kick on 1, snare on 3

A SECTION (8 bars):
  Pulse 1: Main melody (varied 8th/16th pattern, 50% duty)
  Pulse 2: Arpeggios (16th notes, 25% duty) - chord tones
  Triangle: Bass line (8th notes, root-fifth pattern)
  Noise: Full beat - kick on 1+3, snare on 2+4

B SECTION (8 bars):
  Pulse 1: Counter-melody (different phrase, maybe 12.5% duty for contrast)
  Pulse 2: Same as A but inverted arpeggios or different chord voicing
  Triangle: Walking bass line or new pattern
  Noise: Same beat, maybe add hi-hat on 8th notes

BRIDGE (4 bars):
  Drop Pulse 2 and Noise
  Pulse 1: Simplified version of melody
  Triangle: Sustained bass notes (half notes)
  Build tension with rising triangle bass in last bar

A' SECTION (8 bars):
  Return to A section material with one change (different arpeggio or added harmony)
  All channels

LOOP BACK to A SECTION
```

---

## 6. Appendix: NES Hardware Reference

### 6.1 NES APU Channel Summary

| Channel | Waveform | Duty/Volume | Frequency Range | Primary Role |
|---------|----------|-------------|-----------------|--------------|
| Pulse 1 | Square | 4 duties, 16 volume levels | ~28 Hz - ~54 kHz | Melody / Lead |
| Pulse 2 | Square | 4 duties, 16 volume levels | ~28 Hz - ~54 kHz | Harmony / Arpeggio |
| Triangle | Triangle | On/off only (no volume) | ~27 Hz - ~56 kHz | Bass |
| Noise | LFSR noise | 16 volume levels | 16 rate values | Percussion / FX |
| DPCM | 1-bit delta | 64 levels (auto) | 16 sample rates | Samples / Drums |

### 6.2 NES Composition Constraints (Hard Rules)

1. **Maximum 3 melodic voices simultaneously** (2 pulse + 1 triangle; DPCM is not melodic)
2. **No volume control on triangle** -- bass is always at full amplitude
3. **No resonant filter** (unlike C64 SID) -- timbre control only via duty cycle
4. **Each channel is monophonic** -- one note per channel at a time
5. **No reverb or delay** (hardware) -- must be simulated via rapid note repetition
6. **Music must loop seamlessly** -- no gaps when looping back to start
7. **ROM space is limited** -- patterns must be compact and efficient

### 6.3 Key Frequencies for Bass (Triangle Channel)

| Note | Frequency (Hz) | Octave |
|------|---------------|--------|
| C2 | 65.41 | Low |
| E2 | 82.41 | Low |
| G2 | 98.00 | Low |
| A2 | 110.00 | Low |
| C3 | 130.81 | Mid-bass |
| E3 | 164.81 | Mid-bass (also used for kick drum) |
| A3 | 220.00 | Upper range |

### 6.4 FamiTracker Note Mapping (for AI output reference)

In FamiTracker, the standard octave mapping is:
- C-4 = Middle C (MIDI note 60)
- Notes are specified as: Note-Octave (e.g., C-4, D#4, G-5)
- Triangle bass typically plays in octaves 1-3
- Pulse melody typically plays in octaves 3-6

---

## References

- "Compositional Techniques of Chiptune Music" (Academia.edu) -- Doctoral dissertation on Sunsoft NES composers
- "Ear Candy: The SID Chip and the Birth of Chiptunes" (Bath Spa University)
- "Bits and Pieces: A History of Chiptunes" by Kenneth McAlpine (Oxford University Press, 2018)
- NESdev Wiki (nesdev.org) -- Technical APU documentation
- Hooktheory (hooktheory.com) -- Analysis of Koji Kondo and Nobuo Uematsu compositions
- ThinkSpace Education -- Super Mario Bros. harmonic analysis
- LANDR Blog, eMastered, AudioThing -- Chiptune production tutorials
- ChipMusic.org forums -- Community knowledge on NES composition techniques
- Lyric Assistant / Suno -- Chiptune song structure references

---

*End of document. Prepared for AI-driven 8-bit music composition.*
