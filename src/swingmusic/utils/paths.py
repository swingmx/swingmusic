import os
from swingmusic.settings import Paths

def get_client_files_extensions():
    """
    Get all the file extensions for the client files
    """


    extensions = set()
    for root, dirs, files in os.walk(Paths().client_path):
        for file in files:
            ext = file.split(".")[-1]
            extensions.add("." + ext)

    return extensions
