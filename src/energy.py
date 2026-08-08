from audio_utils import (
    compute_rms_streaming,
    smooth_energy,
    frame_to_time,
    format_time,
    find_audio_files,
)
import numpy as np

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

    for file_path in tqdm(audio_files, desc="Computing RMS energy"):
        try:
            rms, sr = compute_rms_streaming(file_path)
            smoothed_rms = smooth_energy(rms)

            min_frame = np.argmin(smoothed_rms)
            max_frame = np.argmax(smoothed_rms)
            min_time = frame_to_time(min_frame, sr)
            max_time = frame_to_time(max_frame, sr)

            print(f"\n{file_path}")
            print(f"  Frames: {len(rms)}")
            print(f"  Quietest moment: {format_time(min_time)} (RMS = {smoothed_rms[min_frame]:.4f})")
            print(f"  Loudest moment:  {format_time(max_time)} (RMS = {smoothed_rms[max_frame]:.4f})")
        except Exception as e:
            print(f"  Skipped {file_path} — error: {e}")