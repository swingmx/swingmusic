export enum playSources {
  playlist,
  album,
  search,
  folder,
}

export enum NotifType {
  Success,
  Info,
  Error,
}

export enum FromOptions {
  playlist = "playlist",
  folder = "folder",
  album = "album",
  search = "search",
}

export enum ContextSrc {
  PHeader = "PHeader",
  Track = "Track",
  AHeader = "AHeader",
  FHeader = "FHeader"
}

export enum Routes {
  home = "Home",
  folder = "FolderView",
  playlists = "Playlists",
  playlist = "PlaylistView",
  albums = "AlbumsView",
  album = "AlbumView",
  artists = "ArtistsView",
  settings = "SettingsView",
}