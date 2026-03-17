from __future__ import annotations

import csv
from pathlib import Path
from typing import Optional

from melody_transcriber.models.frame_pitch import FramePitch
from melody_transcriber.models.note_event import NoteEvent
from melody_transcriber.logger import get_logger

logger = get_logger(__name__)


def segment_notes(
    frames: list[FramePitch],
    min_note_duration_sec: float = 0.05,
    velocity: int = 80,
) -> list[NoteEvent]:
    """Convert a sequence of FramePitch objects into a list of NoteEvent objects.

    Consecutive voiced frames with the same MIDI note are merged into one NoteEvent.
    Notes shorter than min_note_duration_sec are discarded.
    """
    if not frames:
        return []

    notes: list[NoteEvent] = []
    current_note: Optional[int] = None
    note_start_sec: float = 0.0

    for frame in frames:
        frame_note = frame.midi_note if frame.is_voiced else None

        if frame_note != current_note:
            # Close the current note segment
            if current_note is not None:
                duration = frame.time_sec - note_start_sec
                if duration >= min_note_duration_sec:
                    notes.append(NoteEvent(
                        start_time_sec=note_start_sec,
                        end_time_sec=frame.time_sec,
                        midi_note=current_note,
                        velocity=velocity,
                    ))
            current_note = frame_note
            note_start_sec = frame.time_sec

    # Close the final open note
    if current_note is not None and frames:
        last_time = frames[-1].time_sec
        duration = last_time - note_start_sec
        if duration >= min_note_duration_sec:
            notes.append(NoteEvent(
                start_time_sec=note_start_sec,
                end_time_sec=last_time,
                midi_note=current_note,
                velocity=velocity,
            ))

    logger.info(f"  Extracted {len(notes)} notes")
    return notes


def save_note_csv(notes: list[NoteEvent], output_path: str) -> None:
    """Save NoteEvent list to a CSV file."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["start_time_sec", "end_time_sec", "midi_note", "velocity"])
        for note in notes:
            writer.writerow([note.start_time_sec, note.end_time_sec, note.midi_note, note.velocity])
    logger.info(f"  Note CSV saved: {output_path}")
