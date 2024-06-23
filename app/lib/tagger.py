from pprint import pprint
from app.db import AlbumTable, ArtistTable, TrackTable
from app.lib.taglib import get_tags
from app.utils.filesystem import run_fast_scandir
from app.utils.parsers import get_base_album_title
from app.utils.progressbar import tqdm


class IndexTracks:
    def __init__(self) -> None:
        dirs_to_scan = ["/home/cwilvx/Music"]

        files = set()

        for _dir in dirs_to_scan:
            files = files.union(run_fast_scandir(_dir, full=True)[1])

        self.tag_untagged(files)
        # unmodified, modified_tracks = self.remove_modified(tracks)
        # untagged = files - unmodified

    def tag_untagged(self, files: set[str]):
        for file in tqdm(files, desc="Reading files"):
            # if POPULATE_KEY != key:
            #     log.warning("'Populate.tag_untagged': Populate key changed")
            #     return

            tags = get_tags(file)

            if tags is not None:
                TrackTable.insert_one(tags)


class IndexAlbums:
    def __init__(self) -> None:
        albums = dict()

        all_tracks: list[TrackTable] = TrackTable.get_all()

        for track in all_tracks:
            if track.albumhash not in albums:
                albums[track.albumhash] = {
                    "albumartists": track.albumartists,
                    "albumhash": track.albumhash,
                    "base_title": None,
                    "color": None,
                    "created_date": None,
                    "date": None,
                    "duration": track.duration,
                    "genres": [*track.genre] if track.genre else [],
                    "og_title": track.og_album,
                    "title": track.album,
                    "trackcount": 1,
                    "dates": [track.date],
                    "created_dates": [track.last_mod],
                }
            else:
                album = albums[track.albumhash]
                album["trackcount"] += 1
                album["duration"] += track.duration
                album["dates"].append(track.date)
                album["created_dates"].append(track.last_mod)

                if track.genre:
                    album["genres"].append(track.genre)

        for album in albums.values():
            album["date"] = min(album["dates"])
            album["created_date"] = min(album["created_dates"])

            genres = []

            for genre in album["genres"]:
                if genre not in genres:
                    genres.append(genre)

            album["genres"] = genres
            album["base_title"], _ = get_base_album_title(album["og_title"])

            del album["dates"]
            del album["created_dates"]

        pprint(albums)

        AlbumTable.insert_many(list(albums.values()))


class IndexArtists:
    def __init__(self) -> None:
        all_tracks: list[TrackTable] = TrackTable.get_all()
        artists = dict()

        for track in all_tracks:
            this_artists = track.artists

            for a in track.albumartists:
                if a not in this_artists:
                    this_artists.append(a)

            for artist in this_artists:
                if artist["artisthash"] not in artists:
                    artists[artist["artisthash"]] = {
                        "albumcount": None,
                        "albums": {track.albumhash},
                        "artisthash": artist["artisthash"],
                        "created_dates": [track.last_mod],
                        "dates": [track.date],
                        "date": None,
                        "duration": track.duration,
                        "genres": [*track.genre] if track.genre else [],
                        "name": artist["name"],
                        "trackcount": None,
                        "tracks": {track.trackhash},
                    }
                else:
                    artist = artists[artist["artisthash"]]
                    artist["duration"] += track.duration
                    artist["albums"].add(track.albumhash)
                    artist["tracks"].add(track.trackhash)
                    artist["dates"].append(track.date)
                    artist["created_dates"].append(track.last_mod)

                    if track.genre:
                        artist["genres"].append(track.genre)


        for artist in artists.values():
            artist["albumcount"] = len(artist["albums"])
            artist["trackcount"] = len(artist["tracks"])
            artist["date"] = min(artist["dates"])
            artist["created_date"] = min(artist["created_dates"])

            genres = []

            for genre in artist["genres"]:
                if genre not in genres:
                    genres.append(genre)

            artist["genres"] = genres

            del artist["tracks"]
            del artist["albums"]
            del artist["dates"]
            del artist["created_dates"]

        pprint(artists)
        ArtistTable.insert_many(list(artists.values()))

class IndexEverything:
    def __init__(self) -> None:
        # IndexTracks()
        # IndexAlbums()
        # IndexArtists()
        pass
