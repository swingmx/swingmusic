from swingmusic.utils.filesystem import get_home_res_path
from importlib import resources as impresources
import pathlib


def getFlaskOpenApiPath():
    """
    Used to retrieve the path to the flask_openapi3 package

    See: https://github.com/luolingchun/flask-openapi3/issues/147
    """
    return impresources.files("flask_openapi3")


def getClientFilesExtensions():
    """
    Get all the file extensions for the client files
    """

    client_path = get_home_res_path("client")

    extensions = set()
    for files in pathlib.Path(client_path).iterdir():
        for file in files:
            ext = file.suffix
            extensions.add("." + ext)

    return extensions
