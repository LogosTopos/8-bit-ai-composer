"""
SoundFont engine using TinySoundFont (pure Python, no DLL needed).
Drop-in replacement API compatible with the 8-bit engine.
"""

import os
import threading

import numpy as np
import sounddevice as sd

from .constants import KEYMAP, SAMPLE_RATE

_RENDER_BLOCK = 256  # samples per callback block


class SF2Synthesizer:
    """Polyphonic SoundFont synthesizer with real-time audio output."""

    def __init__(self, sf2_path: str | None = None):
        self._lock = threading.Lock()
        self._stream: sd.OutputStream | None = None
        self._active_notes: set[int] = set()
        self._volume = 0.7
        self._synth = None
        self._sfid = 0
        self._preset = 0  # 0 = Acoustic Grand Piano
        self._sf2_path = sf2_path

        if sf2_path and os.path.exists(sf2_path):
            self._load_sf2(sf2_path)

    def _load_sf2(self, path: str) -> None:
        from tinysoundfont import Synth
        self._synth = Synth()
        self._synth.samplerate = SAMPLE_RATE
        # Do NOT call self._synth.start() — it opens its own pyaudio stream
        self._sfid = self._synth.sfload(path)
        self._synth.program_select(0, self._sfid, 0, self._preset)
        self._sf2_path = path

    def load_sf2(self, path: str, preset: int = 0) -> None:
        """Load a .sf2 file. preset: 0=piano, 24=nylon guitar, etc."""
        with self._lock:
            was_running = self._stream is not None
            if was_running:
                self._stream.stop()
                self._stream.close()
                self._stream = None
            self._load_sf2(path)
            self._preset = preset
            self._synth.program_select(0, self._sfid, 0, preset)
            if was_running:
                self._start_stream()

    def set_preset(self, preset: int) -> None:
        """Change MIDI program (instrument)."""
        with self._lock:
            self._preset = preset
            if self._synth:
                self._synth.program_select(0, self._sfid, 0, preset)

    # ---- audio callback ----

    def _audio_callback(self, outdata: np.ndarray, frames: int,
                        _time, _status) -> None:
        with self._lock:
            if self._synth is None:
                outdata.fill(0.0)
                return
            # generate(frames) → memoryview of frames*8 bytes (stereo float32)
            buf = self._synth.generate(frames)
            if buf is None or len(buf) == 0:
                outdata.fill(0.0)
                return
            arr = np.frombuffer(buf, dtype=np.float32).reshape(-1, 2)
            mono = arr.mean(axis=1) * self._volume
            n = min(len(mono), frames)
            outdata[:n, 0] = mono[:n]
            if n < frames:
                outdata[n:, 0] = 0.0

    # ---- stream management ----

    def _start_stream(self) -> None:
        if self._stream is not None:
            return
        self._stream = sd.OutputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            blocksize=_RENDER_BLOCK,
            callback=self._audio_callback,
            latency="low",
        )
        self._stream.start()

    def start(self) -> None:
        with self._lock:
            self._start_stream()

    def stop(self) -> None:
        with self._lock:
            if self._stream is None:
                return
            self._stream.stop()
            self._stream.close()
            self._stream = None

    def note_on(self, midi_note: int, velocity: int = 80) -> None:
        with self._lock:
            if self._synth is None:
                return
            self._synth.noteon(0, midi_note, velocity)
            self._active_notes.add(midi_note)

    def note_off(self, midi_note: int) -> None:
        with self._lock:
            if self._synth is None:
                return
            self._synth.noteoff(0, midi_note)
            self._active_notes.discard(midi_note)

    def set_volume(self, volume: float) -> None:
        self._volume = max(0.0, min(1.0, volume))
        with self._lock:
            if self._synth:
                self._synth.gain = volume

    def all_notes_off(self) -> None:
        with self._lock:
            if self._synth is None:
                return
            for n in list(self._active_notes):
                self._synth.noteoff(0, n)
            self._active_notes.clear()


# Global singleton
_sf2_synth: SF2Synthesizer | None = None


def get_sf2_synth(sf2_path: str | None = None) -> SF2Synthesizer:
    global _sf2_synth
    if _sf2_synth is None:
        p = sf2_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__)))),  # src/audio -> src -> project root
            "assets", "soundfonts", "GeneralUser-GS.sf2"
        )
        _sf2_synth = SF2Synthesizer(p)
    elif sf2_path and sf2_path != _sf2_synth._sf2_path:
        _sf2_synth.load_sf2(sf2_path)
    return _sf2_synth


def start_audio() -> None:
    get_sf2_synth().start()


def stop_audio() -> None:
    global _sf2_synth
    if _sf2_synth is not None:
        _sf2_synth.stop()


def note_on(key: str) -> int | None:
    midi = KEYMAP.get(key.lower())
    if midi is not None:
        get_sf2_synth().note_on(midi)
    return midi


def note_off(key: str) -> int | None:
    midi = KEYMAP.get(key.lower())
    if midi is not None:
        get_sf2_synth().note_off(midi)
    return midi
