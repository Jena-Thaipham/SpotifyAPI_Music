import sqlite3
import numpy as np

db_path = r"D:\SpotifyAPI\SpotifyAPI_Music\spotify_db\spotify.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT followers FROM artists WHERE followers IS NOT NULL AND followers > 0")
followers = [row[0] for row in cursor.fetchall()]

if not followers:
    print("No valid followers data found.")
else:
    log_followers = np.log10(followers)

    mean_log = round(np.mean(log_followers), 2)
    std_log = round(np.std(log_followers), 2)

    low_log = round(mean_log - std_log, 2)
    high_log = round(mean_log + std_log, 2)

    mean_followers = round(np.mean(followers), 2)

    low_threshold = int(10 ** low_log)
    high_threshold = int(10 ** high_log)

    print(f"Mean log10(followers): {mean_log}")
    print(f"Std log10(followers): {std_log}")
    print(f"Mean followers (actual): {mean_followers}")
    print(f"Low threshold (followers): < {low_threshold}")
    print(f"High threshold (followers): >= {high_threshold}")

conn.close()
