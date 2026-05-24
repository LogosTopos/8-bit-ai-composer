"""
8-Bit Composer - Entry point.
Launches the desktop UI and audio engine.
"""

import sys
import os

# Ensure src is on path
sys.path.insert(0, os.path.dirname(__file__))

from src.audio.engine import start_audio, stop_audio
from src.ui.app import launch


def main():
    print("[8-bit] Starting audio engine...")
    start_audio()
    print("[8-bit] Audio engine ready.")
    print("[8-bit] Launching UI...")

    try:
        launch()
    finally:
        print("[8-bit] Shutting down...")
        stop_audio()
        print("[8-bit] Done.")


if __name__ == "__main__":
    main()
