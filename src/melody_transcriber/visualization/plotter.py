from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt

from melody_transcriber.models.frame_pitch import FramePitch
from melody_transcriber.models.note_event import NoteEvent
from melody_transcriber.logger import get_logger

logger = get_logger(__name__)


def plot_results(
    y: np.ndarray,
    sample_rate: int,
    frames: list[FramePitch],
    notes: list[NoteEvent],
    output_path: Optional[str] = None,
) -> None:
    """Plot waveform, estimated F0, and segmented note events.

    Saves to output_path if given, otherwise displays interactively.
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 8))

    # --- Waveform ---
    times_wave = np.linspace(0, len(y) / sample_rate, len(y))
    axes[0].plot(times_wave, y, color="steelblue", linewidth=0.4)
    axes[0].set_title("Waveform")
    axes[0].set_ylabel("Amplitude")
    axes[0].set_xlabel("Time (sec)")

    # --- F0 curve ---
    voiced_times = [f.time_sec for f in frames if f.is_voiced and f.midi_note is not None]
    voiced_notes = [f.midi_note for f in frames if f.is_voiced and f.midi_note is not None]
    axes[1].scatter(voiced_times, voiced_notes, s=2, color="darkorange", label="F0 (MIDI note)")
    axes[1].set_title("Estimated F0")
    axes[1].set_ylabel("MIDI note number")
    axes[1].set_xlabel("Time (sec)")
    axes[1].legend(markerscale=5)

    # --- Note events ---
    for note in notes:
        axes[2].barh(
            y=note.midi_note,
            width=note.end_time_sec - note.start_time_sec,
            left=note.start_time_sec,
            height=0.8,
            color="seagreen",
            alpha=0.75,
        )
    axes[2].set_title("Note Events")
    axes[2].set_ylabel("MIDI note number")
    axes[2].set_xlabel("Time (sec)")

    plt.tight_layout()

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=150)
        logger.info(f"  Plot saved   : {output_path}")
    else:
        plt.show()

    plt.close(fig)
