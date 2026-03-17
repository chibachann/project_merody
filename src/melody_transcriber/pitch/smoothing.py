from melody_transcriber.models.frame_pitch import FramePitch


def smooth_pitch(frames: list[FramePitch], window: int = 5) -> list[FramePitch]:
    """Apply a median filter over MIDI note values to reduce short fluctuations."""
    if window < 2:
        return frames

    notes = [f.midi_note if f.is_voiced and f.midi_note is not None else None for f in frames]
    smoothed = notes.copy()
    half = window // 2

    for i, note in enumerate(notes):
        if note is None:
            continue
        neighbors = [
            notes[j]
            for j in range(max(0, i - half), min(len(notes), i + half + 1))
            if notes[j] is not None
        ]
        if neighbors:
            smoothed[i] = int(sorted(neighbors)[len(neighbors) // 2])

    return [
        FramePitch(
            time_sec=frame.time_sec,
            frequency_hz=frame.frequency_hz,
            midi_note=smoothed_note,
            is_voiced=frame.is_voiced,
        )
        for frame, smoothed_note in zip(frames, smoothed)
    ]
