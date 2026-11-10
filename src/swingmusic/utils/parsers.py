import functools
import re

from rapidfuzz.utils import default_process
from unidecode import unidecode

from swingmusic.config import UserConfig
from swingmusic.enums.album_versions import ANY_VERSION, VERSION_PATTERNS


@functools.lru_cache(maxsize=8)
def _split_tokens(
    ignore_list: tuple[str, ...], separators: tuple[str, ...]
) -> dict[str, list[tuple[str, bool, int]]]:
    """
    Maps a lowercase first character to its (lowercase token, is_ignored, length) candidates, ignored artists first in list order, then separators longest first.
    """
    tokens = [(i, True) for i in ignore_list if i]
    tokens += [(s, False) for s in sorted((s for s in separators if s), key=len, reverse=True)]

    index: dict[str, list[tuple[str, bool, int]]] = {}
    for token, ignored in tokens:
        lowered = token.lower()
        index.setdefault(lowered[0], []).append((lowered, ignored, len(token)))

    return index


def split_artists(src: str, config: UserConfig):
    """
    Splits a string of artists into a list of artists, preserving those in ignoreList.
    Case-insensitive matching is used for the ignoreList.
    """
    result = []
    current = ""
    i = 0
    index = _split_tokens(tuple(config.artistSplitIgnoreList), tuple(config.artistSeparators))
    lowered = src.lower()

    while i < len(src):
        match = next(
            (
                (ignored, length)
                for token, ignored, length in index.get(lowered[i : i + 1], ())
                if lowered.startswith(token, i)
            ),
            None,
        )

        if match is None:
            current += src[i]
            i += 1
            continue

        ignored, length = match
        if current.strip():
            result.extend([a.strip() for a in current.split(",") if a.strip()])
            current = ""

        # INFO: Ignored artists keep their original case
        if ignored:
            result.append(src[i : i + length])

        i += length

    # Process any remaining current string
    if current.strip():
        result.extend([a.strip() for a in current.split(",") if a.strip()])

    return result


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


def parse_feat_from_title(title: str, config: UserConfig) -> tuple[list[str], str]:
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
    artists = split_artists(artists, config)

    # remove "feat" group from title
    new_title = re.sub(regex, "", title, flags=re.IGNORECASE)
    return artists, new_title


TRAILING_BRACKET = re.compile(r"\s*[(\[]([^)\]]*)[)\]]$")


def normalize_version_text(text: str) -> str:
    """
    Lowercases text and turns each run of non-alphanumeric characters into a space.
    """
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def strip_trailing_brackets(text: str) -> str:
    """
    Removes all trailing bracketed blocks from text.
    """
    while (match := TRAILING_BRACKET.search(text)) and match.start() > 0:
        text = text[: match.start()].rstrip()

    return text


def get_base_album_title(string: str) -> tuple[str, str | None]:
    """
    Splits an album title into the title and its trailing bracketed block,
    when that block names an album version.
    """
    match = TRAILING_BRACKET.search(string)

    if match and ANY_VERSION.search(normalize_version_text(match.group(1))):
        return string[: match.start()].strip(), match.group(0).strip()

    return string, None


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
    Returns the album versions named in a bracketed album title block.
    """
    if not bracket_text:
        return []

    bracket_text = normalize_version_text(bracket_text)
    versions = [
        version.name.lower()
        for version, pattern in VERSION_PATTERNS
        if pattern.search(bracket_text)
    ]

    if "anniversary_edition" in versions:
        versions.remove("anniversary_edition")
        versions.insert(0, get_anniversary(bracket_text))

    return versions


def get_base_title_and_versions(
    original_album_title: str, get_versions=True
) -> tuple[str, list[str]]:
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
    return re.sub(
        r"\s*[\\[(][^)\]]*remaster[^)\]]*[)\]]\s*", "", text, flags=re.IGNORECASE
    ).strip()


def remove_hyphen_remasters(text: str):
    """
    Removes remaster info from a track title that contains a hypen (-) using regex.
    """
    return re.sub(
        r"\s-\s*[^-]*\bremaster[^-]*\s*", "", text, flags=re.IGNORECASE
    ).strip()


def clean_title(title: str) -> str:
    """
    Removes remaster info from a track title using regex.
    """
    if "remaster" not in title.lower():
        return title

    rem_1 = remove_bracketed_remaster(title)
    rem_2 = remove_hyphen_remasters(title)

    return rem_1 if len(rem_2) > len(rem_1) else rem_2


def get_sort_name(name: str, articles: set[str]) -> str:
    """
    Returns artist name stripped of articles for sorting purposes.
    """
    # Early return if no whitespace (single word)
    if " " not in name:
        return name

    # Split into words
    [article, sort_name] = name.split(maxsplit=1)
    return sort_name if article.casefold() in articles else name


SYMBOL_LETTERS = str.maketrans({"$": "s", "¥": "y", "€": "e"})
INWORD_SYMBOL_LETTERS = re.compile(r"(?<=[A-Za-z])[!@](?=[A-Za-z])")


def normalize_search_text(text: str) -> str:
    """
    Lowercase ASCII text with punctuation stripped, for fuzzy matching.
    Symbols used as letters in names (A$AP, ¥$, P!nk) become the letter.
    """
    text = INWORD_SYMBOL_LETTERS.sub(
        lambda m: "i" if m.group() == "!" else "a", text.translate(SYMBOL_LETTERS)
    )
    return " ".join(default_process(unidecode(text)).split())
