"""
Shared audio analysis utilities.

Previously, compute_rms_streaming() / smooth_energy() / frame_to_time() /
format_time() were copy-pasted into energy.py, peaks.py, visualize_energy.py,
and visualize_waveform.py. Every file now imports from here instead — one
implementation, one place to fix bugs, and no risk of the copies drifting
out of sync as the project grows.
"""

import numpy as np
import soundfile as sf
from numpy.lib.stride_tricks import sliding_window_view


def compute_rms_streaming(file_path, frame_length=2048, hop_length=512, block_size=2_000_000):
    """
    Computes RMS energy by reading the audio file in chunks from disk,
    instead of loading the entire waveform into memory first.

    Each chunk is combined with a small 'carry-over' from the previous
    chunk (frame_length - hop_length samples) so sliding windows stay
    continuous across chunk boundaries. Works for files of any length —
    minutes or many hours — with a small, fixed memory footprint. This
    is what lets the project scale to large batches (hundreds or
    thousands of files) without running out of RAM.
    """
    with sf.SoundFile(file_path) as f:
        sr = f.samplerate
        channels = f.channels

        rms_chunks = []
        carry = np.array([], dtype="float32")

        while True:
            block = f.read(block_size, dtype="float32", always_2d=False)
            if len(block) == 0:
                break

            if channels > 1:
                block = block.mean(axis=1)  # downmix to mono on the fly

            buf = np.concatenate([carry, block])

            if len(buf) >= frame_length:
                num_frames = 1 + (len(buf) - frame_length) // hop_length
                usable_len = frame_length + (num_frames - 1) * hop_length

                windows = sliding_window_view(buf[:usable_len], frame_length)[::hop_length]
                rms_chunks.append(np.sqrt(np.mean(windows ** 2, axis=1)))

                consumed = num_frames * hop_length
                carry = buf[consumed:]
            else:
                carry = buf

    rms = np.concatenate(rms_chunks) if rms_chunks else np.array([])
    return rms, sr


def smooth_energy(rms, window_size=5):
    """Smooths the RMS energy curve using a simple moving average."""
    if len(rms) == 0:
        return rms
    kernel = np.ones(window_size) / window_size
    return np.convolve(rms, kernel, mode="same")


def frame_to_time(frame_index, sr, hop_length=512):
    """Converts an RMS frame index into a real timestamp (seconds)."""
    return (frame_index * hop_length) / sr


def format_time(seconds):
    """Converts seconds into a timestamp string (H:MM:SS if over an hour, else MM:SS)."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def find_audio_files(folder_path="data", extensions=(".mp3", ".wav"), recursive=True):
    """
    Finds every audio file under folder_path.

    recursive=True walks into subfolders too (os.walk), so you can organize
    thousands of files into subfolders — e.g. data/rock/, data/lofi/ — and
    everything still gets picked up in one run, no code changes needed.
    """
    import os

    found = []
    if recursive:
        for root, _dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.lower().endswith(extensions):
                    found.append(os.path.join(root, filename))
    else:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(extensions):
                found.append(os.path.join(folder_path, filename))
    return sorted(found)