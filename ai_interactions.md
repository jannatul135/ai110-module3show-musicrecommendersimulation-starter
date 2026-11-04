# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I used Claude Code in VS Code as an agent for several multi-step changes: adding 8 new songs to `data/songs.csv`, adding a dictionary of named user profiles to `src/main.py` and running all of them, and running a weight-shift experiment in `src/recommender.py` (genre halved, energy doubled) across six profiles.

**Prompts used:**

- "Generate 8 additional songs in valid CSV format using the exact same headers as the attached file. Make them diverse in genre and mood, avoiding genres and moods already in the file." Then: "append those rows"
- "In main.py, replace the single user_prefs with a dictionary of named profiles: 'High-Energy Pop' (pop, happy, 0.9), 'Chill Lofi' (lofi, chill, 0.35), and 'Deep Intense Rock' (rock, intense, 0.92). Loop over them, print the profile name as a header, and print the top 5 recommendations for each using the existing output format."
- "In main.py, add three more profiles to the profiles dictionary" (conflicting pop/sad/0.9, k-pop/happy/0.8, and classical/melancholic/0.95)
- "In recommender.py, temporarily change the weights so genre is worth 1.0 instead of 2.0 and energy is worth double. Keep the mood weight at 1.0. Verify the math is still valid and the score range is documented. Then run all six profiles."

**What did the agent generate or change?**

- `data/songs.csv`: appended 8 songs (IDs 11 to 18), after checking that the file ended in a newline and that Python's CSV reader parsed all 18 rows with 10 fields each.
- `src/main.py`: replaced the single `user_prefs` with a `profiles` dictionary and a loop that prints each profile's name and top 5 results.
- `src/recommender.py`: moved the scoring weights into constants (`GENRE_WEIGHT`, `MOOD_WEIGHT`, `ENERGY_WEIGHT`), changed them for the experiment, and documented the score range (0.0 to 4.0) in the `score_song` docstring.
- Ran `python3 -m src.main` after each change and summarized the results for all six profiles.

**What did you verify or fix manually?**

- **The CSV append:** I checked the line count (`wc -l`) to confirm 18 songs plus the header.
- **The AI's genre count was wrong.** The Scoring Logic Design chat said the catalog had 14 genres, but it has 15. I caught it and used the correct number in my docs.
- **Profile edit:** the agent's edit to add the three edge-case profiles was rejected because the file had already changed, and the profiles were already there. I checked the output to confirm all six profiles ran.
- **The experiment result:** I checked the scores by hand (for example, Rainfall Requiem at 1.0 + 1.0 + 0.54 = 2.54 vs. Bassline Riot at 1.98). A prediction I had that the weight change would flip the classical profile was wrong. The agent's result, no ranking changes, was correct.
- **Reverting the experiment:** the agent left the experimental weights in place, so I set them back to 2.0 / 1.0 / 1.0 so the code matched my README and saved outputs, then re-ran the program and tests to confirm the baseline numbers came back.
- **Class placement:** when I added the `Recommender` class methods, they ended up outside the class. I fixed that and ran `python -m pytest` to confirm both tests passed.
- **Environment:** the agent ran code with `python3` and found pytest wasn't installed there, so I ran everything myself inside my `.venv`.