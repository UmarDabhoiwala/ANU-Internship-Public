import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from fuzzywuzzy import process
from proompt import generate_songs_from_books, generate_songs_from_movies, generate_songs_from_games

os.environ['SPOTIPY_CLIENT_ID']= ''
os.environ['SPOTIPY_CLIENT_SECRET']= ''
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:3000'

def authenticate_spotify():

    scope = ["playlist-modify-public","user-library-read"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    return sp

def getLast20Saved():
    sp = authenticate_spotify()
    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        last20String = idx, track['artists'][0]['name'], " - ", track['name']

    return last20String

def get_favorite_things(thing):
    books = []
    while True:
        book = input(f"Enter your favorite {thing} (or type 'done' to finish): ")
        if book.lower() == 'done':
            break
        books.append(book)
    return books

def search_songs_on_spotify(sp, song_dict):
    track_uris = []

    for title, artist in song_dict.items():
        query = f"{title} artist:{artist}"
        results = sp.search(query, type="track", limit=1)
        tracks = results["tracks"]["items"]

        if tracks:
            track_uri = tracks[0]["uri"]
            track_uris.append(track_uri)

    return track_uris

def create_and_add_songs_to_playlist(sp, user_id, books, track_uris):
    playlist_name = f"Playlist for books: {books}"
    playlist_description = f"Generated playlist based on the books: {books}"
    new_playlist = sp.user_playlist_create(user_id, playlist_name, description=playlist_description)

    if track_uris:
        sp.playlist_add_items(new_playlist["id"], track_uris)

    return new_playlist["external_urls"]["spotify"]


def find_closest_real_songs(sp, generated_songs, limit=5):
    real_songs = {}

    for title, artist in generated_songs.items():
        query = f"{title}"
        results = sp.search(q = query, type="track", limit=limit)
        tracks = results["tracks"]["items"]

        if tracks:
            track_names = [track["name"] for track in tracks]
            best_match = process.extractOne(title, track_names)
            best_match_index = track_names.index(best_match[0])

            real_songs[tracks[best_match_index]["name"]] = tracks[best_match_index]["artists"][0]["name"]

    return real_songs

sp = authenticate_spotify()

message = []
real_songs = {}
stupid = ""
user_id = sp.current_user()["id"]

def getTrackList(media_type, favorite_media):
    media = ', '.join(favorite_media)
    global stupid
    global message
    global real_songs

    stupid = media

    if media_type == "books":
        generated_songs, message = generate_songs_from_books(media)
    elif media_type == "films":
        generated_songs, message = generate_songs_from_movies(media)
    elif media_type == 'games':
        generated_songs, message = generate_songs_from_games(media)

    real_songs = find_closest_real_songs(sp, generated_songs)

    found_songs = search_songs_on_spotify(sp, real_songs)
    print(f"\nCreated a new playlist with the following songs based on your favorite {media_type} ({media}):")
    listOfTracks = []
    for idx, track_uri in enumerate(found_songs, 1):
        track = sp.track(track_uri)
        trackList = f"{idx}. {track['name']} by {track['artists'][0]['name']}"
        listOfTracks.append(trackList)

    return listOfTracks, media

def moreTracks(media_type, media):
    global message
    global real_songs

    if media_type == "books":
        new_generated_songs, message = generate_songs_from_books(media, message)
    elif media_type == "films":
        new_generated_songs, message = generate_songs_from_movies(media, message)
    elif media_type == "games":
        new_generated_songs, message = generate_songs_from_games(media, message)

    print("New generated songs:", new_generated_songs)

    new_real_songs = find_closest_real_songs(sp, new_generated_songs)
    print("New real songs:", new_real_songs)

    real_songs.update(new_real_songs)

    found_songs = search_songs_on_spotify(sp, real_songs)

    track_list = []
    for idx, track_uri in enumerate(found_songs, 1):
        track = sp.track(track_uri)
        track_list.append(f"{idx}. {track['name']} by {track['artists'][0]['name']}")

    return track_list


def generate_playlist():

    global user_id
    global stupid
    global real_songs



    found_songs = search_songs_on_spotify(sp, real_songs)

    playlist_url = create_and_add_songs_to_playlist(sp, user_id, stupid, found_songs)
    print(f"\nYou can find the playlist at the following URL: {playlist_url}")

    return playlist_url


