import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import FolderView from "../views/FolderView.vue";
import PlaylistView from "../views/PlaylistView.vue";
import Playlists from "../views/Playlists.vue";

import AlbumsExplorer from "../views/AlbumsExplorer.vue";
import AlbumView from "../views/AlbumView.vue";

import ArtistsExplorer from "../views/ArtistsExplorer.vue";
import SettingsView from "../views/SettingsView.vue";

import usePStore from "../stores/playlists";
import usePTrackStore from "../stores/p.ptracks";
import useFStore from "../stores/folder";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/folder/:path",
    name: "FolderView",
    component: FolderView,
    beforeEnter: async (to) => {
      console.log("beforeEnter")
      await useFStore().fetchAll(to.params.path);
    },
  },
  {
    path: "/folder/",
    redirect: "/folder/home",
  },
  {
    path: "/playlists",
    name: "Playlists",
    component: Playlists,
    beforeEnter: async () => {
      await usePStore().fetchAll();
    },
  },
  {
    path: "/playlist/:pid",
    name: "PlaylistView",
    component: PlaylistView,
    beforeEnter: async (to) => {
      await usePTrackStore().fetchAll(to.params.pid);
    },
  },
  {
    path: "/albums",
    name: "AlbumsView",
    component: AlbumsExplorer,
  },
  {
    path: "/albums/:album/:artist",
    name: "AlbumView",
    component: AlbumView,
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
    // alias: "*",
    component: () => import("../views/NotFound.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
