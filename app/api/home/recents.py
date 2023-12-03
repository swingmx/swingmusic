from flask_restful import Resource, reqparse

from app.lib.home.recents import get_recent_items

parser = reqparse.RequestParser()

parser.add_argument("limit", type=int, required=False, default=7, location="args")


class RecentlyAdded(Resource):
    def get(self):
        cutoff = 14

        args = parser.parse_args()
        limit = args["limit"]

        return {"items": get_recent_items(cutoff, limit), "cutoff": cutoff}
