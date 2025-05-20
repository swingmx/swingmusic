"""
Requests related to artists
"""

import urllib.parse

import requests
from requests import ConnectionError, HTTPError, ReadTimeout

from swingmusic.models.lastfm import SimilarArtistEntry
from swingmusic.utils.hashing import create_hash


def fetch_similar_artists(name: str):
    """
    Fetches similar artists from Last.fm
    """
    url = f"https://kerve.last.fm/kerve/similarartists?artist={urllib.parse.quote_plus(name, safe='')}&autocorrect=1&tracks=1&image_size=large&limit=250&format=json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except (ConnectionError, ReadTimeout, HTTPError):
        return None

    data = response.json()

    try:
        artists = data["results"]["artist"]
    except KeyError:
        return []

    return [
        SimilarArtistEntry(
           **{
                "artisthash": create_hash(artist["name"]),
                "name": artist["name"],
                "weight": artist["weight"],
                "listeners": int(artist["listeners"]),
                "scrobbles": int(artist["scrobbles"]),
            }
        )
        for artist in artists
    ]
