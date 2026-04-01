# The Empathy Engine

A Python web service that detects the dominant emotion in text using a HuggingFace transformer model, maps it to vocal parameters, and returns an emotionally-modulated MP3 speech file. The service bridges the gap between text-based sentiment and expressive, human-like audio output. A single-page web UI lets you demo the pipeline interactively in your browser.

---

## Setup

1. Clone the repo:
   ```bash
   git clone <repo-url>
   ```

2. Enter the project directory:
   ```bash
   cd empathy-engine
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

5. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Install ffmpeg:
   - Windows: `choco install ffmpeg` or download from https://ffmpeg.org
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

> **Note:** On first run, ~500 MB of HuggingFace model weights will be downloaded automatically.

---

## How to Run

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Emotion → Voice Mapping

The following table shows the vocal parameters applied at full intensity (intensity = 1.0). At lower intensities each delta is scaled proportionally.

| Emotion  | Rate | Pitch (semitones) | Volume (dB) |
|----------|------|-------------------|-------------|
| joy      | 1.20 | +2                | +3          |
| sadness  | 0.75 | -3                | -4          |
| anger    | 1.15 | +1                | +5          |
| fear     | 1.10 | +3                | -2          |
| disgust  | 0.90 | -1                | 0           |
| surprise | 1.30 | +4                | +4          |
| neutral  | 1.00 | 0                 | 0           |

---

## Design Choices

### Intensity Scaling

Each vocal parameter delta is multiplied by the model's confidence score (intensity). At intensity = 1.0 you get the full effect; at intensity = 0.5 you get half the modulation. This means a weakly-detected emotion produces subtle changes while a high-confidence detection produces strong modulation.

For example, `joy` at intensity 0.5 yields a rate of `1.0 + (0.20 * 0.5) = 1.10` rather than the full `1.20`.

### Pitch Shift Method

Pitch is shifted using pydub's frame rate trick — the audio's frame rate is resampled to a new value computed as:

```python
new_frame_rate = int(original_frame_rate * (2 ** (semitones / 12.0)))
```

This shifts pitch without changing duration (when combined with the subsequent `set_frame_rate(44100)` call to normalise playback speed).
