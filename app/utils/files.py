import mimetypes


def get_mime_from_ext(filename: str):
    """
    Constructs a mime type from a file extension.
    """
    ext = filename.rsplit(".", maxsplit=1)[-1]
    return f"audio/{ext}"


def guess_mime_type(filename: str):
    """
    Guess the mime type of a file.
    """
    type = mimetypes.guess_type(filename)[0]

    if type is None:
        return get_mime_from_ext(filename)

    return type
