# """
# This file contains the TrackColors class for interacting with Track colors documents in MongoDB.
# """
# from app import db
# class TrackColors(db.Mongo):
#     """
#     The class for all track-related database operations.
#     """
#     def __init__(self):
#         super(TrackColors, self).__init__("ALICE_TRACK_COLORS")
#         self.collection = self.db["TRACK_COLORS"]
#     def insert_track_color(self, track_color: dict) -> None:
#         """
#         Inserts a new track object into the database.
#         """
#         return self.collection.update_one(
#             {
#                 "filepath": track_color["filepath"]
#             },
#             {
#                 "$set": track_color
#             },
#             upsert=True,
#         ).upserted_id
#     def get_track_color_by_track(self, filepath: str) -> dict:
#         """
#         Returns a track color object by its filepath.
#         """
#         track_color = self.collection.find_one({"filepath": filepath})
#         return db.convert_one(track_color)
