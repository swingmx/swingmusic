from flask import Blueprint
from flask_restful import Api

from .resources import Albums

api_bp = Blueprint("getall", __name__, url_prefix="/getall")
api = Api(api_bp)


api.add_resource(Albums, "/<itemtype>")
