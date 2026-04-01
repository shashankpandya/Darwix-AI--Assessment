# BASE_MAP stores absolute target values at full intensity (intensity = 1.0).
# Neutral baseline: rate=1.0, pitch=0, volume_db=0.
# Each param is linearly interpolated from the neutral baseline toward the
# target value, scaled by the model's confidence score (intensity).
#
# Tuning notes:
# - Rate and pitch are now combined in a single frame-rate pass in tts.py,
#   so values here represent the true perceptual target without compensation.
# - Volume deltas are kept moderate — gTTS output is already normalised,
#   so large boosts clip and large cuts become inaudible.
BASE_MAP: dict[str, dict] = {
    "joy":      {"rate": 1.25, "pitch":  3, "volume_db":  4},
    "sadness":  {"rate": 0.72, "pitch": -3, "volume_db": -4},
    "anger":    {"rate": 1.35, "pitch":  2, "volume_db":  6},
    "fear":     {"rate": 1.18, "pitch":  4, "volume_db": -3},
    "disgust":  {"rate": 0.85, "pitch": -2, "volume_db": -3},
    "surprise": {"rate": 1.38, "pitch":  5, "volume_db":  4},
    "neutral":  {"rate": 1.00, "pitch":  0, "volume_db":  0},
}

EMOTIONS: list[str] = list(BASE_MAP.keys())

# Neutral baseline used for interpolation
_NEUTRAL = {"rate": 1.0, "pitch": 0, "volume_db": 0}


def get_params(emotion: str, intensity: float) -> dict:
    """
    Returns {'rate': float, 'pitch': int, 'volume_db': int}.

    Each parameter is linearly interpolated from the neutral baseline toward
    the emotion's target value, scaled by intensity (model confidence score).

    Example: joy at intensity=0.5
      rate      = 1.0 + (1.25 - 1.0) * 0.5 = 1.125
      pitch     = round(0 + (3 - 0) * 0.5)  = 2
      volume_db = round(0 + (4 - 0) * 0.5)  = 2

    Falls back to neutral params for unknown emotion labels.
    """
    target = BASE_MAP.get(emotion, BASE_MAP["neutral"])
    return {
        "rate":      _NEUTRAL["rate"]      + (target["rate"]      - _NEUTRAL["rate"])      * intensity,
        "pitch":     round(_NEUTRAL["pitch"]     + (target["pitch"]     - _NEUTRAL["pitch"])     * intensity),
        "volume_db": round(_NEUTRAL["volume_db"] + (target["volume_db"] - _NEUTRAL["volume_db"]) * intensity),
    }
