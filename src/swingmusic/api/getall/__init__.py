from flask_openapi3 import Tag
from natsort import natsorted
from pydantic import BaseModel, Field
from flask_openapi3 import APIBlueprint

from datetime import datetime, timezone
from swingmusic.config import UserConfig
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.plays import NO_PLAYS, PlayStore
from swingmusic.api.apischemas import GenericLimitSchema

from swingmusic.utils import format_number
from swingmusic.utils.dates import (
    create_new_date,
    date_string_to_time_passed,
    seconds_to_time_string,
    timestamp_to_time_passed,
)
from swingmusic.utils.auth import get_current_userid
from swingmusic.utils.parsers import get_sort_name
from swingmusic.serializers.album import serialize_for_card as serialize_album
from swingmusic.serializers.artist import serialize_for_card as serialize_artist

bp_tag = Tag(name="Get all", description="List all items")
api = APIBlueprint("getall", __name__, url_prefix="/getall", abp_tags=[bp_tag])


class GetAllItemsQuery(GenericLimitSchema):
    start: int = Field(
        description="The start index of the items to return",
        example=0,
        default=0,
    )
    sortby: str = Field(
        description="The key to sort items by",
        example="created_date",
        default="created_date",
    )

    reverse: str = Field(
        description="Reverse the sort",
        example=1,
        default="1",
    )


class GetAllItemsPath(BaseModel):
    itemtype: str = Field(
        description="The type of items to return (albums | artists)",
        example="albums",
        default="albums",
    )


COMMON_SORT_KEYS = {
    "date",
    "created_date",
    "trackcount",
    "duration",
    "playcount",
    "playduration",
    "lastplayed",
}
ALBUM_SORT_KEYS = COMMON_SORT_KEYS | {"title", "albumartists"}
ARTIST_SORT_KEYS = COMMON_SORT_KEYS | {"name", "albumcount"}
TEXT_SORT_KEYS = {"title", "albumartists", "name"}
PLAY_SORT_KEYS = {"playcount", "playduration", "lastplayed"}


def resolve_sort_key(sortkey: str, is_albums: bool) -> str:
    """
    Returns the sort key if it is valid for the item type, else the default text key.
    """
    allowed = ALBUM_SORT_KEYS if is_albums else ARTIST_SORT_KEYS

    if sortkey in allowed:
        return sortkey

    return "title" if is_albums else "name"


def build_sort_key(sortkey: str, is_albums: bool, config: UserConfig):
    """
    Returns a total sort key function for the given attribute that never raises.
    """
    is_text = sortkey in TEXT_SORT_KEYS
    article_key = "albumartists" if is_albums else "name"
    article_aware = sortkey == article_key and config.artistArticleAwareSorting
    articles = config.artistSortingArticles

    if sortkey in PLAY_SORT_KEYS:
        plays = PlayStore.of(get_current_userid(), "album" if is_albums else "artist")
        hashattr = "albumhash" if is_albums else "artisthash"
        return lambda x: getattr(plays.get(getattr(x, hashattr), NO_PLAYS), sortkey)

    def sort_key(x):
        value = getattr(x, sortkey, None)

        if sortkey == "albumartists":
            value = value[0].get("name", "") if value else ""

        if is_text:
            name = value if isinstance(value, str) else str(value or "")

            if article_aware:
                name = get_sort_name(name, articles=articles)

            return name.casefold()

        if isinstance(value, (int, float)):
            return value

        try:
            return float(value)
        except (TypeError, ValueError):
            return 0

    return sort_key


@api.get("/<itemtype>")
def get_all_items(path: GetAllItemsPath, query: GetAllItemsQuery):
    """
    Get all items

    Used to show all albums or artists in the library

    Sort keys:
    -
    Both albums and artists: `duration`, `created_date`, `playcount`, `playduration`, `lastplayed`, `trackcount`

    Albums only: `title`, `albumartists`, `date`
    Artists only: `name`, `albumcount`
    """
    is_albums = path.itemtype == "albums"
    is_artists = path.itemtype == "artists"

    if is_albums:
        items = AlbumStore.get_flat_list()
    elif is_artists:
        items = ArtistStore.get_flat_list()

    total = len(items)

    start = query.start
    limit = query.limit
    sortkey = resolve_sort_key(query.sortby, is_albums)
    reverse = query.reverse == "1"

    sort_is_count = sortkey == "trackcount"
    sort_is_duration = sortkey == "duration"
    sort_is_create_date = sortkey == "created_date"
    sort_is_playcount = sortkey == "playcount"
    sort_is_playduration = sortkey == "playduration"
    sort_is_lastplayed = sortkey == "lastplayed"

    sort_is_date = is_albums and sortkey == "date"

    sort_is_artist_trackcount = is_artists and sortkey == "trackcount"
    sort_is_artist_albumcount = is_artists and sortkey == "albumcount"

    sort_key = build_sort_key(sortkey, is_albums, UserConfig())

    if sortkey in TEXT_SORT_KEYS:
        sorted_items = natsorted(items, key=sort_key, reverse=reverse)
    else:
        sorted_items = sorted(items, key=sort_key, reverse=reverse)

    items = sorted_items[start : start + limit]
    album_list = []

    for item in items:
        item_dict = serialize_album(item) if is_albums else serialize_artist(item)

        if sort_is_date:
            item_dict["help_text"] = datetime.fromtimestamp(
                item.date, tz=timezone.utc
            ).year

        if sort_is_create_date:
            date = create_new_date(datetime.fromtimestamp(item.created_date))
            timeago = date_string_to_time_passed(date)
            item_dict["help_text"] = timeago

        if sort_is_count:
            item_dict["help_text"] = (
                f"{format_number(item.trackcount)} track{'' if item.trackcount == 1 else 's'}"
            )

        if sort_is_duration:
            item_dict["help_text"] = seconds_to_time_string(item.duration)

        if sort_is_artist_trackcount:
            item_dict["help_text"] = (
                f"{format_number(item.trackcount)} track{'' if item.trackcount == 1 else 's'}"
            )

        if sort_is_artist_albumcount:
            item_dict["help_text"] = (
                f"{format_number(item.albumcount)} album{'' if item.albumcount == 1 else 's'}"
            )

        if sort_is_playcount:
            item_dict["help_text"] = (
                f"{format_number(item.playcount)} play{'' if item.playcount == 1 else 's'}"
            )

        if sort_is_lastplayed:
            if item.playduration == 0:
                item_dict["help_text"] = "Never played"
            else:
                item_dict["help_text"] = timestamp_to_time_passed(item.lastplayed)

        if sort_is_playduration:
            item_dict["help_text"] = seconds_to_time_string(item.playduration)

        album_list.append(item_dict)

    return {"items": album_list, "total": total}
