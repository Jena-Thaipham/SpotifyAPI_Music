import time
import requests
import base64
import logging
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from dotenv import load_dotenv
import json
import random


class SpotifyExtractor:
    def __init__(self):
        load_dotenv()
        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.access_token = None
        self.token_expiry = None

    def get_access_token(self) -> Optional[str]:
        if self.access_token and datetime.now() < self.token_expiry:
            return self.access_token

        auth_string = f"{self.CLIENT_ID}:{self.CLIENT_SECRET}"
        auth_bytes = auth_string.encode('utf-8')
        auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

        headers = {
            'Authorization': f'Basic {auth_base64}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {'grant_type': 'client_credentials'}

        try:
            response = requests.post('https://accounts.spotify.com/api/token',
                                     headers=headers,
                                     data=data,
                                     timeout=10)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.token_expiry = datetime.now() + timedelta(seconds=token_data['expires_in'] - 60)
            return self.access_token
        except Exception as e:
            logging.error(f"Error getting access token: {str(e)}")
            return None

    def make_request(self, endpoint: str, retries: int = 10, backoff: float = 1.0) -> Optional[Dict]:
        for attempt in range(retries):
            headers = {'Authorization': f'Bearer {self.get_access_token()}'}
            try:
                response = requests.get(f'https://api.spotify.com/v1/{endpoint}',
                                    headers=headers,
                                    timeout=15)

                if response.status_code == 200:
                    time.sleep(random.uniform(0.1, 0.3))
                    return response.json()

                elif response.status_code == 401:
                    logging.warning(f"Unauthorized for {endpoint}. Refreshing token and retrying...")
                    self.access_token = None  
                    continue

                elif response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", "5"))
                    logging.warning(f"Rate limited for {endpoint}, retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue

                else:
                    logging.error(f"API error {response.status_code} for {endpoint}: {response.text}")
                    return None

            except requests.exceptions.RequestException as e:
                logging.warning(f"Attempt {attempt+1}/{retries} failed for {endpoint}: {e}")
                time.sleep(backoff * (2 ** attempt))  
                continue

        logging.error(f"Exceeded max retries for {endpoint}")
        return None



    def get_playlist_info(self, playlist_id: str) -> Optional[Dict]:
        data = self.make_request(f'playlists/{playlist_id}')
        if not data:
            return None

        try:
            playlist_info = {
                'playlist_id': data['id'],
                'playlist_name': data['name'],
                'owner_id': data['owner']['id'],
                'total_tracks': data['tracks']['total'],
                'public': bool(data.get('public', False)),
                'playlist_uri': data['uri']
        }

            playlist_info['tracks'] = []

            for track_item in data['tracks']['items']:
                track = track_item.get('track')
                if not track:
                    continue
                track_info = {
                    'added_at': track_item.get('added_at'),
                    'track_id': track.get('id'),
                    'track_name': track.get('name'),
                }
                playlist_info['tracks'].append(track_info)

            return playlist_info
        except KeyError as e:
            logging.error(f"Missing field in playlist data: {str(e)}")
            return None

    def get_album_info(self, album_id: str) -> Optional[Dict]:
        data = self.make_request(f'albums/{album_id}')
        if not data:
            return None

        try:
            return {
                'album_id': data['id'],
                'album_name': data['name'],
                'album_type': data['album_type'],
                'artist_id': ','.join([artist.get('id', '') for artist in data.get('artists', []) if artist.get('id')]),
                'release_date': data['release_date'],
                'total_tracks': data['total_tracks'],
                'markets': json.dumps(data['available_markets']),
                'popularity': data['popularity'],
                'album_uri': data['uri']
         }
        except (KeyError, IndexError) as e:
            logging.error(f"Missing field in album data: {str(e)}")
        return None

    def get_artist_info(self, artist_id: str) -> Optional[Dict]:
        data = self.make_request(f'artists/{artist_id}')
        if not data:
            return None

        try:
            return {
                'artist_id': data['id'],
                'artist_name': data['name'],
                'genres': json.dumps(data['genres']),
                'followers': data.get('followers', {}).get('total', 0),
                'popularity': data['popularity'],
                'artist_uri': data['uri']
            }
        except KeyError as e:
            logging.error(f"Missing field in artist data: {str(e)}")
            return None

    def get_track_info(self, track_id: str) -> Optional[Dict]:
        data = self.make_request(f'tracks/{track_id}')
        if not data:
            return None

        try:
            return {
                'track_id': data['id'],
                'track_name': data['name'],
                'artist_id': data.get('artists', [{}])[0].get('id', ''),
                'album_id': data['album']['id'],
                'markets': json.dumps(data['available_markets']),
                'popularity': data['popularity'],
                'duration_ms': data['duration_ms'],
                'track_number': data['track_number'],
                'disc_number': data['disc_number'],
                'explicit': bool (data['explicit']),
                'local': bool (data['is_local']),
                'track_uri': data['uri']
             }
        except (KeyError, IndexError) as e:
            logging.error(f"Missing field in track data: {str(e)}")
            return None

    def get_user_info(self, user_id: str) -> Optional[Dict]:
        data = self.make_request(f'users/{user_id}')
        if not data:
            return None

        try:
            return {
                'user_id': data['id'],
                'followers': data.get('followers', {}).get('total', 0),
                'user_uri': data['uri']
            }
        except KeyError as e:
            logging.error(f"Missing field in user data: {str(e)}")
            return None


    def get_albums_batch(self, album_ids: List[str]) -> List[Dict]:
        all_album_infos = []
        for i in range(0, len(album_ids), 20):
            batch = album_ids[i:i + 20]
            ids_param = ','.join(batch)
            data = self.make_request(f'albums?ids={ids_param}')
            if not data:
                continue
            for album in data.get('albums', []):
                if album:
                    try:
                        album_info = {
                            'album_id': album['id'],
                            'album_name': album['name'],
                            'album_type': album['album_type'],
                            'artist_id': ','.join([artist['id'] for artist in album.get('artists', [])]),
                            'release_date': album['release_date'],
                            'total_tracks': album['total_tracks'],
                            'markets': json.dumps(album['available_markets']),
                            'popularity': album.get('popularity', 0),
                            'album_uri': album['uri']
                        }
                        all_album_infos.append(album_info)
                    except KeyError as e:
                        logging.error(f"Album batch missing key: {e}")
        return all_album_infos

    def get_artists_batch(self, artist_ids: List[str]) -> List[Dict]:
        all_artist_infos = []
        for i in range(0, len(artist_ids), 50):  
            batch = artist_ids[i:i + 50]
            ids_param = ','.join(batch)
            data = self.make_request(f'artists?ids={ids_param}')
            if not data:
                continue
            for artist in data.get('artists', []):
                if artist:
                    try:
                        artist_info = {
                            'artist_id': artist['id'],
                            'artist_name': artist['name'],
                            'genres': json.dumps(artist['genres']),
                            'followers': artist['followers']['total'],
                            'popularity': artist['popularity'],
                            'artist_uri': artist['uri']
                        }
                        all_artist_infos.append(artist_info)
                    except KeyError as e:
                        logging.error(f"Artist batch missing key: {e}")
        return all_artist_infos

    def get_tracks_batch(self, track_ids: List[str]) -> List[Dict]:
        all_track_infos = []
        for i in range(0, len(track_ids), 50): 
            batch = track_ids[i:i + 50]
            ids_param = ','.join(batch)
            data = self.make_request(f'tracks?ids={ids_param}')
            if not data:
                continue
            for track in data.get('tracks', []):
                if track:
                    try:
                        track_info = {
                            'track_id': track['id'],
                            'track_name': track['name'],
                            'artist_id': track.get('artists', [{}])[0].get('id', ''),
                            'album_id': track['album']['id'],
                            'markets': json.dumps(track['available_markets']),
                            'popularity': track['popularity'],
                            'duration_ms': track['duration_ms'],
                            'track_number': track['track_number'],
                            'disc_number': track['disc_number'],
                            'explicit': bool(track['explicit']),
                            'local': bool(track['is_local']),
                            'track_uri': track['uri']
                        }
                        all_track_infos.append(track_info)
                    except (KeyError, IndexError) as e:
                        logging.error(f"Track batch missing field: {e}")
        return all_track_infos
