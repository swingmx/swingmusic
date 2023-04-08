"""
Module for managing the JSON config file.
"""

import json
from enum import Enum
from typing import Type

from app.settings import Db


class ConfigKeys(Enum):
    ROOT_DIRS = ("root_dirs", list[str])
    PLAYLIST_DIRS = ("playlist_dirs", list[str])
    USE_ART_COLORS = ("use_art_colors", bool)
    DEFAULT_ART_COLOR = ("default_art_color", str)
    SHUFFLE_MODE = ("shuffle_mode", str)
    REPEAT_MODE = ("repeat_mode", str)
    AUTOPLAY_ON_START = ("autoplay_on_start", bool)
    VOLUME = ("volume", int)

    def __init__(self, key_name: str, data_type: Type):
        self.key_name = key_name
        self.data_type = data_type

    def get_data_type(self) -> Type:
        return self.data_type


class ConfigManager:
    def __init__(self, config_file_path: str):
        self.config_file_path = config_file_path

    def read_config(self):
        try:
            with open(self.config_file_path) as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

        # in case of errors, return an empty dict

    def write_config(self, config_data):
        with open(self.config_file_path, "w") as f:
            json.dump(config_data, f, indent=4)

    def get_value(self, key: ConfigKeys):
        config_data = self.read_config()
        value = config_data.get(key.key_name)

        if value is not None:
            return key.get_data_type()(value)

    def set_value(self, key: ConfigKeys, value):
        config_data = self.read_config()
        config_data[key.key_name] = value
        self.write_config(config_data)


settings = ConfigManager(Db.get_json_config_path())
a = settings.get_value(ConfigKeys.ROOT_DIRS)
