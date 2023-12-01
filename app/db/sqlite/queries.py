"""
This file contains the SQL queries to create the database tables.
"""

CREATE_USERDATA_TABLES = """
CREATE TABLE IF NOT EXISTS playlists (
    id integer PRIMARY KEY,
    image text,
    last_updated text not null,
    name text not null,
    settings text,
    trackhashes text
);

CREATE TABLE IF NOT EXISTS favorites (
    id integer PRIMARY KEY,
    hash text not null,
    type text not null
);

CREATE TABLE IF NOT EXISTS settings (
    id integer PRIMARY KEY,
    root_dirs text NOT NULL,
    exclude_dirs text,
    artist_separators text NOT NULL default '/,;',
    extract_feat integer NOT NULL DEFAULT 1,
    remove_prod integer NOT NULL DEFAULT 1,
    clean_album_title integer NOT NULL DEFAULT 1,
    remove_remaster integer NOT NULL DEFAULT 1,
    merge_albums integer NOT NULL DEFAULT 0,
    show_albums_as_singles integer NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS lastfm_similar_artists (
    id integer PRIMARY KEY,
    artisthash text NOT NULL,
    similar_artists text NOT NULL,
    UNIQUE (artisthash)
);

CREATE TABLE IF NOT EXISTS plugins (
    id integer PRIMARY KEY,
    name text NOT NULL UNIQUE,
    description text NOT NULL,
    active integer NOT NULL DEFAULT 0,
    settings text
);

CREATE TABLE IF NOT EXISTS track_logger (
    id integer PRIMARY KEY,
    trackhash text NOT NULL,
    duration integer NOT NULL,
    timestamp integer NOT NULL,
    source text,
    userid integer NOT NULL DEFAULT 0
)
"""

CREATE_APPDB_TABLES = """
CREATE TABLE IF NOT EXISTS tracks (
    id integer PRIMARY KEY,
    album text NOT NULL,
    albumartist text NOT NULL,
    albumhash text NOT NULL,
    artist text NOT NULL,
    bitrate integer NOT NULL,
    copyright text,
    date integer NOT NULL,
    disc integer NOT NULL,
    duration integer NOT NULL,
    filepath text NOT NULL,
    folder text NOT NULL,
    genre text,
    title text NOT NULL,
    track integer NOT NULL,
    trackhash text NOT NULL,
    last_mod float NOT NULL,
    UNIQUE (filepath)
);

CREATE TABLE IF NOT EXISTS albums (
    id integer PRIMARY KEY,
    albumhash text NOT NULL,
    colors text NOT NULL,
    UNIQUE (albumhash)
);

CREATE TABLE IF NOT EXISTS artists (
    id integer PRIMARY KEY,
    artisthash text NOT NULL,
    colors text,
    bio text,
    UNIQUE (artisthash)
);

CREATE TABLE IF NOT EXISTS folders (
    id integer PRIMARY KEY,
    path text NOT NULL,
    trackcount integer NOT NULL
);
"""

# changed from migrations to dbmigrations in v1.3.0
# to avoid conflicts with the previous migrations.

CREATE_MIGRATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS dbmigrations (
    id integer PRIMARY KEY,
    version integer NOT NULL DEFAULT 0
);

INSERT INTO dbmigrations (version)
SELECT -1
WHERE NOT EXISTS (SELECT 1 FROM dbmigrations);
"""
