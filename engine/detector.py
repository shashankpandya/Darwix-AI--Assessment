"""
Emotion detector using the j-hartmann/emotion-english-distilroberta-base model.

The pipeline is loaded once at module import time and reused across all calls.
Valid emotion labels: joy, sadness, anger, fear, disgust, surprise, neutral
"""

from transformers import pipeline

# Load the model pipeline once at module import time (Requirement 1.5)
_pipeline = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=1,
)


def detect(text: str) -> tuple[str, float]:
    """
    Classify the dominant emotion in `text`.

    Returns a tuple of (emotion_label, intensity) where:
      - emotion_label is one of: joy, sadness, anger, fear, disgust, surprise, neutral
      - intensity is a float in [0.0, 1.0] representing the model's confidence score

    Raises:
        ValueError: if `text` is empty or whitespace-only
    """
    if not text or not text.strip():
        raise ValueError(
            "text must be non-empty: received an empty or whitespace-only string"
        )

    # pipeline returns a list of lists when top_k=1: [[{'label': ..., 'score': ...}]]
    results = _pipeline(text)
    top = results[0][0]

    label: str = top["label"].lower()
    score: float = float(top["score"])

    return (label, score)
