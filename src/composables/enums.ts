export enum playSources {
  playlist,
  album,
  search,
  folder,
  artist,
  albumCard,
}

export enum NotifType {
  Success = "success",
  Info = "info",
  Error = "error",
  Working = "working",
}

export enum FromOptions {
  playlist = "playlist",
  folder = "folder",
  album = "album",
  search = "search",
  artist = "artist",
  albumCard = "albumCard",
}

export enum ContextSrc {
  PHeader = "PHeader",
  Track = "Track",
  AHeader = "AHeader",
  FHeader = "FHeader",
}

export const FuseTrackOptions = {
  keys: [
    { name: "title", weight: 1 },
    { name: "album", weight: 0.7 },
    { name: "artist.name", weight: 0.5 },
    { name: "albumartist", weight: 0.25 },
  ],
};

export enum contextChildrenShowMode {
  click = "click",
  hover = "hover",
}

export enum discographyAlbumTypes {
  all = "All",
  albums = "Albums",
  singles = "Singles",
  eps = "EPs",
  appearances = "Appearances",
}
