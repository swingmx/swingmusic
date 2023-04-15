import os


def get_xdg_config_dir():
    """
    Returns the XDG_CONFIG_HOME environment variable if it exists, otherwise
    returns the default config directory. If none of those exist, returns the
    user's home directory.
    """
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")

    if xdg_config_home:
        return xdg_config_home

    try:
        alt_dir = os.path.join(os.environ.get("HOME"), ".config")

        if os.path.exists(alt_dir):
            return alt_dir
    except TypeError:
        return os.path.expanduser("~")
