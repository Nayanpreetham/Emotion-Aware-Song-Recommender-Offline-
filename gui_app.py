# gui_app.py

import tkinter as tk
from tkinter import ttk, messagebox
from recommender import load_songs, suggest_next_song

songs_db = load_songs("songs_db.csv")
song_titles = [s["title"] for s in songs_db[:10]]  # Top 10 shown

def recommend():
    song = song_var.get()
    try:
        rating = int(rating_var.get())
        if rating not in [1, 2, 3]:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Rating", "Please enter a rating between 1 and 3.")
        return

    result = suggest_next_song(song, rating, songs_db)
    if result:
        result_label.config(
            text=f"🎶 {result['title']}\n🎤 {result['artist']}\n🎬 {result['movie']}\n🎧 {result['language']}\n🎭 {result['emotion']}"
        )
    else:
        result_label.config(text="No suitable next song found.")

root = tk.Tk()
root.title("Emotion-Based Song Recommender")
root.geometry("400x300")

tk.Label(root, text="Select a song:").pack()
song_var = tk.StringVar()
song_menu = ttk.Combobox(root, textvariable=song_var, values=song_titles, width=50)
song_menu.pack()

tk.Label(root, text="Rate this song (1=Bad, 3=Good):").pack()
rating_var = tk.StringVar()
tk.Entry(root, textvariable=rating_var).pack()

tk.Button(root, text="Suggest Next Song", command=recommend).pack(pady=10)

result_label = tk.Label(root, text="", wraplength=350, justify="left")
result_label.pack()

root.mainloop()
