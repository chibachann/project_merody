from dataclasses import dataclass


@dataclass
class TranscribeConfig:
    """Configuration parameters for the transcription pipeline."""

    sample_rate: int = 22050
    fmin: float = 65.0        # C2 - lower bound for pitch detection
    fmax: float = 2093.0      # C7 - upper bound for pitch detection
    min_note_duration_sec: float = 0.05
    pitch_smoothing_window: int = 5
    velocity: int = 80
    tempo_bpm: float = 120.0
    save_f0_csv: bool = False
    save_note_csv: bool = False
    plot: bool = False
