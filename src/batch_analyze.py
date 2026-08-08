import os
import csv
import numpy as np
from audio_utils import (
    compute_rms_streaming,
    smooth_energy,
    frame_to_time,
    format_time,
    find_audio_files,
)
from peaks import find_energy_peaks


def analyze_file(file_path):
    """
    Runs the full pipeline on a single audio file and returns a results dict.
    Uses streaming RMS computation, so this works for files of any length
    without loading the whole waveform into memory.
    """
    rms, sr = compute_rms_streaming(file_path)
    smoothed_rms = smooth_energy(rms)
    peak_indices, valley_indices = find_energy_peaks(smoothed_rms, sr)

    peaks = [(format_time(frame_to_time(i, sr)), float(smoothed_rms[i])) for i in peak_indices]
    valleys = [(format_time(frame_to_time(i, sr)), float(smoothed_rms[i])) for i in valley_indices]

    duration = frame_to_time(len(smoothed_rms), sr)

    return {
        "file": file_path,
        "duration": duration,
        "mean_energy": float(np.mean(smoothed_rms)) if len(smoothed_rms) else 0.0,
        "peaks": peaks,
        "valleys": valleys,
    }


def analyze_folder(folder_path="data", extensions=(".mp3", ".wav"), show_progress=True):
    """
    Runs analyze_file() on every audio file under folder_path (including
    subfolders — see find_audio_files). Scales to large batches because:
      - each file is streamed from disk, never fully loaded into RAM
      - one broken file (corrupt/unsupported) is skipped, not fatal
      - progress is shown via tqdm so long runs (thousands of files)
        give live feedback instead of looking frozen
    """
    try:
        from tqdm import tqdm
        file_iter = tqdm(find_audio_files(folder_path, extensions), desc="Analyzing") if show_progress \
            else find_audio_files(folder_path, extensions)
    except ImportError:
        file_iter = find_audio_files(folder_path, extensions)

    results = []
    for file_path in file_iter:
        try:
            result = analyze_file(file_path)
            results.append(result)
        except Exception as e:
            print(f"  Skipped {file_path} — error: {e}")
    return results


def save_summary_csv(results, output_path="outputs/summary.csv"):
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "duration", "mean_energy", "num_peaks", "num_valleys"])
        for res in results:
            writer.writerow([
                res["file"],
                format_time(res["duration"]),
                round(res["mean_energy"], 4),
                len(res["peaks"]),
                len(res["valleys"]),
            ])
    print(f"Saved summary to {output_path}")


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)

    all_results = analyze_folder("data")

    print(f"\nAnalyzed {len(all_results)} file(s)\n")
    for res in all_results:
        print(f"{res['file']}")
        print(f"   Duration: {format_time(res['duration'])}")
        print(f"   Mean energy: {res['mean_energy']:.4f}")
        print(f"   Loudest: {res['peaks'][0] if res['peaks'] else 'none'}")
        print(f"   Quietest: {res['valleys'][0] if res['valleys'] else 'none'}")

    save_summary_csv(all_results)