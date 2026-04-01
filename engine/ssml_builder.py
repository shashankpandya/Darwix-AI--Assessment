from engine.mapper import get_params


def build_ssml(text: str, emotion: str, intensity: float) -> str:
    """
    Returns a plain-string SSML document.
    Wraps content in <emphasis> based on intensity thresholds.
    No external SSML library is used.
    """
    rate_pct = int(round(get_params(emotion, intensity)["rate"] * 100))

    if intensity > 0.80:
        content = f'<emphasis level="strong">{text}</emphasis>'
    elif intensity > 0.55:
        content = f'<emphasis level="moderate">{text}</emphasis>'
    else:
        content = text

    return f'<speak><prosody rate="{rate_pct}%">{content}</prosody></speak>'
