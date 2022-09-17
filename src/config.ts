// "local" | "remote"
let mode = "remote";

export interface D<T = string> {
  [key: string]: T;
}

const domains: D = {
  local: "http://localhost:",
  remote: "http://10.5.71.115:",
};

const ports = {
  api: 1970,
  images: 1971,
};

const imageRoutes = {
  thumb: "/t/",
  artist: "/a/",
  playlist: "/p/",
  raw: "/raw/",
};

function toggleMode() {
  mode = mode === "local" ? "remote" : "local";
}

const domain = () => domains[mode];

const baseImgUrl = domain() + ports.images;

const baseApiUrl = domain() + ports.api;

const paths = {
  api: {
    album: baseApiUrl + "/album",
    get albumartists() {
      return this.album + "/artists";
    },
    get albumbio() {
      return this.album + "/bio";
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
    thumb: baseImgUrl + imageRoutes.thumb,
    artist: baseImgUrl + imageRoutes.artist,
    playlist: baseImgUrl + imageRoutes.playlist,
    raw: baseImgUrl + imageRoutes.raw,
  },
};

export { paths, toggleMode };

// TODO: Add setting to toggle between extending to edges or not