import requests
import base64
import logging
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from dotenv import load_dotenv
import json
import numpy as np


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

    def make_request(self, endpoint: str) -> Optional[Dict]:
        headers = {'Authorization': f'Bearer {self.get_access_token()}'}

        try:
            response = requests.get(f'https://api.spotify.com/v1/{endpoint}',
                                    headers=headers,
                                    timeout=15)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                self.access_token = None
                return self.make_request(endpoint)
            else:
                logging.error(f"API error {response.status_code} for {endpoint}")
                return None
        except Exception as e:
            logging.error(f"Request failed: {str(e)}")
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
                'public': bool(data['public']),
                'playlist_uri': data['uri']
            }
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
                'artist_ids': ','.join([artist['id'] for artist in data.get('artists', [])]),
                'release_date': data['release_date'],
                'total_tracks': data['total_tracks'],
                'markets': json.dumps(data['available_markets']),
                'popularity': data['popularity'],
                'album_uri': data['uri']
            }
        except (KeyError, IndexError) as e:
            logging.error(f"Missing field in album data: {str(e)}")
            return None

    def get_playlist_track_info(self, playlist_id: str) -> List[Dict]:
        tracks_info = []
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=100'

        while url:
            headers = {'Authorization': f'Bearer {self.get_access_token()}'}
            try:
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    for track_item in data.get('items', []):
                        track_data = track_item.get('track')
                        if not track_data:
                            logging.warning(f"Track is None in playlist {playlist_id}: {track_item}")
                            track_data = {}

                        track_info = {
                            'added_at': track_item.get('added_at', np.nan),
                            'track_id': track_data.get('id', np.nan),
                            'track_name': track_data.get('name', np.nan),
                        }
                        tracks_info.append(track_info)

                    url = data.get('next')  
                elif response.status_code == 401:
                    self.access_token = None
                    continue
                else:
                    logging.error(f"API error {response.status_code} for playlist {playlist_id}")
                    break
            except Exception as e:
                logging.error(f"Request failed: {str(e)}")
                break

        return tracks_info

    def get_artist_info(self, artist_id: str) -> Optional[Dict]:
        data = self.make_request(f'artists/{artist_id}')
        if not data:
            return None

        try:
            return {
                'artist_id': data['id'],
                'artist_name': data['name'],
                'genres': json.dumps(data['genres']),
                'followers': data['followers']['total'],
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
                'artist_id': data['artists'][0]['id'],
                'album_id': data['album']['id'],
                'markets': json.dumps(data['available_markets']),
                'popularity': data['popularity'],
                'duration_ms': data['duration_ms'],
                'track_number': data['track_number'],
                'disc_number': data['disc_number'],
                'explicit': bool(data['explicit']),
                'local': bool(data['is_local']),
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
                'followers': data['followers']['total'],
                'user_uri': data['uri']
            }
        except KeyError as e:
            logging.error(f"Missing field in user data: {str(e)}")
            return None
