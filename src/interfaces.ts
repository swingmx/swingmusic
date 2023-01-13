import { FromOptions, NotifType } from "./composables/enums";

export interface AlbumDisc {
  is_album_disc_number?: boolean;
  album_page_disc_number?: number;
}

export interface Track extends AlbumDisc {
  id: string;
  title: string;
  album?: string;
  artist: Artist[];
  albumartist: Artist[];
  albumhash?: string;
  folder?: string;
  filepath?: string;
  duration?: number;
  bitrate: number;
  image: string;
  track: number;
  disc: number;
  index: number;
  trackhash: string;
  filetype: string;
  is_favorite: boolean;

  genre?: string;
  copyright?: string;
  master_index?: number;
}

export interface Folder {
  name: string;
  path: string;
  has_tracks: number;
  subdircount: number;
  is_sym: boolean;
}

export interface Album {
  albumid: string;
  title: string;
  albumartists: Artist[];
  count: number;
  duration: number;
  date: string;
  image: string;
  artistimg: string;
  albumhash: string;
  colors: string[];
  copyright?: string;

  is_compilation: boolean;
  is_soundtrack: boolean;
  is_single: boolean;
  is_EP: boolean;
  is_favorite: boolean;
  genres: string[];
}

export interface Artist {
  name: string;
  image: string;
  artisthash: string;
  trackcount: number;
  albumcount: number;
  duration: number;
  colors: string[];
  is_favorite?: boolean;
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
  id: string;
  name: string;
  image: string | FormData;
  tracks: Track[];
  count: number;
  last_updated: string;
  thumb: string;
  duration: number;
  has_gif: boolean;
  banner_pos: number;
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
  albumhash: string;
}
export interface fromPlaylist {
  type: FromOptions.playlist;
  name: string;
  id: string;
}

export interface fromSearch {
  type: FromOptions.search;
  query: string;
}

export interface fromArtist {
  type: FromOptions.artist;
  artisthash: string;
  artistname: string;
}

export interface fromFav {
  type: FromOptions.favorite;
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

export interface FuseResult {
  item: Track;
  refIndex: number;
}
