#!/usr/bin/env python
"""
8-Bit AI Composer — CLI Demo

Interactive command-line tool:
  1. Type a description of the music you want
  2. DeepSeek LLM generates a structured composition
  3. Rendered to MP3 via the 8-bit synthesizer
  4. You can request changes ("make it faster", "add drums", "darker tone")
  5. Type "reset" to start fresh, "exit" to quit

Requires: .env with CHAT_API_KEY (DeepSeek API key)
"""

import os
import sys
import time
from pathlib import Path

# Ensure project root on path (demo_v2 is at src/demo/demo_v2/ = 4 levels from root)
_PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, _PROJ_ROOT)
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from colorama import Fore, Style, init as colorama_init

from src.demo.llm_client import LLMComposer
from src.demo.renderer import Renderer

colorama_init(autoreset=True)

# ─── ANSI helpers ───
C = {
    "dim": Style.DIM,
    "bold": Style.BRIGHT,
    "r": Fore.RED,
    "g": Fore.GREEN,
    "b": Fore.BLUE,
    "c": Fore.CYAN,
    "y": Fore.YELLOW,
    "m": Fore.MAGENTA,
    "w": Fore.WHITE,
    "reset": Style.RESET_ALL,
}

LOG_PREFIX = f"{C['dim']}[{C['c']}8-bit{C['dim']}]{C['reset']}"


def log(level: str, msg: str, color: str = "w") -> None:
    """Colored log line."""
    tag = {
        "info": f"{C['c']}INFO{C['reset']}",
        "ok": f"{C['g']}OK{C['reset']}",
        "err": f"{C['r']}ERR{C['reset']}",
        "llm": f"{C['y']}LLM{C['reset']}",
        "warn": f"{C['y']}WARN{C['reset']}",
        "music": f"{C['m']}MUSIC{C['reset']}",
    }.get(level, level.upper())
    print(f"{LOG_PREFIX} [{tag}] {msg}")


def print_banner() -> None:
    print()
    print(f"{C['g']}{C['bold']}  ╔══════════════════════════════════════╗")
    print(f"  ║     {C['c']}8-BIT AI COMPOSER{C['g']}                   ║")
    print(f"  ║     {C['dim']}DeepSeek V4 Pro + 8-bit Synth{C['g']}         ║")
    print(f"  ╚══════════════════════════════════════╝{C['reset']}")
    print(f"  {C['dim']}Commands: exit | reset | flash | [your music idea]{C['reset']}")
    print()


def print_composition_summary(comp: dict) -> None:
    """Display a summary of the generated composition."""
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
        note_range = ""
        notes = t.get("notes", [])
        if notes:
            pitches = set()
            for n in notes:
                try:
                    pitches.add(n["n"])
                except KeyError:
                    pass
            if pitches:
                sorted_p = sorted(pitches, key=lambda x: (x[-1], x[:-1]))
                note_range = f" {C['dim']}[{sorted_p[0]}..{sorted_p[-1]}]{C['reset']}"
        print(f"  {C['dim']}├─ Track {i+1}:{C['reset']}  {inst} ({n_count} notes){note_range}")


def save_output(audio, base_name: str, output_dir: str) -> tuple[str, str]:
    """Save audio as WAV and MP3, return paths."""
    os.makedirs(output_dir, exist_ok=True)

    # Sanitize filename
    safe_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in base_name)
    safe_name = safe_name.strip()[:50] or "composition"

    # Add timestamp to avoid overwrites
    ts = time.strftime("%H%M%S")
    wav_path = os.path.join(output_dir, f"{safe_name}_{ts}.wav")
    mp3_path = os.path.join(output_dir, f"{safe_name}_{ts}.mp3")

    return wav_path, mp3_path


def main():
    print_banner()

    # Check API key
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_BASE_DIR, '.env'))
    if not os.getenv("CHAT_API_KEY"):
        log("err", "CHAT_API_KEY not found in .env. Please set your DeepSeek API key.")
        sys.exit(1)

    # Init
    log("info", f"Initializing LLM composer...")
    composer = LLMComposer()
    current_model = composer.model

    log("info", "Initializing audio renderer...")
    renderer = Renderer()

    output_dir = os.path.join(_BASE_DIR, "output")

    log("ok", f"Ready! [{current_model}] Describe the music, or type 'exit'/'flash'/'reset'.")
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
            log("ok", "Conversation reset. Starting fresh.")
            continue

        if lower == "flash":
            from src.demo.llm_client import DEEPSEEK_FLASH_MODEL
            current_model = DEEPSEEK_FLASH_MODEL
            composer = LLMComposer(model=current_model)
            session_count = 0
            log("ok", f"Switched to [{current_model}]. Conversation reset.")
            continue

        if lower == "pro":
            from src.demo.llm_client import DEEPSEEK_MODEL
            current_model = DEEPSEEK_MODEL
            composer = LLMComposer(model=current_model)
            session_count = 0
            log("ok", f"Switched to [{current_model}]. Conversation reset.")
            continue

        # ── Send to LLM (streaming) ──
        session_count += 1
        print()

        if session_count == 1:
            log("llm", f"[{current_model}] Composing...")
        else:
            log("llm", f"[{current_model}] Refining...")

        reasoning_shown = False
        content_shown = False
        reasoning_chars = 0

        def on_token(reasoning: str, content: str) -> None:
            nonlocal reasoning_shown, content_shown, reasoning_chars
            if reasoning:
                if not reasoning_shown:
                    print(f"  {C['dim']}[{C['y']}思考{C['dim']}]{C['reset']}")
                    reasoning_shown = True
                reasoning_chars += len(reasoning)
                # Warn if reasoning too long
                if reasoning_chars > 3000 and reasoning_chars - len(reasoning) <= 3000:
                    sys.stdout.write(f"\n  {C['y']}[!] 思考较长，请耐心等待...{C['reset']}\n  ")
                sys.stdout.write(f"{C['dim']}{reasoning}{C['reset']}")
                sys.stdout.flush()
            if content:
                if not content_shown:
                    if reasoning_shown:
                        print(f"\n  {C['dim']}[{C['c']}作曲{C['dim']}]{C['reset']}")
                    else:
                        print(f"  {C['dim']}[{C['c']}作曲{C['dim']}]{C['reset']}")
                    content_shown = True
                sys.stdout.write(content)
                sys.stdout.flush()

        if session_count == 1:
            result = composer.compose(user_input, on_token=on_token)
        else:
            result = composer.refine(user_input, on_token=on_token)

        if content_shown:
            print()  # final newline after streaming
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
            log("info", f"Thinking saved: {reason_path}")

        if composer.last_raw:
            raw_path = os.path.join(log_dir, f"{ts}_{tag}_output.txt")
            with open(raw_path, "w", encoding="utf-8") as f:
                f.write(composer.last_raw)
            # Only log if different from thinking
            if not composer.last_reasoning:
                log("info", f"Output saved: {raw_path}")

        if result is None:
            log("err", "LLM did not return valid JSON.")
            if not reasoning_shown and not content_shown:
                print(f"  {C['dim']}{composer.last_raw[:400]}{C['reset']}")
            print()
            log("warn", "Try rephrasing your request or type 'reset' to start over.")
            continue

        # ── Expand macro format if needed ──
        from src.demo.macro_expander import expand_macro_json, is_macro_format

        if is_macro_format(result):
            log("info", f"Expanding macro JSON ({len(result.get('patterns',{}))} patterns → flat tracks)...")
            try:
                result = expand_macro_json(result)
            except Exception as e:
                log("err", f"Macro expansion failed: {e}")
                continue

        # ── Show summary ──
        print_composition_summary(result)

        # ── Render ──
        print()
        log("music", "Rendering audio...")
        t0 = time.time()
        try:
            audio = renderer.render(result, volume=0.65)
        except Exception as e:
            log("err", f"Render failed: {e}")
            continue

        render_time = time.time() - t0
        duration = len(audio) / 44100

        # ── Save ──
        base_name = result.get("title", f"session{session_count}")
        wav_path, mp3_path = save_output(audio, base_name, output_dir)

        log("music", f"Saving WAV...")
        renderer.save_wav(audio, wav_path)
        wav_size = os.path.getsize(wav_path)

        log("music", f"Converting to MP3...")
        renderer.save_mp3(audio, mp3_path)
        mp3_size = os.path.getsize(mp3_path)

        print()
        log("ok", f"Render complete! ({render_time:.1f}s render)")
        print(f"  {C['g']}WAV:{C['reset']} {wav_path} ({wav_size/1024:.0f} KB)")
        print(f"  {C['g']}MP3:{C['reset']} {mp3_path} ({mp3_size/1024:.0f} KB)")
        print(f"  {C['dim']}Duration: {duration:.1f}s | {len(audio)/44100:.1f}s{C['reset']}")
        print()

        log("info", "Want changes? Describe what to modify, or type 'reset'/'exit'.")
        print()


if __name__ == "__main__":
    main()
