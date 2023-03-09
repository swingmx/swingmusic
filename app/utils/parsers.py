import re


def split_artists(src: str, with_and: bool = False):
    exp = r"\s*(?: and |&|,|;)\s*" if with_and else r"\s*[,;]\s*"

    artists = re.split(exp, src)
    return [a.strip() for a in artists]


def parse_artist_from_filename(title: str):
    """
    Extracts artist names from a song title using regex.
    """

    regex = r"^(.+?)\s*[-–—]\s*(?:.+?)$"
    match = re.search(regex, title, re.IGNORECASE)

    if not match:
        return []

    artists = match.group(1)
    artists = split_artists(artists)
    return artists


def parse_title_from_filename(title: str):
    """
    Extracts track title from a song title using regex.
    """

    regex = r"^(?:.+?)\s*[-–—]\s*(.+?)$"
    match = re.search(regex, title, re.IGNORECASE)

    if not match:
        return title

    res = match.group(1)
    # remove text in brackets starting with "official" case-insensitive
    res = re.sub(r"\s*\([^)]*official[^)]*\)", "", res, flags=re.IGNORECASE)
    return res.strip()


def remove_prod(title: str) -> str:
    """
    Removes the producer string in a track title using regex.
    """

    # check if title contain title, if not return it.
    if not ("prod." in title.lower()):
        return title

    # check if title has brackets
    if re.search(r"[()\[\]]", title):
        regex = r"\s?(\(|\[)prod\..*?(\)|\])\s?"
    else:
        regex = r"\s?\bprod\.\s*\S+"

    # remove the producer string
    title = re.sub(regex, "", title, flags=re.IGNORECASE)
    return title.strip()


def parse_feat_from_title(title: str) -> tuple[list[str], str]:
    """
    Extracts featured artists from a song title using regex.
    """
    regex = r"\((?:feat|ft|featuring|with)\.?\s+(.+?)\)"
    # regex for square brackets 👇
    sqr_regex = r"\[(?:feat|ft|featuring|with)\.?\s+(.+?)\]"

    match = re.search(regex, title, re.IGNORECASE)

    if not match:
        match = re.search(sqr_regex, title, re.IGNORECASE)
        regex = sqr_regex

    if not match:
        return [], title

    artists = match.group(1)
    artists = split_artists(artists, with_and=True)

    # remove "feat" group from title
    new_title = re.sub(regex, "", title, flags=re.IGNORECASE)
    return artists, new_title
