import logging
import mimetypes
import setproctitle
import sys
import os
import multiprocessing
from importlib import resources as impresources
from importlib import metadata as impmetadata
from flask import Response, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
    verify_jwt_in_request,
)

from datetime import datetime, timezone, timedelta
import pathlib
import argparse
import swingmusic
from swingmusic import settings
from swingmusic.api import create_api
from swingmusic.crons import start_cron_jobs
from swingmusic.setup import load_into_mem, run_setup
from swingmusic.plugins.register import register_plugins
from swingmusic.start_info_logger import log_startup_info
from swingmusic.utils.threading import background
from swingmusic.utils.paths import getClientFilesExtensions
from swingmusic.utils.xdg_utils import get_xdg_config_dir


def _load_mimetypes():
    """
    Load mimetypes for the web client's static files
    Loading mimetypes should happen automatically but
    sometimes the mimetypes are not loaded correctly
    eg. when the Registry is messed up on Windows.

    See the following issues:
    https://github.com/swingmx/swingmusic/issues/137
    """


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


def _skip_auth_action():
    """
    Skips the JWT verification for the current request.
    """

    # INFO: Routes that don't need authentication
    whitelisted_routes = {
        "/auth/login",
        "/auth/users",
        "/auth/pair",
        "/auth/logout",
        "/auth/refresh",
        "/docs",
    }
    blacklist_extensions = {".webp", ".jpg"}.union(getClientFilesExtensions())

    if request.path == "/" or any(
        request.path.endswith(ext) for ext in blacklist_extensions
    ):
        return True

    # if request path starts with any of the blacklisted routes, don't verify jwt
    if any(request.path.startswith(route) for route in whitelisted_routes):
        return True

    return False


def create_app(host: str, port: int, config: pathlib.Path):
    settings.Paths.set_config_dir(config)

    _load_mimetypes()

    # logging.disable(logging.CRITICAL)
    # werkzeug = logging.getLogger("werkzeug")
    # werkzeug.setLevel(logging.ERROR)

    waitress_logger = logging.getLogger("waitress")
    waitress_logger.setLevel(logging.ERROR)

    log_startup_info(host, port)

    @background
    def run_swingmusic():
        register_plugins()

        setproctitle.setproctitle(f"swingmusic {host}:{port}")
        start_cron_jobs()

    # Setup function calls
    settings.Info.load()
    run_setup()

    # Create the Flask app
    app = create_api()
    # TODO: rework static files: where should they be located
    app.static_folder = impresources.files(swingmusic) / "client"


    @app.before_request
    def verify_auth():
        """
        Verifies the JWT token before each request.
        """
        if _skip_auth_action():
            return

        verify_jwt_in_request()


    @app.after_request
    def refresh_expiring_jwt(response: Response) -> Response:
        """
        Refreshes the cookies JWT token after each request.

        If the Request has an Authorization header, jwt won't be refreshed.
        Check if jwt expires in under 7 days, refresh jwt
        """

        # INFO: If the request has an Authorization header, don't refresh the jwt
        # Request is probably from the mobile client or a third party
        if _skip_auth_action() or request.headers.get("Authorization"):
            return response

        try:
            exp_timestamp = get_jwt()["exp"]
            target_date = datetime.now(timezone.utc)+ timedelta(days=7)
            target_timestamp = datetime.timestamp(target_date)


            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)

            return response
        except (RuntimeError, KeyError):
            return response


    @app.route("/<path:path>")
    def serve_client_files(path: str):
        """
        Serves the static files in the client folder.
        """
        js_or_css = path.endswith(".js") or path.endswith(".css")
        if not js_or_css:
            return app.send_static_file(path)

        gzipped_path = path + ".gz"
        user_agent = request.headers.get("User-Agent")

        # INFO: Safari doesn't support gzip encoding
        # See issue: https://github.com/swingmx/swingmusic/issues/155
        is_safari = (
            user_agent
            and user_agent.find("Safari") >= 0
            and user_agent.find("Chrome") < 0
        )

        if is_safari:
            return app.send_static_file(path)

        accepts_gzip = request.headers.get("Accept-Encoding", "").find("gzip") >= 0

        if accepts_gzip:
            if os.path.exists(os.path.join(app.static_folder or "", gzipped_path)):
                response = app.make_response(app.send_static_file(gzipped_path))
                response.headers["Content-Encoding"] = "gzip"
                return response

        return app.send_static_file(path)

    @app.route("/")
    def serve_client():
        """
        Serves the index.html file at `client/index.html`.
        """
        return app.send_static_file("index.html")

    load_into_mem()
    run_swingmusic()
    # TrackStore.export()
    # ArtistStore.export()

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