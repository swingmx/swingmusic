from flask import Flask
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)

    from . import api
    app.register_blueprint(api.bp, url_prefix='/')

    return app
