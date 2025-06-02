"""
__main__ used for executing module directly e.g. `pyhton -m swingmusic`
"""

import os
import multiprocessing
import sys
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
    default=1970,
    const=1970
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

parser.add_argument(
    "aktion",
    nargs="?",
    help="Aktion to run (default: serve)",
    default="serve",
    const="serve",
    choices=["password-reset", "build", "serve"]
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
        case {"aktion": "build"}:
            multiprocessing.freeze_support()
            handle_build()
        case {"aktion": "password-reset"}:
            handle_password_reset()
        case {"aktion": "serve"}:
            # run checks
            if not args["config"].exists():
                raise ValueError("Path could not be found")

            # TODO: global module wide config
            os.environ["SWINGMUSIC_XDG_CONFIG_DIR"] = str( args["config"].resolve() )
            run_app(args["host"], args["port"], args["config"])
        case _:
            print("Unsupported aktion selected. Aborting")
            sys.exit()

if __name__ == "__main__":
    main()