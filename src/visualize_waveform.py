import matplotlib.pyplot as plt
import numpy as np
from load_audio import load_audio

def plot_waveform(y, sr):
    """
    Plots the raw audio waveform over time.
    """
    time_axis = np.linspace(0, len(y) / sr, num=len(y))

    plt.figure(figsize=(14, 4))
    plt.plot(time_axis, y, linewidth=0.5)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Raw Audio Waveform")
    plt.tight_layout()
    plt.savefig("outputs/waveform.png")  # saves the plot as an image
    plt.show()

if __name__ == "__main__":
    file_path = "data/data.mp3"  # match whatever your real filename is
    y, sr = load_audio(file_path)
    plot_waveform(y, sr)