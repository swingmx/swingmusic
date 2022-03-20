import os
import urllib
from typing import List
from flask import request, send_file

from app import functions, instances, helpers, cache, db, prep
from app import api


home_dir = helpers.home_dir

# @api.bp.route("/populate")
# def find_tracks():
#     """call the populate function"""
#     functions.populate()
#     return "🎸"


# @api.bp.route("/populate/images")
# def populate_images():
#     """
#     Populates the artist images.
#     """
#     functions.populate_images()
#     return "Done"
