import socket
import threading
import mimetypes

import setproctitle

from swingmusic.start_info_logger import log_startup_info


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


class PortManager:
    def __init__(self, host: str):
        self.host = host

    def test_port(self, port: int):
        try:
            http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            http_server.bind((self.host, port))
            http_server.close()
            return True
        except socket.error as e:
            if e.errno == 48:
                return False
            else:
                raise e


def wsgi_loader(target: str):
    """
    Target loader for Granian's WSGI worker process.

    Called by Granian in each worker process before serving requests.
    Performs all application initialization:
    - Configures mimetypes for static file serving
    - Sets up database and config files
    - Loads all data into memory stores
    - Starts background tasks (plugins, cron jobs)
    - Builds and returns the Flask application

    :param target: The target string passed by Granian (ignored, we build our own app)
    :return: The WSGI application callable
    """
    import os
    from swingmusic import app_builder
    from swingmusic.crons import start_cron_jobs
    from swingmusic.plugins.register import register_plugins
    from swingmusic.setup import load_into_mem, run_setup

    # Configure mimetypes for static file serving
    config_mimetypes()

    # Setup config files and database
    run_setup()

    # Build the Flask/OpenAPI application
    app = app_builder.build()

    # Load all data into memory stores
    load_into_mem()

    # Get host:port from environment for process title
    proc_title = os.environ.get("SWINGMUSIC_PROC_TITLE", "swingmusic")

    # Start background tasks in a daemon thread
    def background_tasks():
        register_plugins()
        setproctitle.setproctitle(proc_title)
        start_cron_jobs()

    background_thread = threading.Thread(target=background_tasks, daemon=True)
    background_thread.start()

    return app


def start_swingmusic(host: str, port: int):
    """
    Creates and starts the Flask application server for Swing Music.

    This function configures Granian as a WSGI server with multiple blocking
    threads to support concurrent SSE connections without blocking other requests.

    The application initialization happens in the worker process via the
    wsgi_loader function, which sets up the database, loads data into memory,
    and starts background tasks.

    :param host: The host address to bind the server to (e.g., 'localhost' or '0.0.0.0')
    :param port: The port number to run the server on
    """
    import os
    from granian import Granian
    from granian.constants import Interfaces

    # Set process title for worker to pick up
    os.environ["SWINGMUSIC_PROC_TITLE"] = f"swingmusic {host}:{port}"

    # Log startup info before Granian takes over
    log_startup_info(host, port)

    # docker needs manual flush
    print("", end="", flush=True)

    server = Granian(
        target="swingmusic.app_builder:app",  # Placeholder, loader overrides this
        address=host,
        port=port,
        interface=Interfaces.WSGI,
        workers=1,
        blocking_threads=8,
        workers_kill_timeout=5,
    )

    server.serve(target_loader=wsgi_loader)
