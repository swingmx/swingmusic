from gettext import ngettext
from io import BytesIO
import json
import random
import time
from urllib.parse import quote
import requests
from PIL import Image

from swingmusic.db.userdata import MixTable
from swingmusic.models.artist import Artist
from swingmusic.models.mix import Mix
from swingmusic.models.track import Track
from swingmusic.plugins import Plugin, plugin_method
from swingmusic.settings import Paths
from swingmusic.store.albums import AlbumStore
from swingmusic.store.artists import ArtistStore
from swingmusic.store.tracks import TrackStore
from swingmusic.utils.dates import get_date_range, get_duration_ago
from swingmusic.utils.hashing import create_hash
from swingmusic.utils.mixes import balance_mix
from swingmusic.utils.stats import get_artists_in_period


class MixAlreadyExists(Exception):
    """
    Raised when a mix with the same sourcehash already exists.
    """

    pass


class MixesPlugin(Plugin):
    MAX_TRACKS_TO_FETCH = 5
    MIN_TRACK_MIX_LENGTH = 15
    MIN_ARTISTS_PER_MIX = 4
    MIX_TRACKS_LENGTH = 40

    MIN_DAY_LISTEN_DURATION = 3 * 60  # 3 minutes
    MIN_WEEK_LISTEN_DURATION = 10 * 60  # 10 minutes
    MIN_MONTH_LISTEN_DURATION = 20 * 60  # 20 minutes

    def __init__(self):
        super().__init__("mixes", "Mixes")
        self.server = "https://smcloud.mungaist.com"
        # self.server = "http://localhost:1956"

        # server_online = self.ping_server()
        self.set_active(True)

    def ping_server(self):
        max_retries = 3
        retry_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                requests.get(self.server, timeout=10)
                return True
            except Exception as e:
                print(
                    f"Failed to connect to the recommendation server (attempt {attempt + 1}/{max_retries})"
                )
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                continue

        return False

    @plugin_method
    def get_track_mix_data(self, tracks: list[Track], with_help: bool = False):
        """
        Given a list of tracks, creates a mix by fetching data from the
        Swing Music Cloud recommendation server.

        The server returns a list of weak trackhashes. We use these to fetch
        the matching track data from our library database. Found tracks are
        then balanced and returned as the final mix tracklist.

        :param with_help: Whether to include the help flag in the query.
            The flag tells the server to find more data using other tracks from the same album.
        """
        queries = [
            {
                "title": track.title,
                "artists": [a["name"] for a in track.artists],
                "album": track.og_album,
                "with_help": with_help,
            }
            for track in tracks
        ]

        try:
            response = requests.post(f"{self.server}/radio", json=queries, timeout=30)
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            print("Failed to connect to recommendation server")
            return [], [], []

        try:
            results = response.json()
        except json.JSONDecodeError:
            print("Failed to decode JSON response from recommendation server")
            return [], [], []

        trackhashes: list[str] = results.get("tracks", [])

        trackmatches = TrackStore.get_flat_list()
        trackmatches = [t for t in trackmatches if t.weakhash in trackhashes]

        # filter out duplicates of the same weakhash
        # group by weakhash and pick the one with the highest bitrate
        grouped: dict[str, list[Track]] = {}
        for track in trackmatches:
            grouped.setdefault(track.weakhash, []).append(track)

        trackmatches = [
            max(group, key=lambda x: x.bitrate) for group in grouped.values()
        ]

        # sort by trackhash order
        trackmatches = sorted(trackmatches, key=lambda x: trackhashes.index(x.weakhash))

        # if the mix is short, try to fill it up with tracks
        # from album and artist data from the cloud!

        # Create as many filler tracks as possible
        # Then the mix length will be controlled in the Mix model
        # if len(trackmatches) < self.TRACK_MIX_LENGTH:
        if True:
            filler_tracks = self.fallback_create_artist_mix(
                similar_artists=results.get("artists", []),
                similar_albums=results.get("albums", []),
                omit_trackhashes={t.weakhash for t in trackmatches},
                # limit=self.TRACK_MIX_LENGTH - len(trackmatches),
            )
            trackmatches.extend(filler_tracks)

        # try to balance the mix
        trackmatches = balance_mix(trackmatches)
        return trackmatches, results.get("albums", []), results.get("artists", [])

    # @plugin_method
    # def get_artist_mix(self, artisthash: str):
    #     """
    #     Given an artisthash, creates an artist mix using the
    #     self.MAX_TRACKS_TO_FETCH most listened to tracks.

    #     Returns a tuple of the mix and the sourcehash.
    #     """
    #     artist = ArtistStore.artistmap[artisthash]
    #     tracks = TrackStore.get_tracks_by_trackhashes(artist.trackhashes)

    #     tracks = sorted(tracks, key=lambda x: x.playduration, reverse=True)
    #     sourcetracks = tracks[: self.MAX_TRACKS_TO_FETCH]
    #     sourcehash = create_hash(*[t.trackhash for t in sourcetracks])

    #     if MixTable.get_by_sourcehash(sourcehash):
    #         raise MixAlreadyExists()

    #     tracks, albums, artists = self.get_track_mix(tracks[: self.MAX_TRACKS_TO_FETCH])
    #     return (tracks, albums, artists, sourcehash)

    @plugin_method
    def create_artist_mixes(self, userid: int):
        """
        Creates artist mixes for a given userid.
        """
        mixes: list[Mix] = []
        indexed = set()

        today_start, today_end = get_date_range(duration="day")
        last_2_days_start = get_duration_ago("day", 2)
        last_7_days_start = get_duration_ago("week")
        last_1_month_start = get_duration_ago("month")

        artists = {
            "today": {
                "max": 4,
                "artists": get_artists_in_period(today_start, today_end, userid),
                "created": 0,
            },
            "last_2_days": {
                "max": 3,
                "artists": get_artists_in_period(
                    last_2_days_start, time.time(), userid
                ),
                "created": 0,
            },
            "last_7_days": {
                "max": 4,
                "artists": get_artists_in_period(
                    last_7_days_start, time.time(), userid
                ),
                "created": 0,
            },
            "last_1_month": {
                "max": 4,
                "artists": get_artists_in_period(
                    last_1_month_start, time.time(), userid
                ),
                "created": 0,
            },
        }

        # FIXME: Make sure that different artists don't generate the same mix

        for i, period in enumerate(artists.values()):
            # if previous period has less than its max
            # add the difference to this period's limit
            limit = period["max"]

            if i > 0:
                previous_period = artists[list(artists.keys())[i - 1]]
                if previous_period["created"] < previous_period["max"]:
                    limit += previous_period["max"] - previous_period["created"]

            for artist in period["artists"]:
                if period["created"] >= limit:
                    break

                if artist["artisthash"] in indexed:
                    continue

                # INFO: track['tracks'] is a dict of trackhashes and their counts
                # get the trackhashes sorted by count
                trackhashes = sorted(
                    artist["tracks"], key=lambda x: artist["tracks"][x], reverse=True
                )

                mix = self.create_artist_mix(
                    artist, trackhashes[: self.MAX_TRACKS_TO_FETCH], userid=userid
                )

                if mix:
                    mixes.append(mix)
                    indexed.add(artist["artisthash"])
                    period["created"] += 1

        return mixes

    @classmethod
    def get_mix_description(cls, tracks: list[Track], artishash: str):
        """
        Constructs a description for a mix by putting together the first n=4
        artists in the mix tracklist.
        """
        first_4_artists = []
        indexed = set()

        for track in tracks:
            if len(first_4_artists) < 4:
                if (
                    track.artists[0]["artisthash"] != artishash
                    and track.artists[0]["artisthash"] not in indexed
                ):
                    first_4_artists.append(track.artists[0])
                    indexed.add(track.artists[0]["artisthash"])

        if len(first_4_artists) == 4:
            return f"Featuring {', '.join(a['name'] for a in first_4_artists)} and more"

        if len(first_4_artists) > 0:
            return f"Featuring {', '.join(a['name'] for a in first_4_artists)}"

        return f"Featuring {tracks[0].artists[0]['name']}"

    def create_artist_mix(
        self, artist: dict[str, str], trackhashes: list[str], userid: int
    ):
        """
        Given an artist dict, creates an artist mix.
        """
        _artist = ArtistStore.artistmap.get(artist["artisthash"])

        if not _artist:
            return None

        tracks = TrackStore.get_tracks_by_trackhashes(trackhashes)
        # tracks = sorted(tracks, key=lambda x: x.playduration, reverse=True)
        # sourcetracks = tracks[: self.MAX_TRACKS_TO_FETCH]

        # INFO: Sort the trackhashes when creating the sourcehash
        sourcehash = create_hash(
            *sorted(trackhashes, key=lambda x: trackhashes.index(x))
        )

        db_mix = MixTable.get_by_sourcehash(sourcehash)
        if db_mix:
            return db_mix

        mix_tracks, albums, artists = self.get_track_mix_data(tracks)

        if len(mix_tracks) < self.MIN_TRACK_MIX_LENGTH:
            return None

        # INFO: Dump mixes with no variety
        if len(set(t.artisthashes[0] for t in mix_tracks)) < self.MIN_ARTISTS_PER_MIX:
            return None

        # try downloading artist image
        mix_image = {"image": _artist.artist.image, "color": _artist.artist.color}
        image = self.download_artist_image(_artist.artist)

        if image:
            mix_image["image"] = image

        mix = Mix(
            # the a prefix indicates that this is an artist mix
            id=f"a{userid}{artist['artisthash']}",
            title=artist["artist"] + " Radio",
            description=self.get_mix_description(mix_tracks, artist["artisthash"]),
            tracks=[t.trackhash for t in mix_tracks],
            sourcehash=sourcehash,
            userid=userid,
            extra={
                "type": "artist",
                "artisthash": artist["artisthash"],
                "sourcetracks": trackhashes,
                "image": mix_image,
                # NOTE: Save the similar albums and artists
                # Related to the source tracks that were used to create the mix
                # Will be useful when generating other homepage entries
                "albums": albums,
                "artists": artists,
            },
            timestamp=int(time.time()),
        )

        MixTable.insert_one(mix)
        return mix

    def download_artist_image(self, artist: Artist):
        try:
            res = requests.get(
                f"{self.server}/mix/image?artist={quote(artist.name)}&type=Artist"
            )
        except requests.exceptions.ConnectionError:
            return None

        if res.status_code == 200:
            filename = f"{artist.artisthash}_{int(time.time())}.webp"
            path = Paths.get_md_mixes_img_path() + "/" + filename

            image = Image.open(BytesIO(res.content))
            aspect_ratio = image.width / image.height

            # resize to 512px
            md_width = 512
            md_height = int(md_width / aspect_ratio)

            image = image.resize((md_width, md_height), Image.LANCZOS)
            image.save(path, "webp")

            # resize to 256px
            sm_width = 256
            sm_height = int(sm_width / aspect_ratio)

            image = image.resize((sm_width, sm_height), Image.LANCZOS)
            small_path = Paths.get_sm_mixes_img_path() + "/" + filename
            image.save(small_path, "webp")

            return filename

        return None

    def fallback_create_artist_mix(
        self,
        # artist: dict[str, str],
        similar_albums: list[str],
        similar_artists: list[str],
        omit_trackhashes: set[str],
        limit: int = 99,
    ):
        """
        Creates an artist mix by selecting random tracks from similar albums and artists.

        This is used when:
        - The Swing Music recommendation server is down.
        - The artist has less than self.MIN_TRACK_MIX_LENGTH tracks from the cloud mix.
        - When we need to dilute the mix to balance the artist distribution.

        :param similar_albums: A list of similar album weakhashes to select tracks from.
        :param similar_artists: A list of similar artist hashes to select tracks from.
        :param omit_trackhashes: A set of trackhashes to omit from the new tracklist.
        :param limit: The maximum number of tracks to select.
        """

        mixtracks = []
        albummatches = (
            a
            for a in AlbumStore.albummap.values()
            if a.album.weakhash in similar_albums
        )

        for match in albummatches:
            if len(mixtracks) >= limit:
                return mixtracks

            albumtracks = [
                t
                for t in TrackStore.get_tracks_by_trackhashes(match.trackhashes)
                if t.weakhash not in omit_trackhashes
            ]

            if len(albumtracks) == 0:
                continue

            sample = random.sample(albumtracks, k=1)
            mixtracks.extend(sample)

        artistmatches = (
            a
            for a in ArtistStore.artistmap.values()
            if a.artist.artisthash in similar_artists
        )

        for match in artistmatches:
            if len(mixtracks) >= limit:
                return mixtracks

            artisttracks = [
                t
                for t in TrackStore.get_tracks_by_trackhashes(match.trackhashes)
                if t.weakhash not in omit_trackhashes
            ]

            if len(artisttracks) == 0:
                continue

            sample = random.sample(artisttracks, k=1)
            mixtracks.extend(sample)

        return mixtracks

    def get_mix_from_lastfm_data(self, artisthash: str, limit: int):
        """
        Creates a mix from the locally available lastfm similar artists data.

        The resulting mix is definitely expected to be of low quality.

        TODO: Maybe implement this!
        """
        pass

    @classmethod
    def get_track_mix(cls, mix: Mix):
        """
        Given a mix, returns the excess tracks as a custom mix.
        """

        # INFO: If the mix can't have more than 20 tracks, return None
        if len(mix.tracks) <= cls.MIX_TRACKS_LENGTH + 20:
            return None

        og_track = TrackStore.trackhashmap.get(mix.tracks[0])

        if not og_track:
            return None

        og_track = og_track.get_best()
        tracks = [og_track] + TrackStore.get_tracks_by_trackhashes(
            mix.tracks[cls.MIX_TRACKS_LENGTH :]
        )

        trackmix = Mix(
            id=f"t{mix.userid}{mix.extra['artisthash']}",
            title=og_track.title,
            description=cls.get_mix_description(tracks, mix.extra["artisthash"]),
            tracks=[t.trackhash for t in tracks],
            sourcehash=create_hash(*[t.trackhash for t in tracks]),
            userid=mix.userid,
            extra={
                "type": "track",
                "og_sourcehash": mix.sourcehash,
                "images": cls.get_custom_mix_images(tracks),
                "artists": None,
                "albums": None,
            },
        )
        trackmix.timestamp = mix.timestamp

        # INFO: Write track mix save state
        if mix.extra.get("trackmix_saved"):
            trackmix.saved = True

        return trackmix

    @classmethod
    def get_custom_mix_images(cls, tracks: list[Track]):
        first_album = tracks[0].albumhash
        first_img = {
            "image": first_album + ".webp",
            "type": "album",
            "color": AlbumStore.albummap[first_album].album.color,
        }

        seen = set()
        images = [first_img]

        for track in tracks[1:]:
            artisthash = track.artists[0]["artisthash"]

            if artisthash in seen:
                continue

            artist = ArtistStore.artistmap.get(artisthash)

            if not artist:
                continue

            seen.add(artisthash)

            image = {
                "image": artisthash + ".webp",
                "type": "artist",
                "color": artist.artist.color,
            }

            images.append(image)

            if len(images) == 3:
                break

        return images

    @staticmethod
    def get_because_items(mixes: list[Mix]):
        """
        Given a list of mixes, returns a list of artists that are similar to the
        artists in the mixes.
        """
        artists: dict[str, list[dict[str, str | int]]] = {}
        albums: dict[str, list[dict[str, str | int]]] = {}

        pivot_artist = None
        pivot_artist_index = None

        # Get pivot artist
        for index, mix in enumerate(mixes):
            artist = ArtistStore.artistmap.get(mix.extra["artisthash"])
            if not artist:
                continue

            pivot_artist = artist.artist
            pivot_artist_index = index
            break

        if not pivot_artist:
            return None, None

        for mix in mixes[pivot_artist_index:]:
            mix_artisthash = mix.extra["artisthash"]
            artists.setdefault(mix_artisthash, [])
            albums.setdefault(mix_artisthash, [])

            for artisthash in mix.extra["artists"]:
                artist = ArtistStore.artistmap.get(artisthash)

                if not artist:
                    continue

                artists[mix_artisthash].append(
                    {
                        "type": "artist",
                        "trackcount": artist.artist.trackcount,
                        "hash": artisthash,
                        "help_text": str(artist.artist.trackcount)
                        + ngettext(" track", " tracks", artist.artist.trackcount),
                    }
                )

            for albumhash in mix.extra["albums"]:
                album = AlbumStore.albummap.get(albumhash)

                if not album:
                    continue

                albums[mix_artisthash].append(
                    {
                        "type": "album",
                        "trackcount": album.album.trackcount,
                        "hash": albumhash,
                        "help_text": str(album.album.trackcount)
                        + ngettext(" track", " tracks", album.album.trackcount),
                    }
                )

            # INFO: Sort artists by trackcount
            artists[mix_artisthash] = sorted(
                artists[mix_artisthash],
                key=lambda x: x["trackcount"],
                reverse=True,
            )

            # INFO: Sort albums by trackcount
            albums[mix_artisthash] = sorted(
                albums[mix_artisthash],
                key=lambda x: x["trackcount"],
                reverse=True,
            )

        because_you_listened_to_artist = {
            "title": "Because you listened to "
            + pivot_artist.name,
            "items": albums[pivot_artist.artisthash][:15],
        }

        # Flatten list of artists and remove duplicates by artisthash
        all_artists = []
        seen = set()

        # for artist_list in artists.values():
        #     for artist in artist_list:
        #         if artist["hash"] not in seen:
        #             all_artists.append(artist)
        #             seen.add(artist["hash"])

        artists_you_might_like = {
            "title": "Artists you might like",
            "items": artists[pivot_artist.artisthash][:15],
        }

        return because_you_listened_to_artist, artists_you_might_like
