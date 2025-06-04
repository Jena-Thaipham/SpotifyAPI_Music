import logging
import time
import pandas as pd
from typing import List, Dict
from SpotifyExtractor import SpotifyExtractor
from DatabaseManager import DatabaseManager


class SpotifyETLPipeline:
    def __init__(self):
        self.extractor = SpotifyExtractor()
        self.access_token = self.extractor.get_access_token()
        self.db_manager = DatabaseManager()

    def _read_ids(self, file_path: str) -> List[str]:
        try:
            with open(file_path, 'r') as f:
                ids = [line.strip() for line in f if line.strip()]
                logging.info(f"Read {len(ids)} IDs from {file_path}")
                return ids
        except FileNotFoundError:
            logging.warning(f"ID file not found: {file_path}")
            return []

    def _extract_batch_data(self) -> Dict[str, pd.DataFrame]:
        album_ids = self._read_ids('album_ids.txt')
        artist_ids = self._read_ids('artist_ids.txt')
        track_ids = self._read_ids('track_ids.txt')
        playlist_ids = self._read_ids('playlist_ids.txt')

        def process_in_batches(id_list: List[str], batch_func, name: str) -> pd.DataFrame:
            all_data = []
            for i in range(0, len(id_list), 20):
                batch = id_list[i:i + 20]
                data = batch_func(batch)
                all_data.extend(data)
                logging.info(f"Fetched {len(data)} {name} from batch {i // 20 + 1}")
                time.sleep(0.3)  # Be gentle with rate limits
            return pd.DataFrame(all_data)

        albums_df = process_in_batches(album_ids, self.extractor.get_albums_batch, "albums")
        artists_df = process_in_batches(artist_ids, self.extractor.get_artists_batch, "artists")
        tracks_df = process_in_batches(track_ids, self.extractor.get_tracks_batch, "tracks")

        logging.info(f"Fetched {len(albums_df)} albums in total")
        logging.info(f"Fetched {len(artists_df)} artists in total")
        logging.info(f"Fetched {len(tracks_df)} tracks in total")

        playlists = []
        playlist_tracks = []
        user_infos = {}

        for pid in playlist_ids:
            playlist_info = self.extractor.get_playlist_info(pid)
            time.sleep(0.3)

            if playlist_info:
                playlists.append(playlist_info)

                owner_id = playlist_info.get('owner_id')
                if owner_id and owner_id not in user_infos:
                    user_info = self.extractor.get_user_info(owner_id)
                    time.sleep(0.2)
                    if user_info:
                        user_infos[owner_id] = user_info
                    else:
                        logging.warning(f"User info not found for owner_id: {owner_id}")

                for track in playlist_info['tracks']:
                    playlist_tracks.append({
                        'playlist_id': pid,
                        'track_id': track['track_id'],
                        'added_at': track['added_at']
                    })
            else:
                logging.warning(f"Could not fetch playlist info for ID: {pid}")

        playlists_df = pd.DataFrame(playlists)
        playlist_tracks_df = pd.DataFrame(playlist_tracks)
        users_df = pd.DataFrame(user_infos.values())

        logging.info(f"Total playlists fetched: {len(playlists_df)}")
        logging.info(f"Total users fetched: {len(users_df)}")

        return {
            'albums': albums_df,
            'artists': artists_df,
            'tracks': tracks_df,
            'playlists': playlists_df,
            'playlist_tracks': playlist_tracks_df,
            'users': users_df
        }

    def run(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        logging.info("Starting ETL pipeline with batch support...")
        dataframes = self._extract_batch_data()

        if all(df.empty for df in dataframes.values()):
            logging.error("No data was extracted. Please check your ID files or API access.")
            return

        logging.info("Saving data to database...")
        self.db_manager.save_data(dataframes)
        self.db_manager.close()
        logging.info("ETL pipeline completed and data saved to database.")


if __name__ == "__main__":
    pipeline = SpotifyETLPipeline()
    pipeline.run()
