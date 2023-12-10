from flask_restful import Resource, reqparse
from app.db.sqlite.logger.tracks import SQLiteTrackLogger as db

parser = reqparse.RequestParser()
parser.add_argument("trackhash", type=str, required=True)
parser.add_argument("timestamp", type=int, required=True)
parser.add_argument("duration", type=int, required=True)
parser.add_argument("source", type=str, required=True)


class LogTrack(Resource):
    def post(self):
        args = parser.parse_args(strict=True)

        last_row = db.insert_track(
            args["trackhash"], args["duration"], args["source"], args["timestamp"]
        )

        return {"last_row": last_row}
