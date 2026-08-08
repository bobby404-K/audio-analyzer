import os
import sys

import matplotlib

# Pass "show" as a command-line argument to pop up interactive windows
# (only sensible for testing a single file — it will freeze at each
# plot until you close the window). Without "show", runs headless and
# just saves PNGs — the safe default for batches of many files.
interactive = "show" in sys.argv

if interactive:
    matplotlib.use("TkAgg")  # if this errors, try "Qt5Agg" instead
else:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from audio_utils import find_audio_files


def compute_waveform_envelope(file_path, target_points=100_000, block_size=2_000_000):
    """
    Streams the audio file in chunks and computes a min/max envelope per
    time-bucket, without ever loading the entire waveform into memory —
    the same approach tools like Audacity use to render very long audio.
    """
    with sf.SoundFile(file_path) as f:
        sr = f.samplerate
        channels = f.channels
        total_frames = len(f)
        duration = total_frames / sr

        samples_per_point = max(1, total_frames // target_points)

        mins, maxs = [], []
        leftover = np.array([], dtype="float32")

        while True:
            block = f.read(block_size, dtype="float32", always_2d=False)
            if len(block) == 0:
                break

            if channels > 1:
                block = block.mean(axis=1)

            block = np.concatenate([leftover, block])

            usable_len = len(block) - (len(block) % samples_per_point)
            if usable_len == 0:
                leftover = block
                continue

            usable = block[:usable_len]
            leftover = block[usable_len:]

            reshaped = usable.reshape(-1, samples_per_point)
            mins.append(reshaped.min(axis=1))
            maxs.append(reshaped.max(axis=1))

        if len(leftover) > 0:
            mins.append(np.array([leftover.min()]))
            maxs.append(np.array([leftover.max()]))

    mins = np.concatenate(mins)
    maxs = np.concatenate(maxs)
    time_axis = np.linspace(0, duration, num=len(mins))

    return time_axis, mins, maxs, sr, duration


def plot_waveform(time_axis, mins, maxs, output_path, show=False):
    """Plots a min/max envelope waveform, saves it, and optionally pops up a window."""
    fig = plt.figure(figsize=(14, 4))
    plt.fill_between(time_axis, mins, maxs, color="steelblue", linewidth=0)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Raw Audio Waveform (min/max envelope)")
    plt.tight_layout()
    plt.savefig(output_path)

    if show:
        plt.show()

    plt.close(fig)


if __name__ == "__main__":
    try:
        from tqdm import tqdm
    except ImportError:
        def tqdm(iterable, **kwargs):
            return iterable
        class _FallbackTqdm:
            @staticmethod
            def write(msg):
                print(msg)
        tqdm.write = _FallbackTqdm.write

    data_folder = "data"
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)

    audio_files = find_audio_files(data_folder)
    if not audio_files:
        print(f"No audio files found in '{data_folder}/'")

    for file_path in tqdm(audio_files, desc="Plotting waveforms"):
        filename = os.path.basename(file_path)
        tqdm.write(f"Processing: {filename}")

        try:
            time_axis, mins, maxs, sr, duration = compute_waveform_envelope(file_path)

            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{base_name}_waveform.png")
            plot_waveform(time_axis, mins, maxs, output_path, show=interactive)

            tqdm.write(f"  Saved: {output_path}")
        except Exception as e:
            tqdm.write(f"  Skipped {filename} — error: {e}")

    print(f"\nDone. Saved {len(audio_files)} waveform plot(s) to '{output_folder}/'")