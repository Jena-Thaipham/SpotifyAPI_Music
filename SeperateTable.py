import sqlite3
import json  

db_path = r"D:\SpotifyAPI\SpotifyAPI_Music\spotify_db\spotify.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS genres (
    artist_id TEXT,
    genre TEXT
);
""")


cursor.execute("DELETE FROM genres;")


cursor.execute("SELECT artist_id, genres FROM artists;")
rows = cursor.fetchall()


for artist_id, genres_str in rows:
    if genres_str and genres_str != "[]":
        try:
            genres_list = json.loads(genres_str)  
            for genre in genres_list:
                cleaned_genre = genre.strip().lower()  
                cursor.execute(
                    "INSERT INTO genres (artist_id, genre) VALUES (?, ?)",
                    (artist_id, cleaned_genre)
                )
        except json.JSONDecodeError:
            print(f"Invalid JSON for artist {artist_id}: {genres_str}")

conn.commit()
conn.close()

print("Genres table created successfully.")
