import io
import shutil
import tempfile
import zipfile
from importlib import resources as imres
from pathlib import Path

import requests

from swingmusic.settings import Paths, log

CLIENT_RELEASES_URL = "https://api.github.com/repos/swingmx/swingmusic/releases/latest"

def download_client_from_github(destination:Path) -> bool:
    """
    Downloads the latest supported client from Github
    and places it in the swingmusic client folder.

    :args destination: Where the client should be downloaded
    :returns: If successful ``True`` else ``False``
    """

    try:
        answer = requests.get(CLIENT_RELEASES_URL).json()

        for asset in answer["assets"]:
            if asset["name"] == "client.zip":
                # download and convert client
                client = requests.get(asset["browser_download_url"])
                mem_file = io.BytesIO(client.content)
                file = zipfile.ZipFile(mem_file)

                # create new dir for extraction
                log.info(f"Storing client in '{destination.as_posix()}'.")
                with tempfile.TemporaryDirectory() as temp_folder:
                    file.extractall(temp_folder)

                    shutil.copytree(
                        Path(temp_folder) / "client",
                        destination,
                        copy_function=shutil.copy2,
                        dirs_exist_ok=True,
                    )

                break

    except (
            requests.exceptions.RequestException,
            KeyError,
            requests.exceptions.ConnectionError,
    ) as e:
        log.error(
            "Client could not be downloaded from releases. NETWORK ERROR",
            exc_info=e,
        )
        return False
    except requests.exceptions.InvalidJSONError as e:
        log.error(
            "Client could not be downloaded from releases. JSON ERROR",
            exc_info=e,
        )
        return False
    except zipfile.BadZipfile as e:
        log.error("Client could not be unpacked. ZIP ERROR", exc_info=e)
        return False

def extract_default_client(destination: Path):
    """
    Extracts the default client which is bundled with the wheel
    into the swingmusic client folder.

    :args destination: Path to destination
    """
    client_zip_path = imres.files("swingmusic") / "client.zip"

    if (destination/ "index.html").exists():
        # client already exists. Do not copy
        return

    with zipfile.ZipFile(client_zip_path, "r") as zip_ref:
        zip_ref.extractall(destination)

def copy_assets_dir():
    """
    Copies assets to the app directory.
    """

    assets_source = imres.files("swingmusic") / "assets"
    assets_path = Paths().assets_path

    if assets_path.exists():
        return

    if assets_source.exists():
        shutil.copytree(
            Path(assets_source),
            assets_path,
            ignore=shutil.ignore_patterns(
                "*.pyc",
            ),
            copy_function=shutil.copy2,
            dirs_exist_ok=True,
        )
    else:
        log.error(f"Assets dir could not be found: {assets_source.as_posix()}")

def setup_config_dirs():
    """
    Create the config/cache folder structure.

    base folder
    └───`swingmusic` or `.swingmusic`
        ├───images
        │   ├───artists
        │   │   ├───large
        │   │   ├───medium
        │   │   └───small
        │   ├───mixes
        │   │   ├───medium
        │   │   ├───original
        │   │   └───small
        │   ├───playlists
        │   └───thumbnails
        │       ├───large
        │       ├───medium
        │       ├───small
        │       └───xsmall
        └───plugins
            └───lyrics

    """

    config_dir = Paths().config_dir

    # all dirs relative to `swingmusic` config dir
    dirs = [
        "",  # `swingmusic` or `.swingmusic`
        "plugins/lyrics",
        "images/playlists",
        "images/thumbnails/small",
        "images/thumbnails/large",
        "images/thumbnails/medium",
        "images/thumbnails/xsmall",
        "images/artists/medium",
        "images/artists/small",
        "images/artists/large",
        "images/mixes/",
        "images/mixes/original",
        "images/mixes/medium",
        "images/mixes/small",
    ]

    for folder in dirs:
        path = config_dir / folder
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            path.chmod(mode=0o755)

    # Empty files to create
    empty_files = [
        # artist split ignore list
        config_dir
        / "data"
        / "artist_split_ignore.txt"  # TODO: use USERCONFIG -> circular import error || rework userconfig...
    ]

    for file in empty_files:
        if file.is_dir():
            file.rmdir()

        if not file.exists():
            file.parent.mkdir(parents=True, exist_ok=True)
            file.touch()
