from typing import List, TypeVar

from flask_openapi3 import Tag
from flask_openapi3 import APIBlueprint
from pydantic import BaseModel, Field

from swingmusic.api.apischemas import GenericLimitSchema
from swingmusic.db.userdata import FavoritesTable
from swingmusic.lib.extras import get_extra_info
from swingmusic.models import FavType
from swingmusic.settings import Defaults

from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.tracks import TrackStore

from swingmusic.serializers.track import serialize_track, serialize_tracks
from swingmusic.serializers.artist import serialize_for_card as serialize_artist
from swingmusic.utils.dates import timestamp_to_time_passed
from swingmusic.serializers.album import serialize_for_card, serialize_for_card_many

bp_tag = Tag(name="Favorites", description="Your favorite items")
api = APIBlueprint("favorites", __name__, url_prefix="/favorites", abp_tags=[bp_tag])


T = TypeVar("T")


def remove_none(items: List[T]) -> List[T]:
    return [i for i in items if i is not None]


class FavoritesAddBody(BaseModel):
    hash: str = Field(
        description="The hash of the item",
        min_length=Defaults.HASH_LENGTH,
        max_length=Defaults.HASH_LENGTH,
    )
    type: str = Field(description="The type of the item")
    albumhash: str | None = Field(
        default=None,
        description="Works only: the album of the recording the work was favorited from",
    )


def _classical():
    """
    The classical home module when classical support is on, else None.
    """
    try:
        from swingmusic.config import UserConfig
        from swingmusic.premium import classical_available

        if not classical_available():
            return None
        from swingmusic.premium.classical import home

        return home
    except Exception:  # noqa: BLE001
        return None


def _serialize_movements(tracks: list) -> list[dict]:
    """
    Favorited movements with their movement info.
    """
    from swingmusic.premium.classical.search import serialize_tracks as serialize_movements

    return serialize_movements(tracks)


def _first_of_each_kind(tracks: list, limit: int) -> list:
    """
    The tracks, in order, up to `limit` plain ones and `limit` classical
    ones, so every tracks tab can show its first `limit`.
    """
    counts = {True: 0, False: 0}
    out = []
    for track in tracks:
        if counts[track.is_classical] < limit:
            counts[track.is_classical] += 1
            out.append(track)
        if min(counts.values()) >= limit:
            break
    return out


def _movement_card(track, home) -> dict | None:
    """
    A favorited movement as its work's card on the movement's recording.
    """
    if home is None:
        return None
    entry = home.ClassicalStore.trackmap.get(track.trackhash)
    return home.work_card(entry.workhash, track.albumhash) if entry else None


def toggle_fav(type: str, hash: str):
    """
    Toggles a favorite item.
    """
    if type == FavType.track:
        entry = TrackStore.trackhashmap.get(hash)
        if entry is not None:
            entry.toggle_favorite_user()

    elif type == FavType.album:
        entry = AlbumStore.albummap.get(hash)

        if entry is not None:
            entry.toggle_favorite_user()
    elif type == FavType.artist:
        entry = ArtistStore.artistmap.get(hash)

        if entry is not None:
            entry.toggle_favorite_user()

    return {"msg": "Added to favorites"}


def _artist_card(hash_: str, home=None) -> dict | None:
    """
    A favorite artist's card: the library artist, else a classical
    performer known only from credits.
    """
    entry = ArtistStore.artistmap.get(hash_)
    if entry is not None:
        return serialize_artist(entry.artist)
    if home is not None and home.ClassicalStore.get_performer(hash_) is not None:
        return home.person_card(hash_)
    return None


@api.post("/add")
def toggle_favorite(body: FavoritesAddBody):
    """
    Adds a favorite to the database.
    """
    extra = get_extra_info(body.hash, body.type)
    if body.type == FavType.work:
        # the favorite covers every recording; the album opens the one chosen
        extra["albumhash"] = body.albumhash

    try:
        FavoritesTable.insert_item(
            {"hash": body.hash, "type": body.type, "extra": extra}
        )
    except Exception as e:
        print(e)
        return {"msg": "Failed! An error occured"}, 500

    toggle_fav(body.type, body.hash)

    return {"msg": "Added to favorites"}


@api.post("/remove")
def remove_favorite(body: FavoritesAddBody):
    """
    Removes a favorite from the database.
    """
    try:
        FavoritesTable.remove_item({"hash": body.hash, "type": body.type})
    except Exception as e:
        print(e)
        return {"msg": "Failed! An error occured"}, 500

    toggle_fav(body.type, body.hash)

    return {"msg": "Removed from favorites"}


class GetAllOfTypeQuery(GenericLimitSchema):
    """
    Extending this class will give you a model with the `limit` field
    """

    start: int = Field(
        description="Where to start from",
        default=Defaults.API_CARD_LIMIT,
    )


@api.get("/albums")
def get_favorite_albums(query: GetAllOfTypeQuery):
    """
    Get favorite albums

    Note: Only the first request will return the total number of favorites.
    Others will return -1
    """
    fav_albums, total = FavoritesTable.get_fav_albums(query.start, query.limit)
    albums = AlbumStore.get_albums_by_hashes(a.hash for a in fav_albums)

    return {"albums": serialize_for_card_many(albums), "total": total}


class GetFavoriteTracksQuery(GetAllOfTypeQuery):
    kind: str = Field(
        default="all",
        description="all, tracks (not classical movements), or classical (movements only)",
    )


@api.get("/tracks")
def get_favorite_tracks(query: GetFavoriteTracksQuery):
    """
    Get favorite tracks of a kind: all, plain tracks, or classical movements

    Note: Only the first request will return the total number of favorites.
    Others will return -1
    """
    home = _classical()
    if home is None or query.kind not in ("tracks", "classical"):
        tracks, total = FavoritesTable.get_fav_tracks(query.start, query.limit)
        tracks = TrackStore.get_tracks_by_trackhashes([t.hash for t in tracks])
        return {"tracks": serialize_tracks(tracks), "total": total}

    favorites, _ = FavoritesTable.get_fav_tracks(0, -1)
    classical = query.kind == "classical"
    tracks = [t for t in TrackStore.get_tracks_by_trackhashes([f.hash for f in favorites]) if t.is_classical == classical]
    end = None if query.limit == -1 else query.start + query.limit
    page = tracks[query.start : end]
    serialized = _serialize_movements(page) if classical else serialize_tracks(page)
    return {"tracks": serialized, "total": len(tracks) if query.start == 0 else -1}


@api.get("/artists")
def get_favorite_artists(query: GetAllOfTypeQuery):
    """
    Get favorite artists

    Note: Only the first request will return the total number of favorites.
    Others will return -1
    """
    artists, total = FavoritesTable.get_fav_artists(
        start=query.start,
        limit=query.limit,
    )

    home = _classical()
    cards = [card for a in artists if (card := _artist_card(a.hash, home))]
    return {"artists": cards, "total": total}


@api.get("/works")
def get_favorite_works(query: GetAllOfTypeQuery):
    """
    Get favorite classical works, each with the recording it was favorited from
    """
    home = _classical()
    if home is None:
        return {"works": [], "total": 0}
    favorites = home.favorite_works()
    page = favorites[query.start : query.start + query.limit] if query.limit != -1 else favorites[query.start :]
    works = [row for wh, ah, _ in page if (row := home.work_row(wh, ah))]
    return {"works": works, "total": len(favorites)}


@api.get("/composers")
def get_favorite_composers(query: GetAllOfTypeQuery):
    """
    Get favorite composers as artist cards
    """
    home = _classical()
    if home is None:
        return {"composers": [], "total": 0}
    favorites = home.favorite_composers()
    page = favorites[query.start : query.start + query.limit] if query.limit != -1 else favorites[query.start :]
    composers = [card for hash_, _ in page if (card := home.person_card(hash_))]
    return {"composers": composers, "total": len(favorites)}


class GetAllFavoritesQuery(BaseModel):
    """
    Extending this class will give you a model with the `limit` field
    """

    track_limit: int = Field(
        description="The number of tracks to return",
        default=Defaults.API_CARD_LIMIT,
    )

    album_limit: int = Field(
        description="The number of albums to return",
        default=Defaults.API_CARD_LIMIT,
    )

    artist_limit: int = Field(
        description="The number of artists to return",
        default=Defaults.API_CARD_LIMIT,
    )

    work_limit: int = Field(
        description="The number of classical works to return",
        default=Defaults.API_CARD_LIMIT,
    )


@api.get("")
def get_all_favorites(query: GetAllFavoritesQuery):
    """
    Returns all the favorites in the database.
    """
    track_limit = query.track_limit
    album_limit = query.album_limit
    artist_limit = query.artist_limit

    # largest is x2 to accound for broken hashes if any
    largest = max(track_limit, album_limit, artist_limit)

    favs = FavoritesTable.get_all(with_user=True)
    favs = sorted(favs, key=lambda x: x.timestamp, reverse=True)

    tracks = []
    albums = []
    artists = []

    track_master_hash = TrackStore.trackhashmap.keys()
    album_master_hash = AlbumStore.albummap.keys()
    artist_master_hash = ArtistStore.artistmap.keys()
    home = _classical()

    # INFO: Filter out invalid hashes (file not found or tags edited)
    for fav in favs:
        hash = fav.hash
        type = fav.type

        if type == FavType.track:
            tracks.append(hash) if hash in track_master_hash else None

        if type == FavType.artist and (
            hash in artist_master_hash or (home is not None and home.ClassicalStore.get_performer(hash))
        ):
            artists.append(hash)

        if type == FavType.album:
            albums.append(hash) if hash in album_master_hash else None

    fav_works = home.favorite_works() if home else []
    fav_composers = home.favorite_composers() if home else []

    count = {
        "tracks": len(tracks),
        "albums": len(albums),
        "artists": len(artists),
        "works": len(fav_works),
        "composers": len(fav_composers),
    }

    if home is not None:
        favorite_tracks = TrackStore.get_tracks_by_trackhashes(tracks)
        count["plain_tracks"] = sum(1 for t in favorite_tracks if not t.is_classical)
        count["classical_tracks"] = len(favorite_tracks) - count["plain_tracks"]
        tracks = _first_of_each_kind(favorite_tracks, track_limit)
    else:
        tracks = TrackStore.get_tracks_by_trackhashes(tracks[:track_limit])
    albums = AlbumStore.get_albums_by_hashes(albums[:album_limit])
    artists = {hash_: card for hash_ in artists[:largest] if (card := _artist_card(hash_, home))}

    recents = []

    for fav in favs:
        if len(recents) >= largest:
            break

        if fav.type == FavType.album:
            album = next((a for a in albums if a.albumhash == fav.hash), None)

            if album is None:
                continue

            album = serialize_for_card(album)
            album["help_text"] = "album"
            album["time"] = timestamp_to_time_passed(fav.timestamp)

            recents.append(
                {
                    "type": "album",
                    "item": album,
                }
            )

        if fav.type == FavType.artist:
            artist = artists.get(fav.hash)

            if artist is None:
                continue

            artist = {**artist}
            artist["help_text"] = "artist"
            artist["time"] = timestamp_to_time_passed(fav.timestamp)

            recents.append(
                {
                    "type": "artist",
                    "item": artist,
                }
            )

        if fav.type == FavType.track:
            track = next((t for t in tracks if t.trackhash == fav.hash), None)

            if track is None:
                continue

            card = _movement_card(track, home)
            item = card if card is not None else serialize_track(track)
            item["help_text"] = "track"
            item["time"] = timestamp_to_time_passed(fav.timestamp)

            recents.append({"type": "work" if card is not None else "track", "item": item})

        if fav.type == FavType.work and home is not None:
            workhash = fav.hash
            card = home.work_card(workhash, (fav.extra or {}).get("albumhash"))
            if card is None:
                continue
            card["help_text"] = "work"
            card["time"] = timestamp_to_time_passed(fav.timestamp)
            recents.append({"type": "work", "item": card})

        if fav.type == FavType.composer and home is not None:
            card = home.person_card(fav.hash)
            if card is None:
                continue
            card["help_text"] = "composer"
            card["time"] = timestamp_to_time_passed(fav.timestamp)
            recents.append({"type": "artist", "item": card})

    return {
        "recents": recents[:album_limit],
        "works": [row for wh, ah, _ in fav_works[: query.work_limit] if (row := home.work_row(wh, ah))],
        "composers": [card for h, _ in fav_composers[:artist_limit] if (card := home.person_card(h))],
        "tracks": _serialize_movements(tracks) if home is not None else serialize_tracks(tracks),
        "albums": serialize_for_card_many(albums[:album_limit]),
        "artists": list(artists.values())[:artist_limit],
        "count": count,
    }


@api.get("/check")
def check_favorite(query: FavoritesAddBody):
    """
    Checks if a favorite exists in the database.
    """
    itemhash = query.hash
    itemtype = query.type

    return {"is_favorite": FavoritesTable.check_exists(itemhash, itemtype)}
