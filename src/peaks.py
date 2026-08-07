import numpy as np
from scipy.signal import find_peaks
from load_audio import load_audio
from energy import compute_rms, smooth_energy, frame_to_time, format_time


def find_energy_peaks(smoothed_rms, sr, hop_length=512, distance_seconds=5, prominence=0.02):
    """
    Finds peaks (loud moments) and valleys (quiet moments) in the energy curve
    using local maxima/minima detection.

    distance_seconds = minimum time gap required between two peaks
    prominence        = how much a peak must stand out from surrounding values
    """
    distance_frames = int((distance_seconds * sr) / hop_length)

    peak_indices, _ = find_peaks(
        smoothed_rms,
        distance=distance_frames,
        prominence=prominence
    )

    valley_indices, _ = find_peaks(
        -smoothed_rms,
        distance=distance_frames,
        prominence=prominence
    )

    return peak_indices, valley_indices


def classify_by_second(smoothed_rms, sr, hop_length=512):
    """
    Groups energy values into 1-second buckets, then classifies each second
    as 'PEAK' (above overall mean) or 'valley' (below overall mean).
    """
    frames_per_second = int(sr / hop_length)
    total_seconds = len(smoothed_rms) // frames_per_second
    mean_energy = np.mean(smoothed_rms)

    results = []
    for sec in range(total_seconds):
        start = sec * frames_per_second
        end = start + frames_per_second
        avg_energy = np.mean(smoothed_rms[start:end])

        label = "PEAK" if avg_energy > mean_energy else "valley"
        results.append((sec, avg_energy, label))

    return results, mean_energy


if __name__ == "__main__":
    file_path = "data/data.mp3"
    y, sr = load_audio(file_path)

    rms = compute_rms(y)
    smoothed_rms = smooth_energy(rms)

    # --- Approach 1: local peak/valley detection ---
    peak_indices, valley_indices = find_energy_peaks(smoothed_rms, sr)

    print(f"Found {len(peak_indices)} local peaks (loud moments):")
    for idx in peak_indices:
        t = frame_to_time(idx, sr)
        print(f"  {format_time(t)}  (RMS = {smoothed_rms[idx]:.4f})")

    print(f"\nFound {len(valley_indices)} local valleys (quiet moments):")
    for idx in valley_indices:
        t = frame_to_time(idx, sr)
        print(f"  {format_time(t)}  (RMS = {smoothed_rms[idx]:.4f})")

    # --- Approach 2: per-second classification against overall mean ---
    print("\n" + "=" * 50)
    results, mean_energy = classify_by_second(smoothed_rms, sr)

    print(f"Overall mean energy: {mean_energy:.4f}\n")

    for sec, avg_energy, label in results:
        print(f"{format_time(sec)}  |  Energy: {avg_energy:.4f}  |  {label}")