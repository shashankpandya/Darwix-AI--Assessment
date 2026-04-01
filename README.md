---
Live Demo: https://huggingface.co/spaces/shashankpandya/empathy-engine
---

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

Then open [http://localhost:7860](http://localhost:7860) in your browser.

> To use port 5000 locally instead: `PORT=5000 python app.py`

---

## Emotion → Voice Mapping

The following table shows the vocal parameters applied at full intensity (intensity = 1.0). At lower intensities each value is linearly interpolated from the neutral baseline.

| Emotion  | Rate | Pitch (semitones) | Volume (dB) |
|----------|------|-------------------|-------------|
| joy      | 1.25 | +3                | +4          |
| sadness  | 0.72 | -3                | -4          |
| anger    | 1.35 | +2                | +6          |
| fear     | 1.18 | +4                | -3          |
| disgust  | 0.85 | -2                | -3          |
| surprise | 1.38 | +5                | +4          |
| neutral  | 1.00 |  0                |  0          |

---

## Design Choices

### Intensity Scaling

Each vocal parameter is linearly interpolated from the neutral baseline (rate=1.0, pitch=0, volume=0) toward the emotion's target value, scaled by the model's confidence score (intensity). At intensity=1.0 you get the full effect; at intensity=0.5 you get halfway between neutral and the target.

Example: joy at intensity=0.5 → rate = 1.0 + (1.25 - 1.0) × 0.5 = 1.125

### Pitch Shift + Rate Method

Rate and pitch are combined into a **single frame-rate multiplication** to avoid the distortion caused by two sequential resamples:

```python
rate_multiplier = rate * (2 ** (semitones / 12.0))
new_frame_rate  = int(original_frame_rate * rate_multiplier)
audio = audio._spawn(raw_data, overrides={'frame_rate': new_frame_rate})
audio = audio.set_frame_rate(44100)
```

Applying both in one pass produces cleaner, more natural-sounding output than chaining separate rate and pitch operations.
