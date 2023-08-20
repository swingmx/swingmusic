import hashlib
import re

from unidecode import unidecode


def create_hash(*args: str, decode=False, limit=10) -> str:
    """
    Creates a simple hash for an album
    """
    str_ = "".join(args)

    if decode:
        str_ = unidecode(str_)

    str_ = str_.lower().strip().replace(" ", "")
    str_ = "".join(t for t in str_ if t.isalnum())
    str_ = re.sub(r"[^a-zA-Z0-9\s]", "", str_)
    str_ = str_.encode("utf-8")
    str_ = hashlib.sha256(str_).hexdigest()
    return str_[-limit:]


def create_folder_hash(*args: str, limit=10) -> str:
    """
    Creates a simple hash for an album
    """
    strings = [s.lower().strip().replace(" ", "") for s in args]

    strings = ["".join([t for t in s if t.isalnum()]) for s in strings]
    strings = [s.encode("utf-8") for s in strings]
    strings = [hashlib.sha256(s).hexdigest()[-limit:] for s in strings]
    return "".join(strings)
