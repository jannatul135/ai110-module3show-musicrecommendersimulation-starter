import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Scoring weights (baseline). The weight-shift experiment used GENRE_WEIGHT=1.0, ENERGY_WEIGHT=2.0.
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _prefs(self, user: UserProfile) -> Dict:
        """Convert a UserProfile into the dict that score_song expects."""
        return {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for a user, best first."""
        prefs = self._prefs(user)
        return sorted(
            self.songs,
            key=lambda s: score_song(prefs, asdict(s))[0],
            reverse=True,
        )[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain in one string why a song scored the way it did."""
        return ", ".join(score_song(self._prefs(user), asdict(song))[1])


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into dicts with numeric fields converted."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        songs = list(csv.DictReader(f))
    for song in songs:
        song["id"] = int(song["id"])
        song["tempo_bpm"] = int(song["tempo_bpm"])
        for key in ("energy", "valence", "danceability", "acousticness"):
            song[key] = float(song[key])
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences, returning (score, reasons).

    Score range (energy and target_energy are both in [0, 1]):
      genre match     0 or GENRE_WEIGHT  (2.0)
      mood match      0 or MOOD_WEIGHT   (1.0)
      energy points   ENERGY_WEIGHT * (1 - |song energy - target|), in [0, 1.0]
      total           0.0 to 4.0
    """
    score = 0.0
    reasons = []
    if song["genre"] == user_prefs["favorite_genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT:.1f})")
    if song["mood"] == user_prefs["favorite_mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT:.1f})")
    energy_points = ENERGY_WEIGHT * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")
    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs as (song, score, explanation) tuples, best first."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)[:k]
    return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked]