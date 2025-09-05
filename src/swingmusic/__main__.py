import argparse
import multiprocessing
import pathlib
from importlib.metadata import version

import swingmusic.utils.filesystem as fsys
from swingmusic import shared
from swingmusic import tools as swing_tools
from swingmusic.logger import setup_logger
from swingmusic.start_swingmusic import start_swingmusic
from swingmusic.utils import network

parser = argparse.ArgumentParser(
    prog="swingmusic",
    description="Awesome Music"
)

parser.add_argument(
    "-v", "--version",
    action="version",
    version=f"swingmusic v{version('swingmusic')}")
parser.add_argument(
    "--host",
    default="0.0.0.0",
    help="Host to run the app on. (default: 0.0.0.0)"
)
parser.add_argument(
    "--port",
    default=1970,
    help="HTTP port to run the app on. (default: 1970)",
    type=int
)
parser.add_argument(
    "--debug",
    default=False,
    action="store_true",
    help="If swingmusic should start in debug mode (default: False)"
)
parser.add_argument(
    "--config",
    help=f"The config folder directory (default: {fsys.get_default_config_path()})",
    type=pathlib.Path
)
parser.add_argument(
    "--client",
    help=f"Path to the Web UI folder. (default: {fsys.get_default_config_path() / 'client'})",
    type=pathlib.Path
)

tools = parser.add_argument_group(title="Tools")
tools.add_argument(
    "--password-reset",
    help="Reset the password.",
    action="store_true"
)


def run(*args, **kwargs):
    """
    Swing Music entry point

    Checks config and client path.
    On error resolves to default path.
    """
    args = vars(parser.parse_args())

    # TODO: use 'match case' if we ditch 3.11 support ...
    if args["password_reset"]:
        return swing_tools.handle_password_reset(args["config"])

    else:
        # calculate config and client path and store globally.
        config_path = fsys.get_default_config_path(args["config"]).resolve()
        setup_logger(debug=args["debug"], app_dir=config_path)
        store = shared.EnvStore(config_path)

        if args["client"] is not None:
            if fsys.validate_client_path(args["client"]):
                store["CLIENT_DIR"] = pathlib.Path(args["client"]).resolve()
            else:
                print(shared.TCOLOR.BOLD + shared.TCOLOR.FAIL + f"The client path '{args['client']}' is not valid.")
                print("Please update the client path. Exiting" + shared.TCOLOR.ENDC)
                return 1
        else:
            store["CLIENT_DIR"] = fsys.get_default_client_path(config_path).resolve()


        host = args["host"]
        port = args["port"]

        if not network.is_address_used(host, port):
            return start_swingmusic(host=host, port=port)
        else:
            print(shared.TCOLOR.FAIL + f"Provided address '{host}:{port}' is already used.")
            print("Please either update the 'host' or 'port'. Exiting." + shared.TCOLOR.ENDC)
            return 1


if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn")
    run()