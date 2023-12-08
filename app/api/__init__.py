"""
This module combines all API blueprints into a single Flask app instance.
"""

from flask import Flask
from flask_compress import Compress
from flask_cors import CORS

from .plugins import lyrics as lyrics_plugin
from app.api import (
    album,
    artist,
    colors,
    favorites,
    folder,
    imgserver,
    playlist,
    search,
    send_file,
    settings,
    lyrics,
    plugins,
    logger,
    home,
    getall,
)


def create_api():
    """
    Creates the Flask instance, registers modules and registers all the API blueprints.
    """
    app = Flask(__name__)
    CORS(app, origins="*")
    Compress(app)

    app.config["COMPRESS_MIMETYPES"] = [
        "application/json",
    ]

    with app.app_context():
        app.register_blueprint(album.api)
        app.register_blueprint(artist.api)
        app.register_blueprint(send_file.api)
        app.register_blueprint(search.api)
        app.register_blueprint(folder.api)
        app.register_blueprint(playlist.api)
        app.register_blueprint(favorites.api)
        app.register_blueprint(imgserver.api)
        app.register_blueprint(settings.api)
        app.register_blueprint(colors.api)
        app.register_blueprint(lyrics.api)

        # Plugins
        app.register_blueprint(plugins.api)
        app.register_blueprint(lyrics_plugin.api)

        # Logger
        app.register_blueprint(logger.api_bp)

        # Home
        app.register_blueprint(home.api_bp)

        # Flask Restful
        app.register_blueprint(getall.api_bp)

        return app
