"""
Contains everything that deals with image colour extraction.
"""
import logging
import os
import pathlib

import colorgram
from pathlib import Path
from typing import Generator
from swingmusic.utils.progressbar import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

from swingmusic import settings
from swingmusic.store.albums import AlbumStore
from swingmusic.db.userdata import LibDataTable
from swingmusic.store.artists import ArtistStore

log = logging.getLogger(__name__)

def get_image_colors(image: pathlib.Path, count=1) -> list[str]:
    """
    Extracts ``count`` numbers of the most dominant colours from an image.

    :params image: Path to image.
    :params count: How many colours should be extracted?
    :returns: List["rgb(red, green, blue)", ...]
    """

    if image.exists():
        colors = sorted(colorgram.extract(image, count), key=lambda c: c.hsl.h)
    else:
        return []

    formatted_colors = []

    for color in colors:
        color = f"rgb({color.rgb.r}, {color.rgb.g}, {color.rgb.b})"
        formatted_colors.append(color)

    return formatted_colors


def process_color(item_hash: str, is_album=True) -> list[str]:
    """
    Parse colours from images associated with song

    :param item_hash: hash of item for colour calculation
    :param is_album: if item is an album
    :return: list with colour strings
    """

    if is_album:
        path = settings.Paths().sm_thumb_path
    else:
        path = settings.Paths().sm_artist_img_path

    path = path / (item_hash + ".webp")

    if not path.exists():
        return []

    return get_image_colors(path)


def extract_color_worker(item_data: dict) -> dict:
    """
    Generic worker function for extracting colours in parallel.
    Returns data to main process for batch database operations.
    Works for both albums and artists based on item_data configuration.
    """
    hash_field: str = item_data["hash_field"]
    path_func: Path = item_data["path_func"]
    item_hash: str = item_data[hash_field]

    path = path_func / (item_hash + ".webp")

    if not path.exists():
        return {hash_field: item_hash, "color": None, "error": "Image not found"}

    colors = get_image_colors(path)

    if not colors:
        return {
            hash_field: item_hash,
            "color": None,
            "error": "Color extraction failed",
        }

    return {hash_field: item_hash, "color": colors[0], "error": None}


class ColorProcessor:
    """
    Generic color processor for extracting dominant colors from images.
    Uses multiprocessing for parallel color extraction and batch database operations.
    """

    def __init__(
        self,
        item_type: str,
        store: AlbumStore | ArtistStore,
        path_func: Path,
        hash_field: str,
    ):
        """
        Initialize the color processor.

        Args:
            item_type: Type of item ("album" or "artist")
            store: Store object (AlbumStore or ArtistStore)
            path_func: Function to get the image path
            hash_field: Name of the hash field ("albumhash" or "artisthash")
        """
        self.item_type = item_type
        self.store = store
        self.path_func = path_func
        self.hash_field = hash_field

        # Read existing colors from database to filter out already processed items
        existing_colors = set()
        for color_data in LibDataTable.get_all_colors(item_type):
            if color_data["color"]:
                existing_colors.add(color_data["itemhash"])

        # Filter items that need color processing
        items_needing_colors = self._get_items_needing_colors(existing_colors)

        if not items_needing_colors:
            return

        self._process_colors_parallel(items_needing_colors)

    def _get_items_needing_colors(
        self, existing_colors: set
    ) -> Generator[dict, None, None]:
        """
        Generator that yields items needing color processing.
        """
        for item in self.store.get_flat_list():
            # Skip if item already has color in memory store
            if item.color:
                continue

            # Skip if item already has color in database
            item_hash = getattr(item, self.hash_field)
            if item_hash in existing_colors:
                continue

            yield {
                self.hash_field: item_hash,
                "item_type": self.item_type,
                "path_func": self.path_func,
                "hash_field": self.hash_field,
            }

    def _process_colors_parallel(self, items: Generator[dict, None, None]) -> None:
        """
        Process colors using multiprocessing and batch database operations.
        """
        items_list = list(items)

        if not items_list:
            return

        cpus = max(1, (os.cpu_count() or 1) // 2)
        batch_size = 20  # Process results in batches

        with ProcessPoolExecutor(max_workers=cpus) as executor:
            # Submit all jobs
            future_to_item = {
                executor.submit(extract_color_worker, item): item for item in items_list
            }

            batch = []
            processed_count = 0

            # Process results as they complete
            progress_bar = tqdm(
                as_completed(future_to_item),
                total=len(items_list),
                desc=f"Processing {self.item_type} colors",
            )

            for future in progress_bar:
                try:
                    result = future.result()

                    if result["color"] is not None:
                        batch.append(result)

                    # Process batch when it reaches batch_size or we're done
                    if len(batch) >= batch_size or processed_count + 1 >= len(
                        items_list
                    ):
                        if batch:
                            self._process_batch(batch)
                            batch = []

                    processed_count += 1

                except Exception as e:
                    item_data = future_to_item[future]
                    item_hash = item_data[self.hash_field]
                    log.error(f"Error processing {self.item_type} {item_hash}: {e}")

    def _process_batch(self, batch: list[dict]) -> None:
        """
        Process a batch of color results - update database and memory stores.
        """
        if not batch:
            return

        # Prepare database records
        db_inserts = []
        db_updates = []

        for result in batch:
            item_hash = result[self.hash_field]
            color = result["color"]

            # Check if record exists in database
            existing_record = LibDataTable.find_one(item_hash, type=self.item_type)

            if existing_record is None:
                db_inserts.append(
                    {
                        "itemhash": self.item_type + item_hash,
                        "color": color,
                        "itemtype": self.item_type,
                    }
                )
            else:
                db_updates.append(
                    {"itemhash": self.item_type + item_hash, "color": color}
                )

        # Batch database operations
        if db_inserts:
            LibDataTable.insert_many(db_inserts)

        if db_updates:
            for update_data in db_updates:
                clean_hash = update_data["itemhash"].replace(self.item_type, "")
                LibDataTable.update_one(clean_hash, {"color": update_data["color"]})

        # Update in-memory store
        store_map = getattr(self.store, f"{self.item_type}map")

        for result in batch:
            item_hash = result[self.hash_field]
            color = result["color"]

            item = store_map.get(item_hash)
            if item:
                item.set_color(color)


class ProcessAlbumColors:
    """
    Extracts the most dominant color from the album art and saves it to the database.
    Uses multiprocessing for parallel color extraction and batch database operations.
    """

    def __init__(self) -> None:
        ColorProcessor(
            item_type="album",
            store=AlbumStore,
            path_func=settings.Paths().sm_thumb_path,
            hash_field="albumhash",
        )


class ProcessArtistColors:
    """
    Extracts the most dominant colour from the artist art and saves it to the database.
    Uses multiprocessing for parallel colour extraction and batch database operations.
    """

    def __init__(self) -> None:
        ColorProcessor(
            item_type="artist",
            store=ArtistStore,
            path_func=settings.Paths().sm_artist_img_path,
            hash_field="artisthash",
        )
