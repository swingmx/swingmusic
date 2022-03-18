import os
import urllib
from typing import List
from flask import Blueprint, request, send_file

from app import functions, instances, helpers, cache, models, prep
from app import albumslib, searchlib
from app import trackslib

bp = Blueprint("api", __name__, url_prefix="")
functions.start_watchdog()

DB_TRACKS = instances.songs_instance.get_all_songs()
ALBUMS: List[models.Album] = []
TRACKS: List[models.Track] = []

home_dir = helpers.home_dir


@helpers.background
def initialize() -> None:
    """
    Runs all the necessary setup functions.
    """
    albumslib.create_everything()
    prep.create_config_dir()
    functions.reindex_tracks()


initialize()


@bp.route("/")
def say_hi():
    """Returns some text for the default route"""
    return "^ _ ^"


SEARCH_RESULTS = {
    "tracks": [],
    "albums": [],
    "artists": [],
}


@bp.route("/search")
def search():
    """
    Returns a list of songs, albums and artists that match the search query.
    """
    query = request.args.get("q") or "Mexican girl"

    albums = searchlib.get_search_albums(query)
    artists_dicts = []

    artist_tracks = searchlib.get_artists(query)

    for song in artist_tracks:
        for artist in song.artists:
            if query.lower() in artist.lower():

                artist_obj = {
                    "name": artist,
                    "image": helpers.check_artist_image(artist),
                }

                if artist_obj not in artists_dicts:
                    artists_dicts.append(artist_obj)

    _tracks = searchlib.get_tracks(query)
    tracks = [*_tracks, *artist_tracks]

    SEARCH_RESULTS.clear()
    SEARCH_RESULTS["tracks"] = tracks
    SEARCH_RESULTS["albums"] = albums
    SEARCH_RESULTS["artists"] = artists_dicts

    return {
        "data": [
            {"tracks": tracks[:5], "more": len(tracks) > 5},
            {"albums": albums[:6], "more": len(albums) > 6},
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
            "tracks": SEARCH_RESULTS["tracks"][start : start + 5],
            "more": len(SEARCH_RESULTS["tracks"]) > start + 5,
        }

    elif type == "albums":
        return {
            "albums": SEARCH_RESULTS["albums"][start : start + 6],
            "more": len(SEARCH_RESULTS["albums"]) > start + 6,
        }

    elif type == "artists":
        return {
            "artists": SEARCH_RESULTS["artists"][start : start + 6],
            "more": len(SEARCH_RESULTS["artists"]) > start + 6,
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

    for track in TRACKS:
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
            "image": helpers.check_artist_image(artist),
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
# @cache.cached()
def get_folder_tree(folder: str):
    """
    Returns a list of all the folders and tracks in the given folder.
    """
    req_dir = folder.replace("|", "/")

    if folder == "home":
        req_dir = home_dir

    dir_content = os.scandir(os.path.join(home_dir, req_dir))

    folders = []
    files = []

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

        if entry.is_file():
            if entry.name.endswith(".flac") or entry.name.endswith(".mp3"):
                files.append(entry)

    files.sort(key=lambda x: os.path.getmtime(x.path))

    songs = []

    for entry in files:
        for track in TRACKS:
            if track.filepath == entry.path:
                songs.append(track)

    return {
        "files": helpers.remove_duplicates(songs),
        "folders": sorted(folders, key=lambda i: i["name"]),
    }


@bp.route("/albums")
def get_albums():
    """returns all the albums"""
    albums = []

    for song in DB_TRACKS:
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

    songs = trackslib.get_album_tracks(album, artist)
    album = albumslib.find_album(album, artist)

    return {"songs": songs, "info": album}


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


@bp.route("/sample")
def get_sample_track():
    """
    Returns a sample track object.
    """

    return instances.songs_instance.get_song_by_album("Legends Never Die", "Juice WRLD")
