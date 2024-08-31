from dataclasses import dataclass, asdict, field
import json
import os
from typing import Any
from .settings import Paths

# TODO: Publish this on PyPi


@dataclass
class UserConfig:
    _config_path: str = ""
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
        default_factory=lambda: {
            "AC/DC",
            "Bob marley & the wailers",
            "Crosby, Stills, Nash & Young",
        }
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

    # plugins
    enablePlugins: bool = True

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
            setattr(self, key, value)

        # finally set the config path
        self._config_path = config_path

    def setup_config_file(self) -> None:
        """
        Creates the config file with the default settings
        if it doesn't exist
        """
        # if not exists, create the config file
        if not os.path.exists(self._config_path):
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

        print(f"writing to file: {key}={value}")
        self.write_to_file(asdict(self))
