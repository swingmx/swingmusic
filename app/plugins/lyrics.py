import json
import os
import time
from pathlib import Path
from typing import List, Optional

import requests

from app.db.sqlite.plugins import PluginsMethods
from app.plugins import Plugin, plugin_method
from app.settings import Keys, Paths


class LRCProvider:
    """
    Base class for all of the synced (LRC format) lyrics providers.
    """

    session = requests.Session()

    def __init__(self) -> None:
        self.session.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
            }
        )

    def get_lrc_by_id(self, track_id: str) -> Optional[str]:
        """
        Returns the synced lyrics of the song in lrc.

        ### Arguments
        - track_id: The ID of the track defined in the provider database. e.g. Spotify/Deezer track ID
        """
        raise NotImplementedError

    def get_lrc(self, search_term: str) -> Optional[str]:
        """
        Returns the synced lyrics of the song in lrc.
        """
        raise NotImplementedError


class LyricsProvider(LRCProvider):
    """
    Musixmatch provider class
    """

    ROOT_URL = Keys.PLUGIN_LYRICS_ROOT_URL

    def __init__(self) -> None:
        super().__init__()
        self.token = None
        self.session.headers.update(
            {
                "authority": Keys.PLUGIN_LYRICS_AUTHORITY,
                "cookie": "AWSELBCORS=0; AWSELB=0",
            }
        )

    def _get(self, action: str, query: List[tuple]):
        if action != "token.get" and self.token is None:
            self._get_token()

        query.append(("app_id", "web-desktop-app-v1.0"))
        if self.token is not None:
            query.append(("usertoken", self.token))

        t = str(int(time.time() * 1000))
        query.append(("t", t))

        try:
            url = self.ROOT_URL + action
        except TypeError:
            return None

        try:
            response = self.session.get(url, params=query, timeout=10)
        except:
            return None

        if response is not None and response.ok:
            return response

        return None

    def _get_token(self):
        # Check if token is cached and not expired
        plugin_path = Paths.get_lyrics_plugins_path()
        token_path = os.path.join(plugin_path, "token.json")

        current_time = int(time.time())

        if os.path.exists(token_path):
            with open(token_path, "r", encoding="utf-8") as token_file:
                cached_token_data: dict = json.load(token_file)

            cached_token = cached_token_data.get("token")
            expiration_time = cached_token_data.get("expiration_time")

            if cached_token and expiration_time and current_time < expiration_time:
                self.token = cached_token
                return

        # Token not cached or expired, fetch a new token
        res = self._get("token.get", [("user_language", "en")])

        if res is None:
            return

        res = res.json()
        if res["message"]["header"]["status_code"] == 401:
            time.sleep(10)
            return self._get_token()

        new_token = res["message"]["body"]["user_token"]
        expiration_time = current_time + 600  # 10 minutes expiration

        # Cache the new token
        self.token = new_token
        token_data = {"token": new_token, "expiration_time": expiration_time}

        os.makedirs(plugin_path, exist_ok=True)
        with open(token_path, "w", encoding="utf-8") as token_file:
            json.dump(token_data, token_file)

    def get_lrc_by_id(self, track_id: str) -> Optional[str]:
        res = self._get(
            "track.subtitle.get", [("track_id", track_id), ("subtitle_format", "lrc")]
        )

        try:
            res = res.json()
            body = res["message"]["body"]
        except AttributeError:
            return None

        if not body:
            return None

        return body["subtitle"]["subtitle_body"]

    def get_lrc(self, title: str, artist: str) -> Optional[str]:
        res = self._get(
            "track.search",
            [
                ("q_track", title),
                ("q_artist", artist),
                ("page_size", "5"),
                ("page", "1"),
                ("f_has_lyrics", "1"),
                ("s_track_rating", "desc"),
                ("quorum_factor", "1.0"),
            ],
        )

        try:
            body = res.json()["message"]["body"]
        except AttributeError:
            return []

        try:
            tracks = body["track_list"]
        except TypeError:
            return []

        return [
            {
                "track_id": t["track"]["track_id"],
                "title": t["track"]["track_name"],
                "artist": t["track"]["artist_name"],
                "album": t["track"]["album_name"],
                "image": t["track"]["album_coverart_100x100"],
            }
            for t in tracks
        ]


class Lyrics(Plugin):
    def __init__(self) -> None:
        plugin = PluginsMethods.get_plugin_by_name("lyrics_finder")

        if not plugin:
            return

        name = plugin.name
        description = plugin.description

        super().__init__(name, description)

        self.provider = LyricsProvider()

        if plugin:
            self.set_active(bool(int(plugin.active)))

    @plugin_method
    def search_lyrics_by_title_and_artist(self, title: str, artist: str):
        return self.provider.get_lrc(title, artist)

    @plugin_method
    def download_lyrics(self, trackid: str, path: str):
        lrc = self.provider.get_lrc_by_id(trackid)
        is_valid = lrc is not None and lrc.replace("\n", "").strip() != ""

        if not is_valid:
            return None

        path = Path(path).with_suffix(".lrc")

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(lrc)
                return lrc
        except:
            return lrc
