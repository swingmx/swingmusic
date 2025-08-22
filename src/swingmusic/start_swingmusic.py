from swingmusic import settings, app_builder
from swingmusic.crons import start_cron_jobs
from swingmusic.plugins.register import register_plugins
from swingmusic.setup import load_into_mem, run_setup
from swingmusic.start_info_logger import log_startup_info
from swingmusic.utils.threading import background
from swingmusic.logger import setup_logger

import pathlib
import setproctitle

import mimetypes



def config_mimetypes():
    # Load mimetypes for the web client's static files
    # Loading mimetypes should happen automaticaly but
    # sometimes the mimetypes are not loaded correctly
    # eg. when the Registry is messed up on Windows.

    # See the following issues:
    # https://github.com/swingmx/swingmusic/issues/137

    mimetypes.add_type("text/css", ".css")
    mimetypes.add_type("text/javascript", ".js")
    mimetypes.add_type("text/plain", ".txt")
    mimetypes.add_type("text/html", ".html")
    mimetypes.add_type("image/webp", ".webp")
    mimetypes.add_type("image/svg+xml", ".svg")
    mimetypes.add_type("image/png", ".png")
    mimetypes.add_type("image/vnd.microsoft.icon", ".ico")
    mimetypes.add_type("image/gif", ".gif")
    mimetypes.add_type("font/woff", ".woff")
    mimetypes.add_type("application/manifest+json", ".webmanifest")


def start_swingmusic(host: str, port: int, debug: bool, base_path:pathlib.Path, client:pathlib.Path|None):
    """
    Creates and starts the Flask application server for Swing Music.

    This function sets up the Flask application with all necessary
    configurations, including static file handling, authentication middleware, and
    server setup, then runs it. It also sets up background tasks and cron jobs.

    .. note::
        The application uses either bjoern or waitress as the WSGI server,
        depending on availability. It also includes JWT authentication,
        static file serving with gzip compression support, and automatic
        token refresh functionality.

    :param host: The host address to bind the server to (e.g., 'localhost' or '0.0.0.0')
    :param port: The port number to run the server on
    :param debug: If swingmusic should start in debug mode
    :param base_path: On which path to store config
    :param client: Path to static client file
    """

    # Example: Setting up dirs, database, and loading stuff into memory.
    # TIP: Be careful with the order of the setup functions.
    # NOTE: concurrent and multithreading create own sys.modules -> no globals
    settings.Paths(base_path.resolve(), client)
    setup_logger(debug=debug)

    config_mimetypes()
    run_setup()

    @background
    def run_swingmusic():
        register_plugins()

        setproctitle.setproctitle(f"swingmusic {host}:{port}")
        start_cron_jobs()


    app = app_builder.build()

    log_startup_info(host, port)
    load_into_mem()
    run_swingmusic()
    # TrackStore.export()
    # ArtistStore.export()

    # docker needs manual flush
    print("", end="", flush=True)

    try:
        import bjoern

        bjoern.run(app, host, port)
    except ImportError:
        import waitress

        waitress.serve(
            app,
            host=host,
            port=port,
            threads=100,
            ipv6=True,
            ipv4=True,
        )