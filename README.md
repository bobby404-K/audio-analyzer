# 🎧 Waveform — Audio Energy Analyzer

A digital signal processing project that analyzes audio files and identifies their loudest and quietest moments — built from scratch with **NumPy**, with no pre-trained models or external ML APIs. It streams files from disk rather than loading them fully into memory, so it scales from a single track to large batches of files without running out of RAM.

Given one or more audio files, it computes an energy curve over time, smooths it, detects the sections that hit hardest and the sections that go quiet, and produces both a numeric summary and visual plots for each file.

---


## What it does

- Loads any local MP3/WAV audio file and converts it into a raw waveform array
- Computes **RMS (Root Mean Square) energy** over short sliding windows to measure loudness/intensity over time
- Smooths the energy signal with a moving average to remove noisy, single-frame spikes
- Detects **peaks** (loud moments) and **valleys** (quiet moments) using threshold-based local extrema detection
- Converts every detected moment into a real timestamp (`mm:ss`)
- Visualizes the full energy curve, with peaks and valleys clearly marked against the audio's mean energy line

--- 

## How it works

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

## Example output

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

## Tech stack

- **Python** — core language
- **NumPy** — all signal processing math (RMS calculation, smoothing, thresholding)
- **librosa** — audio file loading/decoding
- **Matplotlib** — waveform and energy visualization
- **SciPy** — peak detection utilities

---

## Project structure

```
audio-energy-analyzer/
├── data/                       # put your audio files here (.mp3 / .wav)
├── outputs/                    # all results are saved here automatically
├── src/
│   ├── audio_utils.py          # shared toolbox — used by every other file
│   ├── load_audio.py           # quick "does this file open?" smoke test
│   ├── energy.py               # per-file loudest/quietest summary
│   ├── peaks.py                # peak & valley (loud/quiet section) detection
│   ├── visualize_waveform.py   # saves a raw waveform image per file
│   ├── visualize_energy.py     # saves an annotated energy-curve image per file
│   ├── batch_analyze.py        # runs the full analysis across all files → CSV
│   └── main.py                 # runs EVERYTHING in one command
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

**1. Clone/open the project and create a virtual environment**

```bash
cd audio-energy-analyzer
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Add audio files**
Drop `.mp3` or `.wav` files into the `data/` folder. Subfolders are supported too (e.g. `data/podcast/`, `data/music/`) — every script finds files recursively.

---

## ▶️ How to run it

### Option A — run everything at once (recommended)

```bash
python src/main.py
```

This runs the full pipeline — energy analysis, CSV summary, waveform plots, and energy plots — for every file in `data/`, in one command.

### Option B — run individual steps

```bash
python src/load_audio.py          # quick smoke test — do all files open OK?
python src/energy.py              # print loudest/quietest moment per file
python src/peaks.py               # print all detected peaks & valleys per file
python src/visualize_waveform.py  # save raw waveform image per file
python src/visualize_energy.py    # save annotated energy plot per file
python src/batch_analyze.py       # run full analysis + save summary.csv
```

Always run these from the project root (`audio-energy-analyzer/`), not from inside `src/`.

**Optional:** `visualize_waveform.py` and `visualize_energy.py` accept a `show` argument to display an interactive window instead of saving images — use this only for testing a single file, since it pauses on every file until the window is closed.

---

## 🧩 What each file does

| File                        | Purpose |
| --------------------------- | ------- |
| `audio_utils.py`            | Shared toolbox for streaming RMS calculation, smoothing, timestamp conversion, and recursive file scanning.
| `load_audio.py`             | Fast sanity check to confirm every file in `data/` can be opened and decoded.
| `energy.py`                 | Computes RMS energy for the full audio file and prints the loudest and quietest moments.
| `peaks.py`                  | Detects every significant loud section (peak) and quiet section (valley) across the file.
| `visualize_waveform.py`     | Saves a raw waveform image for each file.
| `visualize_energy.py`       | Saves an annotated energy curve with peaks, valleys, and mean energy markers.
| `batch_analyze.py`          | Runs the full analysis across all files and exports `summary.csv`.
| `main.py`                   | Convenience entry point that runs the full pipeline in one command.

---

## 📊 Understanding the output

Everything is saved into `outputs/`:

```
outputs/
├── summary.csv
├── data1_waveform.png
├── data1_energy_plot.png
├── data2_waveform.png
├── data2_energy_plot.png
└── ...
```

### `summary.csv`

One row per audio file:

| Column        | Meaning |
| ------------- | ------- |
| `file`        | Path to the analyzed file |
| `duration`    | Total length of the audio (`mm:ss` or `h:mm:ss`) |
| `mean_energy` | The file's average loudness (RMS) across its full length |
| `num_peaks`   | Number of distinct loud sections detected |
| `num_valleys` | Number of distinct quiet sections detected |

### `*_waveform.png`

The raw amplitude waveform over time. Taller sections are louder; flatter sections are quieter.

### `*_energy_plot.png`

The smoothed energy curve with:

- Blue line: energy over time
- Dashed gray line: mean energy
- Red triangles: detected peaks
- Green triangles: detected valleys

```
audio-energy-analyzer/
│
<<<<<<< HEAD
├── data/                       # put your audio files here (.mp3 / .wav)
├── outputs/                    # all results are saved here automatically
├── src/
│   ├── audio_utils.py          # shared toolbox — used by every other file
│   ├── load_audio.py           # quick "does this file open?" smoke test
│   ├── energy.py                # per-file loudest/quietest summary
│   ├── peaks.py                  # peak & valley (loud/quiet section) detection
│   ├── visualize_waveform.py     # saves a raw waveform image per file
│   ├── visualize_energy.py       # saves an annotated energy-curve image per file
│   ├── batch_analyze.py           # runs the full analysis across all files → CSV
│   └── main.py                     # runs EVERYTHING in one command
=======
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
>>>>>>> origin/main
├── requirements.txt
└── README.md
```

---

<<<<<<< HEAD
## ⚙️ Setup

**1. Clone/open the project and create a virtual environment**

```bash
cd audio-energy-analyzer
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Add audio files**
Drop `.mp3` or `.wav` files into the `data/` folder. Subfolders are supported too (e.g. `data/podcast/`, `data/music/`) — every script finds files recursively.

---

## ▶️ How to run it

### Option A — run everything at once (recommended)

```bash
python src/main.py
```

This runs the full pipeline — energy analysis, CSV summary, waveform plots, and energy plots — for every file in `data/`, in one command. Progress bars show live status as it works through however many files you have.

### Option B — run individual steps

Useful if you only want one piece of the pipeline (e.g. just the CSV, or just the plots), or want to debug one stage at a time.

```bash
python src/load_audio.py          # quick smoke test — do all files open OK?
python src/energy.py              # print loudest/quietest moment per file
python src/peaks.py               # print all detected peaks & valleys per file
python src/visualize_waveform.py  # save raw waveform image per file
python src/visualize_energy.py    # save annotated energy plot per file
python src/batch_analyze.py       # run full analysis + save summary.csv
```

Always run these from the project root (`audio-energy-analyzer/`), not from inside `src/`.

**Optional:** `visualize_waveform.py` and `visualize_energy.py` accept a `show` argument to pop up an interactive window per plot instead of just saving silently — only recommended when testing a single file, since it pauses on every file until the window is closed:

```bash
python src/visualize_waveform.py show
=======
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
>>>>>>> origin/main
```

---

<<<<<<< HEAD
## 🧩 What each file does

| File                        | Purpose                                                                                                                                                                                                                                                          |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`audio_utils.py`**        | Shared toolbox, not run directly. Contains the core streaming RMS calculation, smoothing, timestamp conversion, and the folder-scanning function every other script relies on. One implementation, reused everywhere, so fixes only need to happen in one place. |
| **`load_audio.py`**         | A fast sanity check — confirms every file in `data/` can actually be opened and decoded (loads only the first 30 seconds per file, capped intentionally for speed). Good for catching corrupt/unsupported files early.                                           |
| **`energy.py`**             | Computes RMS energy for the _entire_ length of each file (streamed, no cap) and prints the single loudest and single quietest moment, with timestamps.                                                                                                           |
| **`peaks.py`**              | Goes further than `energy.py` — detects _every_ significant loud section (peak) and quiet section (valley) across the whole file, not just the single overall max/min. Also reports how many seconds of the track sit above vs. below the average energy.        |
| **`visualize_waveform.py`** | Saves an image of the raw audio waveform (amplitude over time) for each file — shows the file's overall shape at a glance.                                                                                                                                       |
| **`visualize_energy.py`**   | Saves an image of the smoothed energy curve for each file, with peaks marked in red, valleys marked in green, and a dashed line showing the average energy.                                                                                                      |
| **`batch_analyze.py`**      | Runs the complete energy + peak/valley analysis across every file and exports a single `summary.csv` — the best option when you want to compare many files side by side.                                                                                         |
| **`main.py`**               | Convenience entry point — runs `batch_analyze.py` and both visualization scripts together in one command, so you don't have to run five scripts separately.                                                                                                      |

---

## 📊 Understanding the output

Everything gets saved into `outputs/`:

```
outputs/
├── summary.csv
├── data1_waveform.png
├── data1_energy_plot.png
├── data2_waveform.png
├── data2_energy_plot.png
└── ...
```

### `summary.csv`

One row per audio file:

| Column        | Meaning                                                                                             |
| ------------- | --------------------------------------------------------------------------------------------------- |
| `file`        | Path to the analyzed file                                                                           |
| `duration`    | Total length of the audio (`mm:ss` or `h:mm:ss`)                                                    |
| `mean_energy` | The file's average loudness (RMS) across its full length — higher = generally louder/denser overall |
| `num_peaks`   | How many distinct loud sections were detected (e.g. choruses, drops, loud passages)                 |
| `num_valleys` | How many distinct quiet sections were detected (e.g. intros, breakdowns, silences)                  |

Use this file to quickly compare loudness/dynamics across many tracks — e.g. sort by `mean_energy` to find your loudest file, or by `num_peaks` to find the most dynamically varied one.

### `*_waveform.png`

The raw shape of the audio's amplitude over time. Denser/taller sections are louder; flatter, thinner sections are quieter. This is the "before" view — unprocessed, noisy, useful for a quick visual gut-check of the file's structure.

### `*_energy_plot.png`

The refined, smoothed version of the analysis:

- **Blue line** — the audio's energy (loudness) over time, smoothed to remove noise
- **Dashed gray line** — the file's overall mean energy, used as the reference threshold
- **Red triangles** — detected **peaks**: sustained loud moments (choruses, drops, climactic sections)
- **Green triangles** — detected **valleys**: sustained quiet moments (intros, breakdowns, quiet passages)

This is the main "answer" of the project — at a glance, it shows exactly where a track hits hardest and where it goes quiet.

### Console output (when running `energy.py` / `peaks.py` directly)

- **`energy.py`** prints just the single loudest and quietest timestamp per file — a quick headline number.
- **`peaks.py`** prints a fuller breakdown: total peak/valley counts, how many seconds of the track sit above vs. below average energy, and the timestamp of the single loudest peak and quietest valley.

---

## 🛠️ Tech stack

- **Python** — core language
- **NumPy** — RMS calculation, smoothing, thresholding, all core signal-processing math
- **SciPy** — peak/valley detection
- **soundfile** — streaming audio reads directly from disk (constant memory usage regardless of file length)
- **librosa** — used only in `load_audio.py` for the quick smoke test
- **Matplotlib** — waveform and energy visualizations
- **tqdm** — progress bars across batches of files

---

## 💡 Notes on scaling

The pipeline is built to comfortably handle large batches (tested against 50+ files, designed to scale into the thousands):

- Audio is streamed from disk in chunks — memory use stays constant regardless of file length or count
- Plotting runs headless (no pop-up windows), so nothing blocks or requires manual interaction across a large batch
- One broken/corrupt file is skipped with a message rather than stopping the whole run
- `find_audio_files()` scans subfolders too, so files can be organized into categories without any code changes

---

## 📄 License

MIT — free to use, modify, and build on:)
=======
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
i don't know to add live feature.

##  License

MIT — free to use:), modify, and build on.
>>>>>>> origin/main
