# Only external imports - circular import error
import multiprocessing as mp
import os
from pathlib import Path
# ----- Metaclasses -----


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in Singleton._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# ----- Default and Constants -----


class Defaults:
    """
    Contains default values for various settings.

    XSM_THUMB_SIZE: extra small thumbnail size for web client tracklist
    SM_THUMB_SIZE: small thumbnail size for android client tracklist
    MD_THUMB_SIZE: medium thumbnail size for web client album cards
    LG_THUMB_SIZE: large thumbnail size for web client now playing album art

    NOTE: LG_ARTIST_IMG_SIZE is undefined to save the images in their original size (500px)
    """

    XSM_THUMB_SIZE = 64
    SM_THUMB_SIZE = 96
    MD_THUMB_SIZE = 256
    LG_THUMB_SIZE = 512

    SM_ARTIST_IMG_SIZE = 128
    MD_ARTIST_IMG_SIZE = 256

    HASH_LENGTH = 16
    API_ALBUMHASH = "bfe300e966"
    API_ARTISTHASH = "cae59f1fc5"
    API_TRACKHASH = "0853280a12"
    API_ALBUMNAME = "The Goat"
    API_ARTISTNAME = "Polo G"
    API_TRACKNAME = "Martin & Gina"
    API_CARD_LIMIT = 6


class TCOLOR:
    """
    Terminal colors
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    YELLOW = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    # credits: https://stackoverflow.com/a/287944


# ----- Config Store for multithreading -----

def is_main_process() -> bool:
    """
    Test if current process is main process.

    :returns: True if main process else False
    """
    return mp.current_process().name == "MainProcess"

def main_protection(func) -> callable:
    """
    decorator only allows action when process is main process.

    :returns: wrapper function
    """

    def wrapper(*args, **kwargs):
        if is_main_process():
            func(*args, **kwargs)
        else:
            raise RuntimeWarning("You are trying to set a variable in a forked process. Values are not saved!")

    return wrapper

class EnvStore(metaclass=Singleton):
    """
    This class stores variables in a multiprocessing save way.
    Vars can only be written in the main process, other resolve to exception.
    """

    # config used in class
    env_name = "SWINGMUSIC_STORE_"

    def __init__(self, config:Path|None=None):

        if mp.current_process() == "MainProcess":
            if config is None:
                raise ValueError("client or config cannot be None")
            else:
                self["CONFIG_DIR"] = config

    @main_protection
    def __setitem__(self, key, value):
        key = self.env_name + str(key)
        if key in os.environ:
            raise KeyError("Key already exists and cannot be overwritten")
        else:
            os.environ[key] = str(value)

    def __getitem__(self, item):
        key = self.env_name  + str(item)
        if key in os.environ:
            return os.environ[key]
        else:
            raise KeyError(f"Key '{key}' could not be found in EnvStore")

    @main_protection
    def __delitem__(self, key):
        del self[key]

    @main_protection
    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self[item]

    @main_protection
    def __delattr__(self, item):
        del self[item]

    def __iter__(self):
        for key, value in os.environ.items():
            if key.startswith(self.env_name):
                yield key,value

    def __contains__(self, item):
        return item in os.environ
