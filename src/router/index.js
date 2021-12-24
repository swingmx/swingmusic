import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import FolderView from "../views/FolderView.vue";
import PlaylistView from "../views/PlaylistView.vue";

import AlbumsExplorer from "../views/AlbumsExplorer.vue";
import AlbumView from "../views/AlbumView.vue";

import ArtistsExplorer from "../views/ArtistsExplorer.vue";

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
    name: "AlbumsExplorer",
    component: AlbumsExplorer,
  },
  {
    path: "/albums/:id",
    name: "AlbumView",
    component: AlbumView,
  },
  {
    path: "/artists",
    name: "ArtistsExplorer",
    component: ArtistsExplorer,
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
