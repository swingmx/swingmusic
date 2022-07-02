import colorgram
from app import instances
from app import settings
from app.helpers import Get
from app.logger import get_logger
from app.models import Album

log = get_logger()


def get_image_colors(image: str) -> list:
    """Extracts 2 of the most dominant colors from an image."""
    try:
        colors = sorted(colorgram.extract(image, 4), key=lambda c: c.hsl.h)
    except OSError:
        return []

    formatted_colors = []

    for color in colors:
        color = f"rgb({color.rgb.r}, {color.rgb.g}, {color.rgb.b})"
        formatted_colors.append(color)

    return formatted_colors


class ProcessAlbumColors:

    def __init__(self) -> None:
        log.info("Processing album colors")
        all_albums = Get.get_all_albums()

        all_albums = [a for a in all_albums if len(a.colors) == 0]

        for a in all_albums:
            self.process_color(a)

        log.info("Processing album colors ... ✅")

    @staticmethod
    def process_color(album: Album):
        img = settings.THUMBS_PATH + "/" + album.image

        colors = get_image_colors(img)

        if len(colors) > 0:
            instances.album_instance.set_album_colors(colors, album.hash)

        return colors
