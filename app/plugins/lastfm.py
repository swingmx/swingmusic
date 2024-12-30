import requests
from typing import Any
from hashlib import md5
from urllib.parse import quote_plus

from app.config import UserConfig
from app.models.track import Track
from app.utils.auth import get_current_userid
from app.utils.threading import background
from app.plugins import Plugin, plugin_method


class LastFmPlugin(Plugin):
    def __init__(self):
        self.config = UserConfig()
        super().__init__("lastfm", "Last.fm scrobbler")
        self.set_active(
            bool(
                self.config.lastfmApiKey
                and self.config.lastfmApiSecret
                and self.config.lastfmSessionKeys.get(str(get_current_userid()))
            )
        )

    def get_api_signature(self, data: dict[str, Any]) -> str:
        params = {k: v for k, v in data.items()}

        signature = "".join(f"{k}{v}" for k, v in sorted(params.items()))
        signature += self.config.lastfmApiSecret

        return md5(signature.encode("utf-8")).hexdigest()

    def post(self, data: dict[str, Any], useSessionKey: bool = True):
        url = "http://ws.audioscrobbler.com/2.0/?format=json"
        data["api_key"] = self.config.lastfmApiKey
        if useSessionKey:
            data["sk"] = self.config.lastfmSessionKeys.get(str(get_current_userid()))

        data["api_sig"] = self.get_api_signature(data)

        final_url = (
            url + "&" + "&".join(f"{k}={quote_plus(str(v))}" for k, v in data.items())
        )

        return requests.post(final_url)

    def get_session_key(self, token: str):
        data = {
            "method": "auth.getSession",
            "token": token,
        }

        try:
            res = self.post(data, useSessionKey=False)
            return res.json()["session"]["key"]
        except Exception as e:
            print("get_session_key error", e)
            return None

    @plugin_method
    @background
    def scrobble(self, track: Track, timestamp: int):
        print("Last.fm: logging track: ", track.title, "-", track.artists[0]["name"])
        data = {
            "method": "track.scrobble",
            "artist": track.artists[0]["name"],
            "track": track.title,
            "timestamp": timestamp,
            "album": track.album,
            "albumArtist": track.albumartists[0]["name"],
        }

        print("scrobble data:", data)

        try:
            res = self.post(data)
            print("scrobble response:", res.text)
            print("scrobble response json:", res.json())
        except Exception as e:
            print("scrobble error", e)
