import os
import sys
import click
import pathlib
import pystray
import multiprocessing
from PIL import Image
from typing import Callable
from pystray._base import Icon as PystrayIcon

from swingmusic.start_swingmusic import start_swingmusic
from swingmusic.utils.xdg_utils import get_xdg_config_dir
from swingmusic.utils.filesystem import get_home_res_path
from swingmusic.arg_handler import handle_build, handle_password_reset


class App:
    def __init__(self, host: str, port: int, setup: Callable[[], None]):
        self.host: str = host
        self.port: int = port
        self.icon: PystrayIcon = None
        self.setup = setup
        self.process = multiprocessing.Process(
            target=self.setup, args=(self.host, self.port)
        )

    def start(self, icon: PystrayIcon):
        self.icon = icon
        self.icon.visible = True
        self.process.start()
        self.icon.run()

    def stop(self):
        print("\nShutting down ...", end=" ")
        self.process.terminate()
        self.process.join(timeout=1)
        self.icon.stop()
        print("bye! 👋")


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


def print_version(*args, **kwargs):
    """
    Prints the version of the application.
    """
    if not args[2]:
        return

    path = get_home_res_path("version.txt")
    if not path:
        click.echo("Version file not found.")
        sys.exit(1)

    with open(path, "r") as f:
        version = f.read()

    click.echo(version)
    sys.exit(0)


@click.command(options_metavar="<options>", context_settings={"show_default": True})
@click.option(
    "--build",
    default=False,
    help="Build the project.",
    is_eager=True,
    callback=handle_build,
    is_flag=True,
)
@click.option("--host", default="0.0.0.0", help="Host to run the app on.")
@click.option("--port", default=1970, help="HTTP port to run the app on.")
@click.option(
    "--config",
    default=lambda: get_xdg_config_dir(),
    show_default="XDG_CONFIG_HOME",
    help="Path to the config file.",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        allow_dash=False,
        path_type=pathlib.Path,
    ),
)
@click.option(
    "--password-reset",
    is_flag=True,
    help="Reset the password.",
    is_eager=True,
    callback=handle_password_reset,
)
@click.option(
    "--version",
    is_flag=True,
    default=False,
    callback=print_version,
    help="Show the version and exit",
    is_eager=True,
)
def run(*args, **kwargs):
    """
    Swing Music entry point. All commandline arguments are handled
    here by the click decorators and configuration.
    """
    # INFO: Set the config dir as an environment variable
    os.environ["SWINGMUSIC_XDG_CONFIG_DIR"] = str(
        pathlib.Path(kwargs["config"]).resolve()
    )

    app = App(kwargs["host"], kwargs["port"], start_swingmusic)
    icon = pystray.Icon(
        "Swing Music",
        icon=create_image(64, 64, "black", "white"),
        menu=pystray.Menu(
            pystray.MenuItem("Quit Swing Music", app.stop),
        ),
    )
    app.start(icon)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn")
    run()
