import sys
import uuid as UUID

from posthog import Posthog

from app.logger import log
from app.settings import Keys, Paths, Release
from app.utils.hashing import create_hash
from app.utils.network import has_connection


class Telemetry:
    """
    Handles sending telemetry data to posthog.
    """

    user_id = ""
    off = False

    @classmethod
    def init(cls) -> None:
        try:
            cls.posthog = Posthog(
                project_api_key=Keys.POSTHOG_API_KEY,
                host="https://app.posthog.com",
                disable_geoip=False,
            )

            cls.create_userid()
        except AssertionError:
            cls.disable_telemetry()

    @classmethod
    def create_userid(cls):
        """
        Creates a unique user id for the user and saves it to a file.
        """
        uuid_path = Paths.get_app_dir() + "/userid.txt"

        try:
            with open(uuid_path, "r") as f:
                cls.user_id = f.read().strip()
        except FileNotFoundError:
            uuid = str(UUID.uuid4())
            cls.user_id = "user_" + create_hash(uuid, limit=15)

            with open(uuid_path, "w") as f:
                f.write(cls.user_id)

    @classmethod
    def disable_telemetry(cls):
        cls.off = True

    @classmethod
    def send_event(cls, event: str):
        """
        Sends an event to posthog.
        """
        if cls.off:
            return

        if has_connection():
            cls.posthog.capture(cls.user_id, event=f"v{Release.APP_VERSION}-{event}")

    @classmethod
    def send_artist_visited(cls):
        """
        Sends an event to posthog when an artist page is visited.
        """
        cls.send_event("artist-page-visited")
