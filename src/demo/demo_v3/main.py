#!/usr/bin/env python
"""Interactive v3 CLI for 8bc-ir-v1 composition."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from colorama import Fore, Style, init as colorama_init
from dotenv import load_dotenv

from src.demo.demo_v3.ir_expander import ExpansionError, compile_ir, is_ir_v1, report_to_text, summarize_legacy
from src.demo.demo_v3.llm_client import DEEPSEEK_FLASH_MODEL, DEEPSEEK_MODEL, V3Composer
from src.demo.renderer import Renderer

colorama_init(autoreset=True)

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

LOG_PREFIX = f"{C['dim']}[{C['c']}8bc-v3{C['dim']}]{C['reset']}"


def log(level: str, msg: str) -> None:
    tag = {
        "info": f"{C['c']}INFO{C['reset']}",
        "ok": f"{C['g']}OK{C['reset']}",
        "err": f"{C['r']}ERR{C['reset']}",
        "llm": f"{C['y']}LLM{C['reset']}",
        "warn": f"{C['y']}WARN{C['reset']}",
        "music": f"{C['m']}MUSIC{C['reset']}",
        "ir": f"{C['b']}IR{C['reset']}",
    }.get(level, level.upper())
    print(f"{LOG_PREFIX} [{tag}] {msg}")


def print_banner() -> None:
    print()
    print(f"{C['g']}{C['bold']}  8-BIT AI COMPOSER v3")
    print(f"  {C['c']}8bc-ir-v1 -> legacy JSON -> WAV/MP3{C['reset']}")
    print(f"  {C['dim']}Commands: exit | reset | flash | pro | model <name> | [music brief]{C['reset']}")
    print()


def stream_printer(label: str):
    reasoning_shown = False
    content_shown = False
    reasoning_chars = 0

    def on_token(reasoning: str, content: str) -> None:
        nonlocal reasoning_shown, content_shown, reasoning_chars
        if reasoning:
            if not reasoning_shown:
                print(f"  {C['dim']}[{C['y']}{label}: thinking{C['dim']}]{C['reset']}")
                reasoning_shown = True
            reasoning_chars += len(reasoning)
            if reasoning_chars > 3000 and reasoning_chars - len(reasoning) <= 3000:
                sys.stdout.write(f"\n  {C['y']}[long reasoning stream, waiting for final JSON]{C['reset']}\n  ")
            sys.stdout.write(f"{C['dim']}{reasoning}{C['reset']}")
            sys.stdout.flush()
        if content:
            if not content_shown:
                prefix = "\n" if reasoning_shown else ""
                print(f"{prefix}  {C['dim']}[{C['c']}{label}: ir-json{C['dim']}]{C['reset']}")
                content_shown = True
            sys.stdout.write(content)
            sys.stdout.flush()

    on_token.reasoning_shown = lambda: reasoning_shown  # type: ignore[attr-defined]
    on_token.content_shown = lambda: content_shown  # type: ignore[attr-defined]
    return on_token


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def save_generation_logs(output_dir: Path, ts: str, tag: str, composer: V3Composer, model: str, prompt: str) -> None:
    log_dir = output_dir / "logs"
    if composer.last_reasoning:
        reason_path = log_dir / f"{ts}_{tag}_thinking.txt"
        save_text(reason_path, f"Model: {model}\nPrompt: {prompt}\n\n{composer.last_reasoning}")
        log("info", f"Thinking saved: {reason_path}")
    if composer.last_raw:
        raw_path = log_dir / f"{ts}_{tag}_output.txt"
        save_text(raw_path, composer.last_raw)
        log("info", f"Raw output saved: {raw_path}")


def save_audio_paths(output_dir: Path, title: str, session_count: int) -> tuple[Path, Path]:
    safe_title = "".join(ch if ch.isalnum() or ch in "._- " else "_" for ch in title)
    safe_title = safe_title.strip()[:50] or f"session{session_count}"
    stamp = time.strftime("%H%M%S")
    return output_dir / f"{safe_title}_{stamp}.wav", output_dir / f"{safe_title}_{stamp}.mp3"


def print_ir_summary(ir: dict[str, Any], report: dict[str, Any]) -> None:
    sections = ir.get("sections", []) if isinstance(ir.get("sections"), list) else []
    tracks = ir.get("tracks", []) if isinstance(ir.get("tracks"), list) else []
    key = ir.get("key", {}) if isinstance(ir.get("key"), dict) else {}
    print(f"\n  {C['bold']}IR Summary{C['reset']}")
    print(f"  {C['dim']}Title:{C['reset']}    {ir.get('title', 'composition')}")
    print(f"  {C['dim']}BPM:{C['reset']}      {ir.get('bpm', '?')}")
    print(f"  {C['dim']}Key:{C['reset']}      {key.get('tonic', '?')} {key.get('mode', '?')}")
    print(f"  {C['dim']}Length:{C['reset']}   {ir.get('length_bars', '?')} bars")
    print(f"  {C['dim']}Tracks:{C['reset']}   {len(tracks)}")
    print(f"  {C['dim']}Sections:{C['reset']} {len(sections)}")
    print(f"  {C['dim']}Score:{C['reset']}    {report.get('score', 0)}/100")
    if report.get("warnings"):
        for warning in report["warnings"][:5]:
            print(f"  {C['y']}warn:{C['reset']} {warning}")


def print_legacy_summary(legacy: dict[str, Any]) -> None:
    summary = summarize_legacy(legacy)
    print(f"\n  {C['bold']}Compiled Summary{C['reset']}")
    print(f"  {C['dim']}Tracks:{C['reset']}   {summary['tracks']}")
    print(f"  {C['dim']}Notes:{C['reset']}    {summary['notes']}")
    print(f"  {C['dim']}Length:{C['reset']}   {summary['length_beats']} beats (~{summary['duration_seconds']}s)")
    for idx, track in enumerate(summary["track_summaries"], 1):
        range_text = f" [{track['range'][0]}..{track['range'][1]}]" if track["range"] else ""
        print(f"  {C['dim']}Track {idx}:{C['reset']}  {track['instrument']} ({track['notes']} notes){range_text}")


def build_or_repair(
    composer: V3Composer,
    parsed: dict | None,
    output_dir: Path,
    ts: str,
    tag: str,
    model: str,
    user_prompt: str,
    min_score: int,
    auto_repair: bool,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]] | None:
    compiled: tuple[dict[str, Any], dict[str, Any]] | None = None
    issues = ""

    if parsed is None:
        issues = "The model did not return parseable JSON."
    elif not is_ir_v1(parsed):
        issues = 'The model did not return format "8bc-ir-v1".'
    else:
        try:
            compiled = compile_ir(parsed)
        except ExpansionError as exc:
            issues = str(exc)

    if compiled is not None:
        legacy, report = compiled
        hard_fail = bool(report.get("errors")) or int(report.get("score", 0)) < min_score
        if not hard_fail:
            save_compiled_artifacts(output_dir, ts, tag, parsed, legacy, report)
            return parsed, legacy, report
        issues = report_to_text(report)
        save_validation_failure(output_dir, ts, tag, str(parsed.get("title", "composition")), issues)
    else:
        save_validation_failure(output_dir, ts, tag, "composition", issues or "Validation failed before compilation.")

    if not auto_repair:
        log("err", issues or "IR did not pass validation.")
        return None

    log("warn", "Validation failed or score too low; asking the model for one repair pass.")
    print()
    repair_printer = stream_printer("repair")
    repaired = composer.repair(issues, on_token=repair_printer)
    if repair_printer.content_shown():  # type: ignore[attr-defined]
        print()
    print()
    save_generation_logs(output_dir, ts, f"{tag}_repair1", composer, model, user_prompt)

    if repaired is None or not is_ir_v1(repaired):
        log("err", "Repair did not return valid 8bc-ir-v1 JSON.")
        return None
    try:
        legacy, report = compile_ir(repaired)
    except ExpansionError as exc:
        log("err", f"Repair expansion failed: {exc}")
        return None
    if report.get("errors"):
        log("err", "Repair still has hard validation errors.")
        log("err", report_to_text(report))
        return None

    save_compiled_artifacts(output_dir, ts, f"{tag}_repair1", repaired, legacy, report)
    return repaired, legacy, report


def save_compiled_artifacts(output_dir: Path, ts: str, tag: str, ir: dict[str, Any], legacy: dict[str, Any], report: dict[str, Any]) -> None:
    ir_path = output_dir / "ir" / f"{ts}_{tag}_ir.json"
    legacy_path = output_dir / "legacy" / f"{ts}_{tag}_legacy.json"
    report_path = output_dir / "logs" / f"{ts}_{tag}_validation.json"
    save_json(ir_path, ir)
    save_json(legacy_path, legacy)
    save_json(report_path, report)
    log("info", f"IR saved: {ir_path}")
    log("info", f"Legacy JSON saved: {legacy_path}")
    log("info", f"Validation saved: {report_path}")


def save_validation_failure(output_dir: Path, ts: str, tag: str, title: str, issues: str) -> None:
    path = output_dir / "logs" / f"{ts}_{tag}_validation_fail.txt"
    save_text(path, f"Title: {title}\n\n{issues}")
    log("info", f"Validation failure saved: {path}")


def run_request(
    composer: V3Composer,
    renderer: Renderer,
    user_input: str,
    session_count: int,
    output_dir: Path,
    volume: float,
    min_score: int,
    auto_repair: bool,
) -> bool:
    stage = "compose" if session_count == 1 else f"refine{session_count}"
    log("llm", f"[{composer.model}] {'Composing' if session_count == 1 else 'Refining'} with 8bc-ir-v1...")
    printer = stream_printer(stage)
    result = composer.compose(user_input, on_token=printer) if session_count == 1 else composer.refine(user_input, on_token=printer)
    if printer.content_shown():  # type: ignore[attr-defined]
        print()
    print()

    ts = time.strftime("%Y%m%d_%H%M%S")
    save_generation_logs(output_dir, ts, stage, composer, composer.model, user_input)

    built = build_or_repair(
        composer,
        result,
        output_dir,
        ts,
        stage,
        composer.model,
        user_input,
        min_score=min_score,
        auto_repair=auto_repair,
    )
    if built is None:
        log("warn", "Try a more specific brief, or type reset and retry.")
        return False

    ir, legacy, report = built
    print_ir_summary(ir, report)
    print_legacy_summary(legacy)

    print()
    log("music", "Rendering audio...")
    t0 = time.time()
    try:
        audio = renderer.render(legacy, volume=volume)
    except Exception as exc:
        log("err", f"Render failed: {exc}")
        return False

    output_dir.mkdir(parents=True, exist_ok=True)
    wav_path, mp3_path = save_audio_paths(output_dir, str(legacy.get("title", f"session{session_count}")), session_count)
    log("music", "Saving WAV...")
    renderer.save_wav(audio, str(wav_path))
    log("music", "Converting to MP3...")
    renderer.save_mp3(audio, str(mp3_path))

    duration = len(audio) / 44100
    render_time = time.time() - t0
    print()
    log("ok", f"Render complete in {render_time:.1f}s")
    print(f"  {C['g']}WAV:{C['reset']} {wav_path} ({wav_path.stat().st_size / 1024:.0f} KB)")
    print(f"  {C['g']}MP3:{C['reset']} {mp3_path} ({mp3_path.stat().st_size / 1024:.0f} KB)")
    print(f"  {C['dim']}Duration: {duration:.1f}s{C['reset']}")
    print()
    return True


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="8-Bit AI Composer v3: 8bc-ir-v1 CLI")
    parser.add_argument("prompt", nargs="*", help="Optional one-shot music brief")
    parser.add_argument("--model", default=None, help="Override DeepSeek model")
    parser.add_argument("--output-dir", default=str(BASE_DIR / "output"), help="Output directory")
    parser.add_argument("--volume", type=float, default=0.65, help="Render volume")
    parser.add_argument("--min-score", type=int, default=70, help="Auto-repair if validation score is below this")
    parser.add_argument("--no-auto-repair", action="store_true", help="Disable the single automatic repair pass")
    return parser.parse_args(argv)


def load_environment() -> None:
    load_dotenv(PROJECT_ROOT / ".env")
    local_env = BASE_DIR / ".env"
    if local_env.exists():
        load_dotenv(local_env, override=True)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    load_environment()
    print_banner()

    if not os.getenv("CHAT_API_KEY"):
        log("err", "CHAT_API_KEY not found. Put it in the root .env or src/demo/demo_v3/.env.")
        return 1

    output_dir = Path(args.output_dir)
    composer = V3Composer(model=args.model)
    renderer = Renderer()
    session_count = 0

    log("ok", f"Ready [{composer.model}]")
    log("info", f"Output: {output_dir}")
    log("info", "Use uv from the repo root, e.g. uv run python -m src.demo.demo_v3")
    print()

    if args.prompt:
        session_count = 1
        ok = run_request(
            composer,
            renderer,
            " ".join(args.prompt),
            session_count,
            output_dir,
            args.volume,
            args.min_score,
            not args.no_auto_repair,
        )
        return 0 if ok else 2

    while True:
        try:
            user_input = input(f"  {C['g']}>>{C['reset']} ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if not user_input:
            continue

        lower = user_input.lower()
        if lower in {"exit", "quit"}:
            log("info", "Goodbye.")
            return 0
        if lower == "reset":
            composer.reset()
            session_count = 0
            log("ok", "Conversation reset.")
            continue
        if lower == "flash":
            composer = V3Composer(model=DEEPSEEK_FLASH_MODEL)
            session_count = 0
            log("ok", f"Switched to [{composer.model}]. Conversation reset.")
            continue
        if lower == "pro":
            composer = V3Composer(model=DEEPSEEK_MODEL)
            session_count = 0
            log("ok", f"Switched to [{composer.model}]. Conversation reset.")
            continue
        if lower.startswith("model "):
            model = user_input.split(None, 1)[1].strip()
            composer = V3Composer(model=model)
            session_count = 0
            log("ok", f"Switched to [{composer.model}]. Conversation reset.")
            continue

        session_count += 1
        ok = run_request(
            composer,
            renderer,
            user_input,
            session_count,
            output_dir,
            args.volume,
            args.min_score,
            not args.no_auto_repair,
        )
        if ok:
            log("info", "Describe changes, or type reset/exit.")
        print()


if __name__ == "__main__":
    raise SystemExit(main())
