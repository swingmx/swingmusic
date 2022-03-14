interface Track {
  trackid: string;
  title: string;
  album?: string;
  artists: string[];
  albumartist?: string;
  folder?: string;
  filepath?: string;
  length?: number;
  bitrate?: number;
  genre?: string;
  image: string;
  tracknumber?: number;
  discnumber?: number;
}

interface AlbumInfo {
  album: string;
  artist: string;
  count: number;
  duration: number;
  date: string;
  artistimage: string;
  image: string;
}

interface Artist {
  name: string;
  image: string;
}

export { Track, AlbumInfo, Artist };
