import sys
import uuid as UUID

from posthog import Posthog
from app.settings import Paths, Keys
from app.utils.hashing import create_hash
from app.utils.network import has_connection
from app.logger import log


USER_ID = ""

try:
    posthog = Posthog(
        project_api_key=Keys.POSTHOG_API_KEY,
        host="https://app.posthog.com",
        disable_geoip=False,
        timeout=30,
    )
except AssertionError:
    log.error("ERROR: POSTHOG_API_KEY not set in environment")
    sys.exit(0)


def create_userid():
    """
    Creates a unique user id for the user and saves it to a file.
    """
    uuid_path = Paths.get_app_dir() + "/userid.txt"
    global USER_ID

    try:
        with open(uuid_path, "r") as f:
            USER_ID = f.read().strip()
    except FileNotFoundError:
        uuid = str(UUID.uuid4())
        USER_ID = "user_" + create_hash(uuid, limit=15)

        with open(uuid_path, "w") as f:
            f.write(USER_ID)


def send_event(event: str):
    """
    Sends an event to posthog.
    """
    global USER_ID
    if has_connection():
        posthog.capture(USER_ID, event=f"v1.3.0-{event}")


def send_artist_visited():
    """
    Sends an event to posthog when an artist page is visited.
    """
    send_event("artist-page-visited")
