from pathlib import Path

filepath = "/home/cwilvx/Music/Editor's Pick/Bad Day 😢/6 Dogs - Crying in the Rarri.m4a"


def split_line(line: str):
    items = line.split("]")
    time = items[0].removeprefix("[")
    lyric = items[1] if len(items) > 1 else ""

    return (time, lyric.strip())


def convert_to_milliseconds(time: str):
    minutes, seconds = time.split(":")
    milliseconds = int(minutes) * 60 * 1000 + float(seconds) * 1000
    return int(milliseconds)


def get_lyrics_from_lrc(filepath: str):
    with open(filepath, mode="r") as file:
        lines = (f.removesuffix("\n") for f in file.readlines())

        lyrics = []

        for line in lines:
            time, lyric = split_line(line)
            milliseconds = convert_to_milliseconds(time)

            lyrics.append({milliseconds: lyric})

        return lyrics


def get_lyrics_file_rel_to_track(filepath: str):
    """
    Finds the lyrics file relative to the track file
    """
    lyrics_path = Path(filepath).with_suffix(".lrc")

    if lyrics_path.exists():
        return lyrics_path


def get_lyrics(track_path: str):
    """
    Gets the lyrics for a track
    """
    lyrics_path = get_lyrics_file_rel_to_track(track_path)

    if lyrics_path:
        return get_lyrics_from_lrc(lyrics_path)
    else:
        return None


get_lyrics(filepath)
