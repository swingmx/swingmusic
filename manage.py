"""
This file is used to run the application.
"""
import logging

from app.api import create_api
from app.arg_handler import HandleArgs
from app.functions import run_periodic_checks
from app.lib.watchdogg import Watcher as WatchDog
from app.settings import FLASKVARS
from app.setup import run_setup
from app.start_info_logger import log_startup_info
from app.utils import background, get_home_res_path

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
def run_bg_checks() -> None:
    run_setup()
    run_periodic_checks()


@background
def start_watchdog():
    WatchDog().run()


if __name__ == "__main__":
    HandleArgs()
    log_startup_info()
    run_bg_checks()
    start_watchdog()

    app.run(
        debug=False,
        threaded=True,
        host=FLASKVARS.FLASK_HOST,
        port=FLASKVARS.FLASK_PORT,
        use_reloader=False,
    )

# TODO: Organize code in this file: move args to new file, etc.
