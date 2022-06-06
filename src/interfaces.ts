import { FromOptions } from "./composables/enums";
import { NotifType } from "./composables/enums";

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
  trackcount: number;
  subdircount: number;
}

interface AlbumInfo {
  title: string;
  artist: string;
  count: number;
  duration: number;
  date: string;
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
  image?: string | FormData;
  tracks?: Track[];
  count?: number;
  lastUpdated?: string;
  thumb?: string;
}

interface Notif {
  text: string;
  type: NotifType;
}

interface fromFolder {
  type: FromOptions;
  path: string;
  name: string;
}
interface fromAlbum {
  type: FromOptions;
  name: string;
  albumartist: string;
}
interface fromPlaylist {
  type: FromOptions;
  name: string;
  playlistid: string;
}

interface fromSearch {
  type: FromOptions;
  query: string;
}

interface subPath {
  name: string;
  path: string;
}

export {
  Track,
  Folder,
  AlbumInfo,
  Artist,
  Option,
  Playlist,
  Notif,
  fromFolder,
  fromAlbum,
  fromPlaylist,
  fromSearch,
  subPath,
};
