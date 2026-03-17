from dataclasses import dataclass, field


@dataclass
class NoteEvent:
    """A single musical note with start/end time and MIDI pitch."""

    start_time_sec: float
    end_time_sec: float
    midi_note: int
    velocity: int = 80
