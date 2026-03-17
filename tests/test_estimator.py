from __future__ import annotations

import numpy as np
import pytest

from melody_transcriber.models.frame_pitch import FramePitch
from melody_transcriber.pitch.estimator import estimate_pitch


def _sine_wave(frequency_hz: float = 440.0, duration_sec: float = 1.0, sample_rate: int = 22050) -> np.ndarray:
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec))
    return np.sin(2 * np.pi * frequency_hz * t).astype(np.float32)


def test_estimate_pitch_returns_list_of_frame_pitch():
    y = _sine_wave(440.0)
    frames = estimate_pitch(y, sample_rate=22050)
    assert len(frames) > 0
    assert all(isinstance(f, FramePitch) for f in frames)


def test_estimate_pitch_times_are_strictly_ascending():
    y = _sine_wave(440.0)
    frames = estimate_pitch(y, sample_rate=22050)
    times = [f.time_sec for f in frames]
    assert times == sorted(times)
    assert len(set(times)) == len(times)  # no duplicates


def test_estimate_pitch_detects_voiced_frames_for_pure_tone():
    # A pure 440 Hz sine wave should yield mostly voiced frames
    y = _sine_wave(440.0, duration_sec=2.0)
    frames = estimate_pitch(y, sample_rate=22050, fmin=65.0, fmax=2093.0)
    voiced_ratio = sum(1 for f in frames if f.is_voiced) / len(frames)
    assert voiced_ratio > 0.5


def test_estimate_pitch_midi_notes_in_valid_range():
    y = _sine_wave(440.0)
    frames = estimate_pitch(y, sample_rate=22050)
    for f in frames:
        if f.midi_note is not None:
            assert 0 <= f.midi_note <= 127
