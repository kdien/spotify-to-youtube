#!/usr/bin/env python3

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

def get_spotify_songs():
    load_dotenv()
    scope = 'user-library-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    song_lists = []

    limit = 50
    offset = 0

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        if len(results['items']) == 0:
            break

        for item in results['items']:
            track = item['track']
            artist_names = []
            for artist in track['artists']:
                artist_names.append(artist['name'])

            song_lists.append({'title': track['name'], 'artist(s)': artist_names})

        offset += limit

    return song_lists


if __name__ == '__main__':
    spotify_songs = get_spotify_songs()
    print(spotify_songs)
