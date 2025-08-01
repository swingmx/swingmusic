import os
from swingmusic.utils.filesystem import get_home_res_path

def get_client_files_extensions():
    """
    Get all the file extensions for the client files
    """

    client_path = get_home_res_path("client")

    extensions = set()
    for root, dirs, files in os.walk(client_path):
        for file in files:
            ext = file.split(".")[-1]
            extensions.add("." + ext)

    return extensions
