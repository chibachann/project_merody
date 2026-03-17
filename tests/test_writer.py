import os
import tempfile

import pretty_midi

from melody_transcriber.models.note_event import NoteEvent
from melody_transcriber.midi.writer import write_midi


def _sample_notes() -> list[NoteEvent]:
    return [
        NoteEvent(start_time_sec=0.0, end_time_sec=0.5, midi_note=60, velocity=80),
        NoteEvent(start_time_sec=0.5, end_time_sec=1.0, midi_note=62, velocity=80),
        NoteEvent(start_time_sec=1.0, end_time_sec=1.5, midi_note=64, velocity=80),
    ]


def test_write_midi_creates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "out.mid")
        write_midi(_sample_notes(), output_path)
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 0


def test_write_midi_correct_note_count():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "out.mid")
        notes = _sample_notes()
        write_midi(notes, output_path)
        midi = pretty_midi.PrettyMIDI(output_path)
        assert len(midi.instruments) == 1
        assert len(midi.instruments[0].notes) == len(notes)


def test_write_midi_correct_pitches():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "out.mid")
        write_midi(_sample_notes(), output_path)
        midi = pretty_midi.PrettyMIDI(output_path)
        pitches = sorted(n.pitch for n in midi.instruments[0].notes)
        assert pitches == [60, 62, 64]


def test_write_midi_creates_parent_dirs():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "nested", "dir", "out.mid")
        write_midi(_sample_notes(), output_path)
        assert os.path.exists(output_path)
