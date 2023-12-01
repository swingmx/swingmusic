from flask import Blueprint
from flask_restful import Api

from app.api.logger.tracks import LogTrack


api_bp = Blueprint("logger", __name__, url_prefix="/logger")
api = Api(api_bp)


api.add_resource(LogTrack, "/track/log")
