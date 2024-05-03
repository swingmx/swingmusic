import hmac
import hashlib

from app.config import UserConfig


def encode_password(password: str) -> str:
    """
    This function encodes the given password.

    :param password: The password to encode.

    :return: The encoded password.
    """

    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), UserConfig().userId.encode("utf-8"), 100000
    ).hex()


def check_password(password: str, encoded: str) -> bool:
    """
    This function checks if the given password matches the encoded password.

    :param password: The password to check.
    :param encoded: The encoded password.

    :return: Whether the password matches.
    """

    return hmac.compare_digest(encode_password(password), encoded)
