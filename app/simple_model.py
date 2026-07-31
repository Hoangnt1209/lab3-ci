"""
Pure-Python fallback model for movie rating prediction.
"""

from dataclasses import dataclass
import hashlib


@dataclass(frozen=True)
class Prediction:
    """Lightweight prediction object compatible with Surprise-style usage."""

    uid: str
    iid: str
    est: float


class BaselineRatingModel:
    """Deterministic fallback model that produces ratings in the 1-5 range."""

    def fit(self, *_args, **_kwargs):
        """Keep the training API stable even though this model is rule-based."""
        return self

    def predict(self, user_id: str, movie_id: str) -> Prediction:
        """Return a repeatable pseudo-prediction for a user/movie pair."""
        payload = f"{user_id}:{movie_id}".encode("utf-8")
        digest = hashlib.sha256(payload).hexdigest()
        score = 1.0 + (int(digest[:8], 16) % 400) / 100
        return Prediction(uid=str(user_id), iid=str(movie_id), est=round(score, 2))