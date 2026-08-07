import librosa
import numpy as np

def load_audio(file_path):
    """
    Loads an audio file and returns the waveform + sample rate.
    y  = waveform (NumPy array of amplitude values over time)
    sr = sample rate (how many samples represent 1 second of audio)
    """
    y, sr = librosa.load(file_path, sr=None)
    return y, sr

if __name__ == "__main__":
    file_path = "data/data.mp3" # change this to your actual filename

    y, sr = load_audio(file_path)

    print("Sample rate:", sr)
    print("Waveform shape:", y.shape)
    print("Duration (seconds):", len(y) / sr)