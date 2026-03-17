from __future__ import annotations

import csv
from pathlib import Path
from typing import Optional

import numpy as np
import librosa

from melody_transcriber.models.frame_pitch import FramePitch
from melody_transcriber.logger import get_logger

logger = get_logger(__name__)


def estimate_pitch(
    y: np.ndarray,
    sample_rate: int,
    fmin: float = 65.0,
    fmax: float = 2093.0,
) -> list[FramePitch]:
    """Estimate F0 using pyin and return a list of FramePitch objects."""
    f0, voiced_flag, _ = librosa.pyin(y, fmin=fmin, fmax=fmax, sr=sample_rate)
    times = librosa.times_like(f0, sr=sample_rate)

    frames: list[FramePitch] = []
    for time_sec, freq, is_voiced in zip(times, f0, voiced_flag):
        if is_voiced and freq is not None and not np.isnan(freq):
            midi_note = int(round(librosa.hz_to_midi(freq)))
            frequency_hz: Optional[float] = float(freq)
        else:
            midi_note = None
            frequency_hz = None

        frames.append(FramePitch(
            time_sec=float(time_sec),
            frequency_hz=frequency_hz,
            midi_note=midi_note,
            is_voiced=bool(is_voiced),
        ))

    voiced_count = sum(1 for f in frames if f.is_voiced)
    logger.info(f"  Total frames : {len(frames)}")
    logger.info(f"  Voiced frames: {voiced_count}")
    if voiced_count == 0:
        logger.warning("No voiced frames detected. Check audio content or --fmin/--fmax settings.")

    return frames


def save_f0_csv(frames: list[FramePitch], output_path: str) -> None:
    """Save FramePitch list to a CSV file."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time_sec", "frequency_hz", "midi_note", "is_voiced"])
        for frame in frames:
            writer.writerow([
                frame.time_sec,
                frame.frequency_hz if frame.frequency_hz is not None else "",
                frame.midi_note if frame.midi_note is not None else "",
                frame.is_voiced,
            ])
    logger.info(f"  F0 CSV saved : {output_path}")
