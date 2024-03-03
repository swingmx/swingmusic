"""
This module combines all API blueprints into a single Flask app instance.
"""

from flask_cors import CORS
from flask_compress import Compress

from flask_openapi3 import Info
from flask_openapi3 import OpenAPI

from app.settings import Keys
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
    api_info = Info(
        title=f"Swing Music",
        version=f"v{Keys.SWINGMUSIC_APP_VERSION}",
        license={"name": "MIT", "url": "https://github.com/swing-opensource/swingmusic?tab=MIT-1-ov-file#MIT-1-ov-file"},
        contact={"name": "Mungai Njoroge", "url": "https://mungai.vercel.app", "email": "geoffreymungai45@gmail.com"},
        description="The REST API exposed by your Swing Music server",
    )

    app = OpenAPI(__name__, info=api_info)

    CORS(app, origins="*")
    Compress(app)

    app.config["COMPRESS_MIMETYPES"] = [
        "application/json",
    ]

    with app.app_context():
        app.register_api(album.api)
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
