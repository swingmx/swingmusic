import state from "@/composables/state";
import useAlbumPageStore from "@/stores/pages/album";
import useFolderPageStore from "@/stores/pages/folder";
import usePlaylistPageStore from "@/stores/pages/playlist";
import usePlaylistListPageStore from "@/stores/pages/playlists";
import useArtistPageStore from "@/stores/pages/artist";

const home = {
  path: "/",
  name: "Home",
  redirect: "/folder/$home",
};

const folder = {
  path: "/folder/:path",
  name: "FolderView",
  component: () => import("@/views/FolderView.vue"),
  beforeEnter: async (to: any) => {
    state.loading.value = true;
    await useFolderPageStore()
      .fetchAll(to.params.path)
      .then(() => {
        state.loading.value = false;
      });
  },
};

const playlists = {
  path: "/playlists",
  name: "PlaylistList",
  component: () => import("@/views/PlaylistList.vue"),
  beforeEnter: async () => {
    state.loading.value = true;
    await usePlaylistListPageStore()
      .fetchAll()
      .then(() => {
        state.loading.value = false;
      });
  },
};

const playlistView = {
  path: "/playlist/:pid",
  name: "PlaylistView",
  component: () => import("@/views/PlaylistView/index.vue"),
  beforeEnter: async (to: any) => {
    state.loading.value = true;
    await usePlaylistPageStore()
      .fetchAll(to.params.pid)
      .then(() => {
        state.loading.value = false;
      });
  },
};

const albums = {
  path: "/albums",
  name: "AlbumsView",
  component: () => import("@/views/AlbumsExplorer.vue"),
};

const albumView = {
  path: "/albums/:hash",
  name: "AlbumView",
  component: () => import("@/views/AlbumView/index.vue"),
  beforeEnter: async (to: any) => {
    state.loading.value = true;
    const store = useAlbumPageStore();

    await store.fetchTracksAndArtists(to.params.hash).then(() => {
      state.loading.value = false;
    });
  },
};

const artists = {
  path: "/artists",
  name: "ArtistsView",
  component: () => import("@/views/ArtistsExplorer.vue"),
};

const artistView = {
  path: "/artists/:hash",
  name: "ArtistView",
  component: () => import("@/views/ArtistView"),
  beforeEnter: async (to: any) => {
    state.loading.value = true;

    await useArtistPageStore()
      .getData(to.params.hash)
      .then(() => {
        state.loading.value = false;
      });
  },
};

const ArtistTracks = {
  path: "/artists/:hash/tracks",
  name: "ArtistTracks",
  component: () => import("@/views/ArtistTracks.vue"),
};

const artistDiscography = {
  path: "/artists/:hash/discography",
  name: "ArtistDiscographyView",
  component: () => import("@/views/AlbumsGrid.vue"),
};

const settings = {
  path: "/settings",
  name: "SettingsView",
  component: () => import("@/views/SettingsView.vue"),
};

const search = {
  path: "/search/:page",
  name: "SearchView",
  component: () => import("@/views/SearchView"),
};

const queue = {
  path: "/queue",
  name: "QueueView",
  component: () => import("@/views/QueueView.vue"),
};

const favorites = {
  path: "/favorites",
  name: "FavoritesView",
  component: () => import("@/views/Favorites.vue"),
};

const favoriteAlbums = {
  path: "/favorites/albums",
  name: "FavoriteAlbums",
  component: () => import("@/views/FavoriteAlbums.vue"),
};

const favoriteTracks = {
  path: "/favorites/tracks",
  name: "FavoriteTracks",
  component: () => import("@/views/FavoriteTracks.vue"),
};

const favoriteArtists = {
  path: "/favorites/artists",
  name: "FavoriteArtists",
  component: () => import("@/views/FavoriteArtists.vue"),
};

const notFound = {
  name: "NotFound",
  path: "/:pathMatch(.*)",
  component: () => import("@/views/NotFound.vue"),
};

const routes = [
  home,
  folder,
  playlists,
  playlistView,
  albums,
  albumView,
  artists,
  artistView,
  artistDiscography,
  settings,
  search,
  queue,
  notFound,
  ArtistTracks,
  favorites,
  favoriteAlbums,
  favoriteTracks,
  favoriteArtists,
];

const Routes = {
  home: home.name,
  folder: folder.name,
  playlists: playlists.name,
  playlist: playlistView.name,
  albums: albums.name,
  album: albumView.name,
  artists: artists.name,
  artist: artistView.name,
  artistDiscography: artistDiscography.name,
  settings: settings.name,
  search: search.name,
  queue: queue.name,
  notFound: notFound.name,
  artistTracks: ArtistTracks.name,
  favorites: favorites.name,
  favoriteAlbums: favoriteAlbums.name,
  favoriteTracks: favoriteTracks.name,
  favoriteArtists: favoriteArtists.name,
};

export { routes, Routes };
