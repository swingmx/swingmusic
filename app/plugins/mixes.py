import json
import string
import requests
from urllib.parse import quote

from app.db.userdata import SimilarArtistTable
from app.models.artist import Artist
from app.models.mix import Mix
from app.models.track import Track
from app.plugins import Plugin, plugin_method
from app.store.artists import ArtistStore
from app.store.tracks import TrackStore
from app.utils.dates import get_date_range
from app.utils.mixes import balance_mix
from app.utils.remove_duplicates import remove_duplicates
from app.utils.stats import get_artists_in_period


class MixesPlugin(Plugin):
    MAX_TRACKS_TO_FETCH = 5
    TRACK_MIX_LENGTH = 50
    MIN_TRACK_MIX_LENGTH = 15

    MIN_DAY_LISTEN_DURATION = 3 * 60  # 3 minutes
    MIN_WEEK_LISTEN_DURATION = 10 * 60  # 10 minutes
    MIN_MONTH_LISTEN_DURATION = 20 * 60  # 20 minutes

    def __init__(self):
        super().__init__("mixes", "Mixes")
        self.server = "https://smcloud.mungaist.com"
        self.set_active(True)

    @plugin_method
    def get_track_mix(self, tracks: list[Track], with_help: bool = False):
        # query = f"{track.title} - {','.join(a['name'] for a in track.artists)}"
        queries = [
            {
                "query": f"{track.title} - {','.join(a['name'] for a in track.artists)}",
                "album": track.og_album,
                "with_help": with_help,
            }
            for track in tracks
        ]

        response = requests.post(
            f"{self.server}/radio",
            json=queries,
        )
        results = response.json()

        # artisthashes = results["artists"]
        trackhashes: list[str] = results["tracks"]

        trackmatches = TrackStore.get_flat_list()
        trackmatches = [t for t in trackmatches if t.weakhash in trackhashes]

        # filter out duplicates of the same weakhash
        # group by weakhash and pick the one with the highest bitrate
        grouped: dict[str, list[Track]] = {}
        for track in trackmatches:
            grouped.setdefault(track.weakhash, []).append(track)

        trackmatches = [max(group, key=lambda x: x.bitrate) for group in grouped.values()]

        # sort by trackhash order
        trackmatches = sorted(trackmatches, key=lambda x: trackhashes.index(x.weakhash))
        trackmatches = balance_mix(trackmatches)
        return trackmatches

    @plugin_method
    def get_artist_mix(self, artisthash: str):
        artist = ArtistStore.artistmap[artisthash]
        tracks = TrackStore.get_tracks_by_trackhashes(artist.trackhashes)

        tracks = sorted(tracks, key=lambda x: x.playduration, reverse=True)
        return self.get_track_mix(tracks[: self.MAX_TRACKS_TO_FETCH])

    @plugin_method
    def get_artists(self, limit: int = 10):
        mixes: list[Mix] = []
        indexed = set()

        today_start, today_end = get_date_range(duration="day")
        last_2_days_start, last_2_days_end = get_date_range(duration="day", units_ago=2)
        last_7_days_start, last_7_days_end = get_date_range(duration="week")
        last_1_month_start, last_1_month_end = get_date_range(duration="month")

        artists = {
            "today": {
                "max": 2,
                "artists": get_artists_in_period(today_start, today_end),
                "created": 0,
            },
            "last_2_days": {
                "max": 2,
                "artists": get_artists_in_period(last_2_days_start, last_2_days_end),
                "created": 0,
            },
            "last_7_days": {
                "max": 3,
                "artists": get_artists_in_period(last_7_days_start, last_7_days_end),
                "created": 0,
            },
            "last_1_month": {
                "max": 2,
                "artists": get_artists_in_period(last_1_month_start, last_1_month_end),
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

            for artist in period["artists"][:limit]:
                mix = self.create_artist_mix(artist)

                if mix:
                    mixes.append(mix)
                    indexed.add(artist["artisthash"])
                    period["created"] += 1

        print(f"⭐⭐⭐⭐ Created {len(mixes)} mixes")
        return mixes

    def get_mix_description(self, tracks: list[Track], artishash: str):
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
        mix_tracks = self.get_artist_mix(artist["artisthash"])

        if len(mix_tracks) < self.MIN_TRACK_MIX_LENGTH:
            return None

        return Mix(
            id=artist["artisthash"],
            title=artist["artist"],
            description=self.get_mix_description(mix_tracks, artist["artisthash"]),
            tracks=[t.trackhash for t in mix_tracks],
            extra={
                "type": "artist",
                "artisthash": artist["artisthash"],
            },
        )


    def fallback_create_artist_mix(self, artist: dict[str, str], similar_artists: list[str], trackhashes: set[str], limit: int):
        """
        Creates an artist mix by selecting random tracks from similar artists.

        This is used when:
        - The Swing Music recommendation server is down.
        - The artist has less than self.MIN_TRACK_MIX_LENGTH tracks from the cloud mix.
        - When we need to dilute the mix to balance the artist distribution.

        :param artist: The artist to create a mix for.
        :param similar_artists: A list of similar artists to select tracks from. If not provided, we try reading from the local database. When we exhaust the passed list, we also try reading from the local database.
        :param trackhashes: A set of trackhashes to omit from the new tracklist.
        :param limit: The maximum number of tracks to select.
        """
        artists = similar_artists

        if len(similar_artists) == 0:
            local_similar_artists = SimilarArtistTable.get_by_hash(artist["artisthash"])

            if local_similar_artists:
                artists = [a.artisthash for a in local_similar_artists.similar_artists]

        if len(artists) == 0:
            return []

        # CHECKPOINT: I'M TIRED AF AND I NEED TO SLEEP
        # The plan:
        # Figure out which artists we should skip for the new tracklist
        # these would be artists with a large number of tracks in the mix already

        # Since the artisthashes are ordered by similarity score, we iterate from the start
        # and go forward collecting tracks that aren't in the mix yet.
        # 