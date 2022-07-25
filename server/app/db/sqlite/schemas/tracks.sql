CREATE TABLE IF NOT EXISTS tracks (
        trackid TEXT PRIMARY KEY,
        title TEXT,
        album INTEGER,
        artists TEXT,
        albumartist TEXT,
        albumhash TEXT,
        folder TEXT,
        filepath TEXT,
        length INTEGER,
        bitrate INTEGER,
        genre TEXT,
        image TEXT,
        tracknumber INTEGER,
        disknumber INTEGER,
        uniqhash TEXT
);

