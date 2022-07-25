CREATE TABLE
  IF NOT EXISTS albums (
    albumid TEXt PRIMARY KEY,
    title TEXT,
    artist TEXT,
    albumartist TEXT,
    date TEXT,
    image TEXT,
    hash TEXT,
    colors TEXT
  )