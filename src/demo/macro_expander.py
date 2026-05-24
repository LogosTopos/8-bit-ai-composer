"""
Macro JSON Expander: converts Pattern-Sequencer format to flat note-list format.

Input (LLM output):
{
  "bpm": 130,
  "patterns": {
    "melody_A": [ ["C5", 0.5], ["_", 0.5], ["G4", 0.25] ],
    "bass": [ ["C3", 0.5], ["C4", 0.5] ]
  },
  "arrangement": [
    {
      "instrument": "pulse_50",
      "track": [
        { "pattern": "melody_A", "repeat": 2, "transpose": 0 },
        { "pattern": "melody_A", "repeat": 2, "transpose": 5 }
      ]
    }
  ]
}

Output: flat {"bpm": 130, "tracks": [{"instrument":"pulse_50", "notes":[{"n":"C4","b":0.0,"d":0.5},...]}]}
"""

import re

# ─── note ↔ midi ──────────────────────────────────────────

_NOTE_MAP = {
    "C": 0, "C#": 1, "DB": 1, "D": 2, "D#": 3, "EB": 3,
    "E": 4, "F": 5, "F#": 6, "GB": 6, "G": 7, "G#": 8,
    "AB": 8, "A": 9, "A#": 10, "BB": 10, "B": 11,
}

_MIDI_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_to_midi(note_str: str) -> int | None:
    """Parse 'C4' -> 60, 'D#3' -> 51, 'Eb5' -> 75. Returns None for rests."""
    note_str = note_str.strip()
    if note_str in ("_", "*", ""):
        return None
    # Already a number?
    try:
        return int(note_str)
    except ValueError:
        pass
    # Parse name + octave
    base = note_str.rstrip("0123456789-")
    if base not in _NOTE_MAP:
        return None
    oct_str = note_str[len(base):]
    try:
        octave = int(oct_str)
    except ValueError:
        return None
    return _NOTE_MAP[base] + (octave + 1) * 12


def midi_to_note(midi_val: int) -> str:
    """Convert 60 -> 'C4', 51 -> 'D#3'."""
    octave = (midi_val // 12) - 1
    note = _MIDI_NAMES[midi_val % 12]
    return f"{note}{octave}"


# ─── expander ─────────────────────────────────────────────

def expand_macro_json(macro: dict) -> dict:
    """
    Convert a macro Pattern-Sequencer JSON to flat note-list JSON
    compatible with the existing Renderer.
    """
    bpm = macro.get("bpm", 120)
    patterns = macro.get("patterns", {})
    arrangement = macro.get("arrangement", [])

    flat_tracks = []

    for track_data in arrangement:
        instrument = track_data.get("instrument", "pulse_50")
        flat_notes = []
        current_beat = 0.0

        for seq_item in track_data.get("track", []):
            pat_name = seq_item.get("pattern", "")
            repeats = max(1, int(seq_item.get("repeat", 1)))
            transpose = int(seq_item.get("transpose", 0))

            pattern_notes = patterns.get(pat_name, [])

            for _ in range(repeats):
                for note_data in pattern_notes:
                    if not isinstance(note_data, (list, tuple)) or len(note_data) < 2:
                        continue

                    n_str = str(note_data[0])
                    duration = float(note_data[1])

                    if n_str != "_":
                        midi = note_to_midi(n_str)
                        if midi is not None:
                            midi += transpose
                            final_n = midi_to_note(midi)
                        else:
                            final_n = n_str  # passthrough for non-standard
                        flat_notes.append({
                            "n": final_n,
                            "b": round(current_beat, 4),
                            "d": round(duration, 4),
                        })

                    current_beat += duration

        flat_tracks.append({
            "instrument": instrument,
            "notes": flat_notes,
        })

    return {"bpm": bpm, "tracks": flat_tracks}


def is_macro_format(data: dict) -> bool:
    """Detect whether JSON uses the macro format (has 'patterns' key)."""
    return "patterns" in data and "arrangement" in data
