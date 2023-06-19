from app.models import Album, Artist, Track


def recent_fav_track_serializer(track: Track) -> dict:
    """
    Simplifies a track object into a dictionary to remove unused
    properties on the client.
    """
    return {
        "image": track.image,
        "title": track.title,
        "trackhash": track.trackhash,
        "filepath": track.filepath,
    }


def recent_fav_album_serializer(album: Album) -> dict:
    """
    Simplifies an album object into a dictionary to remove unused
    properties on the client.
    """
    return {
        "image": album.image,
        "title": album.og_title,
        "albumhash": album.albumhash,
        "artist": album.albumartists[0].name,
        "colors": album.colors,
    }


def recent_fav_artist_serializer(artist: Artist) -> dict:
    """
    Simplifies an artist object into a dictionary to remove unused
    properties on the client.
    """
    return {
        "image": artist.image,
        "name": artist.name,
        "artisthash": artist.artisthash,
    }
