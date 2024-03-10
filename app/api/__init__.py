"""
This module combines all API blueprints into a single Flask app instance.
"""

import datetime
from flask_cors import CORS
from flask_compress import Compress

from flask_openapi3 import Info
from flask_openapi3 import OpenAPI
from pydantic import BaseModel, Field
from flask_openapi3 import FileStorage

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

# TODO: Move this description to a separate file
open_api_description = f"""
The REST API exposed by your Swing Music server

### Definition of terms:

#### 1. `limit`: The number of items to return.

In endpoints that request multiple lists of items, this represents the number of items to return for each list.

---

[MIT License](https://github.com/swing-opensource/swingmusic?tab=MIT-1-ov-file#MIT-1-ov-file) | Copyright (c) {datetime.datetime.now().year} [Mungai Njoroge](https://mungai.vercel.app)
"""

def create_api():
    """
    Creates the Flask instance, registers modules and registers all the API blueprints.
    """
    api_info = Info(
        title=f"Swing Music",
        version=f"v{Keys.SWINGMUSIC_APP_VERSION}",
        description=open_api_description,
    )

    app = OpenAPI(__name__, info=api_info)

    CORS(app, origins="*")
    Compress(app)

    app.config["COMPRESS_MIMETYPES"] = [
        "application/json",
    ]

    with app.app_context():
        app.register_api(album.api)
        app.register_api(artist.api)
        app.register_api(send_file.api)
        app.register_api(search.api)
        app.register_api(folder.api)
        app.register_api(playlist.api)
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
