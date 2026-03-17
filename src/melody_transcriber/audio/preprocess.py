import numpy as np

from melody_transcriber.logger import get_logger

logger = get_logger(__name__)


def normalize_audio(y: np.ndarray) -> np.ndarray:
    """Peak-normalize audio to the range [-1, 1]."""
    peak = np.max(np.abs(y))
    if peak < 1e-6:
        logger.warning("Audio signal is nearly silent — skipping normalization.")
        return y
    return y / peak
