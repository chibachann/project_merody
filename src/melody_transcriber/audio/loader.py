import numpy as np
import librosa

from melody_transcriber.logger import get_logger

logger = get_logger(__name__)


def load_audio(file_path: str, sample_rate: int = 22050) -> tuple[np.ndarray, int]:
    """Load an audio file, convert to mono, and resample to the target sample rate."""
    logger.info(f"Loading audio: {file_path}")
    try:
        y, sr = librosa.load(file_path, sr=sample_rate, mono=True)
    except Exception as e:
        raise ValueError(f"Failed to load audio file '{file_path}': {e}") from e

    duration_sec = len(y) / sr
    logger.info(f"  Sample rate : {sr} Hz")
    logger.info(f"  Duration    : {duration_sec:.2f} sec")
    logger.info(f"  Samples     : {len(y)}")
    return y, sr
