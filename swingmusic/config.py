from dataclasses import dataclass, asdict, field
import json
from pathlib import Path
from typing import Any
from .settings import Paths

# TODO: Publish this on PyPi


def load_artist_ignore_list_from_file(filepath: Path) -> set[str]:
    """
    Loads artist names from a text file.
    Returns an empty set if the file doesn't exist.
    """
    try:
        return {
            line.strip() for line in filepath.read_text().splitlines() if line.strip()
        }
    except FileNotFoundError:
        return set()


def load_default_artist_ignore_list() -> set[str]:
    """
    Loads the default artist ignore list from the text file.
    Returns an empty set if the file doesn't exist.
    """
    default_file = Path(__file__).parent / "data" / "artist_split_ignore.txt"
    return load_artist_ignore_list_from_file(default_file)


def load_user_artist_ignore_list() -> set[str]:
    """
    Loads the user-defined artist ignore list from the config directory.
    Returns an empty set if the file doesn't exist.
    """
    user_file = Path(Paths.get_config_file_path()).parent / "artist_split_ignore.txt"
    return load_artist_ignore_list_from_file(user_file)


@dataclass
class UserConfig:
    _config_path: str = ""
    _artist_split_ignore_file_name: str = "artist_split_ignore.txt"
    # NOTE: only auth stuff are used (the others are still reading/writing to db)
    # TODO: Move the rest of the settings to the config file

    # auth stuff
    # NOTE: Don't expose the userId via the API
    serverId: str = ""
    usersOnLogin: bool = True

    # lists
    rootDirs: list[str] = field(default_factory=list)
    excludeDirs: list[str] = field(default_factory=list)
    artistSeparators: set[str] = field(default_factory=lambda: {";", "/"})
    artistSplitIgnoreList: set[str] = field(
        # TODO: in the future, maybe setup a server where users can contribute to the global ignore list?
        default_factory=lambda: load_default_artist_ignore_list().union(
            load_user_artist_ignore_list()
        )
    )
    genreSeparators: set[str] = field(default_factory=lambda: {"/", ";", "&"})

    # tracks
    extractFeaturedArtists: bool = True
    removeProdBy: bool = True
    removeRemasterInfo: bool = True

    # albums
    mergeAlbums: bool = False
    cleanAlbumTitle: bool = True
    showAlbumsAsSingles: bool = False

    # misc
    enablePeriodicScans: bool = False
    scanInterval: int = 10
    enableWatchdog: bool = False
    showPlaylistsInFolderView: bool = False

    # plugins
    enablePlugins: bool = True
    lastfmApiKey: str = "0553005e93f9a4b4819d835182181806"
    lastfmApiSecret: str = "5e5306fbf3e8e3bc92f039b6c6c4bd4e"
    lastfmSessionKeys: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        """
        Loads the config file and sets the values to this instance
        """
        # set config path locally to avoid writing to file
        config_path = Paths.get_config_file_path()

        try:
            config = self.load_config(config_path)
        except FileNotFoundError:
            self._config_path = config_path
            return

        # loop through the config file and set the values
        for key, value in config.items():
            if key == "artistSplitIgnoreList":
                # Merge with default values and user file values instead of overwriting
                default_values = load_default_artist_ignore_list()
                user_values = load_user_artist_ignore_list()
                setattr(self, key, default_values.union(user_values).union(value))
            else:
                setattr(self, key, value)

        # finally set the config path
        self._config_path = config_path

    def setup_config_file(self) -> None:
        """
        Creates the config file with the default settings
        if it doesn't exist
        """
        # if not exists, create the config file
        if not Path(self._config_path).exists():
            self.write_to_file(asdict(self))

    def load_config(self, path: str) -> dict[str, Any]:
        """
        Reads the settings from the config file.
        Returns a dictget_root_dirs
        """
        with open(path, "r") as f:
            settings = json.load(f)

        return settings

    def write_to_file(self, settings: dict[str, Any]):
        """
        Writes the settings to the config file
        """
        # remove internal attributes
        settings = {k: v for k, v in settings.items() if not k.startswith("_")}

        with open(self._config_path, "w") as f:
            json.dump(settings, f, indent=4, default=list)

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Writes to the config file whenever a value is set
        """
        super().__setattr__(key, value)

        # if is internal attribute, don't write to file
        if key.startswith("_") or not self._config_path:
            return

        self.write_to_file(asdict(self))
