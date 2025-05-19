import sqlite3

db_path = db_path = r"D:\SpotifyAPI\SpotifyAPI_Music\spotify_db\spotify.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS artist_genres (
    artist_id INTEGER,
    genre TEXT
);
""")

cursor.execute("DELETE FROM artist_genres;")

cursor.execute("SELECT rowid, genres FROM artists;")
rows = cursor.fetchall()

for artist_id, genres_str in rows:
    if genres_str:
        genres = [g.strip() for g in genres_str.split(",")]
        for genre in genres:
            cursor.execute(
                "INSERT INTO artist_genres (artist_id, genre) VALUES (?, ?)",
                (artist_id, genre)
            )

conn.commit()
conn.close()

print("artist_genres table created successfully.")
