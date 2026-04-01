BASE_MAP: dict[str, dict] = {
    "joy":      {"rate_delta": 0.20,  "pitch_delta": 2,  "volume_db_delta": 3},
    "sadness":  {"rate_delta": -0.25, "pitch_delta": -3, "volume_db_delta": -4},
    "anger":    {"rate_delta": 0.15,  "pitch_delta": 1,  "volume_db_delta": 5},
    "fear":     {"rate_delta": 0.10,  "pitch_delta": 3,  "volume_db_delta": -2},
    "disgust":  {"rate_delta": -0.10, "pitch_delta": -1, "volume_db_delta": 0},
    "surprise": {"rate_delta": 0.30,  "pitch_delta": 4,  "volume_db_delta": 4},
    "neutral":  {"rate_delta": 0.00,  "pitch_delta": 0,  "volume_db_delta": 0},
}

EMOTIONS: list[str] = list(BASE_MAP.keys())


def get_params(emotion: str, intensity: float) -> dict:
    """
    Returns {'rate': float, 'pitch': int, 'volume_db': int}.
    Falls back to neutral if emotion not in BASE_MAP.
    Each delta is scaled by intensity before being added to the neutral baseline.
    """
    entry = BASE_MAP.get(emotion, BASE_MAP["neutral"])
    return {
        "rate":      1.0 + entry["rate_delta"] * intensity,
        "pitch":     round(entry["pitch_delta"] * intensity),
        "volume_db": round(entry["volume_db_delta"] * intensity),
    }
