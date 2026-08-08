import os
import sys

import matplotlib

# Pass "show" as a command-line argument to pop up interactive windows
# (only sensible for testing a single file). Without "show", runs
# headless and just saves PNGs — the safe default for many files.
interactive = "show" in sys.argv

if interactive:
    matplotlib.use("TkAgg")  # if this errors, try "Qt5Agg" instead
else:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from audio_utils import compute_rms_streaming, smooth_energy, frame_to_time, find_audio_files
from peaks import find_energy_peaks


def plot_energy(smoothed_rms, sr, peak_indices, valley_indices, output_path, hop_length=512, show=False):
    """Plots the smoothed energy curve with peaks, valleys, and mean line marked."""
    time_axis = np.array([frame_to_time(i, sr, hop_length) for i in range(len(smoothed_rms))])
    mean_energy = np.mean(smoothed_rms)

    fig = plt.figure(figsize=(14, 5))
    plt.plot(time_axis, smoothed_rms, label="Energy (smoothed RMS)", color="steelblue", linewidth=1)
    plt.axhline(mean_energy, color="gray", linestyle="--", linewidth=1, label="Mean energy")

    if len(peak_indices):
        plt.scatter(time_axis[peak_indices], smoothed_rms[peak_indices],
                    color="red", marker="^", s=80, label="Peaks (loud)", zorder=5)
    if len(valley_indices):
        plt.scatter(time_axis[valley_indices], smoothed_rms[valley_indices],
                    color="green", marker="v", s=80, label="Valleys (quiet)", zorder=5)

    plt.xlabel("Time (seconds)")
    plt.ylabel("Energy (RMS)")
    plt.title("Audio Energy Over Time — Peaks & Valleys")
    plt.legend()
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

    for file_path in tqdm(audio_files, desc="Plotting energy curves"):
        filename = os.path.basename(file_path)
        tqdm.write(f"Processing: {filename}")

        try:
            rms, sr = compute_rms_streaming(file_path)
            smoothed_rms = smooth_energy(rms)
            peak_indices, valley_indices = find_energy_peaks(smoothed_rms, sr)

            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{base_name}_energy_plot.png")
            plot_energy(smoothed_rms, sr, peak_indices, valley_indices, output_path, show=interactive)

            tqdm.write(f"  Saved: {output_path}  "
                       f"({len(peak_indices)} peaks, {len(valley_indices)} valleys)")
        except Exception as e:
            tqdm.write(f"  Skipped {filename} — error: {e}")

    print(f"\nDone. Saved {len(audio_files)} energy plot(s) to '{output_folder}/'")