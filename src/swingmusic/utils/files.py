import mimetypes


def guess_mime_type(filename: str):
    """
    Guess the mime type of a file.
    """
    type = mimetypes.guess_type(filename)[0]

    if type is None:
        ext = filename.rsplit(".", maxsplit=1)[-1]
        return f"audio/{ext}"

    return type
