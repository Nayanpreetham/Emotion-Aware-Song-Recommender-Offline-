# recommender.py

import pandas as pd
import random

emotion_opposites = {
    "joy": "sadness", "trust": "disgust",
    "fear": "anger", "surprise": "anticipation",
    "sadness": "joy", "disgust": "trust",
    "anger": "fear", "anticipation": "surprise"
}

def load_songs(csv_file):
    df = pd.read_csv(csv_file)
    return df.to_dict(orient="records")

def suggest_next_song(current_title, rating, songs_db):
    current_song = next((s for s in songs_db if s["title"] == current_title), None)
    if not current_song:
        return None

    curr_emotion = current_song['emotion']
    curr_language = current_song['language']
    curr_artist = current_song['artist']
    curr_movie = current_song['movie']

    if rating == 3:
        candidates = [s for s in songs_db if s["emotion"] == curr_emotion and s["language"] == curr_language and s["title"] != current_title]
        ranked = sorted(candidates, key=lambda x: (x["artist"] == curr_artist) + (x["movie"] == curr_movie), reverse=True)
        return ranked[0] if ranked else None

    if rating == 2:
        candidates = [s for s in songs_db if s["emotion"] == curr_emotion and s["language"] == curr_language and s["title"] != current_title]
        random.shuffle(candidates)
        return candidates[0] if candidates else None

    if rating == 1:
        opposite = emotion_opposites.get(curr_emotion, curr_emotion)
        candidates = [s for s in songs_db if s["emotion"] == opposite and s["language"] == curr_language and s["title"] != current_title]
        ranked = sorted(candidates, key=lambda x: (x["artist"] != curr_artist) + (x["movie"] != curr_movie), reverse=True)
        return ranked[0] if ranked else None

    return None
