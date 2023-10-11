import hashlib

from unidecode import unidecode


def create_hash(*args: str, decode=False, limit=10) -> str:
    """
    Creates a simple hash for an album
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
    str_ = hashlib.sha256(str_).hexdigest()
    return str_[-limit:]
