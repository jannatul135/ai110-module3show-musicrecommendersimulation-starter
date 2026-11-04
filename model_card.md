# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**VibeFinder 1.0**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

VibeFinder suggests songs from a small catalog based on one user's favorite genre, favorite mood, and target energy level. It returns the top 5 songs, each with a score and the reasons behind that score.

It assumes the user knows what genre and mood they want, and that one genre, one mood, and one energy level are enough to describe their taste.

It is built for classroom exploration, not for real users. It should not be used to power a real music app, to make decisions about artists, or to judge what music a person "should" like.

---

## 3. How the Model Works  

Think of the recommender as a judge giving every song in the catalog points for how well it fits you, then showing you the songs with the most points.

**What it asks you.** You tell it three things: your favorite genre (like pop), your favorite mood (like happy), and how energetic you want the music to feel, on a scale from 0 (very calm) to 1 (very intense).

**How a song earns points.** Each song can earn up to 4 points:

- **Genre (2 points):** If the song's genre is exactly your favorite genre, it gets 2 points. Otherwise it gets none. Genre is worth the most because it usually says the most about whether you'll like a song.
- **Mood (1 point):** If the song's mood is exactly your favorite mood, it gets 1 point.
- **Energy (up to 1 point):** The closer the song's energy is to what you asked for, the more points it gets. A perfect match earns the full point. A song that is a little off earns a bit less, and a song at the opposite extreme earns almost nothing.

**Picking the winners.** After every song has a score, the recommender lines them up from highest to lowest and shows you the top five. Each result comes with the reasons it scored the way it did, so you can see *why* it was picked.

**Example.** If you like happy pop with an energy of 0.8, "Sunrise City" (a happy pop song with energy 0.82) scores 3.98: 2 points for genre, 1 for mood, and 0.98 for energy because it is almost exactly as energetic as you wanted. "Gym Hero" is also pop but has an intense mood, so it gets genre and energy points but no mood point, and lands in second place with 2.87.

**What it ignores.** It doesn't look at tempo, danceability, acousticness, or how positive a song sounds, even though that information is in the dataset. Genre and mood also have to match word for word, so "indie pop" gets no credit from someone who likes "pop".

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog (`data/songs.csv`) has 18 songs.

There are 15 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, hip hop, classical, drum and bass, reggaeton, r&b, metal, and afrobeat. There are 14 moods: happy, chill, intense, relaxed, moody, focused, nostalgic, confident, melancholic, aggressive, playful, romantic, angry, and uplifting. Each song also has energy, tempo, valence, danceability, and acousticness. Only genre, mood, and energy are used in scoring.

The starter file had 10 songs. I added 8 using an AI assistant so the catalog covers more genres and moods. I did not remove any songs.

A lot of musical taste is missing. Most genres have only one song, and only pop and lofi appear more than once. The catalog is tiny and invented, so it doesn't reflect real listening habits, languages, or music from many cultures. It also has no lyrics, artist popularity, or listening history.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best for users whose taste fits one clear genre and mood, like "happy pop." For that profile it ranked Sunrise City first, which matched my intuition: it is a happy pop song with almost exactly the right energy.

The scoring captures "closeness" well. The energy score rewards songs that are near the target instead of just high or low. The scoring is also easy to understand, and every result comes with reasons, so I can see exactly why a song was picked.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The biggest weakness I found is that genre is worth twice as much as mood, so it dominates the results. For the pop/happy profile, Gym Hero (pop, intense) ranked second with 2.87 points, ahead of Rooftop Lights (indie pop, happy) with 1.96. Rooftop Lights fits the user's mood and energy well, but it lost because "indie pop" doesn't exactly match "pop" and got no genre credit.

Genre and mood must match word for word, so similar labels like "chill" and "relaxed" count as completely different. The system only looks at three features and ignores tempo, valence, danceability, and acousticness, which would help tell similar songs apart.

Most genres and moods have only one song, so many users can match at most one song on genre. Users who like popular, well-covered genres like pop and lofi get more choices than users who like a genre with a single song.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

**Additional features or preferences:** Add valence, tempo, and acousticness to the score so songs in the same genre can be told apart. Give partial credit for related genres and moods (for example, "indie pop" counts partly as "pop," and "chill" counts partly as "relaxed").

**Better explanations:** Show the reasons in plain sentences, like "Matches your favorite genre and is close to your energy level," instead of just point values.

**Improving diversity:** Add more songs per genre, and avoid showing several songs from the same genre or artist in the top 5.

**Handling more complex user tastes:** Let users list more than one favorite genre or mood, so someone who likes lofi for studying and rock for the gym can be represented in one profile.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps