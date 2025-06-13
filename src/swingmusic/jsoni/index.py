import os
import json

from typing import Any
from dataclasses import asdict, dataclass


@dataclass
class Jsoni:
    _configpath: str = ""
    _init_complete: bool = False

    # @property
    # def _configpath(self):
    #     """
    #     The path to the config file
    #     """
    #     return None

    @property
    def _config_as_dict(self):
        all_keys = asdict(self)
        # print("all_keys: ", all_keys)
        # remove internal attributes (starting with __)
        return {k: v for k, v in all_keys.items() if not k.startswith("_")}

    def create_file(self):
        # if not exists, create the config file
        if not os.path.exists(self._configpath):
            print("creating file")
            self.write_to_file(self._config_as_dict)

    def write_to_file(self, settings: dict[str, Any]):
        print("writing to file")
        print("settings: ", settings)
        with open(self._configpath, "w") as f:
            json.dump(settings, f, indent=4)

    def __setattr__(self, name: str, value: Any):
        if not self._init_complete:
            print("setting local attr", "name: ", name, ", value: ", value)
            super().__setattr__(name, value)
            return

        # if is internal attribute, set to instance
        # but don't write to file
        super().__setattr__(name, value)
        if name.startswith("_"):
            print("setting local internal attr", "name: ", name, ", value: ", value)
            return

        print("writing attr", "name: ", name, ", value: ", value)
        self.write_to_file(self._config_as_dict)

    def load_config(self):
        with open(self._configpath, "r") as f:
            settings: dict[str, Any] = json.load(f)

        for key, value in settings.items():
            setattr(self, key, value)

    def __post_init__(self):
        if not self._configpath:
            raise AttributeError(
                f"{self.__class__.__name__}: self._configpath is not set"
            )

        print("self: ", self)
        self.create_file()
        self.load_config()
        self._init_complete = True
        print("init complete!!!!")


@dataclass
class MyConfig(Jsoni):
    age: int = 30
    name: str = "John"
    # _configpath: str = "notconfig.json"

    @property
    def _configpath(self):
        return "notconfig.json"


config = MyConfig("notconfig.json")
print("config.name: ", config.name)
config.age = 45
print("config.name: ", config.name)
# config.create_file()
# config.name = "Jane"
