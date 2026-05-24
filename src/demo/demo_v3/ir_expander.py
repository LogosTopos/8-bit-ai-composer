"""Compiler from 8bc-ir-v1 to the legacy renderer JSON."""

from __future__ import annotations

import copy
import json
import math
import re
from dataclasses import dataclass
from typing import Any

VALID_INSTRUMENTS = {
    "pulse_12",
    "pulse_25",
    "pulse_50",
    "pulse_75",
    "triangle",
    "sawtooth",
    "noise_short",
    "noise_long",
    "noise_periodic",
    "sine",
    "wavetable",
}

NOISE_DEFAULT_NOTE = {
    "noise_long": "C2",
    "noise_short": "C4",
    "noise_periodic": "C4",
}

NOTE_MAP = {
    "C": 0,
    "C#": 1,
    "DB": 1,
    "D": 2,
    "D#": 3,
    "EB": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "GB": 6,
    "G": 7,
    "G#": 8,
    "AB": 8,
    "A": 9,
    "A#": 10,
    "BB": 10,
    "B": 11,
}

MIDI_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

MODE_INTERVALS = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "ionian": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "aeolian": [0, 2, 3, 5, 7, 8, 10],
    "natural_minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10],
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "melodic_minor": [0, 2, 3, 5, 7, 9, 11],
    "whole_tone": [0, 2, 4, 6, 8, 10, 12],
    "pentatonic": [0, 2, 4, 7, 9, 12, 14],
    "pentatonic_major": [0, 2, 4, 7, 9, 12, 14],
    "pentatonic_minor": [0, 3, 5, 7, 10, 12, 15],
}


class ExpansionError(Exception):
    """Raised when IR cannot be compiled into legacy note JSON."""


@dataclass
class ClipExpansion:
    clip_id: str
    track_id: str
    absolute_start: float
    unit_notes: list[dict[str, Any]]
    unit_length: float
    relative_notes: list[dict[str, Any]]
    clip_length: float
    absolute_notes: list[dict[str, Any]]


@dataclass(frozen=True)
class DegreeToken:
    degree: int
    accidental: int
    octave_delta: int
    accidental_explicit: bool


def is_ir_v1(data: dict[str, Any]) -> bool:
    return isinstance(data, dict) and data.get("format") == "8bc-ir-v1"


def expand_ir_json(ir: dict[str, Any]) -> dict[str, Any]:
    legacy, _report = compile_ir(ir)
    return legacy


def compile_ir(ir: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    compiler = IRCompiler(ir)
    return compiler.compile()


def validate_ir(ir: dict[str, Any]) -> dict[str, Any]:
    compiler = IRCompiler(ir)
    compiler.validate_structure()
    return compiler.report()


class IRCompiler:
    def __init__(self, ir: dict[str, Any]):
        self.ir = ir
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.score = 100
        self.clip_registry: dict[str, ClipExpansion] = {}
        self.pending_echo: list[tuple[dict[str, Any], dict[str, Any], str, str]] = []
        self.key = ir.get("key", {}) if isinstance(ir.get("key", {}), dict) else {}
        self.tonic = str(self.key.get("tonic", "C"))
        self.mode = str(self.key.get("mode", "major")).lower().replace(" ", "_")
        self.resolution = float(ir.get("resolution", 0.0625) or 0.0625)
        self.bar_beats = self._bar_beats()

    def compile(self) -> tuple[dict[str, Any], dict[str, Any]]:
        self.validate_structure()
        if self.errors:
            raise ExpansionError("; ".join(self.errors))

        flat_tracks: list[dict[str, Any]] = []
        for idx, track in enumerate(self.ir.get("tracks", [])):
            if not isinstance(track, dict):
                self._warn(f"Track {idx + 1} is not an object; skipped", 8)
                continue
            track_id = str(track.get("id") or f"track_{idx + 1}")
            instrument = self._instrument_for_track(track)
            notes: list[dict[str, Any]] = []

            for clip_idx, clip in enumerate(track.get("clips", [])):
                if not isinstance(clip, dict):
                    self._warn(f"Track {track_id} clip {clip_idx + 1} is not an object; skipped", 4)
                    continue
                if self._is_echo_clip(clip):
                    self.pending_echo.append((track, clip, track_id, instrument))
                    continue
                notes.extend(self._expand_clip(track, clip, track_id, instrument))

            flat_tracks.append({"id": track_id, "instrument": instrument, "_events": notes})

        for track, clip, track_id, instrument in self.pending_echo:
            target_track = self._find_flat_track(flat_tracks, track_id)
            if target_track is None:
                continue
            target_track["_events"].extend(self._expand_echo_clip(track, clip, track_id, instrument))

        export = self.ir.get("export", {}) if isinstance(self.ir.get("export"), dict) else {}
        overlap_policy = export.get("same_track_overlap", "truncate_previous")

        legacy_tracks = []
        for flat in flat_tracks:
            events = self._finalize_events(flat["_events"], flat["instrument"], overlap_policy)
            legacy_tracks.append({"instrument": flat["instrument"], "notes": events})

        legacy = {
            "title": self.ir.get("title", "composition"),
            "bpm": float(self.ir.get("bpm", 120)),
            "tracks": legacy_tracks,
        }

        self._score_compiled_legacy(legacy)
        return legacy, self.report(legacy)

    def validate_structure(self) -> None:
        if not is_ir_v1(self.ir):
            self._error('Top-level "format" must be "8bc-ir-v1"')
        for key in (
            "title",
            "bpm",
            "meter",
            "key",
            "length_bars",
            "resolution",
            "instruments",
            "harmony",
            "motifs",
            "patterns",
            "tracks",
            "sections",
            "export",
        ):
            if key not in self.ir:
                self._error(f'Missing required top-level field "{key}"')

        bpm = self._num(self.ir.get("bpm"), 0)
        if bpm < 40 or bpm > 240:
            self._warn(f"BPM {bpm} is outside the practical 40-240 range", 4)

        instruments = self.ir.get("instruments", {})
        if isinstance(instruments, dict):
            for role, instrument in instruments.items():
                if instrument not in VALID_INSTRUMENTS:
                    self._error(f'Instrument role "{role}" maps to invalid instrument "{instrument}"')
        else:
            self._error('"instruments" must be an object')

        if not isinstance(self.ir.get("tracks"), list) or not self.ir.get("tracks"):
            self._error('"tracks" must be a non-empty array')

        if not isinstance(self.ir.get("harmony"), list) or not self.ir.get("harmony"):
            self._warn("Harmony is empty; chord-aware arps and bass will be weaker", 8)

        if not isinstance(self.ir.get("sections"), list) or not self.ir.get("sections"):
            self._warn("Sections are empty; macro-form validation is limited", 8)

        if not isinstance(self.ir.get("motifs"), dict) or not self.ir.get("motifs"):
            self._warn("No motifs defined; melody may be less reusable", 6)

        if not isinstance(self.ir.get("patterns"), dict):
            self._error('"patterns" must be an object')

        self._validate_references()
        self._validate_form_claims()

    def report(self, legacy: dict[str, Any] | None = None) -> dict[str, Any]:
        report = {
            "score": max(0, min(100, self.score)),
            "errors": self.errors,
            "warnings": self.warnings,
            "format": self.ir.get("format"),
            "title": self.ir.get("title"),
            "bpm": self.ir.get("bpm"),
            "length_bars": self.ir.get("length_bars"),
        }
        if legacy is not None:
            total_notes = sum(len(track.get("notes", [])) for track in legacy.get("tracks", []))
            max_end = 0.0
            for track in legacy.get("tracks", []):
                for note in track.get("notes", []):
                    max_end = max(max_end, float(note.get("b", 0)) + float(note.get("d", 0)))
            report["compiled"] = {
                "tracks": len(legacy.get("tracks", [])),
                "notes": total_notes,
                "length_beats": round(max_end, 4),
                "duration_seconds": round(max_end / float(legacy.get("bpm", 120)) * 60.0, 2),
            }
        return report

    def _validate_references(self) -> None:
        motifs = self.ir.get("motifs", {}) if isinstance(self.ir.get("motifs"), dict) else {}
        patterns = self.ir.get("patterns", {}) if isinstance(self.ir.get("patterns"), dict) else {}
        clip_ids: set[str] = set()

        for track in self.ir.get("tracks", []) if isinstance(self.ir.get("tracks"), list) else []:
            if not isinstance(track, dict):
                continue
            role = track.get("instrument_role")
            if role and role not in self.ir.get("instruments", {}):
                self._warn(f'Track "{track.get("id", "?")}" references unknown instrument_role "{role}"', 5)
            for clip in track.get("clips", []) if isinstance(track.get("clips"), list) else []:
                if not isinstance(clip, dict):
                    continue
                if clip.get("id"):
                    clip_id = str(clip["id"])
                    if clip_id in clip_ids:
                        self._warn(f'Duplicate clip id "{clip_id}" may confuse echo_of', 6)
                    clip_ids.add(clip_id)
                if clip.get("use_motif") and clip["use_motif"] not in motifs:
                    self._error(f'Clip references missing motif "{clip["use_motif"]}"')
                if clip.get("use_pattern") and clip["use_pattern"] not in patterns:
                    self._error(f'Clip references missing pattern "{clip["use_pattern"]}"')

        for pattern_id, pattern in patterns.items():
            if isinstance(pattern, dict) and pattern.get("type") == "echo_of":
                target = pattern.get("target_clip")
                if target and target not in clip_ids:
                    self._warn(f'echo_of pattern "{pattern_id}" targets clip "{target}" not seen yet', 4)

    def _validate_form_claims(self) -> None:
        length_bars = int(self._num(self.ir.get("length_bars"), 0))
        tracks = self.ir.get("tracks", []) if isinstance(self.ir.get("tracks"), list) else []
        if length_bars >= 32 and len(tracks) < 4:
            self._warn("Long/big request has fewer than 4 tracks", 15)

        lead_bars: list[float] = []
        for track in tracks:
            if not isinstance(track, dict):
                continue
            role_text = f'{track.get("id", "")} {track.get("instrument_role", "")}'.lower()
            if "lead" not in role_text:
                continue
            for clip in track.get("clips", []) if isinstance(track.get("clips"), list) else []:
                if isinstance(clip, dict) and clip.get("at_bar"):
                    lead_bars.append(float(clip.get("at_bar", 999)))
        if length_bars >= 16 and lead_bars and min(lead_bars) > 12:
            self._warn("Lead hook first appears after bar 12", 8)

        patterns = self.ir.get("patterns", {}) if isinstance(self.ir.get("patterns"), dict) else {}
        technique_types = {p.get("type") for p in patterns.values() if isinstance(p, dict)}
        chip_count = len(technique_types.intersection({"arp", "echo_of", "drum_grid", "fill"}))
        if length_bars >= 16 and chip_count < 2:
            self._warn("Fewer than two explicit chip techniques were used", 10)

    def _score_compiled_legacy(self, legacy: dict[str, Any]) -> None:
        total_notes = sum(len(track.get("notes", [])) for track in legacy.get("tracks", []))
        if total_notes < 16:
            self._warn("Compiled output has very few notes", 12)

        velocities = [
            note.get("v")
            for track in legacy.get("tracks", [])
            for note in track.get("notes", [])
            if "v" in note
        ]
        if total_notes and len(velocities) < total_notes * 0.6:
            self._warn("Less than 60% of notes have explicit velocity", 5)

    def _expand_clip(self, track: dict[str, Any], clip: dict[str, Any], track_id: str, instrument: str) -> list[dict[str, Any]]:
        source = self._resolve_clip_source(clip)
        if source is None:
            return []

        clip_id = str(clip.get("id") or "")
        repeat = max(1, int(self._num(clip.get("repeat", 1), 1)))
        base = self._clip_base_beat(clip)
        base_transform = self._merge_transforms(source.get("transform", {}) if isinstance(source, dict) else {}, clip.get("transform", {}))

        relative_notes: list[dict[str, Any]] = []
        unit_notes_for_registry: list[dict[str, Any]] = []
        unit_length_for_registry = self.bar_beats
        cursor = 0.0

        for repeat_index in range(1, repeat + 1):
            repeat_transform = self._merge_transforms(base_transform, self._transform_for_repeat(clip, repeat_index))
            unit_notes, unit_length = self._expand_source(
                source,
                base_beat=base + cursor,
                instrument=instrument,
                follow_harmony_roots=bool(clip.get("follow_harmony_roots") or source.get("follow_harmony_roots", False)),
                transform=repeat_transform,
            )
            if repeat_index == 1:
                unit_notes_for_registry = copy.deepcopy(unit_notes)
                unit_length_for_registry = unit_length

            for note in unit_notes:
                shifted = copy.deepcopy(note)
                shifted["t"] = shifted.get("t", 0.0) + cursor
                relative_notes.append(shifted)
            cursor += max(unit_length, self.resolution)

        absolute_notes = []
        for note in relative_notes:
            final_note = copy.deepcopy(note)
            final_note["b"] = final_note.pop("t", 0.0) + base
            absolute_notes.append(final_note)

        if clip_id:
            self.clip_registry[clip_id] = ClipExpansion(
                clip_id=clip_id,
                track_id=track_id,
                absolute_start=base,
                unit_notes=unit_notes_for_registry,
                unit_length=unit_length_for_registry,
                relative_notes=copy.deepcopy(relative_notes),
                clip_length=cursor,
                absolute_notes=copy.deepcopy(absolute_notes),
            )

        return absolute_notes

    def _expand_echo_clip(self, track: dict[str, Any], clip: dict[str, Any], track_id: str, instrument: str) -> list[dict[str, Any]]:
        source = self._resolve_clip_source(clip)
        if source is None:
            return []
        target_id = str(source.get("target_clip") or clip.get("target_clip") or "")
        if not target_id or target_id not in self.clip_registry:
            self._warn(f'echo_of target "{target_id}" is unavailable; skipped echo clip on {track_id}', 10)
            return []

        target = self.clip_registry[target_id]
        copy_mode = str(source.get("copy", clip.get("copy", "unit"))).lower()
        if copy_mode == "absolute":
            source_notes = target.absolute_notes
            source_length = target.clip_length
            base = 0.0
        elif copy_mode == "clip":
            source_notes = target.relative_notes
            source_length = target.clip_length
            base = self._clip_base_beat(clip)
        else:
            source_notes = target.unit_notes
            source_length = target.unit_length
            base = self._clip_base_beat(clip)

        clip_repeat = max(1, int(self._num(clip.get("repeat", 1), 1)))
        echo_repeats = max(1, int(self._num(source.get("repeats", 1), 1)))
        delay = float(source.get("delay", 0.75) or 0.75)
        feedback = float(source.get("feedback", 0.5) or 0.5)
        transpose = int(self._num(source.get("transpose", 0), 0))
        v_mul = float(source.get("v_mul", 0.35) or 0.35)
        d_mul = float(source.get("d_mul", 1.0) or 1.0)
        transform = self._merge_transforms(source.get("transform", {}), clip.get("transform", {}))
        if "transpose" in transform:
            transpose += int(self._num(transform.pop("transpose"), 0))

        out: list[dict[str, Any]] = []
        for clip_idx in range(clip_repeat):
            clip_offset = clip_idx * max(source_length, self.resolution)
            for feedback_idx in range(echo_repeats):
                repeat_delay = delay * (feedback_idx + 1)
                velocity_factor = v_mul * (feedback ** feedback_idx)
                for note in source_notes:
                    echoed = copy.deepcopy(note)
                    echoed["t"] = base + clip_offset + echoed.get("t", echoed.get("b", 0.0)) + repeat_delay
                    echoed["b"] = echoed.pop("t")
                    if echoed.get("midi") is not None:
                        echoed["midi"] = int(echoed["midi"]) + transpose
                    echoed["d"] = max(self.resolution, float(echoed.get("d", 0.25)) * d_mul)
                    echoed["v"] = self._clamp(float(echoed.get("v", 0.6)) * velocity_factor, 0.01, 1.0)
                    out.append(echoed)

        transformed, _length = self._apply_transform(
            [{"t": n.pop("b"), **n} for n in out],
            transform=transform,
            length=max(source_length * clip_repeat + delay * echo_repeats, self.resolution),
        )
        return [{"b": n.pop("t"), **n} for n in transformed]

    def _expand_source(
        self,
        source: dict[str, Any],
        base_beat: float,
        instrument: str,
        follow_harmony_roots: bool,
        transform: dict[str, Any],
    ) -> tuple[list[dict[str, Any]], float]:
        effective = copy.deepcopy(source)
        for key in ("rate", "bars", "gate", "octave"):
            if key in transform:
                effective[key] = transform[key]

        source_type = str(effective.get("type", "raw"))
        if "events" in effective and source_type == "raw":
            notes, length = self._expand_raw(effective, base_beat, instrument, follow_harmony_roots)
        elif source_type == "degree_sequence":
            notes, length = self._expand_degree_sequence(effective, base_beat, instrument, follow_harmony_roots)
        elif source_type == "drum_grid":
            notes, length = self._expand_drum_grid(effective, instrument)
        elif source_type == "arp":
            notes, length = self._expand_arp(effective, base_beat, instrument)
        elif source_type == "fill":
            notes, length = self._expand_fill(effective, base_beat, instrument, follow_harmony_roots)
        elif source_type == "raw":
            notes, length = self._expand_raw(effective, base_beat, instrument, follow_harmony_roots)
        else:
            self._warn(f'Unsupported pattern type "{source_type}"; skipped', 8)
            return [], self.bar_beats

        return self._apply_transform(notes, transform, length)

    def _expand_raw(
        self, source: dict[str, Any], base_beat: float, instrument: str, follow_harmony_roots: bool
    ) -> tuple[list[dict[str, Any]], float]:
        events = source.get("events", [])
        notes: list[dict[str, Any]] = []
        cursor = 0.0
        max_end = 0.0
        for event in events if isinstance(events, list) else []:
            if not isinstance(event, dict):
                continue
            start = float(event.get("t", cursor))
            dur = max(self.resolution, float(event.get("d", 0.25) or 0.25))
            cursor = start + dur
            max_end = max(max_end, cursor)
            if self._is_rest_event(event):
                continue
            midi = self._pitch_for_event(event, base_beat + start, instrument, follow_harmony_roots, source.get("octave"))
            notes.append({"midi": midi, "t": start, "d": dur, "v": self._velocity(event.get("v", source.get("v", 0.75)))})
        return notes, max(max_end, self.resolution)

    def _expand_degree_sequence(
        self, source: dict[str, Any], base_beat: float, instrument: str, follow_harmony_roots: bool
    ) -> tuple[list[dict[str, Any]], float]:
        degrees = source.get("degree", source.get("degrees", []))
        if not isinstance(degrees, list):
            degrees = [degrees]
        durations = self._repeat_values(source.get("dur", 0.5), len(degrees), 0.5)
        octaves = self._repeat_values(source.get("oct", source.get("octave", 4)), len(degrees), 4)
        velocities = self._repeat_values(source.get("v", source.get("v_curve", 0.75)), len(degrees), 0.75)

        notes: list[dict[str, Any]] = []
        cursor = 0.0
        degree_source = str(source.get("degree_source", source.get("source", "key"))).lower()
        source_follow = follow_harmony_roots or degree_source in {"current_chord", "chord", "harmony", "follow_harmony"}
        for idx, degree in enumerate(degrees):
            dur = max(self.resolution, float(durations[idx] or 0.5))
            token = str(degree)
            if token in ("_", "rest", "REST") or source.get("rest") is True:
                cursor += dur
                continue
            event = {"sd": token, "oct": int(float(octaves[idx])), "v": velocities[idx]}
            midi = self._pitch_for_event(event, base_beat + cursor, instrument, source_follow, source.get("octave"))
            notes.append({"midi": midi, "t": cursor, "d": dur, "v": self._velocity(velocities[idx])})
            cursor += dur
        return notes, max(cursor, self.resolution)

    def _expand_drum_grid(self, source: dict[str, Any], instrument: str) -> tuple[list[dict[str, Any]], float]:
        hits = source.get("hits", [])
        notes: list[dict[str, Any]] = []
        max_end = 0.0
        default_midi = note_to_midi(NOISE_DEFAULT_NOTE.get(instrument, "C4"))
        for hit in hits if isinstance(hits, list) else []:
            if not isinstance(hit, dict):
                continue
            start = float(hit.get("t", 0.0) or 0.0)
            dur = max(self.resolution, float(hit.get("d", 0.0625) or 0.0625))
            max_end = max(max_end, start + dur)
            midi = default_midi
            if "n" in hit or "midi" in hit:
                midi = self._pitch_for_event(hit, start, instrument, False, None)
            notes.append({"midi": midi, "t": start, "d": dur, "v": self._velocity(hit.get("v", source.get("v", 0.65)))})
        bars = max(1.0, float(source.get("bars", 1) or 1))
        return notes, max(max_end, bars * self.bar_beats)

    def _expand_arp(self, source: dict[str, Any], base_beat: float, instrument: str) -> tuple[list[dict[str, Any]], float]:
        steps = source.get("steps", ["1", "3", "5", "3"])
        if not isinstance(steps, list) or not steps:
            steps = ["1", "3", "5", "3"]
        rate = max(self.resolution, float(source.get("rate", 0.25) or 0.25))
        bars = max(0.25, float(source.get("bars", 1) or 1))
        length = bars * self.bar_beats
        gate = self._clamp(float(source.get("gate", 0.9) or 0.9), 0.05, 1.0)
        octave = int(float(source.get("octave", 4) or 4))
        velocities = self._repeat_values(source.get("v_curve", source.get("v", 0.45)), max(1, math.ceil(length / rate)), 0.45)

        notes: list[dict[str, Any]] = []
        cursor = 0.0
        idx = 0
        while cursor < length - self.resolution / 2:
            step = str(steps[idx % len(steps)])
            if step not in ("_", "rest", "REST"):
                event = {"sd": step, "oct": octave}
                midi = self._pitch_for_event(event, base_beat + cursor, instrument, True, octave)
                notes.append(
                    {
                        "midi": midi,
                        "t": cursor,
                        "d": max(self.resolution, rate * gate),
                        "v": self._velocity(velocities[idx % len(velocities)]),
                    }
                )
            cursor += rate
            idx += 1
        return notes, length

    def _expand_fill(
        self, source: dict[str, Any], base_beat: float, instrument: str, follow_harmony_roots: bool
    ) -> tuple[list[dict[str, Any]], float]:
        dur = max(self.resolution, float(source.get("dur", 0.125) or 0.125))
        length = max(dur, float(source.get("length", self.bar_beats) or self.bar_beats))
        count = max(1, int(round(length / dur)))
        start_degree = str(source.get("start_degree", source.get("start", "1")))
        end_degree = str(source.get("end_degree", source.get("end", "1")))
        oct_start = int(float(source.get("oct_start", source.get("octave", 4)) or 4))
        oct_end = int(float(source.get("oct_end", oct_start) or oct_start))
        v_start = float(source.get("v_start", source.get("v", 0.55)) or 0.55)
        v_end = float(source.get("v_end", source.get("v", 0.9)) or 0.9)

        start_midi = self._pitch_for_event({"sd": start_degree, "oct": oct_start}, base_beat, instrument, follow_harmony_roots, oct_start)
        end_midi = self._pitch_for_event({"sd": end_degree, "oct": oct_end}, base_beat + length, instrument, follow_harmony_roots, oct_end)

        notes: list[dict[str, Any]] = []
        for idx in range(count):
            ratio = idx / max(1, count - 1)
            midi = int(round(start_midi + (end_midi - start_midi) * ratio))
            velocity = v_start + (v_end - v_start) * ratio
            notes.append({"midi": midi, "t": idx * dur, "d": dur, "v": self._velocity(velocity)})
        return notes, length

    def _apply_transform(self, notes: list[dict[str, Any]], transform: dict[str, Any], length: float) -> tuple[list[dict[str, Any]], float]:
        transform = transform if isinstance(transform, dict) else {}
        out = copy.deepcopy(notes)

        if transform.get("reverse"):
            for note in out:
                note["t"] = max(0.0, length - (float(note.get("t", 0.0)) + float(note.get("d", 0.25))))
            out.sort(key=lambda n: n.get("t", 0.0))

        time_scale = float(transform.get("time_scale", 1.0) or 1.0)
        if time_scale != 1.0:
            for note in out:
                note["t"] = float(note.get("t", 0.0)) * time_scale
                note["d"] = max(self.resolution, float(note.get("d", 0.25)) * time_scale)
            length *= time_scale

        shift = float(transform.get("shift", 0.0) or 0.0)
        if shift:
            for note in out:
                note["t"] = float(note.get("t", 0.0)) + shift
            length = max(length + shift, max((n.get("t", 0.0) + n.get("d", 0.0) for n in out), default=length))

        semitone = int(self._num(transform.get("transpose", 0), 0))
        semitone += 12 * int(self._num(transform.get("octave", 0), 0))
        degree_shift = int(self._num(transform.get("degree_transpose", 0), 0))
        if degree_shift:
            semitone += self._degree_shift_to_semitones(degree_shift)
        axis = note_to_midi(transform["invert_around"]) if transform.get("invert_around") else None
        velocity_mul = float(transform.get("velocity_mul", 1.0) or 1.0)
        gate = float(transform.get("gate", 1.0) or 1.0)

        for idx, note in enumerate(out):
            if note.get("midi") is not None:
                midi = int(note["midi"])
                if axis is not None:
                    midi = axis * 2 - midi
                note["midi"] = midi + semitone
            note["v"] = self._clamp(float(note.get("v", 0.75)) * velocity_mul, 0.01, 1.0)
            note["d"] = max(self.resolution, float(note.get("d", 0.25)) * gate)

        accent = transform.get("accent_pattern")
        if isinstance(accent, list) and accent:
            for idx, note in enumerate(out):
                try:
                    note["v"] = self._clamp(float(note.get("v", 0.75)) * float(accent[idx % len(accent)]), 0.01, 1.0)
                except (TypeError, ValueError):
                    pass

        drop_every = int(self._num(transform.get("drop_every", 0), 0))
        if drop_every > 1:
            out = [note for idx, note in enumerate(out, 1) if idx % drop_every != 0]

        thin = transform.get("thin")
        if isinstance(thin, (int, float)) and thin and thin > 0:
            if 0 < float(thin) < 1:
                keep_every = max(2, int(round(1.0 / float(thin))))
                out = [note for idx, note in enumerate(out) if idx % keep_every == 0 or note.get("v", 0) > 0.8]
            elif int(thin) > 1:
                out = [note for idx, note in enumerate(out) if idx % int(thin) != 0]

        ornaments = transform.get("ornaments") or transform.get("ornament")
        if ornaments:
            if isinstance(ornaments, str):
                ornaments = [ornaments]
            out = self._apply_ornaments(out, ornaments)

        length = max(length, max((float(n.get("t", 0.0)) + float(n.get("d", 0.0)) for n in out), default=0.0))
        return out, max(length, self.resolution)

    def _apply_ornaments(self, notes: list[dict[str, Any]], ornaments: list[str]) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        ornament_set = {str(o) for o in ornaments}
        step = self.resolution
        for idx, note in enumerate(notes):
            midi = note.get("midi")
            if midi is None:
                out.append(note)
                continue

            t = float(note.get("t", 0.0))
            v = float(note.get("v", 0.75))
            if "pickup" in ornament_set and idx == 0 and t >= 0.25:
                out.append({**note, "midi": midi - 2, "t": t - 0.25, "d": step, "v": self._clamp(v * 0.55, 0.01, 1.0)})
            if "grace_up" in ornament_set and t >= step:
                out.append({**note, "midi": midi + 1, "t": t - step, "d": step, "v": self._clamp(v * 0.5, 0.01, 1.0)})
            if "grace_down" in ornament_set and t >= step:
                out.append({**note, "midi": midi - 1, "t": t - step, "d": step, "v": self._clamp(v * 0.5, 0.01, 1.0)})
            if "turn" in ornament_set and float(note.get("d", 0.0)) >= 0.5:
                out.append({**note, "midi": midi + 2, "t": t, "d": step, "v": self._clamp(v * 0.45, 0.01, 1.0)})
                out.append({**note, "midi": midi, "t": t + step, "d": step, "v": self._clamp(v * 0.55, 0.01, 1.0)})
                out.append({**note, "midi": midi - 1, "t": t + step * 2, "d": step, "v": self._clamp(v * 0.45, 0.01, 1.0)})
                note = {**note, "t": t + step * 3, "d": max(step, float(note.get("d", 0.25)) - step * 3)}
            if "upper_neighbor" in ornament_set and float(note.get("d", 0.0)) >= 0.375:
                midpoint = t + max(step, float(note.get("d", 0.25)) * 0.5)
                out.append({**note, "midi": midi + 2, "t": midpoint, "d": step, "v": self._clamp(v * 0.45, 0.01, 1.0)})
                note = {**note, "d": max(step, float(note.get("d", 0.25)) * 0.75)}
            if "climax_run" in ornament_set and idx == len(notes) - 1:
                run_start = max(0.0, t - 0.5)
                for run_idx, offset in enumerate((-5, -3, -2, 0)):
                    out.append(
                        {
                            **note,
                            "midi": midi + offset,
                            "t": run_start + run_idx * 0.125,
                            "d": step,
                            "v": self._clamp(v * (0.55 + run_idx * 0.12), 0.01, 1.0),
                        }
                    )
            out.append(note)

        out.sort(key=lambda n: (float(n.get("t", 0.0)), int(n.get("midi") or 0)))
        return out

    def _finalize_events(self, events: list[dict[str, Any]], instrument: str, overlap_policy: str) -> list[dict[str, Any]]:
        finalized: list[dict[str, Any]] = []
        for event in events:
            start = self._quantize(float(event.get("b", event.get("t", 0.0)) or 0.0))
            dur = self._quantize(max(self.resolution, float(event.get("d", 0.25) or 0.25)))
            midi = event.get("midi")
            if midi is None:
                midi = note_to_midi(NOISE_DEFAULT_NOTE.get(instrument, "C4"))
            note = {
                "n": midi_to_note(int(self._clamp(int(midi), 0, 127))),
                "b": start,
                "d": dur,
                "v": round(self._clamp(float(event.get("v", 0.75) or 0.75), 0.01, 1.0), 4),
            }
            finalized.append(note)

        finalized.sort(key=lambda n: (n["b"], n["n"]))
        if overlap_policy == "truncate_previous":
            for idx in range(len(finalized) - 1):
                current = finalized[idx]
                nxt = finalized[idx + 1]
                current_end = current["b"] + current["d"]
                if nxt["b"] > current["b"] and current_end > nxt["b"]:
                    current["d"] = self._quantize(max(self.resolution, nxt["b"] - current["b"]))
        return finalized

    def _resolve_clip_source(self, clip: dict[str, Any]) -> dict[str, Any] | None:
        motifs = self.ir.get("motifs", {}) if isinstance(self.ir.get("motifs"), dict) else {}
        patterns = self.ir.get("patterns", {}) if isinstance(self.ir.get("patterns"), dict) else {}
        if clip.get("use_motif"):
            source = motifs.get(clip["use_motif"])
            if source is None:
                self._warn(f'Missing motif "{clip["use_motif"]}"; skipped clip', 8)
                return None
            return copy.deepcopy(source)
        if clip.get("use_pattern"):
            source = patterns.get(clip["use_pattern"])
            if source is None:
                self._warn(f'Missing pattern "{clip["use_pattern"]}"; skipped clip', 8)
                return None
            return copy.deepcopy(source)
        if "type" in clip or "events" in clip:
            return copy.deepcopy(clip)
        self._warn("Clip has no use_motif/use_pattern/type/events; skipped", 4)
        return None

    def _is_echo_clip(self, clip: dict[str, Any]) -> bool:
        if clip.get("type") == "echo_of":
            return True
        if clip.get("target_clip"):
            return True
        source = self._resolve_clip_source(clip)
        return isinstance(source, dict) and source.get("type") == "echo_of"

    def _instrument_for_track(self, track: dict[str, Any]) -> str:
        if track.get("instrument") in VALID_INSTRUMENTS:
            return str(track["instrument"])
        instruments = self.ir.get("instruments", {}) if isinstance(self.ir.get("instruments"), dict) else {}
        role = track.get("instrument_role")
        instrument = instruments.get(role, "pulse_50")
        if instrument not in VALID_INSTRUMENTS:
            self._warn(f'Track "{track.get("id", "?")}" uses invalid instrument "{instrument}", defaulting to pulse_50', 8)
            return "pulse_50"
        return str(instrument)

    def _pitch_for_event(
        self,
        event: dict[str, Any],
        absolute_beat: float,
        instrument: str,
        chord_relative: bool,
        default_octave: Any,
    ) -> int:
        if "midi" in event:
            return int(event["midi"])
        if "n" in event:
            return note_to_midi(str(event["n"]))
        if "sd" in event:
            octave = int(float(event.get("oct", default_octave if default_octave is not None else 4)))
            if chord_relative:
                chord = self._harmony_at_beat(absolute_beat)
                return chord_step_to_midi(str(event["sd"]), chord, octave, self.tonic)
            return scale_degree_to_midi(str(event["sd"]), octave, self.tonic, self.mode)
        return note_to_midi(NOISE_DEFAULT_NOTE.get(instrument, "C4"))

    def _harmony_at_beat(self, beat: float) -> str:
        harmony = self.ir.get("harmony", []) if isinstance(self.ir.get("harmony"), list) else []
        if not harmony:
            return self.tonic
        current_bar = beat / self.bar_beats + 1
        chosen = harmony[0]
        for item in harmony:
            if not isinstance(item, dict):
                continue
            bar = float(item.get("bar", 1) or 1)
            dur = float(item.get("dur_bars", 1) or 1)
            if bar <= current_bar < bar + dur:
                return str(item.get("chord", self.tonic))
            if bar <= current_bar:
                chosen = item
        return str(chosen.get("chord", self.tonic))

    def _bar_beats(self) -> float:
        meter = self.ir.get("meter", [4, 4])
        if isinstance(meter, list) and len(meter) >= 2:
            numerator = float(meter[0] or 4)
            denominator = float(meter[1] or 4)
            return numerator * 4.0 / denominator
        return 4.0

    def _clip_base_beat(self, clip: dict[str, Any]) -> float:
        at_bar = float(clip.get("at_bar", 1) or 1)
        return (at_bar - 1.0) * self.bar_beats + float(clip.get("t", 0.0) or 0.0)

    def _transform_for_repeat(self, clip: dict[str, Any], repeat_index: int) -> dict[str, Any]:
        transforms = clip.get("transform_each", [])
        if not isinstance(transforms, list):
            return {}
        merged: dict[str, Any] = {}
        for item in transforms:
            if not isinstance(item, dict):
                continue
            target = item.get("repeat_index", item.get("index"))
            if target == repeat_index:
                item_transform = {k: v for k, v in item.items() if k not in {"repeat_index", "index"}}
                merged = self._merge_transforms(merged, item_transform)
        return merged

    def _merge_transforms(self, base: Any, extra: Any) -> dict[str, Any]:
        result = copy.deepcopy(base) if isinstance(base, dict) else {}
        if not isinstance(extra, dict):
            return result
        for key, value in extra.items():
            if key in {"transpose", "degree_transpose", "octave", "shift"}:
                result[key] = self._num(result.get(key, 0), 0) + self._num(value, 0)
            elif key == "velocity_mul":
                result[key] = float(result.get(key, 1.0) or 1.0) * float(value or 1.0)
            elif key in {"ornaments", "ornament"}:
                existing = result.get("ornaments", [])
                if isinstance(existing, str):
                    existing = [existing]
                incoming = value if isinstance(value, list) else [value]
                result["ornaments"] = list(existing) + list(incoming)
            else:
                result[key] = value
        return result

    def _degree_shift_to_semitones(self, degree_shift: int) -> int:
        if degree_shift == 0:
            return 0
        mode = MODE_INTERVALS.get(self.mode, MODE_INTERVALS["major"])
        steps = abs(degree_shift)
        intervals = mode[(steps) % 7] + 12 * (steps // 7)
        return intervals if degree_shift > 0 else -intervals

    def _repeat_values(self, value: Any, length: int, default: Any) -> list[Any]:
        if isinstance(value, list):
            if not value:
                return [default for _ in range(length)]
            return [value[idx % len(value)] for idx in range(length)]
        return [value if value is not None else default for _ in range(length)]

    def _find_flat_track(self, tracks: list[dict[str, Any]], track_id: str) -> dict[str, Any] | None:
        for track in tracks:
            if track.get("id") == track_id:
                return track
        return None

    def _is_rest_event(self, event: dict[str, Any]) -> bool:
        return event.get("rest") is True or str(event.get("n", "")).strip() in {"_", "rest", "REST"}

    def _velocity(self, value: Any) -> float:
        try:
            return self._clamp(float(value), 0.01, 1.0)
        except (TypeError, ValueError):
            return 0.75

    def _quantize(self, value: float) -> float:
        return round(round(value / self.resolution) * self.resolution, 6)

    def _num(self, value: Any, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def _warn(self, message: str, penalty: int = 3) -> None:
        if message not in self.warnings:
            self.warnings.append(message)
            self.score -= penalty

    def _error(self, message: str) -> None:
        if message not in self.errors:
            self.errors.append(message)
            self.score -= 20

    @staticmethod
    def _clamp(value: float, low: float, high: float) -> float:
        return max(low, min(high, value))


def note_to_midi(note: str | int | float) -> int:
    if isinstance(note, (int, float)):
        return int(note)
    value = str(note).strip()
    try:
        return int(value)
    except ValueError:
        pass
    match = re.match(r"^([A-Ga-g])([#bB]?)(-?\d+)$", value)
    if not match:
        raise ExpansionError(f"Cannot parse note: {note}")
    name = (match.group(1).upper() + match.group(2).upper()).replace("B", "B")
    octave = int(match.group(3))
    if name not in NOTE_MAP:
        raise ExpansionError(f"Cannot parse note: {note}")
    return NOTE_MAP[name] + (octave + 1) * 12


def midi_to_note(midi: int) -> str:
    midi = max(0, min(127, int(midi)))
    return f"{MIDI_NAMES[midi % 12]}{midi // 12 - 1}"


def pitch_class(name: str, fallback: str = "C") -> int:
    match = re.match(r"^([A-Ga-g])([#bB]?)", str(name).strip())
    if not match:
        match = re.match(r"^([A-Ga-g])([#bB]?)", fallback)
    if not match:
        return 0
    token = (match.group(1).upper() + match.group(2).upper()).replace("B", "B")
    return NOTE_MAP.get(token, 0)


def root_name(symbol: str, fallback: str = "C") -> str:
    match = re.match(r"^([A-Ga-g])([#bB]?)", str(symbol).strip())
    if not match:
        return fallback
    return match.group(1).upper() + match.group(2)


def parse_degree_token(token: str | int | float) -> DegreeToken:
    text = str(token).strip()
    octave_delta = 0
    while text.endswith(("+", "-")) and len(text) > 1:
        if text[-1] == "+":
            octave_delta += 1
        else:
            octave_delta -= 1
        text = text[:-1]

    accidental = 0
    accidental_explicit = False
    while text.startswith(("b", "B", "#")):
        accidental_explicit = True
        accidental += -1 if text[0] in {"b", "B"} else 1
        text = text[1:]
    match = re.match(r"(-?\d+)", text)
    if not match:
        return DegreeToken(1, accidental, octave_delta, accidental_explicit)
    return DegreeToken(int(match.group(1)), accidental, octave_delta, accidental_explicit)


def scale_degree_to_midi(sd: str, octave: int, tonic: str, mode: str) -> int:
    token = parse_degree_token(sd)
    degree = token.degree
    if degree == 0:
        degree = 1
    zero_based = degree - 1
    octave_shift = math.floor(zero_based / 7) + token.octave_delta
    index = zero_based % 7
    if token.accidental_explicit:
        intervals = MODE_INTERVALS["major"]
    else:
        intervals = MODE_INTERVALS.get(mode.lower().replace(" ", "_"), MODE_INTERVALS["major"])
    root = pitch_class(tonic)
    return root + (int(octave) + 1) * 12 + intervals[index] + octave_shift * 12 + token.accidental


def chord_step_to_midi(step: str, chord_symbol: str, octave: int, fallback_tonic: str = "C") -> int:
    root = root_name(chord_symbol, fallback_tonic)
    quality = str(chord_symbol)[len(root) :].lower()
    root_midi = pitch_class(root, fallback_tonic) + (int(octave) + 1) * 12
    token = parse_degree_token(step)
    degree = token.degree
    if degree == 0:
        degree = 1

    minor = quality.startswith("m") and not quality.startswith("maj")
    diminished = "dim" in quality or "o" in quality or "ø" in quality or "m7b5" in quality
    augmented = "aug" in quality or "#5" in quality or "+" in quality
    sus2 = "sus2" in quality
    sus4 = "sus" in quality and not sus2
    major_seventh = "maj7" in quality or "ma7" in quality or "m7+" in quality
    diminished_seventh = "dim7" in quality or "o7" in quality

    degree_mod = ((degree - 1) % 7) + 1
    octave_shift = (degree - 1) // 7 + token.octave_delta

    if token.accidental_explicit:
        interval = MODE_INTERVALS["major"][degree_mod - 1]
    else:
        if degree_mod == 1:
            interval = 0
        elif degree_mod == 2:
            interval = 2
        elif degree_mod == 3:
            if sus2:
                interval = 2
            elif sus4:
                interval = 5
            else:
                interval = 3 if minor or diminished else 4
        elif degree_mod == 4:
            interval = 6 if "#11" in quality else 5
        elif degree_mod == 5:
            if diminished or "b5" in quality:
                interval = 6
            elif augmented:
                interval = 8
            else:
                interval = 7
        elif degree_mod == 6:
            interval = 8 if "b13" in quality else 9
        else:
            if diminished_seventh:
                interval = 9
            elif major_seventh:
                interval = 11
            else:
                interval = 10
    return root_midi + interval + token.accidental + octave_shift * 12


def summarize_legacy(legacy: dict[str, Any]) -> dict[str, Any]:
    max_end = 0.0
    total_notes = 0
    track_summaries = []
    for track in legacy.get("tracks", []):
        notes = track.get("notes", [])
        total_notes += len(notes)
        for note in notes:
            max_end = max(max_end, float(note.get("b", 0)) + float(note.get("d", 0)))
        pitches = [n.get("n") for n in notes if n.get("n")]
        pitch_midis: list[int] = []
        for pitch in pitches:
            try:
                pitch_midis.append(note_to_midi(str(pitch)))
            except Exception:
                pass
        track_summaries.append(
            {
                "instrument": track.get("instrument"),
                "notes": len(notes),
                "range": [midi_to_note(min(pitch_midis)), midi_to_note(max(pitch_midis))] if pitch_midis else [],
            }
        )
    bpm = float(legacy.get("bpm", 120) or 120)
    return {
        "title": legacy.get("title"),
        "bpm": bpm,
        "tracks": len(legacy.get("tracks", [])),
        "notes": total_notes,
        "length_beats": round(max_end, 4),
        "duration_seconds": round(max_end / bpm * 60.0, 2),
        "track_summaries": track_summaries,
    }


def report_to_text(report: dict[str, Any], max_items: int = 20) -> str:
    parts = [f"Score: {report.get('score', 0)}"]
    errors = report.get("errors", [])
    warnings = report.get("warnings", [])
    if errors:
        parts.append("Errors:")
        parts.extend(f"- {item}" for item in errors[:max_items])
    if warnings:
        parts.append("Warnings:")
        parts.extend(f"- {item}" for item in warnings[:max_items])
    compiled = report.get("compiled")
    if compiled:
        parts.append(f"Compiled: {json.dumps(compiled, ensure_ascii=False)}")
    return "\n".join(parts)
