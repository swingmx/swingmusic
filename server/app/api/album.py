"""
Contains all the album routes.
"""
from app import api
from app import functions
from app import helpers
from app.lib import albumslib
from app.lib import trackslib
from flask import Blueprint
from flask import request

album_bp = Blueprint("album", __name__, url_prefix="")


@album_bp.route("/")
def say_hi():
    """Returns some text for the default route"""
    return "^ _ ^"


@album_bp.route("/albums")
def get_albums():
    """returns all the albums"""
    albums = []

    for song in api.DB_TRACKS:
        al_obj = {"name": song["album"], "artist": song["artists"]}

        if al_obj not in albums:
            albums.append(al_obj)

    return {"albums": albums}


@album_bp.route("/album/tracks", methods=["POST"])
def get_album_tracks():
    """Returns all the tracks in the given album."""
    data = request.get_json()

    album = data["album"]
    artist = data["artist"]

    songs = trackslib.get_album_tracks(album, artist)
    index = albumslib.find_album(album, artist)
    album = api.ALBUMS[index]

    return {"songs": songs, "info": album}


@album_bp.route("/album/bio", methods=["POST"])
def get_album_bio():
    """Returns the album bio for the given album."""
    data = request.get_json()

    bio = functions.fetch_album_bio(data["album"], data["albumartist"])

    if bio is not None:
        return {"bio": bio}
    else:
        return {"bio": "No bio found."}, 404


@album_bp.route("/album/artists", methods=["POST"])
def get_albumartists():
    """Returns a list of artists featured in a given album."""
    data = request.get_json()

    album = data["album"]
    artist = data["artist"]

    tracks = []

    for track in api.TRACKS:
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
