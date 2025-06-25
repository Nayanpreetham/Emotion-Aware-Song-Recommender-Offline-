# emotion_song_sequencer_local.py

import random
import pandas as pd

# ------------------------
# Emotion Mapping (Plutchik Based)
# ------------------------
emotion_opposites = {
    "joy": "sadness",
    "trust": "disgust",
    "fear": "anger",
    "surprise": "anticipation",
    "sadness": "joy",
    "disgust": "trust",
    "anger": "fear",
    "anticipation": "surprise"
}

# ------------------------
# Load Songs Database from CSV
# ------------------------
songs_df = pd.read_csv("songs_db.csv")
songs_df["title_clean"] = songs_df["title"].apply(lambda x: " ".join(x.split(" ")[:-1]) if x.split(" ")[-1].isdigit() else x)
songs_db = songs_df.to_dict(orient="records")

# ------------------------
# Suggest Next Song Based on Rating
# ------------------------
def suggest_next_song(current_title, rating):
    current_song = next((s for s in songs_db if s["title"] == current_title), None)
    if not current_song:
        print("Current song not in history DB")
        return None, None

    curr_emotion = current_song['emotion']
    curr_language = current_song['language']
    curr_artist = current_song['artist']
    curr_movie = current_song['movie']
    curr_title_clean = " ".join(current_song['title'].split(" ")[:-1])

    if rating == 3:
        target_emotion = curr_emotion
        candidates = [s for s in songs_db if
                      s["emotion"] == target_emotion and
                      s["language"] == curr_language and
                      " ".join(s['title'].split(" ")[:-1]) != curr_title_clean]
        ranked = sorted(candidates, key=lambda x: (
            int(x["artist"] == curr_artist) + int(x["movie"] == curr_movie)
        ), reverse=True)
        return current_song, ranked[0] if ranked else None

    if rating == 2:
        target_emotion = curr_emotion
        candidates = [s for s in songs_db if
                      s["emotion"] == target_emotion and
                      s["language"] == curr_language and
                      " ".join(s['title'].split(" ")[:-1]) != curr_title_clean and
                      (s["artist"] != curr_artist or s["movie"] != curr_movie)]
        random.shuffle(candidates)
        return current_song, candidates[0] if candidates else None

    if rating == 1:
        target_emotion = emotion_opposites.get(curr_emotion, curr_emotion)
        candidates = [s for s in songs_db if
                      s["emotion"] == target_emotion and
                      s["language"] == curr_language and
                      " ".join(s['title'].split(" ")[:-1]) != curr_title_clean]
        ranked = sorted(candidates, key=lambda x: (
            int(x["artist"] != curr_artist) + int(x["movie"] != curr_movie)
        ), reverse=True)
        return current_song, ranked[0] if ranked else None

    return current_song, None

# ------------------------
# CLI-Based Interaction
# ------------------------
if __name__ == "__main__":
    print("\n🎵 Top 10 Available Songs:")
    for i, song in enumerate(songs_db[:10], 1):
        clean_title = " ".join(song['title'].split(" ")[:-1]) if song['title'].split(" ")[-1].isdigit() else song['title']
        print(f"{i}. {clean_title} ({song['language']}) - {song['artist']}")

    choice = input("\nSelect song number (1-10) or type full song name: ").strip()

    if choice.isdigit():
        index = int(choice)
        if 1 <= index <= 10:
            current_song = songs_db[index - 1]['title']
        else:
            print("Invalid selection. Exiting.")
            exit()
    else:
        matching = [s for s in songs_db if choice.lower() in s['title'].lower()]
        if matching:
            current_song = matching[0]['title']
        else:
            print("Song not found. Exiting.")
            exit()

    try:
        user_rating = int(input("Rate the song (1 to 3): ").strip())
        if not (1 <= user_rating <= 3):
            raise ValueError
    except ValueError:
        print("Invalid rating. Exiting.")
        exit()

    current, next_song = suggest_next_song(current_song, user_rating)
    if next_song:
        print("\n🎶 Current Song:", " ".join(current['title'].split(" ")[:-1])) # type: ignore
        print("⭐ Rating:", user_rating)
        print("➡️  Next Suggested Song:", next_song['title'])
        print("🎧 Language:", next_song['language'])
        print("🎤 Artist:", next_song['artist'])
        print("🎭 Emotion:", next_song['emotion'])
        
    else:
        print("No suitable next song found.")
