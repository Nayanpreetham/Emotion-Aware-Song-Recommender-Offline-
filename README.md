# Emotion-Aware-Song-Recommender-Offline-
This project is a local music recommendation system that suggests the next song to play based on:

Your emotion-based rating (1 = dislike, 3 = love)

The emotion, genre, artist, language, and movie of the current song

A complementary or similar emotion from Plutchik's emotion wheel

**Data Used**

A local CSV file (songs_db.csv) containing 100 uniquely curated songs:

60 Telugu, 20 Hindi, 20 English

Each song has the following fields:

title, artist, movie, language, genre, emotion

No external API or internet required — runs fully offline using local data.

**How It Works**

User chooses a song by selecting from the top 10 list or typing the title.

User gives a rating (1 to 3):

3 → Recommend a song with same emotion and similar artist/movie

2 → Recommend a song with same emotion but different artist/movie

1 → Recommend a song with the opposite emotion and least similarity

The script filters and ranks possible matches using:

Emotion similarity

Language consistency

Artist and movie match

**Features**

Built entirely in Python

No GUI or web interface — simple command-line interface

Intelligent use of:

Emotion mapping (Plutchik’s emotion wheel)

Weighted relevance based on artist/movie

Fully customizable song list (just update the CSV!)

**Libraries Used**

pandas — for reading and filtering the CSV

random — for unbiased selection in neutral cases
