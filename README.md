#  Waveform — Audio Energy Analyzer

A digital signal processing project that analyzes any audio file and identifies its loudest and quietest moments — built from scratch with **NumPy**, with no pre-trained models or external ML APIs.

Given an audio file, it computes an energy curve over time, smooths it, and detects the sections that hit hardest (peaks/drops) and the sections that go quiet (breakdowns/lulls) — then visualizes the result.

---

##  What it does

- Loads any local MP3/WAV audio file and converts it into a raw waveform array
- Computes **RMS (Root Mean Square) energy** over short sliding windows to measure loudness/intensity over time
- Smooths the energy signal with a moving average to remove noisy, single-frame spikes
- Detects **peaks** (loud moments) and **valleys** (quiet moments) using threshold-based local extrema detection
- Converts every detected moment into a real timestamp (`mm:ss`)
- Visualizes the full energy curve, with peaks and valleys clearly marked against the audio's mean energy line

---

##  How it works

| Stage | What happens |
|-------|-------------|
| 1. Load audio | Read the MP3/WAV into a NumPy waveform array using `librosa` |
| 2. Visualize raw waveform | Plot the raw amplitude signal to understand the audio's shape |
| 3. Compute RMS energy | Slide a window across the waveform, calculating loudness per window |
| 4. Smooth the signal | Apply a moving average to turn noisy energy readings into a clean curve |
| 5. Detect peaks & valleys | Flag sustained sections above/below a statistical threshold (mean ± scaled standard deviation) |
| 6. Visualize results | Plot the final energy curve with peaks, valleys, and the mean line marked |

This mirrors how real audio-engineering tools measure loudness dynamics, implemented from first principles rather than using a black-box library.

---

##  Example output

Running the analyzer on an audio file produces output like:

```
Overall mean energy: 0.0870

Found 4 peaks (loud moments):
  0:45  (RMS = 0.28)
  1:32  (RMS = 0.31)
  2:14  (RMS = 0.29)
  3:01  (RMS = 0.27)

Found 3 valleys (quiet moments):
  0:03  (RMS = 0.008)
  1:58  (RMS = 0.012)
  2:50  (RMS = 0.015)
```

along with a plotted energy graph (`outputs/energy_plot.png`) showing the audio's dynamic shape at a glance.

---

##  Tech stack

- **Python** — core language
- **NumPy** — all signal processing math (RMS calculation, smoothing, thresholding)
- **librosa** — audio file loading/decoding
- **Matplotlib** — waveform and energy visualization
- **SciPy** — peak detection utilities

---

##  Project structure

```
audio-energy-analyzer/
│
├── data/
│   └── your_audio.mp3         # audio file(s) to analyze
├── src/
│   ├── load_audio.py          # Stage 1 — load waveform
│   ├── visualize_waveform.py  # Stage 2 — plot raw waveform
│   ├── energy.py              # Stage 3-4 — RMS energy + smoothing
│   ├── peaks.py                # Stage 5 — peak/valley detection
│   └── visualize_energy.py     # Stage 6 — final annotated plot
├── outputs/
│   └── energy_plot.png        # saved result plots
├── requirements.txt
└── README.md
```

---

##  Getting started

**1. Clone and set up the environment**
```bash
git clone https://github.com/yourusername/audio-energy-analyzer.git
cd audio-energy-analyzer
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Add an audio file**
Place an MP3/WAV file in the `data/` folder.

**3. Run the pipeline**
```bash
python src/load_audio.py
python src/visualize_waveform.py
python src/energy.py
python src/peaks.py
python src/visualize_energy.py
```

---

##  What this project demonstrates

- Applying signal processing fundamentals (RMS, moving averages, threshold-based peak detection) without relying on pre-built "energy analysis" libraries
- Working directly with raw waveform data using vectorized NumPy operations instead of explicit loops
- End-to-end thinking: from raw audio bytes → numerical analysis → human-readable, visual output

---

##  Possible extensions

- Detect tempo/BPM alongside energy
- Compare energy curves across multiple audio files or genres
- Export detected peak/valley timestamps as a shareable JSON or CSV file
- Build an interactive interface for uploading and visualizing results

---

##  License

MIT — free to use:), modify, and build on.
