from flask import Blueprint
from flask_restful import Api

from .recents import RecentlyAdded

api_bp = Blueprint("home", __name__, url_prefix="/home")
api = Api(api_bp)


api.add_resource(RecentlyAdded, "/recents/added")
