"""
Requests related to artists
"""
import requests

from app import settings
from app.utils.hashing import create_hash


def fetch_similar_artists(name: str):
    """
    Fetches similar artists from Last.fm
    """
    url = f"https://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist={name}&api_key=" \
          f"{settings.Keys.LASTFM_API_KEY}&format=json&limit=100"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    artists = data["similarartists"]["artist"]

    for artist in artists:
        yield create_hash(artist["name"])
