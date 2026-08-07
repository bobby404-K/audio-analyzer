import numpy as np
import matplotlib.pyplot as plt
from load_audio import load_audio
from energy import compute_rms, smooth_energy, frame_to_time
from peaks import find_energy_peaks


def plot_energy(smoothed_rms, sr, peak_indices, valley_indices, hop_length=512):
    """
    Plots the smoothed energy curve with peaks, valleys, and mean line marked.
    """
    # Build a time axis (in seconds) matching the RMS frames
    time_axis = np.array([frame_to_time(i, sr, hop_length) for i in range(len(smoothed_rms))])
    mean_energy = np.mean(smoothed_rms)

    plt.figure(figsize=(14, 5))
    plt.plot(time_axis, smoothed_rms, label="Energy (smoothed RMS)", color="steelblue", linewidth=1)

    # Mean reference line
    plt.axhline(mean_energy, color="gray", linestyle="--", linewidth=1, label="Mean energy")

    # Mark peaks
    plt.scatter(time_axis[peak_indices], smoothed_rms[peak_indices],
                color="red", marker="^", s=80, label="Peaks (loud)", zorder=5)

    # Mark valleys
    plt.scatter(time_axis[valley_indices], smoothed_rms[valley_indices],
                color="green", marker="v", s=80, label="Valleys (quiet)", zorder=5)

    plt.xlabel("Time (seconds)")
    plt.ylabel("Energy (RMS)")
    plt.title("Song Energy Over Time — Peaks & Valleys")
    plt.legend()
    plt.tight_layout()
    plt.savefig("outputs/energy_plot.png")
    plt.show()


if __name__ == "__main__":
    file_path = "data/data.mp3"
    y, sr = load_audio(file_path)

    rms = compute_rms(y)
    smoothed_rms = smooth_energy(rms)

    peak_indices, valley_indices = find_energy_peaks(smoothed_rms, sr)

    plot_energy(smoothed_rms, sr, peak_indices, valley_indices)