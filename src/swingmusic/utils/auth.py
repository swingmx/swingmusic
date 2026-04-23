import hmac
import hashlib

from flask_jwt_extended import current_user

from swingmusic.config import UserConfig
from swingmusic.logger import log


def hash_password(password: str, serverId: str = None) -> str:
    """
    Hashes the given password using sha256 algorithm and the user id as salt.

    :param password: The password to hash.

    :return: The hashed password.
    """
    if not serverId:
        serverId = UserConfig().serverId

    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), serverId.encode("utf-8"), 100000
    ).hex()


def check_password(password: str, hashed: str) -> bool:
    """
    This function checks if the given password matches the hashed password.

    :param password: The password to check.
    :param hashed: The hashed password.

    :return: Whether the password matches.
    """

    verified = False
    with_legacy = False

    config = UserConfig()

    # TRY: Verify with legacy serverId
    if config.legacy_serverId:
        verified = hmac.compare_digest(
            hash_password(password, config.legacy_serverId), hashed
        )
        with_legacy = verified

    if not verified:
        verified = hmac.compare_digest(hash_password(password, config.serverId), hashed)

    return verified, with_legacy


def get_current_userid() -> int:
    """
    Get the current session user.
    """
    try:
        return current_user["id"]
    except RuntimeError as e:
        # Catch this error raised during migration execution
        if log:
            log.error("get_current_userid: Unable to get current user id")
            log.error(e)
        # TODO: possible change to other than real userid,
        #       because it is really hard to debug when no fault but data goes to wrong user
        return 1
