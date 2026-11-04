# 🎵 Music Recommender Simulation

## Project Summary

This project is a small content-based music recommender written in Python. It loads a catalog of songs from a CSV file, compares each song to a user's taste profile (favorite genre, favorite mood, and target energy), and gives every song a score with the reasons behind it. It then ranks the songs and prints the top recommendations in the terminal. I built it to learn how recommenders turn data into predictions and to look at where bias can show up in a simple system.

---

## How The System Works

Real-world platforms like Spotify and YouTube predict what you'll enjoy using two kinds of signals. Collaborative filtering uses user behavior (likes, skips, playlists, listening history) to find songs that people with similar habits enjoyed. Content-based filtering uses the song's own features (genre, mood, energy, tempo) to find songs that resemble what you already like. My version is content-based: it compares one user's taste profile to each song's features and prioritizes genre and mood matches, then checks how close the song's energy is to the user's target.

### What features does each `Song` use in your system?
- `genre`
- `mood`
- `energy` (0.0 to 1.0)
- `tempo_bpm` (stored in the data but not used in scoring)

### What information does your `UserProfile` store?
- `favorite_genre`
- `favorite_mood`
- `target_energy`
- The class also has a `likes_acoustic` field, but scoring doesn't use it.

### How does your `Recommender` compute a score for each song?
- Genre match: +2.0 points
- Mood match: +1.0 point
- Energy: `1 - abs(song_energy - target_energy)`, so songs closer to the user's target get more points
- Each song gets a total score plus a list of reasons, such as "genre match (+2.0)"
- The `score_song` function does this for one song, and the `Recommender` class reuses it for its `recommend` and `explain_recommendation` methods.

### How do you choose which songs to recommend?
- The system scores every song in the dataset.
- It sorts the songs from highest score to lowest score.
- It returns the top K songs as the recommendations.

### What possible biases or limitations could the system have?
- Genre is worth the most points, so it may dominate the results.
- A song from another genre could be ignored even if its mood and energy fit the user well.
- The small dataset limits the variety of recommendations.

### Data
The catalog in `data/songs.csv` has 18 songs across 15 genres (pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, hip hop, classical, drum and bass, reggaeton, r&b, metal, and afrobeat). Each song has `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. I added 8 songs to the starter's 10 so the catalog covers more genres and moods. Only `genre`, `mood`, and `energy` are used in scoring. The other columns are stored for possible future use.

### Example user profile
```python
user_prefs = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8}
```
This profile can separate "intense rock" from "chill lofi" because the two groups differ in genre, mood, and energy. It is weaker at telling apart songs that are close to each other, such as Storm Runner (rock) and Gym Hero (pop), where genre is the only real difference.

### Algorithm Recipe
For every song:
1. Genre matches the user's favorite genre: **+2.0**
2. Mood matches the user's favorite mood: **+1.0**
3. Energy closeness: **`1 - abs(song_energy - target_energy)`**, which gives up to **+1.0**. A song exactly at the target gets 1.0, and the farther away it is, the less it gets.
4. Add the points together (maximum **4.0**) and save a reason for each part, such as "genre match (+2.0)".

### Data flow
**Input** (user preferences) → **Process** (loop over every song in the CSV and call `score_song`) → **Output** (sort by score, return the top K with their reasons)

### Expected biases
- Genre match is worth 2 points and mood only 1, so a mood-and-energy match can never beat a genre-only match. For example, with a pop/happy profile, Gym Hero (pop, intense) is expected to rank above Rooftop Lights (indie pop, happy) because "indie pop" gets no genre credit. I confirmed this in my tests.
- Genre and mood must match exactly, so "chill" and "relaxed" count as completely different moods, and so do "pop" and "indie pop."
- Each user can only list one genre and one mood, so someone with mixed tastes can't be represented.
- With only 18 songs, most genres have one song each, so many profiles will have only one possible genre match.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
python -m pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Profile: `favorite_genre="pop"`, `favorite_mood="happy"`, `target_energy=0.8`

```
Top recommendations
========================================
1. Sunrise City by Neon Echo
   Score: 3.98
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.98)

2. Gym Hero by Max Pulse
   Score: 2.87
   Reasons:
     - genre match (+2.0)
     - energy closeness (+0.87)

3. Rooftop Lights by Indigo Parade
   Score: 1.96
   Reasons:
     - mood match (+1.0)
     - energy closeness (+0.96)

4. Sol de Verano by Los Caminantes
   Score: 1.00
   Reasons:
     - energy closeness (+1.00)

5. Night Drive Loop by Neon Echo
   Score: 0.95
   Reasons:
     - energy closeness (+0.95)
```

Outputs for six more profiles (three typical and three edge cases) are in the Evaluation section of `model_card.md`.

---

## Experiments You Tried

### Experiment 1: Weight shift (genre halved, energy doubled)
I changed genre from 2.0 to 1.0 and doubled the energy points (energy weight 1.0 to 2.0), keeping mood at 1.0. The maximum score stayed at 4.0, so the math stayed valid.

**Result: no top-5 ranking changed for any of my six profiles.** Only the gaps between scores moved:
- Classical/melancholic/0.95: Rainfall Requiem (energy 0.22) fell from 3.27 to 2.54 but still ranked first. Its lead over Bassline Riot shrank from about 2.3 points to 0.56.
- High-Energy Pop: the gap between Gym Hero (pop) and Rooftop Lights (not pop) shrank from 1.11 to 0.22.

The change made results slightly less genre-driven but not more accurate. For the classical profile to put a high-energy song first, energy would need a weight above about 2.8 (with genre at 1.0). That means a weight tweak alone won't fix the problem. The system needs a better way to handle mismatches, such as letting a big energy gap cancel a genre match. I reverted to the original weights (2.0 / 1.0 / 1.0) afterward.

### Experiment 2: Different types of users
I tested six profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and three edge cases (pop/sad, k-pop, and classical at high energy). See the Evaluation section of `model_card.md` for the outputs and comparisons.

---

## Limitations and Risks

- The catalog has only 18 songs, and most genres have just one, so many users can match at most one song on genre.
- Genre and mood must match exactly, so "indie pop" gets no credit for "pop" and "sad" matches nothing.
- Genre and mood together are worth 3.0 points and energy at most 1.0, so a song can rank first even when its energy is far from the target (a classical song at 0.22 energy beat everything for a 0.95 energy user).
- It ignores tempo, valence, danceability, acousticness, and lyrics, and each user can have only one genre and one mood.
- It never says when nothing matches. A k-pop user still gets confident-looking results.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

**What I learned about how recommenders turn data into predictions.** A recommender is just a scoring rule plus a ranking rule. My system gives every song points for genre, mood, and energy closeness, then sorts by total. Even with only three rules, the results felt like real recommendations: Sunrise City came first for happy pop and Library Rain for chill lofi. The surprise came from the weights. In my classical test, a quiet 0.22-energy song ranked first for a user who asked for 0.95 energy, because genre and mood matches added up to more than the energy miss cost. When I halved genre and doubled energy, no rankings changed, only the gaps. That showed me that the choice of what to measure and how much to weight it is where a recommender's behavior really comes from.

**Where bias or unfairness could show up.** Bias came from my design choices and my data. Most genres have a single song, so a fan of lofi gets a full list of good matches while a fan of rock gets one good match and then filler. Exact-match labels also treat "pop" and "indie pop" as unrelated, and a mood like "sad" matches nothing because no song has it. In a real app, the same patterns could mean that users with less common tastes get worse recommendations. I also used AI throughout this project, and it helped most when I checked its work: I verified its scores by hand and found a genre count that was off by one and a prediction about the weight experiment that turned out wrong. Next, I would try partial credit for related genres and moods, add features like valence and tempo, and let a large energy gap cancel a genre match.