"""
This file is used to run the application.
"""
import logging
import mimetypes
import os

import setproctitle
from flask import request

from app.telemetry import Telemetry
from app.api import create_api
from app.arg_handler import HandleArgs
from app.lib.watchdogg import Watcher as WatchDog
from app.periodic_scan import run_periodic_scans
from app.settings import FLASKVARS, Keys
from app.setup import run_setup
from app.start_info_logger import log_startup_info
from app.utils.filesystem import get_home_res_path
from app.utils.threading import background
from app.plugins.register import register_plugins

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


# @app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_client_files(path: str):
    """
    Serves the static files in the client folder.
    """
    # js_or_css = path.endswith(".js") or path.endswith(".css")
    # if not js_or_css:
    #     return app.send_static_file(path)

    # gzipped_path = path + ".gz"

    # if request.headers.get("Accept-Encoding", "").find("gzip") >= 0:
    #     if os.path.exists(os.path.join(app.static_folder, gzipped_path)):
    #         response = app.make_response(app.send_static_file(gzipped_path))
    #         response.headers["Content-Encoding"] = "gzip"
    #         return response
    #     else:
    #         return app.send_static_file(path)
    return app.send_static_file(path)


@app.route("/")
def serve_client():
    """
    Serves the index.html file at `client/index.html`.
    """
    return app.send_static_file("index.html")


@background
def bg_run_setup() -> None:
    run_periodic_scans()


@background
def start_watchdog():
    WatchDog().run()


@background
def init_telemetry():
    Telemetry.init()


def run_swingmusic():
    Keys.load()
    HandleArgs()
    log_startup_info()
    run_setup()
    bg_run_setup()
    register_plugins()

    start_watchdog()
    init_telemetry()

    setproctitle.setproctitle(
        f"swingmusic - {FLASKVARS.FLASK_HOST}:{FLASKVARS.FLASK_PORT}"
    )


if __name__ == "__main__":
    run_swingmusic()
    app.run(
        debug=False,
        threaded=True,
        host=FLASKVARS.get_flask_host(),
        port=FLASKVARS.get_flask_port(),
        use_reloader=False,
    )
