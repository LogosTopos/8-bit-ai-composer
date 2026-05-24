"""
JS-API bridge: exposes audio engine methods to the pywebview frontend.
Supports dual mode: 8-bit synth (default) and SoundFont (piano/orchestral).
"""

import os

from ..audio import engine
from ..audio import sf2_engine
from ..audio.constants import (
    ARPEGGIO_TYPES,
    KEYMAP,
    NOTE_DISPLAY,
    PIANO_ORDER,
    WAVE_LABELS,
    WAVE_TYPES,
)


class JsApi:
    """API exposed to JavaScript via window.pywebview.api"""

    def __init__(self):
        self._mode = "8bit"  # "8bit" | "sf2"
        self._sf2_paths: list[str] = []
        self._scan_sf2()

    def _scan_sf2(self) -> None:
        """Find available .sf2 files."""
        asset_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__)))),
            "assets", "soundfonts"
        )
        if os.path.isdir(asset_dir):
            self._sf2_paths = sorted([
                f for f in os.listdir(asset_dir) if f.endswith(".sf2")
            ])

    # ---- mode ----

    def set_mode(self, mode: str) -> dict:
        """Switch between '8bit' and 'sf2' sound engines."""
        # Stop old engine
        if self._mode == "8bit":
            engine.all_notes_off()
        elif self._mode == "sf2":
            sf2_engine.get_sf2_synth().all_notes_off()
        self._mode = mode
        # Start new engine's stream, stop old
        if mode == "sf2":
            engine.stop_audio()
            sf2_engine.start_audio()
        else:
            sf2_engine.stop_audio()
            engine.start_audio()
        return {"mode": mode, "available_sf2": self._sf2_paths}

    def get_mode(self) -> dict:
        return {"mode": self._mode, "available_sf2": self._sf2_paths}

    def set_sf2(self, filename: str) -> dict:
        """Load a specific .sf2 file by name."""
        asset_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__)))),
            "assets", "soundfonts"
        )
        path = os.path.join(asset_dir, filename)
        if os.path.exists(path):
            sf2_engine.get_sf2_synth().load_sf2(path)
            return {"loaded": filename}
        return {"error": f"Not found: {filename}"}

    # ---- note on/off ----

    def note_on(self, key: str) -> dict | None:
        if self._mode == "sf2":
            midi = sf2_engine.note_on(key)
        else:
            midi = engine.note_on(key)
        if midi is not None:
            return {
                "midi": midi,
                "note": NOTE_DISPLAY[midi],
                "key": key.lower(),
            }
        return None

    def note_off(self, key: str) -> dict | None:
        if self._mode == "sf2":
            midi = sf2_engine.note_off(key)
        else:
            midi = engine.note_off(key)
        if midi is not None:
            return {
                "midi": midi,
                "note": NOTE_DISPLAY[midi],
                "key": key.lower(),
            }
        return None

    # ---- 8-bit specific ----

    def set_wave_type(self, wave: str) -> dict:
        engine.set_wave_type(wave)
        return {"wave": wave}

    def set_volume(self, vol: float) -> dict:
        if self._mode == "sf2":
            sf2_engine.get_sf2_synth().set_volume(vol)
        else:
            engine.set_volume(vol)
        return {"volume": vol}

    def set_arpeggio(self, arp_type: str) -> dict:
        engine.set_arpeggio(arp_type)
        return {"arpeggio": arp_type}

    def set_arpeggio_rate(self, rate: float) -> dict:
        engine.set_arpeggio_rate(rate)
        return {"rate": rate}

    def set_vibrato(self, depth: float, rate: float) -> dict:
        engine.set_vibrato(depth, rate)
        return {"depth": depth, "rate": rate}

    # ---- data ----

    def get_keymap(self) -> dict:
        return {
            key: {"midi": midi, "note": NOTE_DISPLAY[midi]}
            for key, midi in KEYMAP.items()
        }

    def get_wave_types(self) -> list:
        return WAVE_TYPES

    def get_wave_labels(self) -> dict:
        return WAVE_LABELS

    def get_arpeggio_types(self) -> list:
        return ARPEGGIO_TYPES

    def get_piano_order(self) -> list:
        result = []
        keymap = {
            key: {"midi": midi, "note": NOTE_DISPLAY[midi]}
            for key, midi in KEYMAP.items()
        }
        for entry in PIANO_ORDER:
            k = entry["key"]
            info = keymap.get(k, {})
            result.append({
                "type": entry["type"],
                "key": k,
                "note": info.get("note", "?"),
                "midi": info.get("midi"),
            })
        return result
