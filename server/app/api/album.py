"""
Contains all the album routes.
"""
from pprint import pprint
from typing import List

from app import api
from app import helpers
from app import models
from app.lib import albumslib
from flask import Blueprint
from flask import request
from app.functions import FetchAlbumBio
from app import instances

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


@album_bp.route("/album", methods=["POST"])
def get_album():
    """Returns all the tracks in the given album."""
    data = request.get_json()
    print(data)
    album, artist = data["album"], data["artist"]
    albumhash = helpers.create_album_hash(album, artist)

    tracks = instances.tracks_instance.find_tracks_by_hash(albumhash)
    tracks = [models.Track(t) for t in tracks]

    album = instances.album_instance.find_album_by_hash(albumhash)

    if not album:
        return {"error": "Album not found."}, 404

    album = models.Album(album)

    album.count = len(tracks)
    album.duration = albumslib.get_album_duration(tracks)

    if (
        album.count == 1
        and tracks[0].title == album.title
        and tracks[0].tracknumber == 1
        and tracks[0].disknumber == 1
    ):
        album.is_single = True

    return {"tracks": tracks, "info": album}


@album_bp.route("/album/bio", methods=["POST"])
def get_album_bio():
    """Returns the album bio for the given album."""
    data = request.get_json()
    fetch_bio = FetchAlbumBio(data["album"], data["albumartist"])
    bio = fetch_bio()

    if bio is None:
        return {"bio": "No bio found."}, 404

    return {"bio": bio}


@album_bp.route("/album/artists", methods=["POST"])
def get_albumartists():
    """Returns a list of artists featured in a given album."""
    data = request.get_json()

    album, artist = data["album"], data["artist"]
    albumhash = helpers.create_album_hash(album, artist)

    tracks = instances.tracks_instance.find_tracks_by_hash(albumhash)
    tracks = [models.Track(t) for t in tracks]

    artists = []

    for track in tracks:
        for artist in track.artists:
            artist = artist.lower()
            if artist not in artists:
                artists.append(artist)

    final_artists = []
    for artist in artists:
        artist_obj = {
            "name": artist,
            "image": helpers.check_artist_image(helpers.create_safe_name(artist)),
        }
        final_artists.append(artist_obj)

    return {"artists": final_artists}
