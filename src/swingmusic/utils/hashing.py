import hashlib
import xxhash

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
    return xxhash.xxh3_64(str_).hexdigest()
    # str_ = hashlib.sha1(str_).hexdigest()

    # INFO: Return first 5 + last 5 characters
    # return (
    #     str_[: limit // 2] + str_[-limit // 2 :]
    #     if limit % 2 == 0
    #     else str_[: limit // 2] + str_[-limit // 2 - 1 :]
    # )
