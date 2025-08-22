import argparse
import pathlib
import platform
from importlib.metadata import version

import multiprocessing
from PIL import Image

from swingmusic.settings import default_base_path
from swingmusic.start_swingmusic import start_swingmusic
from swingmusic.utils.filesystem import get_home_res_path
from swingmusic import tools as swing_tools


def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    padding = 7
    icon_path = get_home_res_path("assets/logo-fill.light.ico")
    image = Image.open(icon_path)

    # Calculate new size with padding
    new_size = (width - 2 * padding, height - 2 * padding)

    # Resize the image while maintaining aspect ratio
    image.thumbnail(new_size, Image.Resampling.LANCZOS)

    # Create a new image with padding
    padded_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    # Calculate position to center the image
    x = (width - image.width) // 2
    y = (height - image.height) // 2

    # Paste the resized image onto the padded image
    padded_image.paste(image, (x, y), image)

    return padded_image


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
        swing_tools.handle_password_reset()

    # else start swingmusik
    else:
        start_swingmusic(
            host=args["host"],
            port=args["port"],
            debug=args["debug"],
            base_path=args["config"],
            client=args["client"]
        )


if __name__ == "__main__":
    # TODO: find a platform independent way to access module globals like `Paths`
    multiprocessing.set_start_method("spawn")
    run()
