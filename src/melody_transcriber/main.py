import argparse
import sys

from melody_transcriber.config import TranscribeConfig
from melody_transcriber.pipeline.transcribe import transcribe


def main() -> None:
    """CLI entry point for melody-transcriber."""
    parser = argparse.ArgumentParser(
        prog="melody-transcriber",
        description="Transcribe a monophonic melody audio file to MIDI.",
    )
    parser.add_argument("--input", required=True, help="Path to input audio file (wav / mp3)")
    parser.add_argument("--output", required=True, help="Path to output MIDI file (.mid)")
    parser.add_argument("--save-f0-csv", action="store_true", help="Save F0 estimation CSV to data/interim/")
    parser.add_argument("--save-note-csv", action="store_true", help="Save note segmentation CSV to data/interim/")
    parser.add_argument("--plot", action="store_true", help="Save visualization plot to data/interim/")
    parser.add_argument("--tempo", type=float, default=120.0, metavar="BPM", help="Tempo in BPM (default: 120)")
    parser.add_argument(
        "--min-note-duration",
        type=float,
        default=0.05,
        metavar="SEC",
        help="Minimum note duration in seconds (default: 0.05)",
    )
    parser.add_argument("--fmin", type=float, default=65.0, help="Min frequency for pitch detection in Hz (default: 65.0 = C2)")
    parser.add_argument("--fmax", type=float, default=2093.0, help="Max frequency for pitch detection in Hz (default: 2093.0 = C7)")

    args = parser.parse_args()

    config = TranscribeConfig(
        save_f0_csv=args.save_f0_csv,
        save_note_csv=args.save_note_csv,
        plot=args.plot,
        tempo_bpm=args.tempo,
        min_note_duration_sec=args.min_note_duration,
        fmin=args.fmin,
        fmax=args.fmax,
    )

    try:
        transcribe(args.input, args.output, config)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
