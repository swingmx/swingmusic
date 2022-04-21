from flask import Flask
from flask_caching import Cache
from flask_cors import CORS

config = {"CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300}

cache = Cache(config=config)


def create_app():
    """
    Creates the Flask instance, registers modules and registers all the API blueprints.
    """
    app = Flask(__name__)
    CORS(app)

    app.config.from_mapping(config)
    cache.init_app(app)

    with app.app_context():
        from app.api import album, artist, folder, playlist, search, track

        app.register_blueprint(album.album_bp, url_prefix="/")
        app.register_blueprint(artist.artist_bp, url_prefix="/")
        app.register_blueprint(track.track_bp, url_prefix="/")
        app.register_blueprint(search.search_bp, url_prefix="/")
        app.register_blueprint(folder.folder_bp, url_prefix="/")
        app.register_blueprint(playlist.playlist_bp, url_prefix="/")

        return app
