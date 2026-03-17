import tempfile

import numpy as np
import pytest
import soundfile as sf

from melody_transcriber.audio.loader import load_audio


def _write_temp_wav(frequency_hz: float = 440.0, duration_sec: float = 1.0, sample_rate: int = 22050) -> str:
    """Write a sine-wave WAV file to a temp location and return its path."""
    t = np.linspace(0, duration_sec, int(sample_rate * duration_sec))
    y = np.sin(2 * np.pi * frequency_hz * t).astype(np.float32)
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, y, sample_rate)
    return tmp.name


def test_load_audio_returns_ndarray_and_sample_rate():
    path = _write_temp_wav()
    y, sr = load_audio(path, sample_rate=22050)
    assert isinstance(y, np.ndarray)
    assert sr == 22050


def test_load_audio_duration_is_approximately_correct():
    duration_sec = 2.0
    path = _write_temp_wav(duration_sec=duration_sec)
    y, sr = load_audio(path, sample_rate=22050)
    actual_duration = len(y) / sr
    assert abs(actual_duration - duration_sec) < 0.05


def test_load_audio_samples_not_empty():
    path = _write_temp_wav()
    y, _ = load_audio(path)
    assert len(y) > 0


def test_load_audio_invalid_file_raises_value_error():
    with pytest.raises(ValueError, match="Failed to load"):
        load_audio("/nonexistent/path/file.wav")
