def handle_unicode(string: str):
    """
    Handles Unicode errors by ignoring unicode characters
    """
    return string.encode("utf-16", "ignore").decode("utf-16")