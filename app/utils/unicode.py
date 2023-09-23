def handle_unicode(string: str):
    """
    Try resolving unicode characters, else escape them.
    """
    return string.encode("utf-16", "replace").decode("utf-16")
    # try:
    # except:
    # return string.encode("unicode_escape").decode("utf-8")
