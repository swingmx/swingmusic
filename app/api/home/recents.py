from flask_restful import Resource, reqparse

from app.lib.home.recentlyadded import get_recent_items
from app.lib.home.recentlyplayed import get_recently_played

parser = reqparse.RequestParser()

parser.add_argument("limit", type=int, required=False, default=7, location="args")


class RecentlyAdded(Resource):
    def get(self):
        cutoff = 14

        args = parser.parse_args()
        limit = args["limit"]

        return {"items": get_recent_items(cutoff, limit), "cutoff": cutoff}


class RecentlyPlayed(Resource):
    def get(self):
        args = parser.parse_args()
        limit = args["limit"]

        return {"items": get_recently_played(limit)}
