import os
import librosa
import numpy as np
from audio_utils import find_audio_files


def load_audio(file_path, duration=None):
    """
    Loads an audio file and returns the waveform + sample rate.
    y  = waveform (NumPy array of amplitude values over time)
    sr = sample rate (how many samples represent 1 second of audio)

    Loaded as mono (mono=True) — halves memory usage vs. stereo,
    and energy/RMS analysis doesn't need separate channels anyway.

    duration = optional cap in seconds. Some MP3s (usually VBR-encoded)
    have inaccurate headers that make librosa think the file is far
    longer than it really is, causing huge/failed memory allocations.
    Passing a duration limits how much librosa tries to read.
    """
    y, sr = librosa.load(file_path, sr=None, mono=True, duration=duration)
    return y, sr


if __name__ == "__main__":
    data_folder = "data"

    if not os.path.isdir(data_folder):
        print(f"'{data_folder}/' folder doesn't exist relative to your current directory.")
        print(f"Current working directory: {os.getcwd()}")
        print(f"(Tip: run this script from the project root, not from inside src/)")
    else:
        audio_files = find_audio_files(data_folder)

        if not audio_files:
            print(f"'{data_folder}/' exists but has no .mp3/.wav files in it.")
        else:
            print(f"Found {len(audio_files)} file(s) — running a quick 30s smoke test on each.\n")

            for file_path in audio_files:
                print(f"{'='*50}")
                print(f"File: {file_path}")
                print(f"{'='*50}")

                try:
                    # Quick smoke test only — capped at 30s. Full-length
                    # analysis happens in energy.py / peaks.py, which
                    # stream the whole file instead of loading it all here.
                    y, sr = load_audio(file_path, duration=30)

                    print("Sample rate:", sr)
                    print("Waveform shape:", y.shape)
                    print("Duration loaded (seconds):", len(y) / sr)
                except Exception as e:
                    print(f"  Skipped {file_path} — error: {e}")

                print()

            print(f"Done. Smoke-tested {len(audio_files)} file(s).")
            print("(Full analysis happens in energy.py / peaks.py / batch_analyze.py, "
                  "which stream the entire file.)")