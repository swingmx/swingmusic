"""
This module combines all API blueprints into a single Flask app instance.
"""

from swingmusic.api import (
    album,
    artist,
    collections,
    colors,
    favorites,
    folder,
    imgserver,
    playlist,
    search,
    settings,
    lyrics,
    plugins,
    scrobble,
    home,
    getall,
    auth,
    stream,
    backup_and_restore,
)

from swingmusic.api.plugins import lyrics as lyrics_plugin
from swingmusic.api.plugins import mixes as mixes_plugin
from swingmusic.api.sse import api as events

__all__ = [
    "album", "artist", "collections", "colors", "favorites", "folder", "imgserver", "playlist", "search", "settings",
    "lyrics", "plugins", "scrobble", "home", "getall", "auth", "stream", "backup_and_restore", "events",

    "lyrics_plugin",
    "mixes_plugin"
]
