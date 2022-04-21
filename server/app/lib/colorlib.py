import colorgram
from progress.bar import Bar
from PIL import Image
from io import BytesIO

from app import api, instances
from app.lib.taglib import return_album_art


def get_image_colors(image) -> list:
    """Extracts 2 of the most dominant colors from an image."""
    try:
        colors = sorted(colorgram.extract(image, 2), key=lambda c: c.hsl.h)
    except OSError:
        return []

    formatted_colors = []

    for color in colors:
        color = f"rgb({color.rgb.r}, {color.rgb.g}, {color.rgb.b})"
        formatted_colors.append(color)

    return formatted_colors


def save_track_colors(img, filepath) -> None:
    """Saves the track colors to the database"""

    track_colors = get_image_colors(img)

    tc_dict = {
        "filepath": filepath,
        "colors": track_colors,
    }

    instances.track_color_instance.insert_track_color(tc_dict)


def save_t_colors():
    _bar = Bar("Processing image colors", max=len(api.DB_TRACKS))

    for track in api.DB_TRACKS:
        filepath = track["filepath"]
        album_art = return_album_art(filepath)

        if album_art is not None:
            img = Image.open(BytesIO(album_art))
            save_track_colors(img, filepath)

        _bar.next()

    _bar.finish()
