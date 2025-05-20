from swingmusic.db.userdata import PluginTable
from sqlalchemy.exc import IntegrityError


def register_plugins():
    try:
        PluginTable.insert_one(
            {
                "name": "lyrics_finder",
                "active": False,
                "settings": {"auto_download": False},
                "extra": {
                    "description": "Find lyrics from the internet",
                },
            }
        )
    except IntegrityError:
        pass
