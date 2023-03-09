"""
This module combines all API blueprints into a single Flask app instance.
"""

from flask import Flask
from flask_cors import CORS

from app.api import (album, artist, favorites, folder, imgserver, playlist,
                     search, settings, track)


def create_api():
    """
    Creates the Flask instance, registers modules and registers all the API blueprints.
    """
    app = Flask(__name__, static_url_path="")
    CORS(app)

    with app.app_context():
        app.register_blueprint(album.api)
        app.register_blueprint(artist.api)
        app.register_blueprint(track.api)
        app.register_blueprint(search.api)
        app.register_blueprint(folder.api)
        app.register_blueprint(playlist.api)
        app.register_blueprint(favorites.api)
        app.register_blueprint(imgserver.api)
        app.register_blueprint(settings.api)

        return app
