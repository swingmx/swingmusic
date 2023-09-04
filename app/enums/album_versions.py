from enum import Enum


class AlbumVersionEnum(Enum):
    """
    Enum for album versions.
    """

    Explicit = ("explicit",)

    ANNIVERSARY_EDITION = ("anniversary",)
    DIAMOND_EDITION = ("diamond",)
    Centennial_EDITION = ("centennial",)
    GOLDEN_EDITION = ("gold",)
    PLATINUM_EDITION = ("platinum",)
    SILVER_EDITION = ("silver",)
    ULTIMATE_EDITION = ("ultimate",)

    EXPANDED = ("expanded",)
    EXTENDED = ("extended",)

    DELUXE = ("deluxe",)
    SUPER_DELUXE = ("super deluxe",)
    COMPLETE = ("complete",)

    LEGACY_EDITION = ("legacy",)
    SPECIAL_EDITION = ("special",)
    COLLECTORS_EDITION = ("collector",)
    ARCHIVE_EDITION = ("archive",)

    Acoustic = ("acoustic",)
    instrumental = ("instrumental",)
    DOUBLE_DISC = ("double disc", "double disk")

    SUMMER_EDITION = ("summer",)
    WINTER_EDITION = ("winter",)
    SPRING_EDITION = ("spring",)
    FALL_EDITION = ("fall",)

    BONUS_EDITION = ("bonus",)
    BONUS_TRACK = ("bonus track",)

    ORIGINAL = ("original",)
    INTL_VERSION = ("international",)
    UK_VERSION = ("uk version",)
    US_VERSION = ("us version",)
    PARENTAL_ADVISORY = ("PA version",)

    Limited_EDITION = ("limited",)

    MONO = ("mono",)
    STEREO = ("stereo",)

    HI_RES = ("Hi-Res",)
    RE_MIX = ("re-mix",)
    RE_RECORDED = ("re-recorded", "rerecorded")
    REISSUE = ("reissue",)
    REMASTERED = ("remaster",)
    TAYLORS_VERSION = ("taylor's version",)


def get_all_keywords():
    return "|".join("|".join(i.value) for i in AlbumVersionEnum)
