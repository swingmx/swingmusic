// "dev" | "prod"
let mode = "dev";

export interface D<T = string> {
  [key: string]: T;
}

const domains: D = {
  dev: "http://localhost:1970",
  prod: "",
};

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

function toggleMode() {
  mode = mode === "dev" ? "prod" : "dev";
}

const domain = () => domains[mode];

const baseApiUrl = domain();
const baseImgUrl = baseApiUrl + "/img";

const paths = {
  api: {
    album: baseApiUrl + "/album",
    favAlbums: baseApiUrl + "/albums/favorite",
    favTracks: baseApiUrl + "/tracks/favorite",
    favArtists: baseApiUrl + "/artists/favorite",
    artist: baseApiUrl + "/artist",
    favorite: baseApiUrl + "/favorite",
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

export { paths, toggleMode };
