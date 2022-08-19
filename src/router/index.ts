import state from "@/composables/state";
import useAStore from "@/stores/pages/album";
import useFStore from "@/stores/pages/folder";
import usePTrackStore from "@/stores/pages/playlist";
import usePStore from "@/stores/pages/playlists";
import AlbumsExplorer from "@/views/AlbumsExplorer.vue";
import AlbumView from "@/views/album/index.vue";
import ArtistsExplorer from "@/views/ArtistsExplorer.vue";
import FolderView from "@/views/FolderView.vue";
import Home from "@/views/Home.vue";
import PlaylistList from "@/views/PlaylistList.vue";
import PlaylistView from "@/views/playlist/index.vue";
import SettingsView from "@/views/SettingsView.vue";
import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    redirect: "/folder/$home",
  },
  {
    path: "/folder/:path",
    name: "FolderView",
    component: FolderView,
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
    path: "/folder/",
    redirect: "/folder/home",
  },
  {
    path: "/playlists",
    name: "PlaylistList",
    component: PlaylistList,
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
    component: PlaylistView,
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
    component: AlbumsExplorer,
  },
  {
    path: "/albums/:hash",
    name: "AlbumView",
    component: AlbumView,
    beforeEnter: async (to: any) => {
      state.loading.value = true;
      const store = useAStore();

      await store
        .fetchTracksAndArtists(to.params.hash)
        .then(() => store.fetchBio(to.params.hash))
        .then(() => {
          state.loading.value = false;
        });
    },
  },
  {
    path: "/artists",
    name: "ArtistsView",
    component: ArtistsExplorer,
  },
  {
    path: "/settings",
    name: "SettingsView",
    component: SettingsView,
  },
  {
    path: "/:pathMatch(.*)",
    component: () => import("../views/NotFound.vue"),
  },
];

const router = createRouter({
  mode: "hash",
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
