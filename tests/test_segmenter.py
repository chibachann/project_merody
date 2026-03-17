from __future__ import annotations

from typing import Optional

from melody_transcriber.models.frame_pitch import FramePitch
from melody_transcriber.notes.segmenter import segment_notes


def _make_frames(
    pattern: list[tuple[Optional[int], int]],
    time_step_sec: float = 0.01,
) -> list[FramePitch]:
    """Build a FramePitch list from (midi_note, frame_count) pairs."""
    frames = []
    current_time = 0.0
    for midi_note, count in pattern:
        for _ in range(count):
            frames.append(FramePitch(
                time_sec=current_time,
                frequency_hz=None,
                midi_note=midi_note,
                is_voiced=midi_note is not None,
            ))
            current_time += time_step_sec
    return frames


def test_segment_notes_basic_two_notes():
    # 60 for 0.1s, then 62 for 0.1s
    frames = _make_frames([(60, 10), (62, 10)])
    notes = segment_notes(frames, min_note_duration_sec=0.05)
    assert len(notes) == 2
    assert notes[0].midi_note == 60
    assert notes[1].midi_note == 62


def test_segment_notes_filters_short_note():
    # note 60 lasts only 3 frames (0.03s) — below 0.05s threshold
    frames = _make_frames([(60, 3), (62, 10)])
    notes = segment_notes(frames, min_note_duration_sec=0.05)
    pitches = [n.midi_note for n in notes]
    assert 60 not in pitches


def test_segment_notes_handles_silence_between_notes():
    frames = _make_frames([(60, 10), (None, 5), (64, 10)])
    notes = segment_notes(frames, min_note_duration_sec=0.05)
    assert len(notes) == 2
    assert notes[0].midi_note == 60
    assert notes[1].midi_note == 64


def test_segment_notes_empty_input():
    assert segment_notes([]) == []


def test_segment_notes_all_silence():
    frames = _make_frames([(None, 20)])
    assert segment_notes(frames) == []


def test_segment_notes_times_are_non_overlapping():
    frames = _make_frames([(60, 10), (62, 10), (64, 10)])
    notes = segment_notes(frames, min_note_duration_sec=0.05)
    for i in range(len(notes) - 1):
        assert notes[i].end_time_sec <= notes[i + 1].start_time_sec
