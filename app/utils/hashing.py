import hashlib

from unidecode import unidecode


def create_hash(*args: str, decode=False, limit=10) -> str:
    """
    This function creates a case-insensitive, non-alphanumeric chars ignoring hash from the given arguments.

    Example use case:
        - Creating computable IDs for duplicate artists. eg. Juice WRLD and Juice Wrld should have the same ID.

    :param args: The arguments to hash.
    :param decode: Whether to decode the arguments before hashing.
    :param limit: The number of characters to return.

    :return: The hash.
    """

    def remove_non_alnum(token: str) -> str:
        token = token.lower().strip().replace(" ", "")
        t = "".join(t for t in token if t.isalnum())

        if t == "":
            return token

        return t

    str_ = "".join(remove_non_alnum(t) for t in args)

    if decode:
        str_ = unidecode(str_)

    str_ = str_.encode("utf-8")
    str_ = hashlib.md5(str_).hexdigest()
    # REVIEW Switched to md5 hashlib.sha256(str_).hexdigest()
    return str_[-limit:]
