#!/usr/bin/env python3

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from dotenv import load_dotenv

scope = 'user-library-read'

if __name__ == '__main__':
    load_dotenv()
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

    # print(json.dumps(song_lists))
    print('Number of songs:', len(song_lists))
