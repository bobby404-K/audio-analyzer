"""
Single entry point that runs the entire pipeline — batch analysis, CSV
summary, waveform plots, and energy plots — across every audio file in
data/ (including subfolders), in one command:

    python src/main.py

Handles 50, 500, 5000+ files the same way: streamed RMS (constant memory
per file), headless plotting (no blocking windows), tqdm progress bars,
and per-file error handling so one bad file doesn't stop the whole batch.
"""

import os
from batch_analyze import analyze_folder, save_summary_csv
from visualize_waveform import compute_waveform_envelope, plot_waveform
from visualize_energy import plot_energy
from audio_utils import compute_rms_streaming, smooth_energy, find_audio_files
from peaks import find_energy_peaks

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable


def run_pipeline(data_folder="data", output_folder="outputs", make_plots=True):
    os.makedirs(output_folder, exist_ok=True)

    print("Step 1/2 — analyzing energy for every file...")
    results = analyze_folder(data_folder)
    save_summary_csv(results, os.path.join(output_folder, "summary.csv"))

    if not make_plots:
        return results

    print("\nStep 2/2 — generating waveform + energy plots...")
    for file_path in tqdm(find_audio_files(data_folder), desc="Plotting"):
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        try:
            time_axis, mins, maxs, sr, duration = compute_waveform_envelope(file_path)
            plot_waveform(time_axis, mins, maxs,
                           os.path.join(output_folder, f"{base_name}_waveform.png"))

            rms, sr = compute_rms_streaming(file_path)
            smoothed_rms = smooth_energy(rms)
            peak_indices, valley_indices = find_energy_peaks(smoothed_rms, sr)
            plot_energy(smoothed_rms, sr, peak_indices, valley_indices,
                        os.path.join(output_folder, f"{base_name}_energy_plot.png"))
        except Exception as e:
            print(f"  Skipped plots for {file_path} — error: {e}")

    return results


if __name__ == "__main__":
    results = run_pipeline()
    print(f"\nAll done — {len(results)} file(s) analyzed. See '{os.path.abspath('outputs')}/'")