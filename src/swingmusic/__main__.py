import argparse
import pathlib
from importlib.metadata import version

import multiprocessing

from swingmusic.settings import default_base_path
from swingmusic.start_swingmusic import start_swingmusic
from swingmusic import tools as swing_tools

parser = argparse.ArgumentParser(
    prog='swingmusic',
    description='Awesome Music',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

parser.add_argument(
    '-v', '--version',
    action='version',
    version=f"swingmusic v{version('swingmusic')}")
parser.add_argument(
    "--host",
    default="0.0.0.0",
    help="Host to run the app on."
)
parser.add_argument(
    "--port",
    default=1970,
    help="HTTP port to run the app on.",
    type=int
)
parser.add_argument(
    "--debug",
    default=False,
    action="store_true",
    help="If swingmusic should start in debug mode"
)
parser.add_argument(
    "--config",
    default=default_base_path(),
    help="Path to the config file.",
    type=pathlib.Path
)
parser.add_argument(
    "--client",
    help="Path to the Web UI folder.",
    type=pathlib.Path
)

tools = parser.add_argument_group(
    title="Tools"
)
tools.add_argument(
    "--password-reset",
    help="Reset the password.",
    action='store_true'
)

def run(*args, **kwargs):
    """
    Swing Music entry point
    """
    args = parser.parse_args()
    args = vars(args)

    # check tools
    if args["password_reset"]:
        swing_tools.handle_password_reset(args["config"])

    # else start swingmusic
    else:
        start_swingmusic(
            host=args["host"],
            port=args["port"],
            debug=args["debug"],
            base_path=args["config"],
            client=args["client"]
        )


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    run()
