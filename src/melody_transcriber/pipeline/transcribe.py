from pathlib import Path

from melody_transcriber.config import TranscribeConfig
from melody_transcriber.audio.loader import load_audio
from melody_transcriber.audio.preprocess import normalize_audio
from melody_transcriber.pitch.estimator import estimate_pitch, save_f0_csv
from melody_transcriber.pitch.smoothing import smooth_pitch
from melody_transcriber.notes.segmenter import segment_notes, save_note_csv
from melody_transcriber.midi.writer import write_midi
from melody_transcriber.visualization.plotter import plot_results
from melody_transcriber.logger import get_logger

logger = get_logger(__name__)

_INTERIM_DIR = "data/interim"


def transcribe(input_path: str, output_path: str, config: TranscribeConfig) -> None:
    """Run the full melody transcription pipeline.

    Steps:
        1. Load and normalize audio
        2. Estimate pitch (F0) with pyin
        3. Smooth pitch
        4. Segment frames into NoteEvents
        5. Write MIDI file
        6. Optionally save CSVs and plot
    """
    stem = Path(input_path).stem

    logger.info("=== Step 1: Load audio ===")
    y, sr = load_audio(input_path, sample_rate=config.sample_rate)
    y = normalize_audio(y)

    logger.info("=== Step 2: Estimate pitch (F0) ===")
    frames = estimate_pitch(y, sr, fmin=config.fmin, fmax=config.fmax)

    logger.info("=== Step 3: Smooth pitch ===")
    frames = smooth_pitch(frames, window=config.pitch_smoothing_window)

    if config.save_f0_csv:
        save_f0_csv(frames, f"{_INTERIM_DIR}/{stem}_f0.csv")

    logger.info("=== Step 4: Segment notes ===")
    notes = segment_notes(
        frames,
        min_note_duration_sec=config.min_note_duration_sec,
        velocity=config.velocity,
    )

    if config.save_note_csv:
        save_note_csv(notes, f"{_INTERIM_DIR}/{stem}_notes.csv")

    logger.info("=== Step 5: Write MIDI ===")
    write_midi(notes, output_path, tempo_bpm=config.tempo_bpm)

    if config.plot:
        logger.info("=== Step 6: Visualize ===")
        plot_results(y, sr, frames, notes, output_path=f"{_INTERIM_DIR}/{stem}_plot.png")

    logger.info(f"=== Done. Output: {output_path} ===")
