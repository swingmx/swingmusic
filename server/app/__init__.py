from flask import Flask
from flask_cors import CORS

from flask_caching import Cache

config = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}

cache = Cache(config = config)

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config.from_mapping(config)
    cache.init_app(app)

    with app.app_context():
        from . import api
        app.register_blueprint(api.bp, url_prefix='/')

        return app
