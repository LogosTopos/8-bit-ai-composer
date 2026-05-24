"""
Audio engine: thin wrapper around Synthesizer for the UI layer.
"""

from .constants import (
    ARPEGGIO_TYPES,
    KEYMAP,
    NOTE_DISPLAY,
    PIANO_ORDER,
    WAVE_LABELS,
    WAVE_TYPES,
)
from .synthesizer import Synthesizer

_synth: Synthesizer | None = None


def get_synth() -> Synthesizer:
    global _synth
    if _synth is None:
        _synth = Synthesizer()
    return _synth


def start_audio() -> None:
    get_synth().start()


def stop_audio() -> None:
    if _synth is not None:
        _synth.stop()


def note_on(key: str) -> int | None:
    midi = KEYMAP.get(key.lower())
    if midi is not None:
        get_synth().note_on(midi)
    return midi


def note_off(key: str) -> int | None:
    midi = KEYMAP.get(key.lower())
    if midi is not None:
        get_synth().note_off(midi)
    return midi


def set_wave_type(wave: str) -> None:
    if wave in WAVE_TYPES:
        get_synth().set_wave_type(wave)


def set_volume(vol: float) -> None:
    get_synth().set_volume(vol)


def set_arpeggio(arp_type: str | None) -> None:
    if arp_type is None or arp_type in ARPEGGIO_TYPES or arp_type == "off":
        get_synth().set_arpeggio(None if arp_type in (None, "off") else arp_type)


def set_arpeggio_rate(rate: float) -> None:
    get_synth().set_arpeggio_rate(rate)


def set_vibrato(depth: float, rate: float) -> None:
    get_synth().set_vibrato(depth, rate)


def set_adsr(attack: float, decay: float, sustain: float, release: float) -> None:
    get_synth().set_adsr(attack, decay, sustain, release)


def all_notes_off() -> None:
    if _synth is not None:
        _synth.all_notes_off()
