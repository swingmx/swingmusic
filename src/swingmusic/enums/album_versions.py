import re
from enum import Enum


class AlbumVersionEnum(Enum):
    """
    Enum that registers supported album versions.
    Keywords are lowercase words matched whole against normalized bracket text.
    """

    Explicit = ("explicit",)
    _360_AUDIO = ("360 audio",)

    ANNIVERSARY_EDITION = ("anniversary",)
    DIAMOND_EDITION = ("diamond edition",)
    Centennial_EDITION = ("centennial edition",)
    GOLDEN_EDITION = ("gold edition", "golden edition")
    PLATINUM_EDITION = ("platinum edition",)
    SILVER_EDITION = ("silver edition",)
    ULTIMATE_EDITION = ("ultimate",)

    EXPANDED = ("expanded",)
    EXTENDED = ("extended",)

    DELUXE = ("deluxe",)
    SUPER_DELUXE = ("super deluxe",)
    COMPLETE = ("complete",)

    LEGACY_EDITION = ("legacy",)
    SPECIAL_EDITION = ("special",)
    COLLECTORS_EDITION = ("collector", "collectors")
    ARCHIVE_EDITION = ("archive",)

    Acoustic = ("acoustic",)
    instrumental = ("instrumental", "instrumentals")
    DOUBLE_DISC = ("double disc", "double disk")
    Unplugged = ("unplugged",)

    SUMMER_EDITION = ("summer edition",)
    WINTER_EDITION = ("winter edition",)
    SPRING_EDITION = ("spring edition",)
    FALL_EDITION = ("fall edition",)

    BONUS_EDITION = ("bonus",)
    BONUS_TRACK = ("bonus track", "bonus tracks")

    ORIGINAL = (
        "original version",
        "original edition",
        "original release",
        "original recording",
        "original mix",
        "original mono",
        "original stereo",
        "og",
    )
    INTL_VERSION = ("international",)
    UK_VERSION = ("uk version",)
    US_VERSION = ("us version",)
    PARENTAL_ADVISORY = ("pa version",)

    Limited_EDITION = ("limited",)

    MONO = ("mono",)
    STEREO = ("stereo",)

    HI_RES = ("hi res",)
    RE_MIX = ("re mix",)
    RE_RECORDED = ("re recorded", "rerecorded")
    REISSUE = ("reissue", "reissued")
    REMASTERED = ("remaster", "remastered", "remasters")


def keyword_pattern(keywords) -> re.Pattern:
    """
    A pattern matching any of `keywords` as whole words.
    """
    alternatives = sorted(keywords, key=len, reverse=True)
    return re.compile(r"\b(?:" + "|".join(map(re.escape, alternatives)) + r")\b")


ANY_VERSION = keyword_pattern(k for v in AlbumVersionEnum for k in v.value)
VERSION_PATTERNS = [(v, keyword_pattern(v.value)) for v in AlbumVersionEnum]
