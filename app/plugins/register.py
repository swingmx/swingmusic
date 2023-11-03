from app.db.sqlite.plugins import PluginsMethods


def register_plugins():
    PluginsMethods.insert_lyrics_plugin()
