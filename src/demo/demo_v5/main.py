#!/usr/bin/env python
"""
8-Bit AI Composer V5 — Intent-Driven Automix DSP.

What's new in V5:
  - Melody-first composition workflow (iron law in system prompt)
  - Per-track mixing via semantic intent DSP engine (AutomixEngine)
  - Global vibe presets: jpop_modern, cyberpunk_boss, fantasy_village, lofi_chill
  - Look-ahead brickwall limiting for clip-free output
"""

from __future__ import annotations

import os
import sys
import time
from typing import Any

# Project root (demo_v5 is 4 levels deep)
_PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, _PROJ_ROOT)
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import numpy as np
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

from src.demo.demo_v5.llm_client import AUTOMIX_VIBES, DEEPSEEK_FLASH_MODEL, \
    DEEPSEEK_MODEL, V5Composer
from src.demo.renderer import Renderer
from src.audio.automix import AutomixEngine
from src.audio.constants import SAMPLE_RATE
from src.demo.tracker_ir_expander import expand_tracker_ir, is_tracker_ir
from src.demo.macro_expander import expand_macro_json, is_macro_format

# ─── ANSI helpers ───
C = {
    "dim": Style.DIM, "bold": Style.BRIGHT,
    "r": Fore.RED, "g": Fore.GREEN, "b": Fore.BLUE,
    "c": Fore.CYAN, "y": Fore.YELLOW, "m": Fore.MAGENTA,
    "w": Fore.WHITE, "reset": Style.RESET_ALL,
}

LOG_PREFIX = f"{C['dim']}[{C['c']}8-bit v5{C['dim']}]{C['reset']}"


def log(level: str, msg: str) -> None:
    tag = {
        "info": f"{C['c']}INFO{C['reset']}",
        "ok":   f"{C['g']}OK{C['reset']}",
        "err":  f"{C['r']}ERR{C['reset']}",
        "llm":  f"{C['y']}LLM{C['reset']}",
        "warn": f"{C['y']}WARN{C['reset']}",
        "music":f"{C['m']}MUSIC{C['reset']}",
        "dsp":  f"{C['m']}DSP{C['reset']}",
    }.get(level, level.upper())
    print(f"{LOG_PREFIX} [{tag}] {msg}")


def print_banner() -> None:
    print()
    print(f"{C['g']}{C['bold']}  ╔══════════════════════════════════════╗")
    print(f"  ║     {C['c']}8-BIT AI COMPOSER V5{C['g']}                 ║")
    print(f"  ║     {C['dim']}Melody-First + Automix DSP{C['g']}           ║")
    print(f"  ╚══════════════════════════════════════╝{C['reset']}")
    print(f"  {C['dim']}Commands: exit | reset | flash | vibes | [music idea]{C['reset']}")
    print()


def print_composition_summary(comp: dict) -> None:
    bpm = comp.get("bpm", "?")
    tracks = comp.get("tracks", [])
    total_notes = sum(len(t.get("notes", [])) for t in tracks)
    total_beats = 0.0
    for t in tracks:
        for n in t.get("notes", []):
            end = n.get("b", 0) + n.get("d", 0)
            if end > total_beats:
                total_beats = end
    duration = total_beats / bpm * 60 if bpm else 0

    print(f"\n  {C['bold']}Composition Summary{C['reset']}")
    print(f"  {C['dim']}├─ BPM:{C['reset']}      {bpm}")
    print(f"  {C['dim']}├─ Tracks:{C['reset']}   {len(tracks)}")
    print(f"  {C['dim']}├─ Notes:{C['reset']}    {total_notes}")
    print(f"  {C['dim']}├─ Length:{C['reset']}   {total_beats:.1f} beats (~{duration:.1f}s)")
    for i, t in enumerate(tracks):
        inst = t.get("instrument", "?")
        n_count = len(t.get("notes", []))
        pitches = {n["n"] for n in t.get("notes", []) if "n" in n}
        note_range = ""
        if pitches:
            sorted_p = sorted(pitches, key=lambda x: (x[-1], x[:-1]))
            note_range = f" {C['dim']}[{sorted_p[0]}..{sorted_p[-1]}]{C['reset']}"
        print(f"  {C['dim']}├─ Track {i+1}:{C['reset']}  {inst} ({n_count} notes){note_range}")


# ─── Instrument → default automix role mapping ───

_INSTRUMENT_ROLE: dict[str, dict[str, str]] = {
    "pulse_50":      {"role": "lead",    "tone": "bright",  "dynamics": "natural",    "space": "hall"},
    "pulse_25":      {"role": "harmony", "tone": "warm",    "dynamics": "natural",    "space": "hall"},
    "pulse_12":      {"role": "harmony", "tone": "bright",  "dynamics": "natural",    "space": "room"},
    "pulse_75":      {"role": "harmony", "tone": "warm",    "dynamics": "natural",    "space": "hall"},
    "triangle":      {"role": "bass",    "tone": "warm",    "dynamics": "compressed", "space": "dry"},
    "sawtooth":      {"role": "pad",     "tone": "bright",  "dynamics": "sustained",  "space": "space_ambient"},
    "wavetable":     {"role": "pad",     "tone": "warm",    "dynamics": "sustained",  "space": "space_ambient"},
    "sine":          {"role": "pad",     "tone": "bright",  "dynamics": "natural",    "space": "cathedral"},
    "noise_long":    {"role": "kick",    "tone": "bass_boost","dynamics": "punchy",    "space": "dry"},
    "noise_short":   {"role": "perc",    "tone": "bright",  "dynamics": "gated",      "space": "room"},
    "noise_periodic":{"role": "perc",    "tone": "scooped", "dynamics": "natural",    "space": "room"},
}

# noise_short variant roles (snare vs hi-hat by suffix)
_NOISE_SHORT_ROLES = {
    0: {"role": "perc",  "tone": "bright", "dynamics": "gated",   "space": "room"},    # snare
    1: {"role": "perc",  "tone": "bright", "dynamics": "natural", "space": "room"},    # hi-hat
}


# Known instruments (must match WAVE_TYPES in audio/constants.py)
_KNOWN_INSTRUMENTS = {
    "pulse_12", "pulse_125", "pulse_25", "pulse_50", "pulse_75",
    "triangle", "sawtooth", "sine", "wavetable",
    "noise_long", "noise_short", "noise_periodic",
}


def _strip_instrument_suffix(inst: str) -> str:
    """'noise_short_2' → 'noise_short', but 'pulse_50' stays 'pulse_50'."""
    if inst in _KNOWN_INSTRUMENTS:
        return inst
    # Try stripping trailing _N suffix and check against known instruments
    import re
    m = re.match(r"(.+)_\d+$", inst)
    if m:
        base = m.group(1)
        if base in _KNOWN_INSTRUMENTS:
            return base
    return inst


def _render_per_track(composition: dict, volume: float = 0.65) -> dict[str, np.ndarray]:
    """Render each track separately via vectorized render_multi, one pass.

    Returns {instrument_with_suffix: audio_array}.
    """
    renderer = Renderer()

    # render_multi already returns per-track arrays
    per_track_raw = renderer.render_multi(composition, volume=volume)

    # Merge tracks that share the same base instrument name
    # (e.g. two sections both using "pulse_50" get merged into one array)
    merged: dict[str, np.ndarray] = {}
    for inst, audio in per_track_raw.items():
        if inst in merged:
            # Pad shorter to match
            existing = merged[inst]
            if len(audio) > len(existing):
                existing = np.pad(existing, (0, len(audio) - len(existing)))
            elif len(audio) < len(existing):
                audio = np.pad(audio, (0, len(existing) - len(audio)))
            merged[inst] = existing + audio
        else:
            merged[inst] = audio

    return merged


def _build_automix_tracks(per_track: dict[str, np.ndarray]) -> dict:
    """Build AutomixEngine-compatible tracks_dict from per-track audio."""
    noise_short_count = 0
    result = {}

    for inst_raw, audio in per_track.items():
        base_inst = _strip_instrument_suffix(inst_raw)

        # Special handling for noise_short variants
        if base_inst == "noise_short":
            role_cfg = _NOISE_SHORT_ROLES.get(
                noise_short_count,
                {"role": "perc", "tone": "bright", "dynamics": "natural", "space": "room"},
            )
            noise_short_count += 1
        else:
            role_cfg = _INSTRUMENT_ROLE.get(base_inst, {
                "role": "melody", "tone": None, "dynamics": "natural", "space": "room",
            })

        result[inst_raw] = {
            "audio": audio,
            "role": role_cfg.get("role", "melody"),
            "tone": role_cfg.get("tone"),
            "dynamics": role_cfg.get("dynamics", "natural"),
            "space": role_cfg.get("space", "room"),
        }

    return result


def save_output(audio: np.ndarray, base_name: str, output_dir: str) -> tuple[str, str]:
    """Save audio as WAV and MP3, return paths."""
    os.makedirs(output_dir, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in base_name)
    safe_name = safe_name.strip()[:50] or "composition"
    ts = time.strftime("%H%M%S")
    return (os.path.join(output_dir, f"{safe_name}_{ts}.wav"),
            os.path.join(output_dir, f"{safe_name}_{ts}.mp3"))


# ─── main ────────────────────────────────────────────────────

def main() -> int:
    print_banner()

    # Check API key
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_BASE_DIR, '.env'))
    if not os.getenv("CHAT_API_KEY"):
        log("err", "CHAT_API_KEY not found in .env")
        return 1

    # Init LLM
    log("info", "Initializing V5 melody-first composer...")
    composer = V5Composer()
    current_model = composer.model

    # Init renderer + automix
    log("info", "Initializing renderer + Automix DSP engine...")
    renderer = Renderer()
    automix = AutomixEngine(fs=SAMPLE_RATE)

    output_dir = os.path.join(_BASE_DIR, "output")

    # Default global vibe
    current_vibe = "jpop_modern"

    log("ok", f"Ready! [{current_model}] vibe={current_vibe}")
    log("info", f"Output: {output_dir}/")
    print()

    session_count = 0

    while True:
        try:
            user_input = input(f"  {C['g']}>>{C['reset']} ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue

        lower = user_input.lower()

        if lower == "exit":
            log("info", "Goodbye!")
            break

        if lower == "reset":
            composer.reset()
            session_count = 0
            log("ok", "Conversation reset.")
            continue

        if lower == "flash":
            composer = V5Composer(model=DEEPSEEK_FLASH_MODEL)
            current_model = composer.model
            session_count = 0
            log("ok", f"Switched to [{current_model}].")
            continue

        if lower == "pro":
            composer = V5Composer(model=DEEPSEEK_MODEL)
            current_model = composer.model
            session_count = 0
            log("ok", f"Switched to [{current_model}].")
            continue

        if lower == "vibes":
            print(f"\n  {C['bold']}Available mix vibes:{C['reset']}")
            for v in AUTOMIX_VIBES:
                marker = f" {C['g']}(active){C['reset']}" if v == current_vibe else ""
                print(f"    {v}{marker}")
            print(f"  {C['dim']}Usage: type a vibe name to switch (e.g. 'cyberpunk_boss'){C['reset']}")
            print()
            continue

        if lower in AUTOMIX_VIBES:
            current_vibe = lower
            log("ok", f"Mix vibe set to [{current_vibe}].")
            continue

        # ── Send to LLM ──
        session_count += 1
        print()

        if session_count == 1:
            log("llm", f"[{current_model}] Composing... (vibe: {current_vibe})")
        else:
            log("llm", f"[{current_model}] Refining...")

        reasoning_shown = False
        content_shown = False
        reasoning_chars = 0

        def on_token(reasoning: str, content: str) -> None:
            nonlocal reasoning_shown, content_shown, reasoning_chars
            if reasoning:
                if not reasoning_shown:
                    print(f"  {C['dim']}[{C['y']}think{C['dim']}]{C['reset']}")
                    reasoning_shown = True
                reasoning_chars += len(reasoning)
                if reasoning_chars > 3000 and reasoning_chars - len(reasoning) <= 3000:
                    sys.stdout.write(f"\n  {C['y']}[!] 思考较长，请耐心等待...{C['reset']}\n  ")
                sys.stdout.write(f"{C['dim']}{reasoning}{C['reset']}")
                sys.stdout.flush()
            if content:
                if not content_shown:
                    if reasoning_shown:
                        print(f"\n  {C['dim']}[{C['c']}compose{C['dim']}]{C['reset']}")
                    else:
                        print(f"  {C['dim']}[{C['c']}compose{C['dim']}]{C['reset']}")
                    content_shown = True
                sys.stdout.write(content)
                sys.stdout.flush()

        if session_count == 1:
            result = composer.compose(user_input, on_token=on_token)
        else:
            result = composer.refine(user_input, on_token=on_token)

        if content_shown:
            print()
        print()

        # ── Save thinking log ──
        log_dir = os.path.join(_BASE_DIR, "output", "logs")
        os.makedirs(log_dir, exist_ok=True)
        ts = time.strftime("%Y%m%d_%H%M%S")
        tag = "compose" if session_count == 1 else f"refine{session_count}"

        if composer.last_reasoning:
            reason_path = os.path.join(log_dir, f"{ts}_{tag}_thinking.txt")
            with open(reason_path, "w", encoding="utf-8") as f:
                f.write(f"Model: {current_model}\nPrompt: {user_input}\n\n")
                f.write(composer.last_reasoning)
            log("info", f"Thinking → {reason_path}")

        if composer.last_raw:
            raw_path = os.path.join(log_dir, f"{ts}_{tag}_output.txt")
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(composer.last_raw)

        if result is None:
            log("err", "LLM did not return valid JSON.")
            if not reasoning_shown and not content_shown:
                print(f"  {C['dim']}{composer.last_raw[:400]}{C['reset']}")
            log("warn", "Try rephrasing or type 'reset'.")
            continue

        # ── Expand IR ──
        if is_tracker_ir(result):
            sections = len(result.get("sections", []))
            patterns = len(result.get("patterns", {}))
            log("info", f"Expanding Tracker IR ({sections}s, {patterns}p → flat)...")
            try:
                result = expand_tracker_ir(result)
            except Exception as e:
                log("err", f"Tracker IR expansion failed: {e}")
                continue
        elif is_macro_format(result):
            log("info", f"Expanding V2 macro ({len(result.get('patterns',{}))}p → flat)...")
            try:
                result = expand_macro_json(result)
            except Exception as e:
                log("err", f"Macro expansion failed: {e}")
                continue

        # ── Check for LLM-specified vibe ──
        if "mix_vibe" in result and result["mix_vibe"] in AUTOMIX_VIBES:
            current_vibe = result["mix_vibe"]
            log("info", f"LLM selected mix vibe: [{current_vibe}]")

        # ── Summary ──
        print_composition_summary(result)

        # ── Per-track render ──
        print()
        log("music", "Rendering per-track audio...")
        t0 = time.time()

        per_track = _render_per_track(result, volume=0.65)

        # ── Automix ──
        log("dsp", f"Mixing & mastering... (vibe: {current_vibe})")
        automix_tracks = _build_automix_tracks(per_track)

        # Show mix assignments
        print(f"\n  {C['bold']}Mix assignments:{C['reset']}")
        for name, cfg in automix_tracks.items():
            print(f"  {C['dim']}├─ {name}:{C['reset']} role={cfg['role']}, tone={cfg['tone']}, "
                  f"dyn={cfg['dynamics']}, space={cfg['space']}")

        try:
            audio = automix.mix_and_master(automix_tracks, global_vibe=current_vibe,
                                           volume=0.70)
        except Exception as e:
            log("err", f"Automix failed: {e}")
            continue

        render_time = time.time() - t0
        duration = len(audio) / SAMPLE_RATE

        # ── Save ──
        base_name = result.get("title", f"v5_session{session_count}")
        wav_path, mp3_path = save_output(audio, base_name, output_dir)

        log("music", "Saving WAV...")
        renderer.save_wav(audio, wav_path)
        wav_size = os.path.getsize(wav_path)

        log("music", "Converting to MP3...")
        renderer.save_mp3(audio, mp3_path)
        mp3_size = os.path.getsize(mp3_path)

        print()
        log("ok", f"Done! ({render_time:.1f}s render + mix/master)")
        print(f"  {C['g']}WAV:{C['reset']} {wav_path} ({wav_size/1024:.0f} KB)")
        print(f"  {C['g']}MP3:{C['reset']} {mp3_path} ({mp3_size/1024:.0f} KB)")
        print(f"  {C['dim']}Duration: {duration:.1f}s | vibe: {current_vibe}{C['reset']}")
        print()

        log("info", "Want changes? Describe what to modify, or 'reset'/'exit'/'vibes'.")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
