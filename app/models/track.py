from dataclasses import dataclass

from app.settings import get_flag, ParserFlags
from app.utils.hashing import create_hash
from app.utils.parsers import split_artists, remove_prod, parse_feat_from_title, clean_title, \
    get_base_title_and_versions
from .artist import ArtistMinimal


@dataclass(slots=True)
class Track:
    """
    Track class
    """

    album: str
    albumartist: str | list[ArtistMinimal]
    albumhash: str
    artist: str | list[ArtistMinimal]
    bitrate: int
    copyright: str
    date: str
    disc: int
    duration: int
    filepath: str
    folder: str
    genre: str | list[str]
    title: str
    track: int
    trackhash: str

    filetype: str = ""
    image: str = ""
    artist_hashes: str = ""
    is_favorite: bool = False
    og_title: str = ""
    og_album: str = ""

    def __post_init__(self):
        self.og_title = self.title
        self.og_album = self.album

        if self.artist is not None:
            artists = split_artists(self.artist)
            new_title = self.title

            if get_flag(ParserFlags.EXTRACT_FEAT):
                featured, new_title = parse_feat_from_title(self.title)
                original_lower = "-".join([a.lower() for a in artists])
                artists.extend([a for a in featured if a.lower() not in original_lower])

            if get_flag(ParserFlags.REMOVE_PROD):
                new_title = remove_prod(new_title)

            # if track is a single
            if self.og_title == self.album:
                self.album = new_title

            if get_flag(ParserFlags.REMOVE_REMASTER_FROM_TRACK):
                new_title = clean_title(new_title)

            self.title = new_title

            if get_flag(ParserFlags.CLEAN_ALBUM_TITLE):
                self.album, _ = get_base_title_and_versions(self.album, get_versions=False)

            self.artist_hashes = "-".join(create_hash(a, decode=True) for a in artists)
            self.artist = [ArtistMinimal(a) for a in artists]

            albumartists = split_artists(self.albumartist)
            self.albumartist = [ArtistMinimal(a) for a in albumartists]

        self.filetype = self.filepath.rsplit(".", maxsplit=1)[-1]
        self.image = self.albumhash + ".webp"

        if self.genre is not None:
            self.genre = str(self.genre).replace("/", ",").replace(";", ",")
            self.genre = str(self.genre).lower().split(",")
            self.genre = [g.strip() for g in self.genre]

        self.recreate_hash()

    def recreate_hash(self):
        """
        Recreates a track hash if the track title was altered
        to prevent duplicate tracks having different hashes.
        """
        if self.og_title == self.title and self.og_album == self.album:
            return

        self.trackhash = create_hash(", ".join([a.name for a in self.artist]), self.og_album, self.title)

    def recreate_artists_hash(self):
        self.artist_hashes = "-".join(a.artisthash for a in self.artist)

    def rename_album(self, new_album: str):
        self.album = new_album

    def add_artists(self, artists: list[str], new_album_title: str):
        for artist in artists:
            if create_hash(artist) not in self.artist_hashes:
                self.artist.append(ArtistMinimal(artist))

        self.recreate_artists_hash()
        self.rename_album(new_album_title)
