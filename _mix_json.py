#!/usr/bin/env python
"""
Offline mixer: take a saved LLM output JSON and render through AutomixEngine.

Usage:
    python _mix_json.py <path_to_output.json> [vibe]
    python _mix_json.py src/demo/demo_v5/output/logs/20260524_170154_compose_output.txt jpop_modern
"""

import json
import os
import sys
import time

_PROJ_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PROJ_ROOT)

import numpy as np

from src.demo.tracker_ir_expander import expand_tracker_ir, is_tracker_ir
from src.demo.macro_expander import expand_macro_json, is_macro_format
from src.demo.renderer import Renderer
from src.audio.automix import AutomixEngine
from src.audio.constants import SAMPLE_RATE
from src.demo.demo_v5.main import (
    _render_per_track, _build_automix_tracks, AUTOMIX_VIBES,
)

# Deduplicate: compatible with both demo_v5 and root
try:
    from src.demo.demo_v5.main import _KNOWN_INSTRUMENTS
except ImportError:
    _KNOWN_INSTRUMENTS = set()


def main():
    if len(sys.argv) < 2:
        print("Usage: python _mix_json.py <path_to_output.json> [vibe]")
        sys.exit(1)

    json_path = sys.argv[1]
    vibe = sys.argv[2] if len(sys.argv) > 2 else "jpop_modern"

    if vibe not in AUTOMIX_VIBES:
        print(f"Unknown vibe '{vibe}'. Available: {AUTOMIX_VIBES}")
        sys.exit(1)

    # ── Load JSON ──
    print(f"[load] Reading {json_path}...")
    with open(json_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Try direct parse
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try extracting JSON from markdown
        import re
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            data = json.loads(m.group(0))
        else:
            print("[err] No valid JSON found.")
            sys.exit(1)

    # ── Check for LLM-specified vibe ──
    if "mix_vibe" in data and data["mix_vibe"] in AUTOMIX_VIBES:
        vibe = data["mix_vibe"]
        print(f"[info] LLM specified vibe: {vibe}")

    # ── Expand IR ──
    if is_tracker_ir(data):
        print(f"[expand] Tracker IR: {len(data['sections'])} sections, {len(data['patterns'])} patterns")
        data = expand_tracker_ir(data)
    elif is_macro_format(data):
        print(f"[expand] Macro format: {len(data['patterns'])} patterns")
        data = expand_macro_json(data)

    bpm = data.get("bpm", "?")
    tracks = data.get("tracks", [])
    total_notes = sum(len(t.get("notes", [])) for t in tracks)
    print(f"[info] Expanded: {bpm} BPM, {len(tracks)} tracks, {total_notes} notes")

    # ── Render per-track ──
    print("[render] Rendering per-track audio...")
    t0 = time.time()
    per_track = _render_per_track(data, volume=0.65)
    render_time = time.time() - t0
    print(f"[render] Done in {render_time:.1f}s. Tracks: {list(per_track.keys())}")

    # ── Build automix tracks ──
    automix_tracks = _build_automix_tracks(per_track)
    print("[mix] Track assignments:")
    for name, cfg in automix_tracks.items():
        print(f"  {name}: role={cfg['role']}, tone={cfg['tone']}, "
              f"dyn={cfg['dynamics']}, space={cfg['space']}")

    # ── Mix & master ──
    print(f"[mix] AutomixEngine with vibe={vibe}...")
    engine = AutomixEngine(fs=SAMPLE_RATE)
    t0 = time.time()
    audio = engine.mix_and_master(automix_tracks, global_vibe=vibe, volume=0.70)
    mix_time = time.time() - t0
    duration = len(audio) / SAMPLE_RATE
    print(f"[mix] Done in {mix_time:.1f}s. Duration: {duration:.1f}s")

    # ── Save ──
    title = data.get("title", "composition")
    safe_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in title)
    safe_name = safe_name.strip()[:50] or "composition"
    ts = time.strftime("%H%M%S")

    out_dir = os.path.join(os.path.dirname(json_path), "..", "..")
    out_dir = os.path.normpath(out_dir)
    wav_path = os.path.join(out_dir, f"{safe_name}_{ts}.wav")
    mp3_path = os.path.join(out_dir, f"{safe_name}_{ts}.mp3")

    renderer = Renderer()
    print(f"[save] WAV → {wav_path}")
    renderer.save_wav(audio, wav_path)
    wav_size = os.path.getsize(wav_path)

    print(f"[save] MP3 → {mp3_path}")
    renderer.save_mp3(audio, mp3_path)
    mp3_size = os.path.getsize(mp3_path)

    print(f"\nDone! WAV: {wav_size/1024:.0f} KB, MP3: {mp3_size/1024:.0f} KB")
    print(f"Duration: {duration:.1f}s | vibe: {vibe}")


if __name__ == "__main__":
    main()
