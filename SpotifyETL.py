import logging
import pandas as pd
from typing import List
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
                logging.info(f"Read {len(ids)} IDs from {file_path}.")
                return ids
        except FileNotFoundError:
            logging.warning(f"ID file not found: {file_path}.")
            return []

    def _extract_albums_data(self) -> pd.DataFrame:
        album_ids = self._read_ids('album_ids.txt')
        albums = [self.extractor.get_album_info(aid) for aid in album_ids]
        albums_df = pd.DataFrame(filter(None, albums))
        logging.info(f"Fetched {len(albums_df)} albums.")
        return albums_df

    def _extract_artists_data(self) -> pd.DataFrame:
        artist_ids = self._read_ids('artist_ids.txt')
        artists = [self.extractor.get_artist_info(aid) for aid in artist_ids]
        artists_df = pd.DataFrame(filter(None, artists))
        logging.info(f"Fetched {len(artists_df)} artists.")
        return artists_df

    def _extract_tracks_data(self) -> pd.DataFrame:
        track_ids = self._read_ids('track_ids.txt')
        tracks = [self.extractor.get_track_info(tid) for tid in track_ids]
        tracks_df = pd.DataFrame(filter(None, tracks))
        logging.info(f"Fetched {len(tracks_df)} tracks.")
        return tracks_df

    def _extract_playlists_data(self) -> pd.DataFrame:
        playlist_ids = self._read_ids('playlist_ids.txt')
        playlists = []
        for pid in playlist_ids:
            playlist_info = self.extractor.get_playlist_info(pid)
            if playlist_info:
                playlists.append(playlist_info)
            else:
                logging.warning(f"Failed to fetch playlist info for ID: {pid}.")
        playlists_df = pd.DataFrame(playlists)
        logging.info(f"Fetched {len(playlists_df)} playlists.")
        return playlists_df

    def _extract_playlist_tracks_data(self) -> pd.DataFrame:
        playlist_ids = self._read_ids('playlist_ids.txt')
        playlist_tracks = []
        for pid in playlist_ids:
            tracks_info = self.extractor.get_playlist_track_info(pid)
            if tracks_info:
                for track in tracks_info:
                    playlist_tracks.append({
                        'playlist_id': pid,
                        'track_id': track['track_id'],
                        'added_at': track['added_at']
                    })
            else:
                logging.warning(f"No tracks found for playlist ID: {pid}.")
        playlist_tracks_df = pd.DataFrame(playlist_tracks)
        logging.info(f"Fetched {len(playlist_tracks_df)} playlist tracks.")
        return playlist_tracks_df

    def _extract_users_data(self) -> pd.DataFrame:
        playlist_ids = self._read_ids('playlist_ids.txt')
        user_infos = {}
        for pid in playlist_ids:
            playlist_info = self.extractor.get_playlist_info(pid)
            if playlist_info:
                owner_id = playlist_info.get('owner_id')
                if owner_id and owner_id not in user_infos:
                    user_info = self.extractor.get_user_info(owner_id)
                    if user_info:
                        user_infos[owner_id] = user_info
                    else:
                        logging.warning(f"User info not found for owner_id: {owner_id}.")
        users_df = pd.DataFrame(user_infos.values())
        logging.info(f"Fetched {len(users_df)} users.")
        return users_df

    def run(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        logging.info("Starting ETL extraction process...")

        data_extractors = {
            'albums': self._extract_albums_data,
            'artists': self._extract_artists_data,
            'tracks': self._extract_tracks_data,
            'playlists': self._extract_playlists_data,
            'playlist_tracks': self._extract_playlist_tracks_data,
            'users': self._extract_users_data,
        }

        for table_name, extractor_func in data_extractors.items():
            try:
                df = extractor_func()
                if df.empty:
                    logging.warning(f"No data extracted for {table_name}.")
                    continue
                success = self.db_manager.save_table(table_name, df)
                if not success:
                    logging.error(f"Failed to save data for table: {table_name}.")
            except Exception as e:
                logging.error(f"Error processing {table_name}: {str(e)}")

        self.db_manager.close()
        logging.info("ETL pipeline completed successfully.")

if __name__ == "__main__":
    pipeline = SpotifyETLPipeline()
    pipeline.run()
