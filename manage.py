"""
This file is used to run the application.
"""
import logging
import mimetypes

from app.api import create_api
from app.arg_handler import HandleArgs
from app.periodic_scan import run_periodic_scans
from app.lib.watchdogg import Watcher as WatchDog
from app.settings import FLASKVARS
from app.setup import run_setup
from app.start_info_logger import log_startup_info
from app.utils.filesystem import get_home_res_path
from app.utils.threading import background
from alive_progress import config_handler

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

werkzeug = logging.getLogger("werkzeug")
werkzeug.setLevel(logging.ERROR)

app = create_api()
app.static_folder = get_home_res_path("client")


@app.route("/<path:path>")
def serve_client_files(path):
    """
    Serves the static files in the client folder.
    """
    return app.send_static_file(path)


@app.route("/")
def serve_client():
    """
    Serves the index.html file at `client/index.html`.
    """
    return app.send_static_file("index.html")


@background
def bg_run_setup() -> None:
    run_setup()
    run_periodic_scans()


@background
def start_watchdog():
    WatchDog().run()


def configure_alive_bar():
    """
    Sets the default alive bar settings.
    """
    config_handler.set_global(spinner="classic", bar="classic2", enrich_print=False)


if __name__ == "__main__":
    configure_alive_bar()
    HandleArgs()
    log_startup_info()
    bg_run_setup()
    start_watchdog()

app.run(
    debug=False,
    threaded=True,
    host=FLASKVARS.get_flask_host(),
    port=FLASKVARS.get_flask_port(),
    use_reloader=False,
)

# TODO: Organize code in this file: move args to new file, etc.
