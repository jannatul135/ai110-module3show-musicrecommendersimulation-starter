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

### How does your `Recommender` compute a score for each song?
- Genre match: +2.0 points
- Mood match: +1.0 point
- Energy: `1 - abs(song_energy - target_energy)`, so songs closer to the user's target get more points
- Each song gets a total score plus a list of reasons, such as "genre match (+2.0)"

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
- Genre match is worth 2 points and mood only 1, so a mood-and-energy match can never beat a genre-only match. For example, with a pop/happy profile, Gym Hero (pop, intense) is expected to rank above Rooftop Lights (indie pop, happy) because "indie pop" gets no genre credit. I plan to test lower genre weight and partial genre credit in Phase 4.
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
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this