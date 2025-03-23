import multiprocessing
import pathlib
import click
import sys
from app.arg_handler import handle_build, handle_password_reset
from app.utils.filesystem import get_home_res_path
from app.utils.xdg_utils import get_xdg_config_dir
from manage import run_app


def version(*args, **kwargs):
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
    callback=version,
    help="Show the version and exit",
    is_eager=True,
)
def run(*args, **kwargs):
    run_app(kwargs["host"], kwargs["port"], kwargs["config"])


if __name__ == "__main__":
    multiprocessing.freeze_support()
    run()
