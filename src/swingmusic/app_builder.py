from importlib import metadata
import datetime as dt
import pathlib
import logging

from flask import Response, request
from flask_cors import CORS
from flask_compress import Compress
from flask_openapi3 import Info
from flask_openapi3 import OpenAPI
from flask_jwt_extended import JWTManager, create_access_token, get_jwt, get_jwt_identity, set_access_cookies, verify_jwt_in_request

from swingmusic import api as swing_api
from swingmusic.config import UserConfig
from swingmusic.db.userdata import UserTable
from swingmusic.settings import Paths
from swingmusic.utils.paths import get_client_files_extensions

from swingmusic.api.plugins import lyrics as lyrics_plugin
from swingmusic.api.plugins import mixes as mixes_plugin

log = logging.getLogger(__name__)
# # # # # # # # # # # # # # # # # #
# Grouped configuration function  #
# # # # # # # # # # # # # # # # # #

def config_app(web):

    # CORS
    CORS(web, origins="*", supports_credentials=True)

    # RESPONSE COMPRESSION
    # Only compress JSON responses
    Compress(web)
    web.config["COMPRESS_MIMETYPES"] = [
        "application/json",
    ]


def config_jwt(web):
    # JWT CONFIGS
    web.config["JWT_VERIFY_SUB"] = False
    web.config["JWT_SECRET_KEY"] = UserConfig().serverId
    web.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
    web.config["JWT_COOKIE_CSRF_PROTECT"] = False
    web.config["JWT_SESSION_COOKIE"] = False

    jwt_expiry = int(dt.timedelta(days=30).total_seconds())
    web.config["JWT_ACCESS_TOKEN_EXPIRES"] = jwt_expiry

    jwt = JWTManager(web)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        userid = identity["id"]
        user = UserTable.get_by_id(userid)

        if user:
            return user.todict()


def load_endpoints(web):
    # Register all the API blueprints
    with web.app_context():
        web.register_api(swing_api.album.api)
        web.register_api(swing_api.artist.api)
        web.register_api(swing_api.stream.api)
        web.register_api(swing_api.search.api)
        web.register_api(swing_api.folder.api)
        web.register_api(swing_api.playlist.api)
        web.register_api(swing_api.favorites.api)
        web.register_api(swing_api.imgserver.api)
        web.register_api(swing_api.settings.api)
        web.register_api(swing_api.colors.api)
        web.register_api(swing_api.lyrics.api)
        web.register_api(swing_api.backup_and_restore.api)
        web.register_api(swing_api.collections.api)

        # Logger
        web.register_api(swing_api.scrobble.api)

        # Home
        web.register_api(swing_api.home.api)
        web.register_api(swing_api.getall.api)

        # Auth
        web.register_api(swing_api.auth.api)


def load_plugins(web):
        # TODO: rework plugin support
        # Plugins
        web.register_api(swing_api.plugins.api)
        web.register_api(lyrics_plugin.api)
        web.register_api(mixes_plugin.api)


# # # # # # # # # # #
# Create App object #
# # # # # # # # # # #

api_info = Info(
    title="Swing Music",
    version=f"v{metadata.version('swingmusic')}",
    description="The REST API exposed by your Swing Music server",
)

app = OpenAPI(__name__, info=api_info, doc_prefix="/docs")


def check_auth_need() -> bool:
    """
    Check if the current request is for a static file.
    We do not need auth for index or static images of index.

    :return: True if static file else False
    """

    # INFO: Routes that don't need authentication
    urls = {
        "/auth/login",
        "/auth/users",
        "/auth/pair",
        "/auth/logout",
        "/auth/refresh",
        "/docs",
    }
    files = {
        ".webp",
        ".jpg",
        *get_client_files_extensions()
    }

    urls = tuple(urls)
    files = tuple(files)

    if request.path == "/" or request.path.endswith(files):
        return True

    # if request path starts with any of the blacklisted routes, don't verify jwt
    if request.path.startswith(urls):
        return True

    return False

# # # # # # # # # # # # #
# global endpoint logic #
# # # # # # # # # # # # #

@app.route("/<path:path>")
def serve_client_files(path: str):
    """
    Serves the static files in the client folder.
    """

    # TODO: rule out possible double /client path.
    # path sometimes prepended with /client like '/client/some.js' resolves to '/client/client/some.js'

    js_or_css = path.endswith(".js") or path.endswith(".css")

    if not js_or_css:
        return app.send_static_file(path)

    # INFO: Safari doesn't support gzip encoding
    # See issue: https://github.com/swingmx/swingmusic/issues/155
    user_agent = request.headers.get("User-Agent", "")
    if "Safari" in user_agent and not "Chrome" in user_agent:
        return app.send_static_file(path)

    if "gzip" in request.headers.get("Accept-Encoding", ""):
        gz_name = path + ".gz"
        gzipped_path = pathlib.Path(app.static_folder or "") / gz_name

        if gzipped_path.exists():
            response = app.make_response(app.send_static_file(gz_name))
            response.headers["Content-Encoding"] = "gzip"
            return response

    return app.send_static_file(path)


@app.route("/")
def serve_client():
    """
    Serves the index.html file at `client/index.html`.
    """
    return app.send_static_file("index.html")


def build() -> OpenAPI:
    """
    Call this function to obtain the final flask/openapi object.

    Do not import app directly as the static_folder can only be set
    when cli args are parsed.

    :return: OpenApi object with all config set
    """

    # set late state config
    app.static_folder = Paths().client_path
    log.info(f"Serving client from '{app.static_folder}'")

    @app.before_request
    def verify_auth():
        """
        Verifies the JWT token before each request.
        """

        if check_auth_need():
            return

        verify_jwt_in_request()

    @app.after_request
    def refresh_expiring_jwt(response: Response):
        """
        Refreshes the cookies JWT token after each request.
        """

        # INFO: If the request has an Authorization header, don't refresh the jwt
        # Request is probably from the mobile client or a third party
        if check_auth_need() or request.headers.get("Authorization"):
            return response

        try:
            exp_timestamp = get_jwt()["exp"]
            until = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=7)

            if until.timestamp() > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)

            return response
        except (RuntimeError, KeyError):
            return response

    config_app(app)
    config_jwt(app)
    load_endpoints(app)
    load_plugins(app)

    return app
