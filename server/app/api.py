from crypt import methods
import os
from pprint import pprint
import urllib
from typing import List
from flask import Blueprint, request, send_file

from app import functions, instances, helpers, cache, models

bp = Blueprint("api", __name__, url_prefix="")

home_dir = helpers.home_dir

all_the_f_music = helpers.get_all_songs()


def initialize() -> None:
    """
    Runs all the necessary setup functions.
    """
    helpers.create_config_dir()
    helpers.reindex_tracks()
    helpers.start_watchdog()


initialize()


@bp.route("/")
def say_hi():
    """Returns some text for the default route"""
    return "^ _ ^"


def get_tracks(query: str) -> List[models.Track]:
    """
    Gets all songs with a given title.
    """
    return [track for track in all_the_f_music if query.lower() in track.title.lower()]


def get_search_albums(query: str) -> List[models.Track]:
    """
    Gets all songs with a given album.
    """
    return [track for track in all_the_f_music if query.lower() in track.album.lower()]


def get_artists(artist: str) -> List[models.Track]:
    """
    Gets all songs with a given artist.
    """
    return [
        track
        for track in all_the_f_music
        if artist.lower() in str(track.artists).lower()
    ]


search_results = {
    "tracks": [],
    "albums": [],
    "artists": [],
}


@bp.route("/search")
def search_by_title():
    """
    Returns a list of songs, albums and artists that match the search query.
    """
    query = request.args.get("q") or "Mexican girl"

    albums = get_search_albums(query)
    albums_dicts = []
    artists_dicts = []
    search_results.clear()

    for song in albums:
        album_obj = {
            "name": song.album,
            "artist": song.albumartist,
        }

        if album_obj not in albums_dicts:
            albums_dicts.append(album_obj)

    for album in albums_dicts:
        for track in albums:
            if album["name"] == track.album:
                album["image"] = track.image

    for song in get_artists(query):
        for artist in song.artists:
            if query.lower() in artist.lower():

                artist_obj = {
                    "name": artist,
                    "image": "http://0.0.0.0:8900/images/artists/"
                    + artist.replace("/", "::")
                    + ".webp",
                }

                if artist_obj not in artists_dicts:
                    artists_dicts.append(artist_obj)

    tracks = helpers.remove_duplicates(get_tracks(query))

    search_results["tracks"] = tracks
    search_results["albums"] = albums_dicts
    search_results["artists"] = artists_dicts

    return {
        "data": [
            {"tracks": tracks[:5], "more": len(tracks) > 5},
            {"albums": albums_dicts[:6], "more": len(albums_dicts) > 6},
            {"artists": artists_dicts[:6], "more": len(artists_dicts) > 6},
        ]
    }


@bp.route("/search/loadmore")
def search_load_more():
    """
    Returns more songs, albums or artists from a search query.
    """
    type = request.args.get("type")
    start = int(request.args.get("start"))

    if type == "tracks":
        return {
            "tracks": search_results["tracks"][start : start + 5],
            "more": len(search_results["tracks"]) > start + 5,
        }

    elif type == "albums":
        return {
            "albums": search_results["albums"][start : start + 6],
            "more": len(search_results["albums"]) > start + 6,
        }

    elif type == "artists":
        return {
            "artists": search_results["artists"][start : start + 6],
            "more": len(search_results["artists"]) > start + 6,
        }


@bp.route("/populate")
def find_tracks():
    """call the populate function"""
    functions.populate()
    return "🎸"


@bp.route("/album/artists", methods=["POST"])
def get_albumartists():
    """Returns a list of artists featured in a given album."""
    data = request.get_json()

    album = data["album"]
    artist = data["artist"]

    tracks = []

    for track in all_the_f_music:
        if track.album == album and track.albumartist == artist:
            tracks.append(track)

    artists = []

    for track in tracks:
        for artist in track.artists:
            if artist not in artists:
                artists.append(artist)

    final_artists = []
    for artist in artists:
        artist_obj = {
            "name": artist,
            "image": "http://0.0.0.0:8900/images/artists/"
            + artist.replace("/", "::")
            + ".webp",
        }
        final_artists.append(artist_obj)

    return {"artists": final_artists}


@bp.route("/populate/images")
def populate_images():
    """
    Populates the artist images.
    """
    functions.populate_images()
    return "Done"


@bp.route("/artist/<artist>")
@cache.cached()
def get_artist_data(artist: str):
    """Returns the artist's data, tracks and albums"""
    artist = urllib.parse.unquote(artist)
    artist_obj = instances.artist_instance.get_artists_by_name(artist)

    def get_artist_tracks():
        songs = instances.songs_instance.find_songs_by_artist(artist)

        return songs

    artist_songs = get_artist_tracks()
    songs = helpers.remove_duplicates(artist_songs)

    def get_artist_albums():
        artist_albums = []
        albums_with_count = []

        albums = instances.songs_instance.find_songs_by_albumartist(artist)

        for song in albums:
            if song["album"] not in artist_albums:
                artist_albums.append(song["album"])

        for album in artist_albums:
            count = 0
            length = 0

            for song in artist_songs:
                if song["album"] == album:
                    count = count + 1
                    length = length + song["length"]

            album_ = {"title": album, "count": count, "length": length}

            albums_with_count.append(album_)

        return albums_with_count

    return {"artist": artist_obj, "songs": songs, "albums": get_artist_albums()}


@bp.route("/f/<folder>")
@cache.cached()
def get_folder_tree(folder: str):
    """
    Returns a list of all the folders and tracks in the given folder.
    """
    req_dir = folder.replace("|", "/")

    if folder == "home":
        req_dir = home_dir

    dir_content = os.scandir(os.path.join(home_dir, req_dir))

    folders = []

    for entry in dir_content:
        if entry.is_dir() and not entry.name.startswith("."):
            files_in_dir = helpers.run_fast_scandir(entry.path, [".flac", ".mp3"])[1]

            if len(files_in_dir) != 0:
                _dir = {
                    "name": entry.name,
                    "count": len(files_in_dir),
                    "path": entry.path.replace(home_dir, ""),
                }

                folders.append(_dir)

    songs = []

    for track in all_the_f_music:
        if track.folder == req_dir:
            songs.append(track)

    return {
        "files": helpers.remove_duplicates(songs),
        "folders": sorted(folders, key=lambda i: i["name"]),
    }


@bp.route("/albums")
def get_albums():
    """returns all the albums"""
    s = instances.songs_instance.get_all_songs()

    albums = []

    for song in s:
        al_obj = {"name": song["album"], "artist": song["artists"]}

        if al_obj not in albums:
            albums.append(al_obj)

    return {"albums": albums}


@bp.route("/album/tracks", methods=["POST"])
def get_album_tracks():
    """Returns all the tracks in the given album."""
    data = request.get_json()

    album = data["album"]
    artist = data["artist"]

    songs = []

    for track in all_the_f_music:
        if track.albumartist == artist and track.album == album:
            songs.append(track)

    songs = helpers.remove_duplicates(songs)

    album_obj = {
        "name": album,
        "count": len(songs),
        "duration": "56 Minutes",
        "image": songs[0].image,
        "date": songs[0].date,
        "artist": songs[0].albumartist,
        "artist_image": "http://127.0.0.1:8900/images/artists/"
        + songs[0].albumartist.replace("/", "::")
        + ".webp",
    }

    return {"songs": songs, "info": album_obj}


@bp.route("/album/<title>/<artist>/bio")
@cache.cached()
def get_album_bio(title, artist):
    """Returns the album bio for the given album."""
    bio = functions.get_album_bio(title, artist)
    return {"bio": bio}, 200


@bp.route("/file/<trackid>")
def send_track_file(trackid):
    """
    Returns an audio file that matches the passed id to the client.
    """
    try:
        filepath = instances.songs_instance.get_song_by_id(trackid)["filepath"]
        return send_file(filepath, mimetype="audio/mp3")
    except FileNotFoundError:
        return "File not found", 404
