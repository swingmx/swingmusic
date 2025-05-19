"""
Handles Tool argument functions
"""

import sys
from getpass import getpass

import click
import PyInstaller.__main__ as bundler

from swingmusic import settings
from swingmusic.db.userdata import UserTable
from swingmusic.logger import log
from swingmusic.setup.sqlite import setup_sqlite
from swingmusic.utils.auth import hash_password
from swingmusic.utils.paths import getFlaskOpenApiPath
from swingmusic.utils.wintools import is_windows

from flask import Response, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
    verify_jwt_in_request,
)

from datetime import datetime, timezone


def handle_build(*args, **kwargs):
    """
    Handles the --build argument. Builds the project into a single executable.
    """
    if not args[2]:
        return

    if settings.IS_BUILD:
        click.echo("Can't build the project. Exiting ...")
        sys.exit(0)

    info_keys = [
        "SWINGMUSIC_APP_VERSION",
        "GIT_LATEST_COMMIT_HASH",
        "GIT_CURRENT_BRANCH",
    ]

    lines = []

    for key in info_keys:
        value = settings.Info.get(key)

        if not value:
            log.error(
                f"WARNING: {key} not resolved. Can't build the project. Exiting ..."
            )
            sys.exit(0)

        lines.append(f'{key} = "{value}"\n')

    try:
        # write the info to the config file
        with open("./app/configs.py", "w", encoding="utf-8") as file:
            # copy the api keys to the config file
            file.writelines(lines)

        _s = ";" if is_windows() else ":"

        flask_openapi_path = getFlaskOpenApiPath()
        server_module = "waitress" if is_windows() else "bjoern"

        bundler.run(
            [
                "main.py",
                "--onefile",
                "--name",
                "swingmusic",
                "--clean",
                f"--add-data=assets{_s}assets",
                f"--add-data=client{_s}client",
                f"--add-data=version.txt{_s}.",
                f"--add-data={flask_openapi_path}/templates/static{_s}flask_openapi3/templates/static",
                f"--hidden-import={server_module}",
                "--icon=assets/logo-fill.light.ico",
                "-y",
            ]
        )
    finally:
        # revert and remove the api keys for dev mode
        with open("./app/configs.py", "w", encoding="utf-8") as file:
            lines = [f'{key} = ""\n' for key in info_keys]
            file.writelines(lines)

        sys.exit(0)


def handle_password_reset(*args, **kwargs):
    """
    Handles the --password-reset argument. Resets the password.
    """
    if not args[2]:
        return

    setup_sqlite()

    username: str = ""
    password: str = ""

    # collect username
    try:
        username = input("Enter username: ")
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled! Exiting ...")
        sys.exit(0)

    username = username.strip()
    user = UserTable.get_by_username(username)

    if not user:
        click.echo(f"User {username} not found")
        sys.exit(0)

    # collect password
    try:
        password = getpass("Enter new password: ")
    except KeyboardInterrupt:
        click.echo("\nOperation cancelled! Exiting ...")
        sys.exit(0)

    try:
        UserTable.update_one({"id": user.id, "password": hash_password(password)})
        click.echo("Password reset successfully!")
    except Exception as e:
        click.echo(f"Error resetting password: {e}")
        sys.exit(0)

    sys.exit(0)


## create openapi app.
def create_app(host: str, port: int, config: pathlib.Path):
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
    # TODO: rework static files: where should they be located
    app.static_folder = impresources.files(swingmusic) / "client"

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
