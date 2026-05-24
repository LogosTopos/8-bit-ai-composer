# Chiptune / Retro Game Music Community, Tools, and Culture

> Research document compiled for building AI that authentically creates chiptune music.
> Last updated: 2026-05-24

---

## Table of Contents

1. [Tracker Software Ecosystem](#1-tracker-software-ecosystem)
2. [Chiptune Creation Workflow](#2-chiptune-creation-workflow)
3. [Community and Culture](#3-community-and-culture)
4. [Composition Tutorials and Resources](#4-composition-tutorials-and-resources)
5. [SoundFont and Sample Resources](#5-soundfont-and-sample-resources)
6. [File Formats for Chiptune](#6-file-formats-for-chiptune)
7. [Python Tools for Chiptune](#7-python-tools-for-chiptune)

---

## 1. Tracker Software Ecosystem

Trackers are the primary tool for chiptune composition. They arrange music in a grid of patterns where time flows vertically (top to bottom) and channels are arranged horizontally.

### 1.1 FamiTracker (NES)

- **Focus**: NES/Famicom (Ricoh 2A03 APU) plus expansion chips (VRC6, VRC7, MMC5, FDS, Namco 163, Sunsoft 5B)
- **Platform**: Windows (runs via Wine on Linux/macOS)
- **License**: Free / Open Source (GPL)
- **Status**: Original upstream discontinued; forks are actively maintained
- **Native file format**: `.ftm`
- **Exports**: `.wav`, `.nsf`, `.txt` (text export for assembly), `.vgm` (via forks)

**Active Forks**:
- **Dn-FamiTracker** (v0.5+) -- most active fork, adds bug fixes and new features. GitHub: https://github.com/Dn-Programming-Core-Management/Dn-FamiTracker
- **0CC-FamiTracker** -- backward-compatible extension with NSF export and extra features

**Key Features**:
- Emulates all 5 NES channels: 2x Pulse (square wave), 1x Triangle, 1x Noise, 1x DPCM (samples)
- Instrument Editor with volume, arpeggio, pitch, duty/noise envelopes
- Pattern-based sequencing with frame arrangement for song structure
- Effect columns (up to 4 per channel) for arpeggio, portamento, vibrato, volume slide, etc.
- Can produce modules that play back on real NES hardware

**Limitations for Hardware Targets**:
- Notes must be C-1 to D-6 only
- No volume column support on real hardware -- all volume must be in instrument envelopes
- Maximum 64 instruments
- Global tempo must be 150 BPM; speed changed via F0x commands
- Sound effects must be under 255 bytes each
- DPCM samples should be under 12 KB total

### 1.2 Furnace Tracker

- **Focus**: Multi-system -- supports **dozens** of sound chips simultaneously
- **Platform**: Windows, macOS, Linux (native cross-platform)
- **License**: Free / Open Source (GPLv2+)
- **GitHub**: https://github.com/tildearrow/furnace (~2,750 stars, very active)
- **Native file format**: `.fur`
- **Exports**: `.wav` (per-chip or per-channel), `.vgm`, DefleMask `.dmf` format
- **Imports**: DefleMask `.dmf`, `.dmp`, `.dmw` (all versions)

**Key Features**:
- Up to **32 sound chips** or **128 channels** in a single project
- Chip duplication (run multiple instances of the same chip for greater polyphony)
- 200+ presets from computers, consoles, and arcade boards
- Wavetable synthesizer, built-in sample editor, per-channel oscilloscope
- MIDI input support
- Quality emulation cores: Nuked, MAME, SameBoy, Mednafen PCE, NSFplay, puNES, reSID, Stella, SAASound, vgsound_emu, ymfm
- Sub-songs, decimal tempo/tick rate, chip mixing settings
- DefleMask module format compatibility -- the de facto bridge between the two trackers

**Supported Sound Chips (50+)**:

| Category | Chips |
|----------|-------|
| **Yamaha FM** | YM2612 (Genesis), YM2151 (Arcade), YM2203 (PC-88), YM2413 (MSX), YM2608 (PC-98), YM2610 (Neo Geo), YM3526, YM3812 (AdLib), YMF262 (OPL3), Y8950 |
| **Sample Chips** | SNES SPC700, Amiga, SegaPCM, Capcom QSound, YMZ280B, RF5C68, OKI MSM6258/MSM6295, Konami K007232/K053260, Ensoniq ES5506, Namco C140/C219 |
| **Wavetable** | HuC6280 (PC Engine/TG-16), Konami SCC/SCC+, Namco WSG/C15/C30, WonderSwan, Seta X1-010 |
| **NES + Expansions** | 2A03/2A07, VRC6, VRC7, MMC5, FDS, Sunsoft 5B, Namco 163, Family Noraebang (OPLL) |
| **Square Wave** | AY-3-8910/YM2149, SN76489 (SMS/GG), Commodore VIC, PC Speaker, Philips SAA1099 |
| **Other Classic** | SID 6581/8580 (C64), Mikey (Atari Lynx), POKEY (Atari 8-bit), Game Boy (zombie/envelope mode), Virtual Boy, GBA, NDS |
| **Fantasy/Modern** | Commander X16 VERA, tildearrow Sound Unit, PowerNoise, Bifurcator, SID2, SID3, Generic PCM DAC |

**Systems Covered**: Genesis/Mega Drive, SNES, Neo Geo, PC-98, PC Engine/TG-16, SMS/Game Gear, C64, NES (with expansions), Amiga, Game Boy/GBA/NDS, Atari 2600/Lynx/8-bit, ZX Spectrum, WonderSwan, and many arcade boards.

### 1.3 DefleMask

- **Focus**: Multi-system chiptune tracker
- **Platform**: Windows, macOS, Linux, Android, iOS
- **License**: **Paid / Proprietary** -- the only major paid tracker
- **Latest version**: Actively developed (check https://www.deflemask.com)
- **Native file format**: `.dmf`

**Supported Systems**: Genesis, SMS/Game Gear, C64, NES, Game Boy, PC Engine, Neo Geo, Arcade (YM2151), Sega CD, Amiga, and more.

**Key Points**:
- Its module format (`.dmf`) is used as the base for Furnace's import/export -- Furnace is fully DefleMask-compatible
- Well-documented effect system; has a comprehensive PDF manual
- Cross-platform native support
- Considered the "Pro Tools" of chiptune by some, but its price tag limits adoption versus free alternatives

### 1.4 LSDJ (Little Sound DJ) -- Game Boy

- **Focus**: Nintendo Game Boy (exclusively)
- **Platform**: Runs on real Game Boy hardware + emulators
- **License**: **Paid / Proprietary**
- **Latest version**: 9.3.9 (June 2023)
- **Website**: http://www.littlesounddj.com

**Key Features**:
- Uses the Game Boy's 4 sound channels: 2x Pulse (square), 1x Wave, 1x Noise
- Dual sample playback on the wave channel
- Drawable waveform synthesizer, speech synthesis
- Sync options: Analog, Game Boy link cable, MIDI, VST integration
- Up to 256 phrases, 256 chains, 64 instruments, 32 effect tables

**Workflow**:
- Tree-structured sequencer: Song -> Chain -> Phrase -> Instrument -> Table
- 9 screens navigated via SELECT + D-Pad
- Song Mode (all 4 channels) vs. Live Mode (single channel for improvisation)
- Multiple Game Boys can sync via link cable for collaborative live performance

**Community Notes**:
- Still actively used today for live chiptune performances
- DMG-01 (original Game Boy) preferred for bass response and battery life
- Official cartridges out of production; users typically flash ROMs onto blank carts
- Used by Grammy winners, Bit Shifter, Comptroller, Chipocrite, and many others

### 1.5 FamiStudio

- **Focus**: NES/Famicom (DAW-style alternative to FamiTracker)
- **Platform**: Windows, macOS, Linux (native)
- **License**: Free / Open Source
- **GitHub**: https://github.com/joncampbell123/FamiStudio
- **Latest version**: v4.4.4 (November 2025)

**Key Differences from FamiTracker**:
- **DAW-style interface**: Piano roll + sequencer instead of text-based tracker grid
- **No hexadecimal** -- all decimal/visual, much friendlier for beginners
- **MIDI input**, undo/redo, note drag-and-drop with audio preview
- Imports FTM files from FamiTracker (official 0.4.6)
- Exports WAV, NSF, ROM, VGM, ASM (FamiTone2)
- Supports NES expansions: VRC6, VRC7, FDS, MMC5, Namco 163, Sunsoft 5B, EPSM (OPN3)
- **Limited effect command support** vs FamiTracker (subset only)
- Uses its own sound engine for ROM export (not FamiTone2)

**When to Use**: Beginner-friendly, DAW users transitioning to chiptune, Linux/macOS users who don't want Wine.

### 1.6 Other Notable Trackers

| Tracker | Focus | License | Notable For |
|---------|-------|---------|-------------|
| **MilkyTracker** | XM format (FastTracker II clone) | Open Source | Cross-platform, general chiptune/sample tracking |
| **Schism Tracker** | IT format (Impulse Tracker clone) | Open Source | Most feature-complete IT clone |
| **OpenMPT** | Modern PC tracker | Open Source | MOD/XM/S3M/IT, very active development |
| **BambooTracker** | YM2608 (PC-88/98) | Open Source | Specialist FM synthesis tracker |
| **Bintracker** | Multi-system (via MAME backend) | Open Source | Hackable, Lisp-based, very flexible |
| **klystrack** | Multi-system | Open Source | Imports FamiTracker, AHX, FT2, Protracker |
| **SNES Tracker** (snestracker) | SNES SPC700 | Open Source | SPC debugger included; development paused |

### 1.7 Summary Comparison

| Tracker | Price | Open Source | Multi-Chip | Real HW Export | Platform | Active Dev (2026) |
|---------|-------|-------------|------------|----------------|----------|-------------------|
| FamiTracker (forks) | Free | Yes | NES only | Yes (NSF) | Windows | Moderate (forks) |
| Furnace | Free | Yes | 50+ chips | Via emulation | Win/Mac/Linux | Very active |
| DefleMask | Paid | No | Multi | Via emulation | Win/Mac/Linux | Active |
| LSDJ | Paid | No | GB only | Yes (ROM) | GB hardware | Maintained |
| FamiStudio | Free | Yes | NES | Yes (NSF/ROM) | Win/Mac/Linux | Very active |

---

## 2. Chiptune Creation Workflow

### 2.1 Understanding Channel Limitations

The core constraint that defines chiptune composition is the severe channel limit of early sound chips:

| System | Sound Chip | Total Channels | Usable Melodic Channels |
|--------|-----------|----------------|-------------------------|
| NES/Famicom | Ricoh 2A03 | 5 | 3 (2 Pulse + 1 Triangle) |
| Game Boy | LR35902 | 4 | 3 (2 Pulse + 1 Wave) |
| Sega Genesis | YM2612 + SN76489 | 10 (6 FM + 4 PSG) | 10 (but limited polyphony) |
| C64 | SID 6581/8580 | 3 | 3 |
| PC Engine | HuC6280 | 6 | 6 |

### 2.2 Step-by-Step Composition Workflow (NES-focused)

1. **Set up the tracker**: Choose tempo, create instrument definitions (volume envelope, arpeggio, pitch, duty cycle)
2. **Start with the bassline** (Triangle channel): Triangle wave cannot change volume dynamically, so it excels at steady bass lines or tom-like percussion
3. **Write the main melody** (Pulse 1): Square wave with duty cycle changes (12.5%, 25%, 50%, 75%) for timbral variation
4. **Add harmony/counter-melody** (Pulse 2): Often an arpeggio-driven chord progression or a second melodic line
5. **Percussion** (Noise + Triangle): Snare = short noise burst, Hi-hat = quick noise tick, Kick = descending triangle pitch sweep
6. **Drum samples** (DPCM): Kicks, snares, or vocal samples stored as DPCM data
7. **Structure the song**: Arrange patterns into frames (verse, chorus, bridge, etc.)
8. **Add effects**: Vibrato, portamento, arpeggio, volume slides for expressiveness
9. **Export**: WAV for listening, NSF for hardware playback

### 2.3 Common Composition Strategies

**Arpeggios Instead of Chords**:
Since each channel is monophonic, rapid cycling through chord tones (root-3rd-5th) on a single channel implies full harmony. Use 1/16 or 1/32 note arpeggios. Once harmony is established, drop the arpeggio -- the listener's brain fills it in.

**Call & Response**:
One channel plays a held bass note while another plays a fast arpeggio. The brain merges them into a single chord perception.

**Counterpoint**:
Two independent melodic lines complementing each other sound fuller than one melody + one chord. Classic game composers (Koji Kondo, Junichi Masuda, Yuzo Koshiro) used this heavily.

**Channel Role Switching**:
Swap a channel's role between melody and percussion within the arrangement (e.g., a channel plays snare during verse, switches to melody during chorus).

**Duty Cycle Animation**:
Changing pulse wave duty cycle (12.5% -> 50% -> 75%) mid-note creates evolving, dynamic lead sounds without using additional channels.

### 2.4 Effects Columns in Trackers

Trackers use a standardized effect system inherited from ProTracker. Most trackers support 1-4 effect columns per channel.

| Command | Effect | Common Usage |
|---------|--------|-------------|
| `0xy` | Arpeggio | Fake chords (cycles 3 notes: root, x semitones up, y semitones up) |
| `1xx` | Portamento Up | Slide pitch up at speed xx |
| `2xx` | Portamento Down | Slide pitch down at speed xx |
| `3xx` | Tone Portamento | Glide to the next note |
| `4xy` | Vibrato | x = speed, y = depth (chip-specific behavior on NES) |
| `7xy` | Tremolo | Volume oscillation |
| `Axy` | Volume Slide | Smooth volume changes |
| `Bxx` | Position Jump | Jump to frame xx |
| `Cxx` | Note Cut | Cut note after xx ticks |
| `Dxx` | Pattern Break | Skip to next frame at row xx |
| `EDx` | Note Delay | Delay note by x ticks |
| `Fxx` | Set Speed | Change global tempo/speed |

**NES-Specific Effects (FamiTracker/Furnace)**:
- Hardware vibrato uses chip-specific modulation
- Linear pitch model for portamento
- Fine pitch offset (`Pxx`) for NES's limited pitch range
- Duty cycle commands for timbre changes
- DPCM sample bank selection

### 2.5 Common Beginner Mistakes

| Mistake | Cause | Fix |
|---------|-------|-----|
| Too many simultaneous voices | Exceeding channel limits | Strip to core motif; assign each channel one clear role |
| Muddy low end | Non-bass channels in bass frequencies | High-pass everything that isn't bass |
| Overusing reverb/echo | Kills crisp chip character | Small reverb for space; large reverb destroys clarity |
| Static loops | No micro-variations | Change duty cycle, add filter sweeps, drop channels |
| Over-compression | Destroys transient snap | Preserve sharp attacks; limit gently |
| Unclear roles per channel | Two parts in same frequency | EQ or move one part an octave |
| Too many ideas at once | Chip textures are bright | One emotional idea per loop; add variation later |

---

## 3. Community and Culture

### 3.1 Battle of the Bits (BotB)

- **Website**: https://battleofthebits.com
- **Founded**: 2005
- **Description**: Online chiptune competition community where composers submit original tracks on various hardware formats
- **Members called**: BotBrs

**Battle Types**:
- **Major Battles**: Run for a month+, annual events: Spring Tracks, Summer Chip, Winter Chip, Detroit
- **XHBs** (formerly OHBs): 1-4 hour battles with bitpack restrictions, anonymous submissions
- **Tournament**: Swiss Robin Round -> Elimination Brackets
- **3xThemeChip**: Three community-voted themes, one entry per theme, each in a different format

**Format System**:
- **Chipist formats**: Music designed to play on old consoles using sound chips (NSF, SPC, etc.) -- awards Chipist points
- **Mixist formats**: Sample-based music
- **Wildchip**: "Anything remotely chip and/or fakebit" - accepts post-processing, vocals, multiple soundchips
- **Allgear**: No limitations other than filesize
- Format badges unlock after 7 entries in a format with score >= 20

**Classes**:
- Chipist, Mixist, Samplist, Criticist, XHBist, Pixelist, Hostist, Signalist, Pedagogist

**Lyceum (Wiki)**: https://battleofthebits.com/lyceum/ -- Contains articles on formats, battles, classes, tools, terminology

### 3.2 ChipMusic.org

- **Website**: https://chipmusic.org
- **Description**: Online community hub for chip music, art, and discussion
- Forums for sharing tracks, production techniques, event promotion
- Deep ties to both BotB and MAGFest's Chipspace
- Active forum discussions on tools, techniques, and collaboration

### 3.3 Reddit: r/chiptunes

- **Subscribers**: Large community (estimated 50,000+)
- Active with track shares, tool discussions, WIP feedback
- Cross-posts with r/gamemusic, r/nes, r/Gameboy

### 3.4 MAGFest and Chipspace

**MAGFest** (Music And Gaming Festival) -- Major US festival for game music and chiptune.

**Chipspace**: Dedicated chiptune stage and open space at MAGFest:
- **Open Mic**: Chiptune-only sessions (10 min slots). Bring your own gear (Game Boy, Atari, laptop, etc.)
- **Curated Showcases**: Pre-scheduled sets by invited artists, labels, collectives
- **Chip Rave**: Originated from a 10-hour impromptu party
- **Performer Benefits**: Comped badge, merch space, streamed sets, professional photography
- **Resources**: https://super.magfest.org/chipspace-guidelines/

### 3.5 Notable Chiptune Artists

| Artist | Real Name | Signature Style | Key Works | Tools |
|--------|-----------|----------------|-----------|-------|
| **Jake "virt" Kaufman** | Jake Kaufman | NES authentic, VRC6 expansion | Shovel Knight OST, DuckTales Remastered, Double Dragon Neon | FamiTracker, VRC6 |
| **Sabrepulse** | Ashley Charles | Chiptune + breakcore/electronic | "First Crush", "Bubbleguns" | LSDJ, Game Boy |
| **Chipzel** | Niamh Houston | Melodic chiptune, energetic | "Spectra", "Phonetic Symphony" | LSDJ, Game Boy |
| **Danimal Cannon** | Daniel Behrens | Chiptune + live guitar (metal) | "Corrupted", "Chronos", "Logic Gatekeeper" | LSDJ + guitar |
| **FearOfDark** | -- | Ambient chiptune + breakbeat | "Rolling Down the Street...", "Surfing on a Sine Wave" | Trackers |
| **c-jeff** | -- | Complex FM synthesis, melodic | Ubiktune releases, VGM covers | DefleMask/Furnace |
| **Bit Shifter** | -- | Game Boy virtuoso | "Information Chase" | LSDJ |
| **Zabutom** | -- | NES chiptune, melodic | Various BotB entries | FamiTracker |
| **an0va** | -- | Modern chiptune production | Various releases | Trackers + DAW |
| **FearOfDark** | -- | Ambient/breakbeat + chiptune | "Dr Kobushi's Labyrinthine Laboratory" | Trackers |

### 3.6 Notable Composer Techniques (from interviews)

**Jake "virt" Kaufman (Shovel Knight)**:
- Used FamiTracker with VRC6 expansion chip for extra channels
- "There was no way generic '8-bit-esque' music would cut it. Needed the real, raw sound of the 2A03 chip."
- Every song can play on real NES hardware if given the entire cartridge space
- "NES music is incredibly time-consuming -- the minimal sound allows no filler or shortcuts"
- Entire Shovel Knight OST released as playable NSF files

**Danimal Cannon**:
- Combines live guitar with LSDJ Game Boy chiptune
- Has presented at PAX, Blip Festival, TEDx
- "Digital fusion" -- chiptune + prog rock/metal

### 3.7 Other Community Hubs

- **This Week in Chiptune**: https://thisweekinchiptune.com -- Weekly chiptune news and releases
- **OCReMix Chiptune Community**: https://ocremix.org -- Remix community with strong chiptune presence
- **NESDev Forums**: https://forums.nesdev.org -- Homebrew development including music
- **FamiBoards Chiptune Hangout**: Active chiptune discussion thread
- **Nerd Noise Radio Network**: Podcast episodes featuring BotB music

---

## 4. Composition Tutorials and Resources

### 4.1 YouTube Tutorial Series

**FamiTracker**:
- **8BitDanooct1** (5-part series): Instrument Editor, Pattern Editor, Note Effects, Covering a Song, Finishing. Most recommended beginner FamiTracker series.
- **nu11_ft** (https://www.youtube.com/@nu11_ft): Active channel dedicated to FamiTracker music
- **FamiTracker Tutorial Playlist**: https://youtube.com/playlist?list=PLW08UHPY2AEoWhZJVfaE4tUF9jpso8KI0

**LSDJ**:
- **LSDJ Tutorials** by various creators: Covers song structure, live performance, instrument creation
- Official LSDJ manual is the best reference: Available at https://www.littlesounddj.com

**DefleMask**:
- Official DefleMask PDF manual: https://www.deflemask.com/manual.pdf
- Various chiptune YouTubers cover DefleMask workflow

**General Chiptune**:
- **Soundfly Course**: "Getting Started with Chip Music" and "Arranging in Four Channels" -- Structured courses at https://soundfly.com/courses/getting-started-with-chip-music

### 4.2 Written Guides

- **Synthtopia**: "How To Make 8-Bit Music: An Introduction To FamiTracker" -- classic beginner guide covering 2A03 chip, 5 channels, instrument editing
- **LANDR Blog**: "How to Make Chiptune Music in 7 Steps" -- covers counterpoint, arpeggios, bassline, melody, counter-melody, drums
- **eMastered**: "How to Make Chiptune Music" -- covers waveforms, duty cycle, song structures (A-B-A, Rondo)
- **MegaCat Studios**: "Creating Music and Sound for the NES: A Primer for Using Famitracker" -- detailed guide covering hardware constraints
- **TechRadar**: "How to create 8-bit music" -- DefleMask-focused guide with pattern window layout
- **Lyric Assistant**: "How to Write Chiptune Songs" -- practical beginner mistakes and fixes
- **Composer Focus**: "How to Make 8-Bit Music" -- six methods, tools comparison
- **JekyllPark Tracker Parameters**: Cross-tracker effect reference table at https://jekyllpark.neocities.org/txt/tracker

### 4.3 BotB Academy Resources

- **MML Guide**: Active thread on Music Macro Language for chiptune
- **Format-specific tutorials**: N163, VRC6, SID, and other expansion chip guides
- **EZNSF tool guide**: Converting NSF to NES ROM

### 4.4 Key Composition Principles for AI Training

1. **Channel role clarity**: Each channel must have a distinct, identifiable role (bass, melody, harmony, percussion)
2. **Arpeggios for harmony**: Rapid note cycling creates chord perception on monophonic channels
3. **Duty cycle animation**: Timbre variation within single notes
4. **Counterpoint over chords**: Two independent melodic lines beat one melody + one chord
5. **Noise percussion**: Short noise bursts for snare, quick ticks for hi-hat, pitched sweeps for kick
6. **DPCM for samples**: Kicks, vocal clips, or special effects
7. **Call and response**: Brain merges bass + arpeggio into a chord
8. **Micro-variations**: Small changes each loop to prevent listener fatigue
9. **Space as a tool**: Dropping channels creates dramatic impact
10. **Format-aware composition**: Different chips handle different techniques

---

## 5. SoundFont and Sample Resources

### 5.1 Musical Artifacts (Primary Repository)

- **Website**: https://musical-artifacts.com
- **Description**: Libre resources for music making. Search for "chiptune", "NES", "Genesis", "SNES", "soundfont"

### 5.2 Chiptune SoundFonts (.sf2)

| Name | Size | Description | Source |
|------|------|-------------|--------|
| **aobu's chiptune soundfont v0.03** | 8.12 MB | NES waveforms (pulse waves, noise, DPCM drums). 6,368 downloads | https://musical-artifacts.com/artifacts/1626 |
| **Dan The Man Inspired Soundfont** | 73.1 MB | Hybrid (NES + Genesis + SNES), General MIDI compatible | https://musical-artifacts.com/artifacts/7892 |
| **NES Soundfont V1.0** (by iand255) | 284 KB | Basic NES soundfont | Musical Artifacts |
| **Super Mario Kart (SNES) Restored** | -- | Restored SNES soundfont | Musical Artifacts |
| **Top Gear (SNES) Soundfont** | -- | SPC-ripped samples, BRR-to-WAV conversion | Musical Artifacts |
| **My JummBox Chiptune SoundFont** | -- | Chiptune soundfont for JummBox/BeepBox | Vogons forums |

### 5.3 Finding More SoundFonts

- Search `site:musical-artifacts.com` for "nes sf2", "genesis sf2", "snes sf2", "chiptune"
- Filter by tags: `soundfont`, `chiptune`, `nes`, `genesis`, `snes`
- Check `apps=fluidsynth` filter for FluidSynth-compatible SoundFonts

### 5.4 Using SoundFonts with FluidSynth

```python
import fluidsynth

synth = fluidsynth.Synth()
sfid = synth.sfload("path/to/chiptune.sf2")
synth.program_select(0, sfid, 0, 0)
synth.noteon(0, 60, 100)  # Play middle C
```

### 5.5 VST Instruments for Chiptune

- **Chipsounds** (by Plogue): Emulates NES, C64, Genesis, and more (paid)
- **Magical 8bit Plug** (by ymm): Free simple 8-bit VST
- **Pulse** (by Waldorf): Modern wavetable synth with chiptune capabilities
- **NES VST** (various): Individual chip emulators

---

## 6. File Formats for Chiptune

### 6.1 Console/Native Formats

#### NSF (NES Sound Format)
- **Extension**: `.nsf`
- **Description**: Contains raw 6502 sound engine code + music data for the NES 2A03 APU
- **Channels**: 2 square + 1 triangle + 1 noise + 1 DPCM
- **Created by**: FamiTracker (export NSF), MCK (Music Creation Kit), hand-coded assembly
- **Players**: NSFPlay (Windows), NEZPlug (Winamp), Game Music Emu (libgme, cross-platform), foobar2000 with NSF plugin
- **Ripping**: Extracting NSF from NES ROMs using tools like NSF Ripper
- **File structure**: Header (80 bytes with song info, chip flags) + PRG bank data + optional bankswitching

#### SPC (SNES Sound Format)
- **Extension**: `.spc`
- **Description**: Captures the S-SMP audio coprocessor state (the SNES's dedicated sound CPU)
- **Channels**: 8 ADPCM channels, 64KB sample memory
- **Created by**: SNESGSS, SPC ripping tools, SNES Tracker, Furnace Tracker
- **Players**: SPC Player, ZSNES, SNES9x, Game Music Emu
- **Tags**: ID666 tags embedded for metadata (title, artist, game, etc.)
- **File structure**: Header + DSP registers + 64KB SPC700 RAM + optional echo buffer + ID666 tag

#### VGM (Video Game Music)
- **Extension**: `.vgm`
- **Description**: Modern, actively maintained format for capturing synthesized console audio
- **Chip support**: Genesis YM2612 (FM), SN76489 (PSG), and many other chips
- **Status**: **OBSOLETED `.gym`** -- VGM is the current standard for Genesis/Mega Drive music
- **Created by**: VGM dumps from emulators, Furnace Tracker exports, specialized ripping tools
- **Players**: VGMPlay (cross-platform), foobar2000 with VGM plugin, Game Music Emu

#### GYM (Genesis YM2612 Music)
- **Extension**: `.gym`
- **Description**: Older format for Sega Genesis music -- largely replaced by VGM
- **Status**: Obsolete. VGM is recommended for all new projects.

#### SID (Commodore 64)
- **Extension**: `.sid`
- **Description**: Uses MOS 6581/8580 SID chip
- **Channels**: 3 channels of synthesis
- **Very active scene**: HVSC (High Voltage SID Collection) is the definitive archive

#### GBS (Game Boy Sound)
- **Extension**: `.gbs`
- **Description**: Game Boy sound format, similar concept to NSF/SPC

### 6.2 Tracker/Module Formats

#### MOD (ProTracker Module)
- **Extension**: `.mod`
- **Origin**: Amiga, Ultimate Soundtracker (1987), later ProTracker
- **Channels**: 4 (original) up to 32
- **Samples**: 8-bit, 15 sample slots
- **Patterns**: Discreet patterns with rows (64 rows typical)
- **Players**: Extremely wide support (XMP, MikMod, OpenMPT, almost all media players)

#### XM (Extended Module)
- **Extension**: `.xm`
- **Origin**: FastTracker 2 (PC, 1990s)
- **Channels**: Up to 32+
- **Features**: Multisampling, volume/panning envelopes, pattern compression, 16-bit samples
- **Very common for chiptunes** -- widely exported by MilkyTracker and OpenMPT

#### S3M (Scream Tracker 3 Module)
- **Extension**: `.s3m`
- **Origin**: Future Crew, Scream Tracker 3 (PC, 1990s)
- **Features**: Supports sampled instruments AND synthesized (AdLib/OPL2) channels
- **Samples**: 16-bit, up to 32 channels

#### IT (Impulse Tracker Module)
- **Extension**: `.it`
- **Origin**: Jeffrey Lim, Impulse Tracker (PC, 1990s)
- **Channels**: Up to 256
- **Features**: Most advanced of the "Big 4" -- 16-bit samples, stereo panning, filters, resonant filters, compression, embedded instruments

**"The Big Four"**: MOD, XM, S3M, IT -- most modern players support all four via libxmp, libmodplug, or OpenMPT.

### 6.3 Modern Tracker Formats

| Format | Tracker | Notes |
|--------|---------|-------|
| `.ftm` | FamiTracker | Native NES tracker format |
| `.fur` | Furnace | Multi-system format, JSON-based |
| `.dmf` | DefleMask | DefleMask native, importable by Furnace |
| `.0cc` | 0CC-FamiTracker | FamiTracker fork extension |
| `.ftm` (Dn) | Dn-FamiTracker | Extended FamiTracker format |
| `.fms` | FamiStudio | FamiStudio project files |

### 6.4 Converting Between Formats

| Conversion | Tools |
|------------|-------|
| FTM -> NSF | FamiTracker (export), Dn-FamiTracker |
| FTM -> DMF | Manual recreation (no direct converter) |
| FTM -> FUR | Manual import (Furnace has partial import) |
| DMF -> FUR | Native (Furnace reads all DefleMask versions) |
| XM -> SPC | eKid's XMSNES converter |
| XM -> NSF | Barnyard (converter tool) |
| Any -> MIDI | OpenMPT (export tracker to MIDI), some tracker features lost |
| Any -> WAV | Nearly all trackers export WAV directly |
| NSF -> ROM | EZNSF (Python tool, NSF -> NES ROM) |
| SPC -> BRR | Various SPC ripping tools extract samples |
| VGM -> WAV | VGMPlay, various converters |
| MIDI -> XM/IT | OpenMPT (import MIDI to tracker), manual cleanup needed |

### 6.5 MIDI as an Intermediate Format

- **Strengths**: Universal format, supported by all DAWs, facilitates AI training data pipelines
- **Weaknesses**: Loses chiptune-specific articulations (duty cycle, hardware arpeggio, DPCM samples). Cannot represent per-chip channel limits.
- **Best use**: Capturing note/pitch/timing data, then converting to tracker for chip-accurate instrumentation
- **Conversion**: OpenMPT is the best tool for MIDI <-> tracker translation, but always requires manual cleanup

---

## 7. Python Tools for Chiptune

### 7.1 Tracker Format Manipulation

| Library | PyPI | Formats | Purpose | Stars |
|---------|------|---------|---------|-------|
| **xmodits-py** | Yes | IT, XM, S3M, MOD, MPTM, UMX | Extract/rip samples from tracker files | ~3 |
| **trackrip** | Yes | MOD, S3M, IT | Extract samples from tracker modules | -- |
| **fasttracker-parser** | Yes | XM | Parse FastTracker XM metadata | -- |
| **pymidas** | Yes | MOD, S3M, XM, IT | Playback and audio streaming | -- |

**xmodits-py** usage:
```python
import xmodits
xmodits.dump("~/Downloads/music.xm", "~/Music/samples/")
```

### 7.2 NSF and Console Format Tools

| Tool | Type | Description | URL |
|------|------|-------------|-----|
| **EZNSF** | Python tool | Transforms NSF files into NES ROMs (Mapper 31/NROM) | https://github.com/bbbradsmith/eznsf |
| **Chiptune-Python-Scripts** | Script collection | NSFPlay multichannel exporter, DPCM splitter, wavestretcher | https://github.com/Gumball2415/Chiptune-Python-Scripts |
| **newdump** | Python module | Chiptune player -> oscilloscope video (NSF via nosefart, SPC, VGM, XM) | https://codeberg.org/Riedler/newdump/ |
| **chipchune** | Python library | Manipulate Furnace tracker format (.fur). WIP, early stage | https://github.com/ZoomTen/chipchune |

**EZNSF** usage:
```bash
# Convert NSF to playable NES ROM
eznsf.py input.nsf -o output.nes --title "My Song"
```

### 7.3 Emulation-Based Audio Capture

| Approach | Description |
|----------|-------------|
| **FCEUX + Lua** | FCEUX NES emulator has Lua scripting. Can script audio channel isolation and capture |
| **libgme (Game Music Emu)** | C library, wrap via ctypes/cffi in Python. Plays NSF, SPC, VGM, GBS, SID, etc. |
| **nosefart** | C-based NSF player. Used by newdump as backend. Wrap via ctypes |
| **Furnace headless** | Furnace can run in headless mode for batch WAV export |
| **pyPSG** | AY-3-8910 (PSG) emulator written in pure Python |
| **MicroPython SN76489** | Sega/SNES PSG emulator for MicroPython |

**libgme via ctypes** (conceptual):
```python
import ctypes

# Load libgme shared library
gme = ctypes.CDLL("libgme.dll")

# Open NSF file, start playback, render to WAV
```

### 7.4 Direct Python Libraries by Chip

| Library | Chip/Format | Description |
|---------|-------------|-------------|
| pyPSG | AY-3-8910 | Pure Python PSG emulator |
| MicroPython SN76489 | SN76489 | Game Gear/SMS PSG |
| various (GitHub topics) | YM -> VGM | YM file format conversion tools |

### 7.5 Non-Python Libraries with Python Bindings

| Library | Language | Description | Formats |
|---------|----------|-------------|---------|
| **libxmp** | C | Extended Module Player library. Renders modules to PCM | MOD, S3M, XM, IT + 90+ formats |
| **libmodplug** | C++ | Open ModPlug Tracker library | MOD, S3M, XM, IT + ~18 more |
| **libgme** | C | Game Music Emu (Blargg's libraries) | NSF, SPC, VGM, GBS, SID, AY, HES, etc. |
| **nosefart** | C | NES Sound Format player | NSF |

### 7.6 Web-Based Chiptune Player (for reference)

**Web-Chiptune-Player**: JavaScript library using game_music_emu for NSF/NSFE, VGM, SPC, PSF, GBS, AY, SAP, HES playback in browsers.

### 7.7 Python Strategy for AI Chiptune Generation

Based on this research, the recommended Python pipeline for authentic chiptune AI would be:

```
AI Model -> MIDI/tracker data -> Furnace/FamiTracker (headless) -> WAV render -> validation
```

**Toolchain options**:
1. **MOD/XM export**: Train AI to output XM format. Use libxmp (via ctypes) for audio rendering. Lossy for chip-specific features.
2. **Furnace project generation**: Train AI to output `.fur` format (JSON-based). Use Furnace headless for rendering. Best multi-chip support.
3. **MIDI + SoundFont**: Train AI to output MIDI. Render with FluidSynth + chiptune SoundFont. Most flexible but least authentic.
4. **Direct PCM generation**: Train AI to output raw audio. Requires emulating chip characteristics. Most complex but full control.

**Gap analysis**: There is no mature Python library for writing NSF/Fur/DMF files directly. The most practical approach is generating MIDI -> converting via OpenMPT -> rendering via tracker emulation.

---

## Key Links Summary

### Trackers
- FamiTracker (forks): https://github.com/Dn-Programming-Core-Management/Dn-FamiTracker
- Furnace Tracker: https://github.com/tildearrow/furnace
- DefleMask: https://www.deflemask.com
- LSDJ: http://www.littlesounddj.com
- FamiStudio: https://github.com/joncampbell123/FamiStudio
- MilkyTracker: https://github.com/milkytracker/MilkyTracker
- OpenMPT: https://openmpt.org

### Communities
- Battle of the Bits: https://battleofthebits.com
- ChipMusic.org: https://chipmusic.org
- Reddit r/chiptunes: https://reddit.com/r/chiptunes
- MAGFest Chipspace: https://super.magfest.org/activities/music/chipspace/
- This Week in Chiptune: https://thisweekinchiptune.com
- NESDev Forums: https://forums.nesdev.org

### SoundFonts
- Musical Artifacts: https://musical-artifacts.com
- aobu's chiptune sf2: https://musical-artifacts.com/artifacts/1626
- Dan The Man Hybrid sf2: https://musical-artifacts.com/artifacts/7892

### Python Tools
- EZNSF: https://github.com/bbbradsmith/eznsf
- Chiptune-Python-Scripts: https://github.com/Gumball2415/Chiptune-Python-Scripts
- chipchune: https://github.com/ZoomTen/chipchune
- newdump: https://codeberg.org/Riedler/newdump/
- xmodits-py: https://github.com/b0ney/xmodits-py
- libxmp: https://github.com/libxmp/libxmp
- libgme: https://github.com/sysfce2/libgme

### Education
- Synthtopia FamiTracker Guide: https://www.synthtopia.com/content/2015/05/01/how-to-make-8-bit-music-an-introduction-to-famitracker/
- LANDR Chiptune Guide: https://blog.landr.com/how-to-make-chiptune-music/
- MegaCat Studios NES Primer: https://megacatstudios.com/blogs/retro-development/creating-music-and-sound-for-nes-games
- Soundfly Chip Music Course: https://soundfly.com/courses/getting-started-with-chip-music
- BotB Lyceum Wiki: https://battleofthebits.com/lyceum/
- Cross-Tracker Effect Reference: https://jekyllpark.neocities.org/txt/tracker
