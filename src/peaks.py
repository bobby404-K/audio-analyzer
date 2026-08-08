import numpy as np
from scipy.signal import find_peaks
from audio_utils import (
    compute_rms_streaming,
    smooth_energy,
    frame_to_time,
    format_time,
    find_audio_files,
)


def find_energy_peaks(smoothed_rms, sr, hop_length=512, distance_seconds=5, prominence=0.02):
    """
    Finds peaks (loud moments) and valleys (quiet moments) in the energy curve
    using local maxima/minima detection.
    """
    distance_frames = int((distance_seconds * sr) / hop_length)

    peak_indices, _ = find_peaks(smoothed_rms, distance=distance_frames, prominence=prominence)
    valley_indices, _ = find_peaks(-smoothed_rms, distance=distance_frames, prominence=prominence)

    return peak_indices, valley_indices


def classify_by_second(smoothed_rms, sr, hop_length=512):
    """
    Groups energy values into 1-second buckets, then classifies each second
    as 'PEAK' (above overall mean) or 'valley' (below overall mean).

    Returns the full per-second list (for anyone who wants it programmatically)
    plus a compact summary — the __main__ block below only prints the summary,
    since printing one line per second becomes unreadable once you're running
    this across hundreds/thousands of files.
    """
    frames_per_second = int(sr / hop_length)
    if frames_per_second == 0 or len(smoothed_rms) == 0:
        return [], 0.0

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
    try:
        from tqdm import tqdm
    except ImportError:
        def tqdm(iterable, **kwargs):
            return iterable

    data_folder = "data"
    audio_files = find_audio_files(data_folder)

    if not audio_files:
        print(f"No audio files found in '{data_folder}/'")

    for file_path in tqdm(audio_files, desc="Analyzing peaks/valleys"):
        try:
            rms, sr = compute_rms_streaming(file_path)
            smoothed_rms = smooth_energy(rms)

            peak_indices, valley_indices = find_energy_peaks(smoothed_rms, sr)
            results, mean_energy = classify_by_second(smoothed_rms, sr)
            peak_seconds = sum(1 for _, _, label in results if label == "PEAK")
            valley_seconds = len(results) - peak_seconds

            print(f"\n{file_path}")
            print(f"  Mean energy: {mean_energy:.4f}")
            print(f"  Local peaks: {len(peak_indices)}   Local valleys: {len(valley_indices)}")
            print(f"  Seconds above mean (PEAK): {peak_seconds}   below mean (valley): {valley_seconds}")

            if len(peak_indices):
                loudest = peak_indices[np.argmax(smoothed_rms[peak_indices])]
                print(f"  Loudest peak: {format_time(frame_to_time(loudest, sr))} "
                      f"(RMS = {smoothed_rms[loudest]:.4f})")
            if len(valley_indices):
                quietest = valley_indices[np.argmin(smoothed_rms[valley_indices])]
                print(f"  Quietest valley: {format_time(frame_to_time(quietest, sr))} "
                      f"(RMS = {smoothed_rms[quietest]:.4f})")
        except Exception as e:
            print(f"  Skipped {file_path} — error: {e}")