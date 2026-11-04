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

The system lets genre and mood outweigh energy, which can give a user the opposite of what they asked for. When I tested a classical/melancholic profile with a target energy of 0.95, Rainfall Requiem (energy 0.22) ranked first with 3.27 points, because genre and mood together are worth 3.0 points and its energy gap only cost 0.73. Four high-energy songs that matched the requested energy ranked below it. Exact-match scoring also made the “sad” mood in the pop/sad profile useless, since no song carries that label. A real recommender would need to treat energy as something that can veto a result, or at least weight it more.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

**Profiles tested.** High-Energy Pop (pop, happy, 0.9), Chill Lofi (lofi, chill, 0.35), Deep Intense Rock (rock, intense, 0.92), and three edge cases: Conflicting (pop, sad, 0.9), Genre Not in File (k-pop, happy, 0.8), and Mismatched Vibe (classical, melancholic, 0.95).

**What I looked for.** Whether the top results matched my intuition, whether the reasons explained each score, and whether I could trick the scoring into a bad result.

**What surprised me.** Deep Intense Rock has only one rock song, so after Storm Runner the list fell apart: Gym Hero ranked second on a mood match alone, and #3 to #5 got energy points only. The classical profile was the biggest surprise. Rainfall Requiem has an energy of 0.22, but it still ranked first for a user who wanted 0.95, because genre and mood together are worth 3.0 points. The k-pop profile still returned confident-looking results even though no song could match the genre. Doubling energy and halving genre did not change any rankings, only the gaps. 
I asked my AI assistant why Rainfall Requiem ranked first for the classical profile. It showed that the song earns genre (+2.0) and mood (+1.0) points and only loses 0.73 on energy, so it scores 3.27 against 0.99 for Bassline Riot, whose only points come from energy. I checked this by hand. In the weight experiment (genre 1.0, energy doubled), Rainfall Requiem still won 2.54 to 1.98, and energy would need a weight above about 2.8 to flip it.

**Profile comparisons.**
- **High-Energy Pop vs. Chill Lofi:** The pop profile favors loud, upbeat songs (Sunrise City, Gym Hero). Chill Lofi shifts to calm songs (Library Rain, Midnight Coding) because the target energy drops from 0.9 to 0.35 and the genre and mood both change. This makes sense, since the two profiles ask for opposite vibes.
- **High-Energy Pop vs. Deep Intense Rock:** Both want high energy, so Gym Hero and Bassline Riot appear in both lists. Genre and mood decide the winner: Sunrise City for pop/happy, Storm Runner for rock/intense.
- **Chill Lofi vs. Deep Intense Rock:** They share almost nothing because their energy targets are far apart (0.35 vs. 0.92). Lofi has three genre matches while rock has only one, which shows the dataset is uneven.
- **High-Energy Pop vs. Conflicting (pop, sad):** Gym Hero and Sunrise City lead both lists. Since no song is "sad," the mood does nothing, and Sunrise City drops from 3.92 to 2.92 because it loses its mood point.
- **High-Energy Pop vs. Genre Not in File (k-pop):** The mood is the same (happy), but with no genre match the top score falls from 3.92 to 1.98. Sunrise City is still first on mood plus energy, but the system never says it couldn't find the genre.
- **Deep Intense Rock vs. Mismatched Vibe (classical):** Both want very high energy, and #2 to #5 are mostly the same energy-only songs. The difference is #1: Storm Runner fits the energy, but Rainfall Requiem does not, because genre and mood outweigh energy.

**Outputs.** (Paste each profile's terminal output below in its own fenced code block, with the profile name above it.)

### High-Energy Pop
```
High-Energy Pop
========================================
Top recommendations
----------------------------------------
1. Sunrise City by Neon Echo
   Score: 3.92
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.92)

2. Gym Hero by Max Pulse
   Score: 2.97
   Reasons:
     - genre match (+2.0)
     - energy closeness (+0.97)

3. Rooftop Lights by Indigo Parade
   Score: 1.86
   Reasons:
     - mood match (+1.0)
     - energy closeness (+0.86)

4. Storm Runner by Voltline
   Score: 0.99
   Reasons:
     - energy closeness (+0.99)

5. Bassline Riot by Shockwave Theory
   Score: 0.94
   Reasons:
     - energy closeness (+0.94)
```

### Chill Lofi
```
Chill Lofi
========================================
Top recommendations
----------------------------------------
1. Library Rain by Paper Lanterns
   Score: 4.00
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+1.00)

2. Midnight Coding by LoRoom
   Score: 3.93
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.93)

3. Focus Flow by LoRoom
   Score: 2.95
   Reasons:
     - genre match (+2.0)
     - energy closeness (+0.95)

4. Spacewalk Thoughts by Orbit Bloom
   Score: 1.93
   Reasons:
     - mood match (+1.0)
     - energy closeness (+0.93)

5. Coffee Shop Stories by Slow Stereo
   Score: 0.98
   Reasons:
     - energy closeness (+0.98)
```

### Deep Intense Rock
```
Deep Intense Rock
========================================
Top recommendations
----------------------------------------
1. Storm Runner by Voltline
   Score: 3.99
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.99)

2. Gym Hero by Max Pulse
   Score: 1.99
   Reasons:
     - mood match (+1.0)
     - energy closeness (+0.99)

3. Bassline Riot by Shockwave Theory
   Score: 0.96
   Reasons:
     - energy closeness (+0.96)

4. Iron Cathedral by Graveheart
   Score: 0.94
   Reasons:
     - energy closeness (+0.94)

5. Sunrise City by Neon Echo
   Score: 0.90
   Reasons:
     - energy closeness (+0.90)
```

### Conflicting (pop, sad, 0.9)
```
Conflicting (pop, sad, 0.9)
========================================
Top recommendations
----------------------------------------
1. Gym Hero by Max Pulse
   Score: 2.97
   Reasons:
     - genre match (+2.0)
     - energy closeness (+0.97)

2. Sunrise City by Neon Echo
   Score: 2.92
   Reasons:
     - genre match (+2.0)
     - energy closeness (+0.92)

3. Storm Runner by Voltline
   Score: 0.99
   Reasons:
     - energy closeness (+0.99)

4. Bassline Riot by Shockwave Theory
   Score: 0.94
   Reasons:
     - energy closeness (+0.94)

5. Iron Cathedral by Graveheart
   Score: 0.92
   Reasons:
     - energy closeness (+0.92)
```

### Genre Not in File (k-pop)
```
Genre Not in File (k-pop)
========================================
Top recommendations
----------------------------------------
1. Sunrise City by Neon Echo
   Score: 1.98
   Reasons:
     - mood match (+1.0)
     - energy closeness (+0.98)

2. Rooftop Lights by Indigo Parade
   Score: 1.96
   Reasons:
     - mood match (+1.0)
     - energy closeness (+0.96)

3. Sol de Verano by Los Caminantes
   Score: 1.00
   Reasons:
     - energy closeness (+1.00)

4. Night Drive Loop by Neon Echo
   Score: 0.95
   Reasons:
     - energy closeness (+0.95)

5. Lantern Festival by Kora Sky
   Score: 0.94
   Reasons:
     - energy closeness (+0.94)

```

### Mismatched Vibe (classical, 0.95)
```

Mismatched Vibe (classical, 0.95)
========================================
Top recommendations
----------------------------------------
1. Rainfall Requiem by Aurelia Strings
   Score: 3.27
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy closeness (+0.27)

2. Bassline Riot by Shockwave Theory
   Score: 0.99
   Reasons:
     - energy closeness (+0.99)

3. Gym Hero by Max Pulse
   Score: 0.98
   Reasons:
     - energy closeness (+0.98)

4. Iron Cathedral by Graveheart
   Score: 0.97
   Reasons:
     - energy closeness (+0.97)

5. Storm Runner by Voltline
   Score: 0.96
   Reasons:
     - energy closeness (+0.96)

```

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

**What I learned about recommender systems.** A recommender is a scoring rule plus a ranking rule. My system gives each song points for genre, mood, and energy closeness, then sorts by the total. I learned that the weights are where the real decisions are made. Genre and mood together are worth 3 points and energy only 1, so those two labels end up controlling most results.

**Something unexpected.** In my classical test, a quiet song with an energy of 0.22 ranked first for a user who asked for 0.95. Its genre and mood matches added up to more than the energy miss cost it. I was also surprised that halving genre and doubling energy changed no rankings, only the gaps between scores. I predicted the order would flip, and checking the numbers by hand showed I was wrong. That taught me to verify results instead of trusting a guess, whether it comes from me or from an AI.

**How this changes how I think about music apps.** Three simple rules were enough to make the results feel like real recommendations, so I now see that apps like Spotify are doing something much bigger, but built on the same idea. I also notice that what gets measured decides what you get. Users with less common tastes, like my rock profile with only one rock song, would get worse results, and I'd expect that to happen in real apps too.