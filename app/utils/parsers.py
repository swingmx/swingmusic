import re
from enum import Enum


def split_artists(src: str, with_and: bool = False):
    """
    Splits a string of artists into a list of artists.
    """
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


def get_base_album_title(string) -> tuple[str, str | None]:
    """
    Extracts the base album title from a string.
    """
    pattern = re.compile(r'\s*(\(|\[)[^\)\]]*?(version|remaster|deluxe|edition|expanded|anniversary)[^\)\]]*?(\)|\])$',
                         re.IGNORECASE)
    # TODO: Fix "Redundant character escape '\]' in RegExp "
    match = pattern.search(string)

    if match:
        removed_block = match.group(0)
        title = string.replace(removed_block, '')
        return title.strip(), removed_block.strip()

    return string, None


class AlbumVersionEnum(Enum):
    """
    Enum for album versions.
    """
    Explicit = ("explicit",)

    ANNIVERSARY = ("anniversary",)
    DIAMOND = ("diamond",)
    Centennial = ("centennial",)
    GOLDEN = ("gold",)
    PLATINUM = ('platinum',)
    SILVER = ("silver",)

    EXPANDED = ("expanded",)
    EXTENDED = ("extended",)

    DELUXE = ("deluxe",)
    SUPER_DELUXE = ("super deluxe",)

    LEGACY = ("legacy",)
    SPECIAL = ("special",)
    COLLECTORS_EDITION = ("collector",)
    ARCHIVE = ("archive",)

    Acoustic = ("acoustic",)
    DOUBLE_DISC = ('double disc', 'double disk')

    SUMMER = ("summer",)
    WINTER = ("winter",)
    SPRING = ("spring",)
    FALL = ("fall",)

    BONUS_TRACK = ("bonus track",)

    ORIGINAL = ("original",)
    INTL_VERSION = ("international",)
    UK_VERSION = ("uk version",)
    US_VERSION = ("us version",)

    Limited = ("limited",)

    MONO = ("mono",)
    STEREO = ("stereo",)

    HI_RES = ("Hi-Res",)
    RE_MIX = ("re-mix",)
    RE_RECORDED = ("re-recorded", "rerecorded")
    REISSUE = ("reissue",)
    REMASTER = ("remaster",)


def get_anniversary(text: str) -> str | None:
    """
    Extracts anniversary from text using regex.
    """
    _end = "anniversary"
    match = re.search(r"\b\d+\w*(?= anniversary)", text, re.IGNORECASE)
    if match:
        return match.group(0).strip().lower() + f" {_end}"
    else:
        return _end


def get_album_info(bracket_text: str | None) -> list[str]:
    """
    Extracts album version info from the bracketed text on an album title string using regex.
    """
    if not bracket_text:
        return []

    versions = []

    for version_keywords in AlbumVersionEnum:
        for keyword in version_keywords.value:
            if re.search(keyword, bracket_text, re.IGNORECASE):
                versions.append(version_keywords.name.lower())
                break

    if "anniversary" in versions:
        anniversary = get_anniversary(bracket_text)
        versions.insert(0, anniversary)
        versions.remove("anniversary")

    return versions


def get_base_title_and_versions(original_album_title: str, get_versions=True) -> tuple[str, list[str]]:
    """
    Extracts the base album title and version info from an album title string using regex.
    """
    album_title, version_block = get_base_album_title(original_album_title)

    if version_block is None:
        return original_album_title, []

    if not get_versions:
        return album_title, []

    versions = get_album_info(version_block)

    # if no version info could be extracted, accept defeat!
    if len(versions) == 0:
        album_title = original_album_title

    return album_title, versions


def remove_bracketed_remaster(text: str):
    """
    Removes remaster info from a track title that contains brackets using regex.
    """
    return re.sub(r'\s*[\\[(][^)\]]*remaster[^)\]]*[)\]]\s*', '', text, flags=re.IGNORECASE).strip()


def remove_hyphen_remasters(text: str):
    """
    Removes remaster info from a track title that contains a hypen (-) using regex.
    """
    return re.sub(r'\s-\s*[^-]*\bremaster[^-]*\s*', '', text, flags=re.IGNORECASE).strip()


def clean_title(title: str) -> str:
    """
    Removes remaster info from a track title using regex.
    """
    if "remaster" not in title.lower():
        return title

    rem_1 = remove_bracketed_remaster(title)
    rem_2 = remove_hyphen_remasters(title)

    return rem_1 if len(rem_2) > len(rem_1) else rem_2

    # if "[" in title or "(" in title:
    #     return remove_bracketed_remaster(title)
    #
    # if "-" in title:
    #     return remove_hyphen_remasters(title)
