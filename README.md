# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

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



