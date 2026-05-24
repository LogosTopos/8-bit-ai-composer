"""
8-bit synthesizer: waveform generation and real-time audio output.

Covers NES (2A03), Game Boy (DMG), C64 (SID) era chips.
Features: 11 waveforms, arpeggio, vibrato, ADSR envelope.
"""

import math
import threading

import numpy as np
import sounddevice as sd

from .constants import (
    ARPEGGIO_INTERVALS,
    BUFFER_SIZE,
    CHANNELS,
    DEFAULT_WAVETABLE,
    MAX_POLYPHONY,
    MIDI_FREQS,
    SAMPLE_RATE,
    WAVE_NOISE_LONG,
    WAVE_NOISE_PERIODIC,
    WAVE_NOISE_SHORT,
    WAVE_PULSE_125,
    WAVE_PULSE_25,
    WAVE_PULSE_50,
    WAVE_PULSE_75,
    WAVE_SAWTOOTH,
    WAVE_SINE,
    WAVE_TRIANGLE,
    WAVE_WAVETABLE,
)


class Voice:
    """A single active voice."""

    __slots__ = (
        "midi_note", "base_frequency", "frequency", "wave_type",
        "velocity", "phase", "sample_idx", "active", "release",
        "envelope_phase", "attack_samples", "decay_samples",
        "sustain_level", "release_samples", "env_level",
        "vibrato_depth", "vibrato_rate",
        "arpeggio_intervals", "arpeggio_rate",
        "arpeggio_step", "arpeggio_step_samples",
        "portamento_freq", "portamento_samples",
    )

    def __init__(self, midi_note: int, wave_type: str = WAVE_PULSE_50,
                 velocity: float = 0.7):
        self.midi_note = midi_note
        self.base_frequency = MIDI_FREQS.get(midi_note, 440.0)
        self.frequency = self.base_frequency
        self.wave_type = wave_type
        self.velocity = velocity
        self.phase = 0.0
        self.sample_idx = 0
        self.active = True
        self.release = False

        # ADSR envelope
        self.envelope_phase = 0        # 0=attack, 1=decay, 2=sustain, 3=release
        self.attack_samples = int(SAMPLE_RATE * 0.02)   # 20ms attack
        self.decay_samples = int(SAMPLE_RATE * 0.05)    # 50ms decay
        self.sustain_level = 0.7
        self.release_samples = int(SAMPLE_RATE * 0.1)   # 100ms release
        self.env_level = 0.0

        # Vibrato
        self.vibrato_depth = 0.0       # semitones
        self.vibrato_rate = 6.0        # Hz

        # Arpeggio (list of semitone offsets from base note)
        self.arpeggio_intervals: list[int] = []
        self.arpeggio_rate = 10.0      # notes per second
        self.arpeggio_step = 0
        self.arpeggio_step_samples = 0

        # Portamento
        self.portamento_freq = 0.0
        self.portamento_samples = 0


class Synthesizer:
    """8-bit polyphonic synthesizer with real-time audio output."""

    def __init__(self):
        self._voices: dict[int, Voice] = {}
        self._lock = threading.Lock()
        self._stream: sd.OutputStream | None = None

        # Global parameters
        self._wave_type = WAVE_PULSE_50
        self._volume = 0.7

        # Arpeggio (global — applied to all new voices)
        self._arpeggio_type: str | None = None
        self._arpeggio_rate = 10.0

        # Vibrato (global)
        self._vibrato_depth = 0.0
        self._vibrato_rate = 6.0

        # ADSR (global)
        self._attack = 0.02
        self._decay = 0.05
        self._sustain = 0.7
        self._release = 0.1

        # Custom wavetable
        self._wavetable: list[float] = list(DEFAULT_WAVETABLE)

        # Noise state
        self._noise_seed_short = 0x7FFF   # 15-bit LFSR
        self._noise_seed_long = 0x7FFF    # 15-bit → 93-bit mode
        self._noise_periodic_phase = 0

    # ── wave generators ───────────────────────────────────

    @staticmethod
    def _pulse(phase: float, duty: float) -> float:
        return 1.0 if (phase % 1.0) < duty else -1.0

    @staticmethod
    def _triangle(phase: float) -> float:
        p = phase % 1.0
        if p < 0.25:
            return 4.0 * p
        elif p < 0.75:
            return 2.0 - 4.0 * p
        else:
            return 4.0 * p - 4.0

    @staticmethod
    def _sawtooth(phase: float) -> float:
        return 2.0 * (phase % 1.0) - 1.0

    @staticmethod
    def _sine(phase: float) -> float:
        return math.sin(2.0 * math.pi * phase)

    def _noise_short(self) -> float:
        """NES noise mode 0: 15-bit LFSR, 32767-bit period."""
        bit = (self._noise_seed_short & 1) ^ ((self._noise_seed_short >> 1) & 1)
        self._noise_seed_short = (self._noise_seed_short >> 1) | (bit << 14)
        return (self._noise_seed_short & 1) * 2.0 - 1.0

    def _noise_long(self) -> float:
        """NES noise mode 1: 15-bit LFSR with 6-bit feedback (93-bit period)."""
        bit = (self._noise_seed_long & 1) ^ ((self._noise_seed_long >> 6) & 1)
        self._noise_seed_long = (self._noise_seed_long >> 1) | (bit << 14)
        return (self._noise_seed_long & 1) * 2.0 - 1.0

    def _noise_periodic(self, freq: float) -> float:
        """C64-style tuned noise: cycle noise seed at given frequency."""
        self._noise_periodic_phase += freq / SAMPLE_RATE
        if self._noise_periodic_phase >= 1.0:
            self._noise_periodic_phase -= 1.0
        # XOR-feedback tone generator → metallic ring
        val = ((int(self._noise_periodic_phase * 16) & 0xF) << 1) - 15
        return val / 15.0

    def _wavetable_sample(self, phase: float) -> float:
        """Read from custom wavetable (32 samples)."""
        idx = int(phase % 1.0 * len(self._wavetable)) % len(self._wavetable)
        return self._wavetable[idx]

    # ── envelope ──────────────────────────────────────────

    def _tick_envelope(self, v: Voice) -> float:
        """Update envelope level, return current amplitude (0-1)."""
        if v.envelope_phase == 0:  # attack
            if v.attack_samples > 0:
                v.env_level += 1.0 / v.attack_samples
            if v.env_level >= 1.0:
                v.env_level = 1.0
                v.envelope_phase = 1
        elif v.envelope_phase == 1:  # decay
            if v.decay_samples > 0:
                v.env_level -= (1.0 - v.sustain_level) / v.decay_samples
            if v.env_level <= v.sustain_level:
                v.env_level = v.sustain_level
                v.envelope_phase = 2
        elif v.envelope_phase == 2:  # sustain
            if v.release:
                v.envelope_phase = 3
        elif v.envelope_phase == 3:  # release
            if v.release_samples > 0:
                v.env_level -= v.sustain_level / v.release_samples
            if v.env_level <= 0.0:
                v.env_level = 0.0
                v.active = False
        return v.env_level

    # ── per-sample generation ─────────────────────────────

    def _generate_sample(self, voice: Voice) -> float:
        """Generate one sample for a voice, accounting for all effects."""

        # Arpeggio: cycle through intervals
        if voice.arpeggio_intervals:
            samples_per_step = max(1, int(SAMPLE_RATE / voice.arpeggio_rate))
            if voice.arpeggio_step_samples >= samples_per_step:
                voice.arpeggio_step_samples = 0
                voice.arpeggio_step = (voice.arpeggio_step + 1) % len(
                    voice.arpeggio_intervals
                )
            offset = voice.arpeggio_intervals[voice.arpeggio_step]
            freq = voice.base_frequency * (2.0 ** (offset / 12.0))
            voice.arpeggio_step_samples += 1
        else:
            freq = voice.base_frequency

        # Portamento (slide toward target)
        if voice.portamento_samples > 0:
            voice.portamento_samples -= 1
            t = 1.0 - voice.portamento_samples / max(1, voice.portamento_samples + 1)
            voice.frequency = voice.frequency + (
                voice.portamento_freq - voice.frequency
            ) * (1.0 - math.cos(t * math.pi)) / 2
        else:
            voice.frequency = freq

        # Vibrato (LFO)
        eff_freq = voice.frequency
        if voice.vibrato_depth > 0:
            lfo = math.sin(2.0 * math.pi * voice.vibrato_rate *
                          voice.sample_idx / SAMPLE_RATE)
            eff_freq *= 2.0 ** ((voice.vibrato_depth / 12.0) * lfo)

        # Generate raw waveform
        wt = voice.wave_type
        if wt == WAVE_PULSE_125:
            value = self._pulse(voice.phase, 0.125)
        elif wt == WAVE_PULSE_25:
            value = self._pulse(voice.phase, 0.25)
        elif wt == WAVE_PULSE_50:
            value = self._pulse(voice.phase, 0.5)
        elif wt == WAVE_PULSE_75:
            value = self._pulse(voice.phase, 0.75)
        elif wt == WAVE_TRIANGLE:
            value = self._triangle(voice.phase)
        elif wt == WAVE_SAWTOOTH:
            value = self._sawtooth(voice.phase)
        elif wt == WAVE_NOISE_SHORT:
            value = self._noise_short()
        elif wt == WAVE_NOISE_LONG:
            value = self._noise_long()
        elif wt == WAVE_NOISE_PERIODIC:
            value = self._noise_periodic(eff_freq)
        elif wt == WAVE_SINE:
            value = self._sine(voice.phase)
        elif wt == WAVE_WAVETABLE:
            value = self._wavetable_sample(voice.phase)
        else:
            value = self._pulse(voice.phase, 0.5)

        voice.phase += eff_freq / SAMPLE_RATE
        voice.sample_idx += 1

        # Apply envelope
        env = self._tick_envelope(voice)
        return value * voice.velocity * self._volume * env

    # ── audio callback ────────────────────────────────────

    def _audio_callback(self, outdata: np.ndarray, frames: int,
                        _time, _status) -> None:
        outdata.fill(0.0)
        with self._lock:
            active_voices = [v for v in self._voices.values() if v.active]
            if not active_voices:
                return

            for i in range(frames):
                sample = 0.0
                for voice in active_voices:
                    sample += self._generate_sample(voice)
                # Hard clip (authentic 8-bit)
                sample = max(-1.0, min(1.0, sample))
                outdata[i, 0] = sample

            # Clean up finished voices
            finished = [
                midi for midi, v in self._voices.items()
                if not v.active
            ]
            for midi in finished:
                del self._voices[midi]

    # ── public API ────────────────────────────────────────

    def start(self) -> None:
        if self._stream is not None:
            return
        sd.default.samplerate = SAMPLE_RATE
        sd.default.channels = CHANNELS
        self._stream = sd.OutputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            blocksize=BUFFER_SIZE,
            callback=self._audio_callback,
            latency="low",
        )
        self._stream.start()

    def stop(self) -> None:
        if self._stream is None:
            return
        self._stream.stop()
        self._stream.close()
        self._stream = None

    def _make_voice(self, midi_note: int) -> Voice:
        v = Voice(midi_note, self._wave_type, self._volume)
        v.vibrato_depth = self._vibrato_depth
        v.vibrato_rate = self._vibrato_rate
        v.attack_samples = int(SAMPLE_RATE * self._attack)
        v.decay_samples = int(SAMPLE_RATE * self._decay)
        v.sustain_level = self._sustain
        v.release_samples = int(SAMPLE_RATE * self._release)
        if self._arpeggio_type and self._arpeggio_type in ARPEGGIO_INTERVALS:
            v.arpeggio_intervals = list(
                ARPEGGIO_INTERVALS[self._arpeggio_type]
            )
            v.arpeggio_rate = self._arpeggio_rate
        return v

    def note_on(self, midi_note: int) -> None:
        with self._lock:
            if midi_note in self._voices:
                existing = self._voices[midi_note]
                existing.phase = 0.0
                existing.sample_idx = 0
                existing.env_level = 0.0
                existing.envelope_phase = 0
                existing.active = True
                existing.release = False
                return

            if len(self._voices) >= MAX_POLYPHONY:
                oldest = min(
                    (v for v in self._voices.values() if not v.release),
                    key=lambda v: v.sample_idx,
                    default=None,
                )
                if oldest is not None:
                    oldest.release = True
                else:
                    return  # all are releasing, don't steal

            self._voices[midi_note] = self._make_voice(midi_note)

    def note_off(self, midi_note: int) -> None:
        with self._lock:
            if midi_note in self._voices:
                self._voices[midi_note].release = True

    def set_wave_type(self, wave_type: str) -> None:
        self._wave_type = wave_type
        with self._lock:
            for voice in self._voices.values():
                voice.wave_type = wave_type

    def set_volume(self, volume: float) -> None:
        self._volume = max(0.0, min(1.0, volume))

    def set_arpeggio(self, arp_type: str | None) -> None:
        self._arpeggio_type = arp_type

    def set_arpeggio_rate(self, rate: float) -> None:
        self._arpeggio_rate = max(1.0, min(30.0, rate))

    def set_vibrato(self, depth: float, rate: float) -> None:
        self._vibrato_depth = depth
        self._vibrato_rate = rate

    def set_adsr(self, attack: float, decay: float,
                 sustain: float, release: float) -> None:
        self._attack = attack
        self._decay = decay
        self._sustain = sustain
        self._release = release

    def set_wavetable(self, samples: list[float]) -> None:
        """Load custom wavetable (list of 32 floats -1.0..1.0)."""
        if len(samples) >= 2:
            self._wavetable = list(samples)

    def all_notes_off(self) -> None:
        with self._lock:
            self._voices.clear()
