import numpy as np
from load_audio import load_audio


def compute_rms(y, frame_length=2048, hop_length=512):
    """
    Computes RMS (Root Mean Square) energy over short windows of the waveform.
    frame_length = number of samples per window
    hop_length   = how far the window slides each step (overlap control)
    """
    num_frames = 1 + (len(y) - frame_length) // hop_length
    rms_values = np.zeros(num_frames)

    for i in range(num_frames):
        start = i * hop_length
        end = start + frame_length
        frame = y[start:end]
        rms_values[i] = np.sqrt(np.mean(frame ** 2))

    return rms_values


def smooth_energy(rms, window_size=5):
    """
    Smooths the RMS energy curve using a simple moving average.
    window_size = how many neighboring frames to average together
    """
    kernel = np.ones(window_size) / window_size
    smoothed = np.convolve(rms, kernel, mode='same')
    return smoothed


def frame_to_time(frame_index, sr, hop_length=512):
    """
    Converts an RMS frame index into a real timestamp (seconds).
    """
    return (frame_index * hop_length) / sr


def format_time(seconds):
    """
    Converts seconds into a MM:SS string.
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


if __name__ == "__main__":
    file_path = "data/data.mp3"
    y, sr = load_audio(file_path)

    rms = compute_rms(y)
    smoothed_rms = smooth_energy(rms)

    print("Number of RMS frames:", len(rms))
    print("Min RMS (raw):", rms.min())
    print("Max RMS (raw):", rms.max())

    # Use SMOOTHED values from here on
    min_frame = np.argmin(smoothed_rms)
    max_frame = np.argmax(smoothed_rms)

    min_time = frame_to_time(min_frame, sr)
    max_time = frame_to_time(max_frame, sr)

    print(f"\nQuietest moment (smoothed): {format_time(min_time)} (RMS = {smoothed_rms[min_frame]:.4f})")
    print(f"Loudest moment (smoothed):  {format_time(max_time)} (RMS = {smoothed_rms[max_frame]:.4f})")