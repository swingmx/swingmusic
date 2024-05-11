import os
import sys

from app.utils.filesystem import get_home_res_path


def getFlaskOpenApiPath():
    """
    Used to retrieve the path to the flask_openapi3 package

    See: https://github.com/luolingchun/flask-openapi3/issues/147
    """
    site_packages_path = [p for p in sys.path if "site-packages" in p][0]

    return f"{site_packages_path}/flask_openapi3"


def getClientFilesExtensions():
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
