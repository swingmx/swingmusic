import { NotifType } from "./stores/enums";

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

interface Folder {
  name: string;
  path: string;
  trackscount: number;
  subdircount: number;
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

interface Option {
  type?: string;
  label?: string;
  action?: Function;
  children?: Option[] | false;
  icon?: string;
  critical?: Boolean;
}

interface Playlist {
  playlistid: string;
  name: string;
  description?: string;
  image?: string;
}

interface Notif {
  text: string;
  type: NotifType;
}

export { Track, Folder, AlbumInfo, Artist, Option, Playlist, Notif };
