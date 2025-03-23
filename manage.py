"""
This file is used to run the application.
"""

import os
import logging
import mimetypes
import setproctitle
from pathlib import Path

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
    verify_jwt_in_request,
)
from datetime import datetime, timezone
from flask import Response, request

from app import settings
from app.api import create_api
from app.crons import start_cron_jobs
from app.utils.threading import background
from app.setup import load_into_mem, run_setup
from app.plugins.register import register_plugins
from app.start_info_logger import log_startup_info
from app.utils.filesystem import get_home_res_path
from app.utils.paths import getClientFilesExtensions


def run_app(host: str, port: int, config: Path):
    settings.Paths.set_config_dir(config)

    # Load mimetypes for the web client's static files
    # Loading mimetypes should happen automatically but
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
    app.static_folder = get_home_res_path("client")

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

    def skipAuthAction():
        """
        Skips the JWT verification for the current request.
        """
        if request.path == "/" or any(
            request.path.endswith(ext) for ext in blacklist_extensions
        ):
            return True

        # if request path starts with any of the blacklisted routes, don't verify jwt
        if any(request.path.startswith(route) for route in whitelisted_routes):
            return True

        return False

    @app.before_request
    def verify_auth():
        """
        Verifies the JWT token before each request.
        """
        if skipAuthAction():
            return

        verify_jwt_in_request()

    @app.after_request
    def refresh_expiring_jwt(response: Response):
        """
        Refreshes the cookies JWT token after each request.
        """

        # INFO: If the request has an Authorization header, don't refresh the jwt
        # Request is probably from the mobile client or a third party
        if skipAuthAction() or request.headers.get("Authorization"):
            return response

        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now) + 60 * 60 * 24 * 7  # 7 days

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
