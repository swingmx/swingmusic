"""
__main__ used for executing module directly e.g. `pyhton -m swingmusic`
"""

import os
import multiprocessing
from importlib import metadata as impmetadata
import pathlib
import argparse
from swingmusic.utils.xdg_utils import get_xdg_config_dir
from swingmusic.args import handle_build, handle_password_reset, run_app

parser = argparse.ArgumentParser(
    description="Cli for swingmusic",
)
server = parser.add_argument_group(title="Server")
server.add_argument(
    "--host",
    dest="host",
    nargs="?",
    help="Host to run the app on. (default: %(default)s)",
    default="0.0.0.0",
    const="0.0.0.0"
)
server.add_argument(
    "-p", "--port",
    dest="port",
    nargs="?",
    help="Port to run the app on. (default: %(default)s)",
    default=8080,
    const=8080
)
server.add_argument(
    "-c", "--config",
    dest="config",
    nargs="?",
    help="Config file to load. (default: %(default)s)",
    default=get_xdg_config_dir(),
    const=get_xdg_config_dir(),
    type=pathlib.Path,
)

tools = parser.add_argument_group(title="Tools")
tools.add_argument(
    "--build",
    dest="build",
    action="store_true",
    help="Build the app."
)
tools.add_argument(
    "--password-reset",
    dest="password_reset",
    action="store_true",
    help="Reset password."
)
parser.add_argument(
    "-v", "--version",
    action="version",
    version=f"swingmusic, version {impmetadata.version('swingmusic')}"
)

def main() -> None:
    """
    main functions for interaction with swingmusic.
    can be called directly.
    args are parsed with argparse
    """
    args = vars(parser.parse_args())

    #TODO: check if frozen and then run freeze_support functions

    match args:
        case {"build": True}:
            multiprocessing.freeze_support()
            handle_build()
        case {"password_reset": True}:
            handle_password_reset()
        case _:
            # run checks
            if not args["config"].exists():
                raise ValueError("Path could not be found")

            # TODO: global module wide config
            os.environ["SWINGMUSIC_XDG_CONFIG_DIR"] = str( args["config"].resolve() )
            run_app(args["host"], args["port"], args["config"])

if __name__ == "__main__":
    main()