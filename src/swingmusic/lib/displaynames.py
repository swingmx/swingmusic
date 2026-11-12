"""
Stylized artist names shown on the artist page.
"""

import json
import logging
from pathlib import Path

from swingmusic.data import ARTIST_DISPLAY_NAMES
from swingmusic.settings import Paths
from swingmusic.utils.hashing import create_hash

log = logging.getLogger(__name__)

def read_names(path: Path) -> dict[str, str]:
    """
    Returns the {artist name: display name} entries in a json file, or {} if unreadable.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as e:
        log.warning("could not read %s: %s", path, e)
        return {}

    if not isinstance(data, dict):
        return {}

    return {str(k): str(v) for k, v in data.items() if v}


class DisplayNames:
    """
    Display names keyed by artisthash: the shipped defaults overlaid by the user file.
    """

    names: dict[str, str] = {}

    @staticmethod
    def user_path() -> Path:
        return Paths().config_dir / "artist_display_names.json"

    @classmethod
    def load(cls):
        entries = {**ARTIST_DISPLAY_NAMES, **read_names(cls.user_path())}
        cls.names = {create_hash(name, decode=True): value for name, value in entries.items()}

    @classmethod
    def get(cls, artisthash: str) -> str | None:
        return cls.names.get(artisthash)

    @classmethod
    def set(cls, artistname: str, display_name: str | None):
        """
        Saves the user's display name for an artist. An empty name removes the user's entry.
        """
        path = cls.user_path()
        entries = read_names(path)
        artisthash = create_hash(artistname, decode=True)
        entries = {k: v for k, v in entries.items() if create_hash(k, decode=True) != artisthash}

        if display_name:
            entries[artistname] = display_name

        path.write_text(json.dumps(entries, indent=4, ensure_ascii=False), encoding="utf-8")
        cls.load()
