import sqlite3
import numpy as np

db_path = r"D:\SpotifyAPI\SpotifyAPI_Music\spotify_db\spotify.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


cursor.execute("SELECT popularity FROM artists WHERE popularity IS NOT NULL")
popularities = [row[0] for row in cursor.fetchall()]


mean_pop = round(np.mean(popularities), 2)
std_pop = round(np.std(popularities), 2)
low_threshold = round(mean_pop - std_pop, 2)
high_threshold = round(mean_pop + std_pop, 2)


print(f"Mean popularity: {mean_pop}")
print(f"Standard deviation: {std_pop}")
print(f"Low threshold: < {low_threshold}")
print(f"High threshold: >= {high_threshold}")

conn.close()
