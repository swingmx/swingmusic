import json
from pathlib import Path
import time
import requests
from typing import Any
from hashlib import md5
from urllib.parse import quote_plus

from swingmusic.config import UserConfig
from swingmusic.models.track import Track
from swingmusic.settings import Paths
from swingmusic.utils.auth import get_current_userid
from swingmusic.utils.threading import background
from swingmusic.plugins import Plugin, plugin_method

from swingmusic.logger import log


class LastFmPlugin(Plugin):
    """
    Last.fm scrobbler plugin.
    """

    UPLOADING_DUMPS = False

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
        data = {
            "method": "track.scrobble",
            "artist": track.artists[0]["name"],
            "track": track.title,
            "timestamp": timestamp,
            "album": track.album,
            "albumArtist": track.albumartists[0]["name"],
        }

        success = self.post_scrobble_data({**data})

        if not success:
            self.dump_scrobble(data)
        else:
            self.upload_dumps()

        return success

    def post_scrobble_data(self, data: dict[str, Any]):
        """
        Uploads the scrobble data and handles the
        response from the lastfm scrobble endpoint.
        """
        try:
            res = self.post(data)
        except Exception as e:
            log.warn("scrobble response error" + str(e))
            return False

        try:
            res_json: dict[str, Any] = res.json()
        except requests.exceptions.JSONDecodeError:
            return False

        if res_json.get("error"):
            log.error("LASTFM: scrobble error" + str(res_json))

            if res_json["error"] == 9:
                log.error("LAST.FM: Invalid session key")
                # Invalid session key
                try:
                    self.config.lastfmSessionKeys.pop(str(get_current_userid()))
                except KeyError:
                    pass

                self.config.lastfmSessionKeys = self.config.lastfmSessionKeys
                return False

        if res_json.get("scrobbles", {}).get("@attr", {}).get("accepted") == 1:
            return True

        return False

    # SECTION: Persistence
    def dump_scrobble(self, data: dict[str, Any]):
        """
        Dumps the scrobble data to a file in the lastfm plugin directory.
        """
        dump_dir = Path(Paths.get_plugins_path(), "lastfm")
        if not dump_dir.exists():
            dump_dir.mkdir(parents=True, exist_ok=True)

        path = dump_dir / f"{int(time.time())}.json"

        with open(path, "w") as f:
            json.dump(data, f)

    def upload_dumps(self):
        """
        Uploads the scrobble dumps to the lastfm api.
        """
        if self.UPLOADING_DUMPS:
            return

        self.UPLOADING_DUMPS = True
        dump_dir = Path(Paths.get_plugins_path(), "lastfm")

        if not dump_dir.exists():
            return

        try:
            for file in dump_dir.iterdir():
                with open(file, "r") as f:
                    data = json.load(f)
                    success = self.post_scrobble_data(data)

                    if success:
                        file.unlink()
        finally:
            self.UPLOADING_DUMPS = False
