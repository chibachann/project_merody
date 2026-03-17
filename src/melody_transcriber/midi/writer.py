from pathlib import Path

import pretty_midi

from melody_transcriber.models.note_event import NoteEvent
from melody_transcriber.logger import get_logger

logger = get_logger(__name__)


def write_midi(
    notes: list[NoteEvent],
    output_path: str,
    tempo_bpm: float = 120.0,
) -> None:
    """Write a list of NoteEvent objects to a MIDI file.

    Uses a single piano instrument (program 0). Velocity and timing are taken
    directly from each NoteEvent.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    midi = pretty_midi.PrettyMIDI(initial_tempo=tempo_bpm)
    instrument = pretty_midi.Instrument(program=0, name="Melody")

    for note in notes:
        instrument.notes.append(pretty_midi.Note(
            velocity=note.velocity,
            pitch=note.midi_note,
            start=note.start_time_sec,
            end=note.end_time_sec,
        ))

    midi.instruments.append(instrument)
    midi.write(output_path)
    logger.info(f"  MIDI saved   : {output_path}")
