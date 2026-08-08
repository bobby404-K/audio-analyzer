# 🎧 Waveform — Audio Energy Analyzer

A digital signal processing project that analyzes audio files and identifies their loudest and quietest moments — built from scratch with **NumPy**, with no pre-trained models or external ML APIs. It streams files from disk rather than loading them fully into memory, so it scales from a single track to large batches of files without running out of RAM.

Given one or more audio files, it computes an energy curve over time, smooths it, detects the sections that hit hardest and the sections that go quiet, and produces both a numeric summary and visual plots for each file.

---

## 📁 Project structure

```
audio-energy-analyzer/
│
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
```

---

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
