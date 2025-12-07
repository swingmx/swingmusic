import json
from pathlib import Path
from typing import Any
from dataclasses import dataclass, asdict, field, InitVar
from swingmusic.data import ARTIST_SPLIT_IGNORE_LIST
from swingmusic.settings import Paths, Singleton


def load_artist_ignore_list_from_file(filepath: Path) -> set[str]:
    """
    Loads artist names from a text file.

    :params filepath: filepath to file
    :returns: Lines with content as ``set``, else empty ``set``
    """
    if filepath.exists():
        text = filepath.read_text()
        return set([line.strip() for line in text.splitlines() if line.strip()])
    else:
        return set()


def load_default_artist_ignore_list() -> set[str]:
    """
    Loads the default artist-ignore-list from the text file.
    Returns an empty set if the file doesn't exist.
    """
    return ARTIST_SPLIT_IGNORE_LIST


def load_user_artist_ignore_list() -> set[str]:
    """
    Loads the user-defined artist ignore list from the config directory.
    Returns an empty set if the file doesn't exist.
    """
    user_file = Paths().config_dir / "artist_split_ignore.txt"
    if user_file.exists():
        lines = user_file.read_text().splitlines()
        return set([line.strip() for line in lines if line.strip()])
    else:
        return set()


@dataclass
class UserConfig(metaclass=Singleton):
    _finished: bool = field(default=False, init=False)  # if post init succesfully
    _config_path: InitVar[Path] = Path("")
    _artist_split_ignore_file_name: InitVar[str] = "artist_split_ignore.txt"
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

    def __post_init__(self, _config_path, _artist_split_ignore_file_name):
        """
        Loads the config file and sets the values to this instance
        """
        # set config path locally to avoid writing to file
        config_path = Paths().config_file_path

        if config_path.exists():
            config = self.load_config(config_path)
        else:
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

        # finally, set the config path
        self._config_path = config_path
        self._finished = True

    def setup_config_file(self) -> None:
        """
        Creates the config file with the default settings
        if it doesn't exist
        """
        # if not exists, create the config file
        config = Path(self._config_path)
        if not config.exists():
            self.write_to_file(asdict(self))

    def load_config(self, path: Path) -> dict[str, Any]:
        """
        Reads the settings from the config file.
        Returns a dictget_root_dirs
        """
        return json.loads(path.read_text())

    def write_to_file(self, settings: dict[str, Any]):
        """
        Writes the settings to the config file
        """
        # remove internal attributes
        settings = {k: v for k, v in settings.items() if not k.startswith("_")}

        with self._config_path.open(mode="w") as f:
            json.dump(settings, f, indent=4, default=list)

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Writes to the config file whenever a value is set
        """

        # protection.
        # only write to file if post_init completed
        if not self._finished:
            super().__setattr__(key, value)
            return

        super().__setattr__(key, value)

        # if is internal attribute, don't write to file
        if key.startswith("_") or not self._config_path:
            return

        self.write_to_file(asdict(self))
