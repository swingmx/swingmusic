import { FromOptions, NotifType } from "./composables/enums";

export interface Track {
  trackid: string;
  title: string;
  album?: string;
  artists: string[];
  albumartist?: string;
  albumhash?: string;
  folder?: string;
  filepath?: string;
  length?: number;
  bitrate?: number;
  genre?: string;
  image: string;
  tracknumber?: number;
  discnumber?: number;
  index?: number;
  uniq_hash: string;
  copyright?: string;
}

export interface Folder {
  name: string;
  path: string;
  trackcount: number;
  subdircount: number;
  is_sym: boolean;
}

export interface AlbumInfo {
  albumid: string;
  title: string;
  artist: string;
  count: number;
  duration: number;
  date: string;
  image: string;
  is_compilation: boolean;
  is_soundtrack: boolean;
  is_single: boolean;
  hash: string;
  colors: string[];
  copyright?: string;
}

export interface Artist {
  name: string;
  image: string;
}

export interface Option {
  type?: string;
  label?: string;
  action?: () => void;
  children?: Option[] | false;
  icon?: string;
  critical?: Boolean;
}

export interface Playlist {
  playlistid: string;
  name: string;
  description?: string;
  image?: string | FormData;
  tracks?: Track[];
  count?: number;
  lastUpdated?: string;
  thumb?: string;
  duration?: number;
}

export interface Notif {
  text: string;
  type: NotifType;
}

export interface fromFolder {
  type: FromOptions.folder;
  path: string;
  name: string;
}
export interface fromAlbum {
  type: FromOptions.album;
  name: string;
  hash: string;
  albumartist: string;
}
export interface fromPlaylist {
  type: FromOptions.playlist;
  name: string;
  playlistid: string;
}

export interface fromSearch {
  type: FromOptions.search;
  query: string;
}

export interface subPath {
  name: string;
  path: string;
  active: boolean;
}

export interface FetchProps {
  url: string;
  props?: {};
  get?: boolean;
  put?: boolean;
  headers?: {};
}
