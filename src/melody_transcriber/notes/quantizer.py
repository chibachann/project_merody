from __future__ import annotations

from melody_transcriber.models.note_event import NoteEvent


def quantize_notes(notes: list[NoteEvent], tempo_bpm: float, subdivisions: int = 4) -> list[NoteEvent]:
    """Snap note start/end times to the nearest rhythmic grid position.

    subdivisions: number of divisions per beat (4 = sixteenth notes).
    """
    if not notes or tempo_bpm <= 0:
        return notes

    beat_sec = 60.0 / tempo_bpm
    grid_sec = beat_sec / subdivisions

    def snap(t: float) -> float:
        return round(t / grid_sec) * grid_sec

    quantized = []
    for note in notes:
        start = snap(note.start_time_sec)
        end = snap(note.end_time_sec)
        if end <= start:
            end = start + grid_sec
        quantized.append(NoteEvent(
            start_time_sec=start,
            end_time_sec=end,
            midi_note=note.midi_note,
            velocity=note.velocity,
        ))
    return quantized
