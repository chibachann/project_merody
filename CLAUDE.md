# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**メロディ採譜ソフト (Melody Transcription Tool)** - A Python CLI tool that converts monophonic audio files (WAV/MP3 of humming, singing, or single instruments) into MIDI files.

This project is currently in the **planning phase**. The full specification is in `melody_transcription_project_plan.md`.

## Commands

Once the project is set up (Phase 1), the standard commands will be:

```bash
# Development install
pip install -e .

# Run the CLI
python -m melody_transcriber.main \
  --input data/raw/sample.wav \
  --output data/output/sample.mid \
  [--save-f0-csv] [--save-note-csv] [--plot] [--tempo <bpm>]

# Run all tests
pytest

# Run a single test file
pytest tests/test_audio_loader.py

# Run a single test
pytest tests/test_audio_loader.py::test_function_name
```

## Architecture

### Processing Pipeline

Audio file → **Preprocess** (mono/resample/normalize) → **F0 Estimation** (`librosa.pyin`) → **Note Segmentation** (frames → NoteEvent) → **MIDI Output** (`pretty_midi`)

### Planned Source Structure

```
src/melody_transcriber/
├── audio/          # Audio loading & preprocessing
├── pitch/          # F0 estimation & smoothing
├── notes/          # Frame-to-note conversion
├── midi/           # MIDI file generation
├── visualization/  # Waveform/pitch plotting
├── models/         # FramePitch, NoteEvent data classes
└── pipeline/       # Main orchestration
```

### Key Data Models

- **`FramePitch`**: `time_sec`, `frequency_hz`, `midi_note`, `is_voiced`
- **`NoteEvent`**: `start_time_sec`, `end_time_sec`, `midi_note`, `velocity`

### Core Libraries

| Purpose | Library |
|---|---|
| Audio loading | `librosa` |
| Pitch (F0) estimation | `librosa.pyin` |
| MIDI generation | `pretty_midi` |
| Visualization | `matplotlib` |
| Testing | `pytest` |
| Sheet music (future) | `music21` |

## Naming Conventions

- **Files/functions:** `snake_case`
- **Classes:** `PascalCase`
- **Function names:** verb-first (e.g., `load_audio()`, `estimate_pitch()`)
- **Variables:** include units where relevant (e.g., `start_time_sec`, `frequency_hz`)

## Design Principles

- **Single Responsibility:** Each module handles exactly one processing step
- **Separation:** Core algorithms (`src/`) isolated from orchestration (`pipeline/`)
- **Data Preservation:** Save intermediate results as CSV for debugging
- **Experiments:** Use `notebooks/` for exploration; move finalized code to `src/`

## Development Phases

The project plan defines 8 phases. Implement in order:

1. Project setup & CLI skeleton
2. Audio input & preprocessing
3. F0 pitch estimation
4. Note segmentation
5. MIDI output
6. Visualization & validation
7. Accuracy improvements
8. Sheet music generation (future)
