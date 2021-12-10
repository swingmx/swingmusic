import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import FolderView from "../views/FolderView.vue";
import PlaylistView from "../views/PlaylistView.vue";
import AlbumsExplorer from "../views/AlbumsExplorer.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/folder",
    name: "FolderView",
    component: FolderView,
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
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
