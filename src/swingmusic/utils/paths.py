from swingmusic.utils.filesystem import get_home_res_path
from importlib import resources as impresources
import pathlib


def getFlaskOpenApiPath():
    """
    Used to retrieve the path to the flask_openapi3 package

    See: https://github.com/luolingchun/flask-openapi3/issues/147
    """
    return impresources.files("flask_openapi3")


def get_client_files_extensions() -> set:
    """
    Get all file extension from client folder.
    Only checks top-most layer of dir.

    :return: list of file extensions
    """

    client_path = get_home_res_path("client")

    extensions = set()
    for item in pathlib.Path(client_path).iterdir():

        if item.is_file() and len(item.suffix) > 0:
            extensions.add(item.suffix)

    return extensions
