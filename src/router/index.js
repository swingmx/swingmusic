import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import FolderView from "../views/FolderView.vue";
import PlaylistView from "../views/PlaylistView.vue";

import AlbumsExplorer from "../views/AlbumsExplorer.vue";
import AlbumView from "../views/AlbumView.vue";

import ArtistsExplorer from "../views/ArtistsExplorer.vue";
import SettingsView from "../views/SettingsView.vue";

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
  },
  {
    path: "/folder/",
    redirect: "/folder/home",
  },
  {
    path: "/playlist",
    name: "PlaylistView",
    component: PlaylistView,
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
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
