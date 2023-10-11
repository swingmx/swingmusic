import json
import sqlite3
import os
from app.db.sqlite.artistcolors import SQLiteArtistMethods
from app.db.sqlite.queries import CREATE_APPDB_TABLES

from app.db.sqlite.utils import SQLiteManager

db_path = "test.db"


def test_sqlite_manager():
    with SQLiteManager(test_db_path=db_path) as cur:
        for query in CREATE_APPDB_TABLES.split(";"):
            cur.execute(query)

        cur.execute(
            "INSERT INTO tracks (album, albumartist, albumhash, artist, bitrate, copyright, date, disc, duration, filepath, folder, genre, last_mod, title, track, trackhash) VALUES ('Dummy Album', 'Dummy Album Artist', 'dummyalbumhash', 'Dummy Artist', 320, 'Dummy Copyright', 1630454400, 1, 180, '/path/to/dummy/file.mp3', '/path/to/dummy/folder', 'Dummy Genre', 1630454400.5, 'Dummy Title', 1, 'dummytrackhash');"
        )

        cur.execute("SELECT * FROM tracks")
        result = cur.fetchone()
        assert result[7] == 1630454400

    # Test using a connection
    with SQLiteManager(conn=sqlite3.connect(db_path)) as cur:
        cur.execute("SELECT * FROM tracks")
        result = cur.fetchone()
        assert result[7] == 1630454400


def test_insert_one_artist():
    color1 = "rgb(0, 0, 0)"
    color2 = "rgb(255, 255, 255)"

    with SQLiteManager(test_db_path=db_path) as cur:
        SQLiteArtistMethods.insert_one_artist(cur, "artisthash1", [color1, color2])
        cur.execute("SELECT * FROM artists WHERE artisthash=?", ("artisthash1",))

        result = cur.fetchone()
        assert result[1:] == ("artisthash1", json.dumps([color1, color2]), None)


def test_get_all_artists():
    with SQLiteManager(test_db_path=db_path) as cur:
        artists = SQLiteArtistMethods.get_all_artists(cur)

        # assert that that the generator is not empty and that for each tuple has 4 elements

        try:
            while True:
                artist = next(artists)
                assert len(artist) == 4
        except StopIteration:
            pass


def test_remove_test_db():
    os.remove(db_path)
