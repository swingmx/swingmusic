const development = import.meta.env.DEV;
const dev_url = "http://localhost:1970";

const baseApiUrl = development ? dev_url : "";
const baseImgUrl = baseApiUrl + "/img";

const imageRoutes = {
  thumb: {
    large: "/t/",
    small: "/t/s/",
  },
  artist: {
    large: "/a/",
    small: "/a/s/",
  },
  playlist: "/p/",
  raw: "/raw/",
};

const paths = {
  api: {
    album: baseApiUrl + "/album",
    favorite: baseApiUrl + "/favorite",
    favorites: baseApiUrl + "/favorites",
    favAlbums: baseApiUrl + "/albums/favorite",
    favTracks: baseApiUrl + "/tracks/favorite",
    favArtists: baseApiUrl + "/artists/favorite",
    isFavorite: baseApiUrl + "/favorites/check",
    artist: baseApiUrl + "/artist",
    get addFavorite() {
      return this.favorite + "/add";
    },
    get removeFavorite() {
      return this.favorite + "/remove";
    },
    get albumartists() {
      return this.album + "/artists";
    },
    get albumbio() {
      return this.album + "/bio";
    },
    get albumsByArtistUrl() {
      return this.album + "/from-artist";
    },
    folder: baseApiUrl + "/folder",
    playlist: {
      base: baseApiUrl + "/playlist",
      get new() {
        return this.base + "/new";
      },
      get all() {
        return this.base + "s";
      },
      get artists() {
        return this.base + "/artists";
      },
    },
    search: {
      base: baseApiUrl + "/search",
      get tracks() {
        return this.base + "/tracks?q=";
      },
      get albums() {
        return this.base + "/albums?q=";
      },
      get artists() {
        return this.base + "/artists?q=";
      },
      get load() {
        return this.base + "/loadmore";
      },
    },
    files: baseApiUrl + "/file",
  },
  images: {
    thumb: {
      small: baseImgUrl + imageRoutes.thumb.small,
      large: baseImgUrl + imageRoutes.thumb.large,
    },
    artist: {
      small: baseImgUrl + imageRoutes.artist.small,
      large: baseImgUrl + imageRoutes.artist.large,
    },
    playlist: baseImgUrl + imageRoutes.playlist,
    raw: baseImgUrl + imageRoutes.raw,
  },
};

export { paths };
