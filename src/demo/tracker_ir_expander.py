"""
8Bit-Tracker-IR Expander: converts V4 tracker IR JSON to legacy flat note-list JSON.

Input (LLM output):
{
  "bpm": 135,
  "patterns": { "bass": [["C2",0.5,0.9],["G2",0.5,0.7]], ... },
  "sections": [
    {
      "name": "Intro", "bars": 8,
      "tracks": {
        "triangle": [
          {"play": "bass", "repeat": 4, "transpose": 0},
          ...
        ],
        "pulse_50": [
          {"arp": ["C4","E4","G4"], "rate": 0.125, "dur": 8.0, "v": 0.6},
          ...
        ]
      }
    }
  ]
}

Supports:
- Raw notes:    ["C4", 0.5, 0.8]
- Pattern play: {"play": "name", "repeat": N, "transpose": X, "velocity_mul": M}
- Arpeggio:     {"arp": [notes], "rate": R, "dur": D, "v": V}
- Trill:        {"trill": [N1,N2], "rate": R, "dur": D}
- Slide:        {"slide": [start, end], "steps": N, "dur": D}
- Delay start:  {"delay_start": 0.75}
"""

import math

_NOTE_MAP = {
    "C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
    "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
    "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11,
}
_MIDI_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def _to_midi(note_str: str) -> int | None:
    """'C4' -> 60, 'D#3' -> 51. None for rests."""
    note_str = note_str.strip()
    if note_str in ("_", "rest", ""):
        return None
    try:
        return int(note_str)
    except ValueError:
        pass
    base = note_str.rstrip("0123456789-")
    if base not in _NOTE_MAP:
        return None
    oct_str = note_str[len(base):]
    try:
        octave = int(oct_str)
    except ValueError:
        return None
    return _NOTE_MAP[base] + (octave + 1) * 12


def _to_note(midi_val: int) -> str:
    octave = (midi_val // 12) - 1
    note = _MIDI_NAMES[midi_val % 12]
    return f"{note}{octave}"


def expand_tracker_ir(ir: dict) -> dict:
    """
    Convert 8Bit-Tracker-IR to legacy renderer JSON.
    """
    bpm = ir.get("bpm", 120)
    patterns = ir.get("patterns", {})
    sections = ir.get("sections", [])
    bar_beats = 4.0  # always 4/4 for now

    # Collect notes per instrument
    flat: dict[str, list[dict]] = {}
    current_section_start = 0.0

    for section in sections:
        bars = section.get("bars", 8)
        tracks = section.get("tracks", {})

        for instrument, events in tracks.items():
            if instrument not in flat:
                flat[instrument] = []

            beat = current_section_start

            # Handle delay_start (must be first event in track)
            evs = list(events)
            if evs and isinstance(evs[0], dict) and "delay_start" in evs[0]:
                beat += evs[0]["delay_start"]
                evs = evs[1:]

            for event in evs:
                beat = _process_event(event, instrument, flat, beat, patterns)

        current_section_start += bars * bar_beats

    # Build legacy output
    tracks_out = []
    for inst, notes in sorted(flat.items()):
        if notes:
            tracks_out.append({"instrument": inst, "notes": notes})

    return {"bpm": bpm, "tracks": tracks_out}


def _add_note(flat: dict, instrument: str, note: str, beat: float,
              dur: float, vel: float) -> float:
    """Add a note and return the new beat position."""
    midi = _to_midi(note)
    if midi is not None:
        n_str = _to_note(midi) if midi >= 0 else note
    else:
        n_str = note
    flat[instrument].append({
        "n": n_str,
        "b": round(beat, 4),
        "d": round(dur, 4),
        "v": round(vel, 3),
    })
    return beat + dur


def _process_event(event, instrument: str, flat: dict,
                   beat: float, patterns: dict) -> float:
    """Process one event, return new beat position."""

    # 1. Raw note tuple: ["C4", 0.5] or ["C4", 0.5, 0.8] or ["_", 0.25]
    if isinstance(event, list) and len(event) >= 2:
        note = str(event[0])
        dur = float(event[1])
        vel = float(event[2]) if len(event) > 2 else 0.8
        if note not in ("_", "rest"):
            beat = _add_note(flat, instrument, note, beat, dur, vel)
        else:
            beat += dur
        return beat

    if not isinstance(event, dict):
        return beat

    # 2. Delay start: {"delay_start": 0.75}
    if "delay_start" in event:
        return beat + event["delay_start"]

    # 3. Pattern play: {"play": "name", "repeat": 4, "transpose": 5, "velocity_mul": 0.8}
    if "play" in event:
        pat_name = event["play"]
        repeats = int(event.get("repeat", 1))
        transpose = int(event.get("transpose", 0))
        v_mul = float(event.get("velocity_mul", 1.0))

        pat = patterns.get(pat_name, [])
        for _ in range(repeats):
            for pe in pat:
                if isinstance(pe, list) and len(pe) >= 2:
                    p_note = str(pe[0])
                    p_dur = float(pe[1])
                    p_vel = float(pe[2]) if len(pe) > 2 else 0.8
                    p_vel *= v_mul

                    if p_note not in ("_", "rest"):
                        midi = _to_midi(p_note)
                        if midi is not None and transpose != 0:
                            final = _to_note(midi + transpose)
                        else:
                            final = p_note
                        beat = _add_note(flat, instrument, final, beat, p_dur, p_vel)
                    else:
                        beat += p_dur
        return beat

    # 4. Arpeggio: {"arp": ["C4","E4","G4"], "rate": 0.125, "dur": 2.0, "v": 0.7}
    if "arp" in event:
        notes = event["arp"]
        rate = float(event.get("rate", 0.125))
        total = float(event.get("dur", 1.0))
        vel = float(event.get("v", 0.7))
        steps = max(1, int(total / rate))
        for i in range(steps):
            n = notes[i % len(notes)]
            beat = _add_note(flat, instrument, n, beat, rate, vel)
        return beat

    # 5. Trill: {"trill": ["C5","D5"], "rate": 0.125, "dur": 1.0}
    if "trill" in event:
        pair = event["trill"]
        rate = float(event.get("rate", 0.125))
        total = float(event.get("dur", 1.0))
        vel = float(event.get("v", 0.8))
        steps = max(1, int(total / rate))
        for i in range(steps):
            n = pair[0] if i % 2 == 0 else pair[1]
            v = vel if i % 2 == 0 else vel * 0.65
            beat = _add_note(flat, instrument, n, beat, rate, v)
        return beat

    # 6. Slide: {"slide": ["C4","E4"], "steps": 4, "dur": 0.5}
    if "slide" in event:
        start_n, end_n = event["slide"]
        total = float(event.get("dur", 0.5))
        steps = int(event.get("steps", 4))
        vel = float(event.get("v", 0.8))
        s_midi = _to_midi(start_n)
        e_midi = _to_midi(end_n)
        if s_midi is None or e_midi is None:
            return beat
        rate = total / steps
        for i in range(steps):
            if steps > 1:
                curr = int(s_midi + (e_midi - s_midi) * i / (steps - 1))
            else:
                curr = s_midi
            beat = _add_note(flat, instrument, _to_note(curr), beat, rate, vel)
        return beat

    return beat


def is_tracker_ir(data: dict) -> bool:
    return "sections" in data and isinstance(data.get("sections"), list)
