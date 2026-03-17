from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class FramePitch:
    """F0 estimation result for a single audio frame."""

    time_sec: float
    frequency_hz: Optional[float]
    midi_note: Optional[int]
    is_voiced: bool
