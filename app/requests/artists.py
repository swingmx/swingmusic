"""
Requests related to artists
"""
from pprint import pprint
import requests

from app import settings
from app.utils.hashing import create_hash
from requests import ConnectionError
import urllib.parse


def fetch_similar_artists(name: str):
    """
    Fetches similar artists from Last.fm
    """
    url = f"https://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist={urllib.parse.quote_plus(name, safe='')}&api_key={settings.Keys.LASTFM_API}&format=json&limit=250"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except ConnectionError:
        return []

    data = response.json()

    try:
        artists = data["similarartists"]["artist"]
    except KeyError:
        return []

    for artist in artists:
        yield create_hash(artist["name"])
