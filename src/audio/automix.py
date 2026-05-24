"""
Intent-Driven Automix DSP Engine.

A self-contained, zero-external-dependency mixing and mastering system
for 8-bit chiptune music. Accepts semantic intent tags and translates
them into deterministic DSP parameters — biquad EQ, synthetic IR reverb,
envelope-following compression, sidechain ducking, and look-ahead limiting.

All algorithms are implemented in pure NumPy/SciPy — no external .wav IR
files, no commercial plugins.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np
import scipy.signal as signal

# ---------------------------------------------------------------------------
# 1. Biquad Filter Designer (RBJ Audio EQ Cookbook)
# ---------------------------------------------------------------------------

class BiquadFilterDesigner:
    """Coefficient designer for peaking, shelving, highpass, lowpass filters."""

    @staticmethod
    def design_peaking_eq(fs: float, f0: float, q: float, gain_db: float):
        A = 10.0 ** (gain_db / 40.0)
        w0 = 2.0 * math.pi * f0 / fs
        alpha = math.sin(w0) / (2.0 * q)
        cos_w0 = math.cos(w0)

        b0 = 1.0 + alpha * A
        b1 = -2.0 * cos_w0
        b2 = 1.0 - alpha * A
        a0 = 1.0 + alpha / A
        a1 = -2.0 * cos_w0
        a2 = 1.0 - alpha / A

        return [b0 / a0, b1 / a0, b2 / a0], [1.0, a1 / a0, a2 / a0]

    @staticmethod
    def design_highpass(fs: float, f0: float, q: float = 0.7071):
        w0 = 2.0 * math.pi * f0 / fs
        alpha = math.sin(w0) / (2.0 * q)
        cos_w0 = math.cos(w0)

        b0 = (1.0 + cos_w0) / 2.0
        b1 = -(1.0 + cos_w0)
        b2 = (1.0 + cos_w0) / 2.0
        a0 = 1.0 + alpha
        a1 = -2.0 * cos_w0
        a2 = 1.0 - alpha

        return [b0 / a0, b1 / a0, b2 / a0], [1.0, a1 / a0, a2 / a0]

    @staticmethod
    def design_lowpass(fs: float, f0: float, q: float = 0.7071):
        w0 = 2.0 * math.pi * f0 / fs
        alpha = math.sin(w0) / (2.0 * q)
        cos_w0 = math.cos(w0)

        b0 = (1.0 - cos_w0) / 2.0
        b1 = 1.0 - cos_w0
        b2 = (1.0 - cos_w0) / 2.0
        a0 = 1.0 + alpha
        a1 = -2.0 * cos_w0
        a2 = 1.0 - alpha

        return [b0 / a0, b1 / a0, b2 / a0], [1.0, a1 / a0, a2 / a0]

    @staticmethod
    def design_low_shelf(fs: float, f0: float, gain_db: float, q: float = 0.7071):
        A = 10.0 ** (gain_db / 40.0)
        w0 = 2.0 * math.pi * f0 / fs
        alpha = math.sin(w0) / (2.0 * q)
        cos_w0 = math.cos(w0)
        two_sqrt_A_alpha = 2.0 * math.sqrt(A) * alpha

        b0 = A * ((A + 1.0) - (A - 1.0) * cos_w0 + two_sqrt_A_alpha)
        b1 = 2.0 * A * ((A - 1.0) - (A + 1.0) * cos_w0)
        b2 = A * ((A + 1.0) - (A - 1.0) * cos_w0 - two_sqrt_A_alpha)
        a0 = (A + 1.0) + (A - 1.0) * cos_w0 + two_sqrt_A_alpha
        a1 = -2.0 * ((A - 1.0) + (A + 1.0) * cos_w0)
        a2 = (A + 1.0) + (A - 1.0) * cos_w0 - two_sqrt_A_alpha

        return [b0 / a0, b1 / a0, b2 / a0], [1.0, a1 / a0, a2 / a0]

    @staticmethod
    def design_high_shelf(fs: float, f0: float, gain_db: float, q: float = 0.7071):
        A = 10.0 ** (gain_db / 40.0)
        w0 = 2.0 * math.pi * f0 / fs
        alpha = math.sin(w0) / (2.0 * q)
        cos_w0 = math.cos(w0)
        two_sqrt_A_alpha = 2.0 * math.sqrt(A) * alpha

        b0 = A * ((A + 1.0) + (A - 1.0) * cos_w0 + two_sqrt_A_alpha)
        b1 = -2.0 * A * ((A - 1.0) + (A + 1.0) * cos_w0)
        b2 = A * ((A + 1.0) + (A - 1.0) * cos_w0 - two_sqrt_A_alpha)
        a0 = (A + 1.0) - (A - 1.0) * cos_w0 + two_sqrt_A_alpha
        a1 = 2.0 * ((A - 1.0) - (A + 1.0) * cos_w0)
        a2 = (A + 1.0) - (A - 1.0) * cos_w0 - two_sqrt_A_alpha

        return [b0 / a0, b1 / a0, b2 / a0], [1.0, a1 / a0, a2 / a0]


# ---------------------------------------------------------------------------
# 2. Synthetic Impulse Response Generator
# ---------------------------------------------------------------------------

class SyntheticIRGenerator:
    """Mathematically synthesised spatial impulse responses.

    No external .wav IR files needed — the acoustic space is modelled via
    exponentially decaying noise with time-varying high-frequency damping,
    producing convincing room/hall/cathedral/space ambience.
    """

    @staticmethod
    def generate_ir(fs: float, decay_time: float, pre_delay_ms: float,
                    damping: float) -> np.ndarray:
        """Generate a synthetic IR for convolution reverb.

        Args:
            fs: Sample rate (Hz).
            decay_time: RT60 decay time in seconds.
            pre_delay_ms: Pre-delay in milliseconds.
            damping: High-frequency damping coefficient (0=none, 1=heavy).

        Returns:
            Normalised impulse response as float32 numpy array.
        """
        if decay_time <= 0.0:
            # Dry: return a unit impulse
            ir = np.zeros(int(fs * 0.01) + 1, dtype=np.float32)
            ir[0] = 1.0
            return ir

        total_samples = int(fs * (decay_time + pre_delay_ms / 1000.0)) + 1
        pre_delay_samples = max(1, int(fs * (pre_delay_ms / 1000.0)))
        decay_samples = total_samples - pre_delay_samples

        if decay_samples < 1:
            decay_samples = 1

        # 1. White noise excitation
        rng = np.random.default_rng()
        noise = rng.normal(0.0, 1.0, decay_samples).astype(np.float32)

        # 2. Exponential decay envelope (-60 dB at RT60)
        t = np.linspace(0.0, decay_time, decay_samples, dtype=np.float32)
        envelope = np.exp(-6.91 * t / max(decay_time, 1e-6))

        # 3. Time-varying low-pass filter (simulates air absorption)
        #    Damping increases with time — later reflections lose high frequencies
        filtered = np.zeros(decay_samples, dtype=np.float32)
        prev = 0.0
        for i in range(decay_samples):
            # Coefficient ramps from 'damping' toward 0.95 over the decay
            progress = i / max(decay_samples - 1, 1)
            current_damping = damping + (0.95 - damping) * progress * 0.5
            current_damping = min(0.99, current_damping)
            filtered[i] = (1.0 - current_damping) * noise[i] + current_damping * prev
            prev = filtered[i]

        # 4. Apply envelope and insert pre-delay
        ir = np.zeros(total_samples, dtype=np.float32)
        start = min(pre_delay_samples, total_samples - 1)
        end = min(start + decay_samples, total_samples)
        write_len = end - start
        ir[start:end] = filtered[:write_len] * envelope[:write_len]

        # 5. Normalise energy
        energy = np.sqrt(np.sum(ir ** 2))
        if energy > 1e-12:
            ir /= energy

        return ir


# ---------------------------------------------------------------------------
# 3. Dynamic Compressor
# ---------------------------------------------------------------------------

class DynamicCompressor:
    """Envelope-following dynamics compressor with optional sidechain."""

    def __init__(self, fs: float):
        self.fs = fs

    def process(self, input_sig: np.ndarray, sidechain_sig: np.ndarray | None = None,
                threshold_db: float = -12.0, ratio: float = 4.0,
                attack_ms: float = 10.0, release_ms: float = 100.0,
                makeup_db: float = 0.0) -> np.ndarray:
        """Apply compression to input_sig.

        Args:
            input_sig: Audio to compress.
            sidechain_sig: External sidechain trigger (e.g. kick for ducking).
            threshold_db: Threshold in dBFS.
            ratio: Compression ratio (e.g. 4.0 = 4:1).
            attack_ms: Attack time in milliseconds.
            release_ms: Release time in milliseconds.
            makeup_db: Makeup gain in dB.

        Returns:
            Compressed audio.
        """
        detector = sidechain_sig if sidechain_sig is not None else input_sig

        num_samples = len(input_sig)
        if num_samples == 0:
            return input_sig.copy()

        # 1. Time constants
        alpha_attack = math.exp(-1.0 / max(attack_ms * 0.001 * self.fs, 1e-6))
        alpha_release = math.exp(-1.0 / max(release_ms * 0.001 * self.fs, 1e-6))

        # 2. Peak envelope follower (vectorized dual-filter approach)
        abs_detector = np.abs(detector).astype(np.float64)
        # Attack filter: fast rise AND fast fall
        env_attack = signal.lfilter(
            [1.0 - alpha_attack], [1.0, -alpha_attack], abs_detector,
        )
        # Release filter: fast rise AND slow fall
        env_release = signal.lfilter(
            [1.0 - alpha_release], [1.0, -alpha_release], abs_detector,
        )
        # max(envelope_att, envelope_rel) ≈ conditional attack/release behavior
        envelope = np.maximum(env_attack, env_release).astype(np.float32)

        # 3. Gain reduction computation
        eps = 1e-10
        envelope_db = 20.0 * np.log10(envelope + eps)
        gain_reduction_db = np.zeros(num_samples, dtype=np.float32)

        over = envelope_db > threshold_db
        gain_reduction_db[over] = (threshold_db - envelope_db[over]) * (1.0 - 1.0 / ratio)

        # 4. Apply gain
        gain_linear = 10.0 ** ((gain_reduction_db + makeup_db) / 20.0)
        output_sig = input_sig * gain_linear

        return output_sig.astype(np.float32)


# ---------------------------------------------------------------------------
# 4. Master Look-ahead Limiter
# ---------------------------------------------------------------------------

class MasterLimiter:
    """Brick-wall look-ahead limiter to prevent digital clipping."""

    @staticmethod
    def process(input_sig: np.ndarray, limit_db: float = -0.3,
                lookahead_ms: float = 2.0, release_ms: float = 50.0,
                fs: float = 44100.0) -> np.ndarray:
        """Apply look-ahead peak limiting (vectorized)."""
        num_samples = len(input_sig)
        if num_samples == 0:
            return input_sig.copy()

        lookahead_samples = max(1, int(fs * (lookahead_ms / 1000.0)))
        limit_linear = 10.0 ** (limit_db / 20.0)

        # 1. Running max over look-ahead window (vectorized via scipy)
        from scipy.ndimage import maximum_filter1d
        abs_sig = np.abs(input_sig).astype(np.float64)
        peak_envelope = maximum_filter1d(abs_sig, size=lookahead_samples,
                                         mode='constant', cval=0.0)

        # 2. Release smoothing (one-pole lowpass on the peak envelope)
        alpha_release = math.exp(-1.0 / max(release_ms * 0.001 * fs, 1e-6))
        peak_smoothed = signal.lfilter(
            [1.0 - alpha_release], [1.0, -alpha_release], peak_envelope,
        )

        # 3. Gain reduction
        gains = np.ones(num_samples, dtype=np.float32)
        over = peak_smoothed > limit_linear
        gains[over] = limit_linear / (peak_smoothed[over].astype(np.float32) + 1e-10)

        return (input_sig * gains).astype(np.float32)


# ---------------------------------------------------------------------------
# 5. Automix Engine (orchestrator)
# ---------------------------------------------------------------------------

class AutomixEngine:
    """Semantic-intent-driven automatic mixing and mastering engine.

    Usage:
        engine = AutomixEngine(fs=44100)
        mastered = engine.mix_and_master({
            "lead":   {"audio": lead_arr,   "role": "lead",   "tone": "bright",
                       "dynamics": "natural", "space": "hall"},
            "bass":   {"audio": bass_arr,   "role": "bass",   "tone": "warm",
                       "dynamics": "compressed", "space": "dry"},
            "kick":   {"audio": kick_arr,   "role": "kick",   "tone": "bass_boost",
                       "dynamics": "punchy", "space": "dry"},
            "snare":  {"audio": snare_arr,  "role": "perc",   "tone": "bright",
                       "dynamics": "gated", "space": "room"},
            "hihat":  {"audio": hihat_arr,  "role": "perc",   "tone": "bright",
                       "dynamics": "natural", "space": "room"},
            "pad":    {"audio": pad_arr,    "role": "pad",    "tone": "warm",
                       "dynamics": "sustained", "space": "space_ambient"},
        }, global_vibe="jpop_modern")
    """

    def __init__(self, fs: float = 44100.0):
        self.fs = fs
        self.compressor = DynamicCompressor(self.fs)

        # ── Space / Reverb map ──
        self.space_map: dict[str, dict] = {
            "dry":           {"decay": 0.0, "pre_delay": 0,  "damping": 1.0, "wet": 0.0},
            "room":          {"decay": 0.6, "pre_delay": 10, "damping": 0.4, "wet": 0.15},
            "hall":          {"decay": 2.2, "pre_delay": 25, "damping": 0.6, "wet": 0.30},
            "cathedral":     {"decay": 4.5, "pre_delay": 45, "damping": 0.8, "wet": 0.45},
            "space_ambient": {"decay": 8.0, "pre_delay": 60, "damping": 0.3, "wet": 0.55},
            "plate_retro":   {"decay": 1.8, "pre_delay": 5,  "damping": 0.2, "wet": 0.35},
        }

        # ── Dynamics / Compression map ──
        self.dynamics_map: dict[str, dict] = {
            "natural":    {"thresh_offset": -3.0,  "ratio": 1.5, "attack": 40.0,  "release": 150.0},
            "punchy":     {"thresh_offset": -8.0,  "ratio": 3.5, "attack": 30.0,  "release": 50.0},
            "compressed": {"thresh_offset": -15.0, "ratio": 6.0, "attack": 10.0,  "release": 200.0},
            "sustained":  {"thresh_offset": -20.0, "ratio": 8.0, "attack": 2.0,   "release": 600.0},
            "gated":      {"thresh_offset": -12.0, "ratio": 10.0,"attack": 1.0,   "release": 20.0},
        }

        # ── Tone / EQ map: list of (type, f0, Q, gain_db) ──
        self.tone_map: dict[str, list[tuple]] = {
            "bright": [
                ("hpf", 80.0, 0.707, 0.0),
                ("peaking", 3000.0, 0.7, 3.0),
                ("high_shelf", 8000.0, 0.707, 4.0),
            ],
            "warm": [
                ("low_shelf", 200.0, 0.707, 3.0),
                ("peaking", 500.0, 0.5, 1.5),
                ("lpf", 12000.0, 0.707, 0.0),
            ],
            "dark": [
                ("hpf", 40.0, 0.707, 0.0),
                ("peaking", 1000.0, 0.5, -2.0),
                ("lpf", 6000.0, 0.707, 0.0),
            ],
            "telephony": [
                ("hpf", 400.0, 0.707, 0.0),
                ("peaking", 1500.0, 1.0, 6.0),
                ("lpf", 4000.0, 0.707, 0.0),
            ],
            "bass_boost": [
                ("low_shelf", 100.0, 0.707, 6.0),
                ("peaking", 250.0, 0.7, -2.0),
                ("high_shelf", 10000.0, 0.707, -2.0),
            ],
            "scooped": [
                ("low_shelf", 120.0, 0.707, 2.0),
                ("peaking", 1000.0, 1.5, -6.0),
                ("high_shelf", 6000.0, 0.707, 3.0),
            ],
        }

        # ── Sidechain-eligible roles ──
        self._sc_roles = {"bass", "pad", "harmony", "arp"}

    # ------------------------------------------------------------------
    # Internal: apply EQ chain
    # ------------------------------------------------------------------

    def _apply_eq(self, sig: np.ndarray, tone_tag: str | None) -> np.ndarray:
        if tone_tag is None or tone_tag not in self.tone_map:
            return sig

        processed = sig.copy()
        for f_type, f0, q, gain in self.tone_map[tone_tag]:
            if f_type == "hpf":
                b, a = BiquadFilterDesigner.design_highpass(self.fs, f0, q)
            elif f_type == "lpf":
                b, a = BiquadFilterDesigner.design_lowpass(self.fs, f0, q)
            elif f_type == "peaking":
                b, a = BiquadFilterDesigner.design_peaking_eq(self.fs, f0, q, gain)
            elif f_type == "low_shelf":
                b, a = BiquadFilterDesigner.design_low_shelf(self.fs, f0, gain, q)
            elif f_type == "high_shelf":
                b, a = BiquadFilterDesigner.design_high_shelf(self.fs, f0, gain, q)
            else:
                continue
            processed = signal.lfilter(b, a, processed)

        return processed.astype(np.float32)

    # ------------------------------------------------------------------
    # Main entry point
    # ------------------------------------------------------------------

    def mix_and_master(self, tracks_dict: dict, global_vibe: str = "jpop_modern",
                       volume: float = 0.65) -> np.ndarray:
        """Mix and master a set of per-track audio buffers.

        Args:
            tracks_dict: {track_id: {"audio": np.ndarray, "role": str,
                         "tone": str|None, "dynamics": str|None,
                         "space": str|None}}
            global_vibe: Master genre preset.
            volume: Final output volume multiplier (0-1).

        Returns:
            Mastered mono audio as float32 numpy array.
        """
        if not tracks_dict:
            return np.zeros(int(self.fs * 0.5), dtype=np.float32)

        # Determine output length (longest track)
        max_len = max(len(t["audio"]) for t in tracks_dict.values())

        # ── Global vibe settings ──
        vibe_sc_threshold = -12.0
        vibe_reverb_send = 0.15
        master_limit_db = -0.3

        if global_vibe == "cyberpunk_boss":
            vibe_sc_threshold = -18.0
            vibe_reverb_send = 0.08
            master_limit_db = -0.1
        elif global_vibe == "fantasy_village":
            vibe_sc_threshold = 0.0  # sidechain off
            vibe_reverb_send = 0.28
            master_limit_db = -1.0
        elif global_vibe == "lofi_chill":
            vibe_sc_threshold = -10.0
            vibe_reverb_send = 0.35
            master_limit_db = -1.5

        # ── Locate kick for sidechain ──
        kick_signal = None
        for t_info in tracks_dict.values():
            if t_info.get("role") == "kick":
                kick_signal = t_info["audio"].astype(np.float32)
                break

        # Pad kick_signal to max_len for safe sidechain use
        if kick_signal is not None:
            if len(kick_signal) < max_len:
                kick_signal = np.pad(kick_signal, (0, max_len - len(kick_signal)))
            elif len(kick_signal) > max_len:
                kick_signal = kick_signal[:max_len]

        mixed_sum = np.zeros(max_len, dtype=np.float64)
        reverb_sum = np.zeros(max_len, dtype=np.float64)

        for _t_id, t_info in tracks_dict.items():
            audio = t_info["audio"].astype(np.float64)
            # Pad to max_len
            if len(audio) < max_len:
                padded = np.zeros(max_len, dtype=np.float64)
                padded[:len(audio)] = audio
                audio = padded
            elif len(audio) > max_len:
                audio = audio[:max_len]

            role = t_info.get("role", "melody")

            # A. EQ
            audio_eq = self._apply_eq(audio.astype(np.float32),
                                      t_info.get("tone")).astype(np.float64)

            # B. Dynamics
            dyn_tag = t_info.get("dynamics")
            if dyn_tag in self.dynamics_map:
                cfg = self.dynamics_map[dyn_tag]
                rms_db = 20.0 * math.log10(
                    math.sqrt(float(np.mean(audio_eq ** 2))) + 1e-6
                )
                t_val = rms_db + cfg["thresh_offset"]
                audio_dyn = self.compressor.process(
                    audio_eq.astype(np.float32),
                    threshold_db=t_val,
                    ratio=cfg["ratio"],
                    attack_ms=cfg["attack"],
                    release_ms=cfg["release"],
                ).astype(np.float64)
            else:
                audio_dyn = audio_eq

            # C. Sidechain ducking
            if (vibe_sc_threshold < 0.0 and kick_signal is not None
                    and role in self._sc_roles and role != "kick"):
                audio_dyn = self.compressor.process(
                    audio_dyn.astype(np.float32),
                    sidechain_sig=kick_signal,
                    threshold_db=vibe_sc_threshold,
                    ratio=4.0,
                    attack_ms=5.0,
                    release_ms=80.0,
                ).astype(np.float64)

            # D. Reverb send
            space_tag = t_info.get("space")
            if space_tag in self.space_map and space_tag != "dry":
                cfg_sp = self.space_map[space_tag]
                ir = SyntheticIRGenerator.generate_ir(
                    self.fs, cfg_sp["decay"], cfg_sp["pre_delay"],
                    cfg_sp["damping"],
                )
                wet = signal.fftconvolve(
                    audio_dyn.astype(np.float32), ir, mode="same",
                )
                reverb_sum += wet * cfg_sp["wet"] * vibe_reverb_send
                # Dry signal (slightly attenuated to make room for wet)
                mixed_sum += audio_dyn * (1.0 - cfg_sp["wet"] * 0.5)
            else:
                mixed_sum += audio_dyn

        # ── Sum reverb into master ──
        mixed_sum += reverb_sum

        # ── Master glue compression ──
        master_rms_db = 20.0 * math.log10(
            math.sqrt(float(np.mean(mixed_sum ** 2))) + 1e-6
        )
        mixed_sum = self.compressor.process(
            mixed_sum.astype(np.float32),
            threshold_db=master_rms_db - 4.0,
            ratio=2.0,
            attack_ms=25.0,
            release_ms=250.0,
            makeup_db=1.5,
        )

        # ── Master look-ahead limiting ──
        mastered = MasterLimiter.process(
            mixed_sum.astype(np.float32),
            limit_db=master_limit_db,
            lookahead_ms=2.0,
            release_ms=50.0,
            fs=self.fs,
        )

        # ── Safety normalisation ──
        max_peak = float(np.max(np.abs(mastered)))
        if max_peak > 1.0:
            mastered /= max_peak

        # ── Volume trim ──
        mastered *= volume

        return mastered.astype(np.float32)
