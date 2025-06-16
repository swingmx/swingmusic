import datetime
import pathlib
from pathlib import Path
from typing import Iterable

from swingmusic.store.tracks import TrackStore


def parse_lyrics_lines(lyrics:str) -> list[dict]:
    """
    Split lyrics into lines and determine there tag type.

    Parses the tag if the following format is present: [tag]*[tags] <body>
    else tag_type is unknown
    tag-type and tags are lists combined by their index


    :param lyrics: Full lyrics body
    :return: {'tag_types', 'body', 'tags'}
    """


    entries = []
    for line in lyrics.splitlines():

        data = {
            "tag_types": [],
            "tags": []
        }
        if line.startswith("["):

            # loop until all tags are parsed in line
            while True:
                if "[" in line and "]" in line: # second tag
                    bracket_content, after_content = line.split("]", 1)
                    bracket_content = bracket_content.removeprefix("[")

                    data["tags"].append(bracket_content)
                    data["body"] = after_content

                    line = after_content

                    # check which tag type it is
                    if bracket_content[0].isnumeric():
                        data["tag_types"].append( "time" )

                    elif bracket_content[0].isalpha():
                        data["tag_types"].append( "meta" )
                else:
                    # if no brackets inside the line, there is also no tag.
                    break

        elif line.startswith("#"):
            data["tag_types"].append("comment")
            data["tags"] = ""
            data["body"] = line

        else:
            data["tag_types"].append("unknown")
            data["tags"] = "unknown"
            data["body"] = line

        entries.append(data)

    return entries


def filter_parse_lyrics_lines(lines:list[dict], tag_types:list|str) -> list[dict]:
    """
    filter all lyrics line to only contain given tags

    :param lines: list returned by `parse_lyrics_lines`
    :param tag_types: list or string of tags return should contain
    """

    if isinstance(tag_types, str):
        tag_types = [tag_types]

    found_tags = []

    # line = {"tags", "body", "tag_types"}
    for line in lines:
        group = {
            "tag_types": [],
            "tags": []
        }
        for (tag, tag_type) in zip(line["tags"], line["tag_types"]):
            if tag_type in tag_types:
                group["tag_types"].append(tag_type)
                group["tags"].append(tag)
                group["body"] = line["body"]

        # filter out no match
        if len(group["tags"]) > 0:
            found_tags.append(group)

    return found_tags


def parse_time_tag(lines:list[dict]) -> list[dict]:
    """
    Filter time-tags from lines and parse them.
    """

    # filter tag-type time
    # format into dict with timestamps

    parsed_times = []
    time_tags = filter_parse_lyrics_lines(lines, "time")

    # line = {"tags", "body", "tag_types"}
    for line in time_tags:
        for (tag, tag_type) in zip(line["tags"], line["tag_types"]):
            minute, seconds = tag.split(":", 1)

            parsed_times.append({
            "minute": minute,
            "seconds": seconds,
            "body": line["body"],
            })

    return parsed_times


class Lyrics:

    SUPPORTED_METATAGS = {
        "ti": "title",
        "ar": "artist",
        "al": "album",
        "au": "author",
        "lr": "lyricist",
        "length": "lenght",
        "by": "lrc_author",
        "offset": "offset",
        "re": "recorder",
        "tool": "recorder",
        "ve": "version"
    }

    lyrics:str
    parsed_lyrics:list[dict]
    meta:dict = {}

    is_synced:bool = False


    def __init__(self, lyrics:str):
        """

        :param lyrics: entire lyrics body
        """

        if lyrics is None:
            raise ValueError("Lyrics can not be None")

        if isinstance(lyrics, list):
            lyrics = lyrics[0]

        lyrics = lyrics.replace("engdesc", "")
        self.lyrics = lyrics

        parsed = parse_lyrics_lines(lyrics)

        # translate meta tags
        meta = filter_parse_lyrics_lines(parsed, "meta")
        for line in meta:
            for tag in line["tags"]:
                name, body = tag.split(":", 1)
                name = name.lower()

                dict_name = self.SUPPORTED_METATAGS.get(name, name)
                self.meta[dict_name] = body


        # check if synced or not.
        # not fail-save:
        # If even just one time tag in the entire lyrics gets flagged as synced
        if len(filter_parse_lyrics_lines(parsed, "time")) > 0:
            self.is_synced = True
            self.parsed_lyrics = filter_parse_lyrics_lines(parsed, "time")
        else:
            self.is_synced = False
            self.parsed_lyrics = filter_parse_lyrics_lines(parsed, "unknown")

        # TODO: add support for multilanguage lyrics


    def format_synced_lyrics(self):
        """
        Formats synced lyrics into a list of dicts
        """
        if not self.is_synced:
            raise ValueError("Cannot format synced lyrics if no synced lyrics exist for track.")
        lyrics = []

        time_tags = parse_time_tag(self.parsed_lyrics)

        for entry in time_tags:
            minutes = entry["minute"]
            if "." in entry["seconds"]:
                seconds = entry["seconds"].split(".")[0]
                milli = entry["seconds"].split(".")[-1]
            else:
                seconds = entry["seconds"]
                milli = "0"

            minutes = int(minutes)
            seconds = int(seconds)
            milli = int(milli)

            milliseconds = datetime.timedelta(minutes=minutes, seconds=seconds, milliseconds=milli).total_seconds() * 1000
            lyrics.append({"time": milliseconds, "text": entry["body"]})

        return lyrics


# # # # # # # # # # # # # # # # # # # # # # # # # # #
# Path and parse function to get lyrics from track  #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

def get_lyrics_file(track_path: str|pathlib.Path, trackhash: str):
    """
    Try to get lyrics from a relative lrc file.
    #TODO: reformat return type to be one type only

    :param track_path: path of track
    :param trackhash: Track-hash value
    """

    track_path = Path(track_path)
    lyrics_path = track_path.with_suffix(".lrc")
    extended_path = track_path.with_suffix(".rlrc")


    # get copyright first
    copyright = ""
    if entry:=TrackStore.trackhashmap.get(trackhash, None):
        for track in entry.tracks:
            copyright = track.copyright

            if copyright:
                break


    if lyrics_path.exists():
        lyrics = Lyrics(lyrics_path.read_text()).format_synced_lyrics()

        return lyrics, copyright
    elif extended_path.exists():
        lyrics = Lyrics(extended_path.read_text()).format_synced_lyrics()
        return lyrics, copyright

    else:
        return None, copyright


def get_lyrics_from_duplicates(track_path: str, trackhash: str):
    """
    Finds the lyrics from other duplicate tracks

    :param track_path: path of track
    :param trackhash: Track-hash value
    """

    entry = TrackStore.trackhashmap.get(trackhash, None)

    if entry is None:
        return None, ""

    for track in entry.tracks:
        if track.trackhash == trackhash and track.filepath != track_path:
            lyrics, copyright = get_lyrics_file(track.filepath, trackhash)

            if lyrics:
                return lyrics, copyright

    return None, ""


def get_lyrics_from_tags(trackhash: str, just_check: bool = False) -> tuple[Lyrics, str]:
    """
    Gets the lyrics from the tags of the track

    :param trackhash:
    :param just_check: check if lyrics exist -> return bool
    """

    entry = TrackStore.trackhashmap.get(trackhash, None)

    if entry is None:
        return None, False, ""

    lyrics = ""
    copyright = ""

    # loop tracks until copyright and lyrics is filled
    for track in entry.tracks:
        if lyrics and copyright:
            break

        if not lyrics:
            lyrics = track.extra.get("lyrics", None)

        if not copyright:
            copyright = track.copyright


    if just_check:
        return len(lyrics) > 0 # if lyrics exist

    if len(lyrics) == 0: # no lyrics found
        return None, ""

    return Lyrics(lyrics), copyright


def check_lyrics_file(filepath: str, trackhash: str):
    """
    Checks if the lyrics file exists for a track
    """

    lyrics_file = Path(filepath).with_suffix(".lrc")
    if lyrics_file.exists:
        return True

    entry = TrackStore.trackhashmap.get(trackhash, None)

    if entry is None:
        return False

    for track in entry.tracks:
        if track.trackhash == trackhash and track.filepath != filepath:
            lyrics_file = Path(track.filepath).with_suffix(".lrc")

            if lyrics_file.exists():
                return True

    return False