from pathlib import Path
from tinytag import TinyTag

from app.store.tracks import TrackStore


def split_line(line: str):
    """
    Split a lyrics line into time and lyrics
    """
    items = line.split("]")
    time = items[0].removeprefix("[")
    lyric = items[1] if len(items) > 1 else ""

    return (time, lyric.strip())


def convert_to_milliseconds(time: str):
    """
    Converts a lyrics time string into milliseconds.
    """
    try:
        minutes, seconds = time.split(":")
    except ValueError:
        return 0

    milliseconds = int(minutes) * 60 * 1000 + float(seconds) * 1000
    return int(milliseconds)


def format_synced_lyrics(lines: list[str]):
    """
    Formats synced lyrics into a list of dicts
    """
    lyrics = []

    for line in lines:
        # if line starts with [ and ends with ] .ie. ID3 tag, skip it
        if line.startswith("[") and line.endswith("]"):
            continue

        # if line does not start with [ skip it
        if not line.startswith("["):
            continue

        time, lyric = split_line(line)
        milliseconds = convert_to_milliseconds(time)

        lyrics.append({"time": milliseconds, "text": lyric})

    return lyrics


def get_lyrics_from_lrc(filepath: str):
    with open(filepath, mode="r") as file:
        lines = (f.removesuffix("\n") for f in file.readlines())
        return format_synced_lyrics(lines)


def get_lyrics_file_rel_to_track(filepath: str):
    """
    Finds the lyrics file relative to the track file
    """
    lyrics_path = Path(filepath).with_suffix(".lrc")

    if lyrics_path.exists():
        return lyrics_path


def check_lyrics_file_rel_to_track(filepath: str):
    """
    Checks if the lyrics file exists relative to the track file
    """
    lyrics_path = Path(filepath).with_suffix(".lrc")

    if lyrics_path.exists():
        return True
    else:
        return False


def get_lyrics(track_path: str):
    """
    Gets the lyrics for a track
    """
    lyrics_path = get_lyrics_file_rel_to_track(track_path)

    if lyrics_path:
        lyrics = get_lyrics_from_lrc(lyrics_path)
        copyright = get_extras(track_path, ["copyright"])

        return lyrics, copyright[0]
    else:
        return None, ""


def get_lyrics_from_duplicates(trackhash: str, filepath: str):
    """
    Finds the lyrics from other duplicate tracks
    """

    for track in TrackStore.tracks:
        if track.trackhash == trackhash and track.filepath != filepath:
            lyrics, copyright = get_lyrics(track.filepath)

            if lyrics:
                return lyrics, copyright

    return None, ""


def check_lyrics_file(filepath: str, trackhash: str):
    lyrics_exists = check_lyrics_file_rel_to_track(filepath)

    if lyrics_exists:
        return True

    for track in TrackStore.tracks:
        if track.trackhash == trackhash and track.filepath != filepath:
            lyrics_exists = check_lyrics_file_rel_to_track(track.filepath)

            if lyrics_exists:
                return True

    return False


def test_is_synced(lyrics: list[str]):
    """
    Tests if the lyric lines passed are synced.
    """
    for line in lyrics:
        time, _ = split_line(line)
        milliseconds = convert_to_milliseconds(time)

        if milliseconds != 0:
            return True

    return False


def get_extras(filepath: str, keys: list[str]):
    """
    Get extra tags from an audio file.
    """
    try:
        tags = TinyTag.get(filepath)
    except Exception:
        return [""] * len(keys)

    extras = tags.extra

    return [extras.get(key, "").strip() for key in keys]


def get_lyrics_from_tags(filepath: str, just_check: bool = False):
    """
    Gets the lyrics from the tags of the track
    """
    lyrics, copyright = get_extras(filepath, ["lyrics", "copyright"])
    lyrics = lyrics.replace("engdesc", "")
    exists = bool(lyrics.replace("\n", "").strip())

    if just_check:
        return exists

    if not exists:
        return None, False, ""

    lines = lyrics.split("\n")
    synced = test_is_synced(lines[:15])

    if synced:
        return format_synced_lyrics(lines), synced, copyright

    return lines, synced, copyright
