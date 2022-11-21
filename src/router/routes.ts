import state from "@/composables/state";
import useAStore from "@/stores/pages/album";
import useFStore from "@/stores/pages/folder";
import usePTrackStore from "@/stores/pages/playlist";
import usePStore from "@/stores/pages/playlists";

const routes = [
  {
    path: "/",
    name: "Home",
    redirect: "/folder/$home",
  },
  {
    path: "/folder/:path",
    name: "FolderView",
    component: () => import("@/views/FolderView.vue"),
    beforeEnter: async (to: any) => {
      state.loading.value = true;
      await useFStore()
        .fetchAll(to.params.path)
        .then(() => {
          state.loading.value = false;
        });
    },
  },
  {
    path: "/playlists",
    name: "PlaylistList",
    component: () => import("@/views/PlaylistList.vue"),
    beforeEnter: async () => {
      state.loading.value = true;
      await usePStore()
        .fetchAll()
        .then(() => {
          state.loading.value = false;
        });
    },
  },
  {
    path: "/playlist/:pid",
    name: "PlaylistView",
    component: () => import("@/views/PlaylistView/index.vue"),
    beforeEnter: async (to: any) => {
      state.loading.value = true;
      await usePTrackStore()
        .fetchAll(to.params.pid)
        .then(() => {
          state.loading.value = false;
        });
    },
  },
  {
    path: "/albums",
    name: "AlbumsView",
    component: () => import("@/views/AlbumsExplorer.vue"),
  },
  {
    path: "/albums/:hash",
    name: "AlbumView",
    component: () => import("@/views/AlbumView/index.vue"),
    beforeEnter: async (to: any) => {
      state.loading.value = true;
      const store = useAStore();

      await store.fetchTracksAndArtists(to.params.hash).then(() => {
        state.loading.value = false;
      });
    },
  },
  {
    path: "/artists",
    name: "ArtistsView",
    component: () => import("@/views/ArtistsExplorer.vue"),
  },
  {
    path: "/artists/:hash",
    name: "ArtistView",
    component: () => import("@/views/ArtistView"),
  },
  {
    path: "/settings",
    name: "SettingsView",
    component: () => import("@/views/SettingsView.vue"),
  },
  {
    path: "/search/:page",
    name: "SearchView",
    component: () => import("@/views/SearchView"),
  },
  {
    path: "/queue",
    name: "QueueView",
    component: () => import("@/views/QueueView.vue"),
  },
  {
    name: "NotFound",
    path: "/:pathMatch(.*)",
    component: () => import("@/views/NotFound.vue"),
  },
];

const keys = [
  "home",
  "folder",
  "playlists",
  "playlist",
  "albums",
  "album",
  "artists",
  "settings",
  "search",
  "queue",
  "notfound",
];

const routesList = routes.map((route, index) => {
  const key = keys[index];
  return { route: route.name };
});

// TODO: Use dynamic keys in routesList
//       Try adding an index.ts on Foldered views, import main component and export it ...
//       Then try importing it here as @/views/ThatView

export { routes, routesList };
