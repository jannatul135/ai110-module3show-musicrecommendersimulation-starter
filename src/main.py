"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

def main() -> None:
    """Load songs, recommend for each sample profile, and print the ranked results."""
    songs = load_songs("data/songs.csv")

    # profiles
    profiles = {
        "High-Energy Pop": {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.9},
        "Chill Lofi": {"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.35},
        "Deep Intense Rock": {"favorite_genre": "rock", "favorite_mood": "intense", "target_energy": 0.92},
        "Conflicting (pop, sad, 0.9)": {"favorite_genre": "pop", "favorite_mood": "sad", "target_energy": 0.9},
        "Genre Not in File (k-pop)": {"favorite_genre": "k-pop", "favorite_mood": "happy", "target_energy": 0.8},
        "Mismatched Vibe (classical, 0.95)": {"favorite_genre": "classical", "favorite_mood": "melancholic", "target_energy": 0.95},
    }

    for profile_name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n{profile_name}")
        print("=" * 40)
        print("Top recommendations")
        print("-" * 40)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} by {song['artist']}")
            print(f"   Score: {score:.2f}")
            print("   Reasons:")
            for reason in explanation.split(", "):
                print(f"     - {reason}")
            print()


if __name__ == "__main__":
    main()
