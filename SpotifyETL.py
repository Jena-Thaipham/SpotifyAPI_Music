import logging
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

    def _extract_data(self) -> Dict[str, pd.DataFrame]:
        album_ids = self._read_ids('album_ids.txt')
        artist_ids = self._read_ids('artist_ids.txt')
        track_ids = self._read_ids('track_ids.txt')
        playlist_ids = self._read_ids('playlist_ids.txt')

        albums_data = [self.extractor.get_album_info(aid) for aid in album_ids]
        albums_df = pd.DataFrame(filter(None, albums_data))
        logging.info(f"Fetched {len(albums_df)} albums")

        artists_data = [self.extractor.get_artist_info(aid) for aid in artist_ids]
        artists_df = pd.DataFrame(filter(None, artists_data))
        logging.info(f"Fetched {len(artists_df)} artists")

        tracks_data = [self.extractor.get_track_info(tid) for tid in track_ids]
        tracks_df = pd.DataFrame(filter(None, tracks_data))
        logging.info(f"Fetched {len(tracks_df)} tracks")

        playlists = []
        playlist_tracks = []
        user_infos = {}

        for pid in playlist_ids:
            playlist_info = self.extractor.get_playlist_info(pid)
            if playlist_info:
                playlists.append(playlist_info)

                owner_id = playlist_info.get('owner_id')
                if owner_id and owner_id not in user_infos:
                    user_info = self.extractor.get_user_info(owner_id)
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
        
        dataframes = self._extract_data()
    
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
