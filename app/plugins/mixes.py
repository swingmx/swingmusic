import datetime
import json
from pprint import pprint
import random
import string
import time
import requests
from urllib.parse import quote
from PIL import Image

from app.db.userdata import MixTable, SimilarArtistTable
from app.lib.colorlib import get_image_colors
from app.models.artist import Artist
from app.models.mix import Mix
from app.models.track import Track
from app.plugins import Plugin, plugin_method
from app.settings import Paths
from app.store.albums import AlbumStore
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore
from app.utils.dates import get_date_range, get_duration_ago
from app.utils.hashing import create_hash
from app.utils.mixes import balance_mix
from app.utils.remove_duplicates import remove_duplicates
from app.utils.stats import get_artists_in_period


class MixAlreadyExists(Exception):
    """
    Raised when a mix with the same sourcehash already exists.
    """

    pass


class MixesPlugin(Plugin):
    MAX_TRACKS_TO_FETCH = 5
    TRACK_MIX_LENGTH = 30
    MIN_TRACK_MIX_LENGTH = 15

    MIN_DAY_LISTEN_DURATION = 3 * 60  # 3 minutes
    MIN_WEEK_LISTEN_DURATION = 10 * 60  # 10 minutes
    MIN_MONTH_LISTEN_DURATION = 20 * 60  # 20 minutes

    def __init__(self):
        super().__init__("mixes", "Mixes")
        self.server = "https://smcloud.mungaist.com"

        server_online = self.ping_server()
        self.set_active(server_online)

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
    def get_track_mix(self, tracks: list[Track], with_help: bool = False):
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
                "query": f"{track.title} - {','.join(a['name'] for a in track.artists)}",
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

        trackhashes: list[str] = results["tracks"]

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
                similar_artists=results["artists"],
                similar_albums=results["albums"],
                omit_trackhashes={t.weakhash for t in trackmatches},
                # limit=self.TRACK_MIX_LENGTH - len(trackmatches),
            )
            trackmatches.extend(filler_tracks)

        # try to balance the mix
        trackmatches = balance_mix(trackmatches)
        return trackmatches, results["albums"], results["albums"]

    @plugin_method
    def get_artist_mix(self, artisthash: str):
        """
        Given an artisthash, creates an artist mix using the
        self.MAX_TRACKS_TO_FETCH most listened to tracks.

        Returns a tuple of the mix and the sourcehash.
        """
        artist = ArtistStore.artistmap[artisthash]
        tracks = TrackStore.get_tracks_by_trackhashes(artist.trackhashes)

        tracks = sorted(tracks, key=lambda x: x.playduration, reverse=True)
        sourcetracks = tracks[: self.MAX_TRACKS_TO_FETCH]
        sourcehash = create_hash(*[t.trackhash for t in sourcetracks])

        if MixTable.get_by_sourcehash(sourcehash):
            raise MixAlreadyExists()

        tracks, albums, artists = self.get_track_mix(tracks[: self.MAX_TRACKS_TO_FETCH])
        return (tracks, albums, artists, sourcehash)

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
                "max": 3,
                "artists": get_artists_in_period(today_start, today_end, userid),
                "created": 0,
            },
            "last_2_days": {
                "max": 2,
                "artists": get_artists_in_period(
                    last_2_days_start, time.time(), userid
                ),
                "created": 0,
            },
            "last_7_days": {
                "max": 3,
                "artists": get_artists_in_period(
                    last_7_days_start, time.time(), userid
                ),
                "created": 0,
            },
            "last_1_month": {
                "max": 2,
                "artists": get_artists_in_period(
                    last_1_month_start, time.time(), userid
                ),
                "created": 0,
            },
        }

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

                mix = self.create_artist_mix(artist)

                if mix:
                    mixes.append(mix)
                    indexed.add(artist["artisthash"])
                    period["created"] += 1

        print(f"⭐⭐⭐⭐ Created {len(mixes)} mixes")
        return mixes

    def get_mix_description(self, tracks: list[Track], artishash: str):
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

    def create_artist_mix(self, artist: dict[str, str]):
        """
        Given an artist dict, creates an artist mix.
        """
        _artist = ArtistStore.artistmap.get(artist["artisthash"])

        if not _artist:
            return None

        tracks = TrackStore.get_tracks_by_trackhashes(_artist.trackhashes)
        tracks = sorted(tracks, key=lambda x: x.playduration, reverse=True)
        sourcetracks = tracks[: self.MAX_TRACKS_TO_FETCH]
        sourcehash = create_hash(*[t.trackhash for t in sourcetracks])

        db_mix = MixTable.get_by_sourcehash(sourcehash)
        if db_mix:
            print(f"🔍 Found existing mix for {_artist.artist.name}")
            print(db_mix.title)
            return db_mix

        mix_tracks, albums, artists = self.get_track_mix(sourcetracks)

        if len(mix_tracks) < self.MIN_TRACK_MIX_LENGTH:
            return None

        # try downloading artist image
        mix_image = {"image": _artist.artist.image, "color": _artist.artist.color}
        downloaded_img_color = self.download_artist_image(_artist.artist)

        if downloaded_img_color:
            mix_image["image"] = f"{_artist.artist.artisthash}.jpg"
            mix_image["color"] = downloaded_img_color[0]

        mix = Mix(
            # the a prefix indicates that this is an artist mix
            id=f"a{artist['artisthash']}",
            title=artist["artist"] + " Radio",
            description=self.get_mix_description(mix_tracks, artist["artisthash"]),
            tracks=[t.trackhash for t in mix_tracks],
            sourcehash=sourcehash,
            extra={
                "type": "artist",
                "artisthash": artist["artisthash"],
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
            res = requests.get(f"{self.server}/image?artist={artist.name}")
        except requests.exceptions.ConnectionError:
            return None

        if res.status_code == 200:
            # save to file
            with open(
                f"{Paths.get_md_mixes_img_path()}/{artist.artisthash}.jpg", "wb"
            ) as f:
                f.write(res.content)

            # resize to 256px width while maintaining aspect ratio
            img = Image.open(f"{Paths.get_md_mixes_img_path()}/{artist.artisthash}.jpg")
            aspect_ratio = img.width / img.height

            newwidth = 256
            newheight = int(256 / aspect_ratio)

            img = img.resize((newwidth, newheight), Image.LANCZOS)
            img.save(f"{Paths.get_sm_mixes_img_path()}/{artist.artisthash}.jpg")

            return get_image_colors(
                f"{Paths.get_sm_mixes_img_path()}/{artist.artisthash}.jpg"
            )

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

        TODO: Implement this!
        """
        pass
