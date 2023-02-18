#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic


def get_spotify_songs():
    print('Fetching songs from Spotify "Liked Songs" playlist...')

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

    print('Finished!')
    return song_lists


def add_songs_to_yt_music(songs):
    print('Searching and adding songs to YouTube Music...')

    yt_brand_account = os.getenv('YT_BRAND_ACCOUNT')
    if yt_brand_account:
        ytmusic = YTMusic('headers_auth.json', yt_brand_account)
    else:
        ytmusic = YTMusic('headers_auth.json')

    playlist_id = ytmusic.create_playlist(title='Liked Songs', description='Liked Songs', privacy_status='PRIVATE')

    for song in songs:
        print(f"Processing \"{song['title']}\" by {song['artist(s)']}")

        query = song['title']
        for artist in song['artist(s)']:
            query += ' ' + artist

        search_results = ytmusic.search(query=query, filter='songs')
        ytmusic.add_playlist_items(playlist_id, [search_results[0]['videoId']])

    print('Done!')


if __name__ == '__main__':
    load_dotenv()
    spotify_songs = get_spotify_songs()
    add_songs_to_yt_music(spotify_songs)
