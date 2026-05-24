"""
Offline audio renderer: converts structured note timelines to WAV/MP3.

Input format (from LLM):
{
  "bpm": 140,
  "tracks": [
    {"instrument": "pulse_50", "notes": [{"n": "C4", "b": 0.0, "d": 0.5, "v": 0.8}]}
  ]
}
"""

from __future__ import annotations

import math
import os
import subprocess
import tempfile

import numpy as np
import soundfile as sf

from ..audio.constants import MIDI_FREQS, SAMPLE_RATE, WAVE_TYPES

_NOTE_MAP = {
    "C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
    "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
    "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11,
}

# Envelope constants (samples at 44100 Hz)
_ATTACK_SAMPLES = int(SAMPLE_RATE * 0.005)   # 5 ms
_RELEASE_SAMPLES = int(SAMPLE_RATE * 0.05)   # 50 ms


def parse_note(name: str) -> int:
    """Parse 'C4' -> 60, 'D#3' -> 51, etc."""
    name = name.strip().upper()
    try:
        return int(name)
    except ValueError:
        pass
    if len(name) >= 2:
        note_part = name[:-1]
        octave_part = name[-1]
        if note_part in _NOTE_MAP and octave_part.isdigit():
            return _NOTE_MAP[note_part] + (int(octave_part) + 1) * 12
    raise ValueError(f"Cannot parse note: {name}")


# ─── Vectorized waveform generators ──────────────────────────

def _gen_pulse(phase_norm: np.ndarray, duty: float) -> np.ndarray:
    return np.where(phase_norm < duty, 1.0, -1.0).astype(np.float32)


def _gen_triangle(phase_norm: np.ndarray) -> np.ndarray:
    """Vectorized triangle wave. phase_norm in [0, 1)."""
    p = phase_norm.astype(np.float32)
    out = np.empty_like(p)
    # 0.00-0.25: 4p
    mask1 = p < 0.25
    out[mask1] = 4.0 * p[mask1]
    # 0.25-0.75: 2 - 4p
    mask2 = (p >= 0.25) & (p < 0.75)
    out[mask2] = 2.0 - 4.0 * p[mask2]
    # 0.75-1.00: 4p - 4
    mask3 = p >= 0.75
    out[mask3] = 4.0 * p[mask3] - 4.0
    return out


def _gen_sawtooth(phase_norm: np.ndarray) -> np.ndarray:
    return (2.0 * phase_norm - 1.0).astype(np.float32)


def _gen_sine(phase_norm: np.ndarray) -> np.ndarray:
    return np.sin(2.0 * np.pi * phase_norm).astype(np.float32)


def _gen_wavetable(phase_norm: np.ndarray) -> np.ndarray:
    return (_gen_triangle(phase_norm) * 0.7 +
            _gen_pulse(phase_norm, 0.25) * 0.3)


def _gen_noise_lfsr(n_samples: int, seed: int, tap1: int, tap2: int) -> np.ndarray:
    """Generate N samples of LFSR noise (vectorized for speed using numpy)."""
    # For long sequences, use a fast dtype loop
    reg = np.uint16(seed)
    out = np.empty(n_samples, dtype=np.float32)
    # Pre-compute in chunks for speed
    for i in range(n_samples):
        bit = ((int(reg) & 1) ^ ((int(reg) >> tap1) & 1)) & 1
        reg = (reg >> 1) | (np.uint16(bit) << 14)
        out[i] = float(int(reg) & 1) * 2.0 - 1.0
    return out


# ─── Envelope generator ──────────────────────────────────────

def _make_ar_envelope(n_samples: int, velocity: float, volume: float) -> np.ndarray:
    """Create attack-release envelope for a note."""
    env = np.ones(n_samples, dtype=np.float32) * velocity * volume
    # Attack ramp
    att_len = min(_ATTACK_SAMPLES, n_samples)
    if att_len > 1:
        env[:att_len] *= np.linspace(0.0, 1.0, att_len, dtype=np.float32)
    # Release ramp
    rel_len = min(_RELEASE_SAMPLES, n_samples)
    if rel_len > 1:
        env[-rel_len:] *= np.linspace(1.0, 0.0, rel_len, dtype=np.float32)
    return env


# ─── Waveform dispatch ───────────────────────────────────────

def _gen_waveform(wave_type: str, phase_norm: np.ndarray) -> np.ndarray:
    """Generate periodic waveform samples. Noise handled separately by Renderer."""
    if wave_type in ("pulse_12", "pulse_125"):
        return _gen_pulse(phase_norm, 0.125)
    elif wave_type == "pulse_25":
        return _gen_pulse(phase_norm, 0.25)
    elif wave_type == "pulse_50":
        return _gen_pulse(phase_norm, 0.5)
    elif wave_type == "pulse_75":
        return _gen_pulse(phase_norm, 0.75)
    elif wave_type == "triangle":
        return _gen_triangle(phase_norm)
    elif wave_type == "sawtooth":
        return _gen_sawtooth(phase_norm)
    elif wave_type == "sine":
        return _gen_sine(phase_norm)
    elif wave_type == "wavetable":
        return _gen_wavetable(phase_norm)
    else:
        return _gen_pulse(phase_norm, 0.5)


# ─── Renderer ────────────────────────────────────────────────

class Renderer:
    """Offline audio renderer with vectorized sample generation."""

    # Pre-generated noise buffers (lazy, shared across all instances)
    _noise_cache: dict[str, np.ndarray] = {}
    _NOISE_CACHE_SECS = 30  # pre-generate 30 seconds of noise

    def __init__(self):
        self._noise_offset: dict[str, int] = {
            "noise_short": 0,
            "noise_long": 0,
            "noise_periodic": 0,
        }

    @classmethod
    def _get_noise_buffer(cls, noise_type: str) -> np.ndarray:
        """Get or create a pre-generated noise buffer."""
        if noise_type not in cls._noise_cache:
            n_samples = int(SAMPLE_RATE * cls._NOISE_CACHE_SECS)
            if noise_type == "noise_short":
                buf = _gen_noise_lfsr(n_samples, 0x7FFF, 1, 1)
            elif noise_type == "noise_long":
                buf = _gen_noise_lfsr(n_samples, 0x7FFF, 6, 6)
            elif noise_type == "noise_periodic":
                buf = _gen_noise_lfsr(n_samples, 0x7FFF, 6, 1)
            else:
                buf = np.zeros(n_samples, dtype=np.float32)
            cls._noise_cache[noise_type] = buf
        return cls._noise_cache[noise_type]

    def _slice_noise(self, noise_type: str, n: int) -> np.ndarray:
        """Get N samples of pre-generated noise, advancing the offset."""
        buf = self._get_noise_buffer(noise_type)
        offset = self._noise_offset.get(noise_type, 0)
        # Wrap around if needed
        if offset + n > len(buf):
            # Simple wrap: take from offset to end, then from start
            first = buf[offset:]
            second = buf[:n - len(first)]
            result = np.concatenate([first, second])
            self._noise_offset[noise_type] = n - len(first)
        else:
            result = buf[offset:offset + n].copy()
            self._noise_offset[noise_type] = offset + n
        return result

    def render_multi(self, composition: dict, volume: float = 0.6
                     ) -> dict[str, np.ndarray]:
        """Render all tracks, returning per-track audio arrays.

        Returns: {instrument_name: np.ndarray}
        """
        bpm = composition.get("bpm", 120)
        tracks = composition.get("tracks", [])

        if not tracks:
            return {"silence": np.zeros(int(SAMPLE_RATE * 1), dtype=np.float32)}

        beat_dur = 60.0 / bpm

        # ── Compute total length ──
        max_end = 0.0
        for track in tracks:
            for note in track.get("notes", []):
                end_beat = note.get("b", 0.0) + note.get("d", 0.25)
                if end_beat > max_end:
                    max_end = end_beat
        total_beats = max_end + 0.25
        total_samples = int(total_beats * beat_dur * SAMPLE_RATE)

        # ── Render each track ──
        result: dict[str, np.ndarray] = {}

        for track in tracks:
            instrument = track.get("instrument", "pulse_50")
            if instrument not in WAVE_TYPES:
                instrument = "pulse_50"

            is_noise = instrument in ("noise_short", "noise_long",
                                      "noise_periodic")
            buf = np.zeros(total_samples, dtype=np.float32)
            notes = track.get("notes", [])

            for note in notes:
                try:
                    pitch = parse_note(note["n"])
                except (KeyError, ValueError):
                    continue

                freq = MIDI_FREQS.get(pitch, 440.0)
                start_beat = note.get("b", 0.0)
                dur_beat = note.get("d", 0.25)
                vel = note.get("v", 0.8)

                start_s = int(start_beat * beat_dur * SAMPLE_RATE)
                n_s = max(1, int(dur_beat * beat_dur * SAMPLE_RATE))
                end_s = min(start_s + n_s, total_samples)
                n_s = end_s - start_s
                if n_s <= 0:
                    continue

                # ── Waveform generation ──
                if is_noise:
                    wave = self._slice_noise(instrument, n_s)
                else:
                    t = np.arange(n_s, dtype=np.float32)
                    phase_norm = (freq * t / SAMPLE_RATE) % 1.0
                    wave = _gen_waveform(instrument, phase_norm)

                # ── Envelope ──
                env = _make_ar_envelope(n_s, vel, volume)

                # ── Mix into buffer ──
                buf[start_s:end_s] += wave * env

            result[instrument] = buf

        return result

    def render(self, composition: dict, volume: float = 0.6) -> np.ndarray:
        """Render to a single mixed buffer (backward-compatible)."""
        per_track = self.render_multi(composition, volume=volume)
        if not per_track:
            return np.zeros(int(SAMPLE_RATE * 1), dtype=np.float32)

        # Sum all tracks
        max_len = max(len(a) for a in per_track.values())
        audio = np.zeros(max_len, dtype=np.float64)
        for arr in per_track.values():
            audio[:len(arr)] += arr.astype(np.float64)

        # Normalize
        peak = float(np.max(np.abs(audio)))
        if peak > 0.99:
            audio = audio / peak * 0.95

        return audio.astype(np.float32)

    def save_wav(self, audio: np.ndarray, path: str) -> str:
        sf.write(path, audio, SAMPLE_RATE)
        return path

    def save_mp3(self, audio: np.ndarray, path: str, bitrate: str = "192k") -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            wav_path = tmp.name
        try:
            self.save_wav(audio, wav_path)
            subprocess.run(
                ["ffmpeg", "-y", "-i", wav_path, "-b:a", bitrate, path],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True,
            )
        finally:
            os.unlink(wav_path)
        return path
