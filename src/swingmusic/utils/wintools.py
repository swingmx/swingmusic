import platform

IS_WIN = platform.system() == "Windows"


# TODO: Check is_windows on app start in settings.py
def is_windows():
    """
    Returns True if the OS is Windows.
    """
    return IS_WIN


def win_replace_slash(path: str):
    if is_windows():
        return path.replace("\\", "/").replace("//", "/")

    return path
