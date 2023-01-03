<template>
  <div class="side-nav-container">
    <router-link
      v-for="menu in menus"
      :key="menu.name"
      :to="{
        name: menu.route_name,
        params: menu?.params,
        query: menu.query && menu.query(),
      }"
    >
      <div
        v-if="menu.separator"
        :class="{
          separator: menu.separator,
        }"
      ></div>
      <div
        class="nav-button"
        :class="{ active: $route.name === menu.route_name }"
        id="home-button"
        v-else
      >
        <div class="in">
          <component :is="menu.icon"></component>
          <span>{{ menu.name }}</span>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { Routes } from "@/router/routes";
import FolderSvg from "../../assets/icons/folder-1.svg";
import PlaylistSvg from "../../assets/icons/playlist-1.svg";
import QueueSvg from "../../assets/icons/queue.svg";
import SearchSvg from "../../assets/icons/search.svg";
import SettingsSvg from "../../assets/icons/settings.svg";
import HeartSvg from "../../assets/icons/heart.svg";
import useSearchStore from "@/stores/search";

const menus = [
  {
    name: "playlists",
    route_name: Routes.playlists,
    icon: PlaylistSvg,
  },
  {
    name: "folders",
    route_name: "FolderView",
    params: { path: "$home" },
    icon: FolderSvg,
  },

  {
    separator: true,
  },
  {
    name: "favorites",
    route_name: Routes.favorites,
    icon: HeartSvg,
  },
  {
    name: "queue",
    route_name: Routes.queue,
    icon: QueueSvg,
  },
  {
    name: "search",
    route_name: Routes.search,
    params: { page: "tracks" },
    query: () => ({ q: useSearchStore().query }),
    icon: SearchSvg,
  },
  {
    separator: true,
  },
  {
    name: "settings",
    route_name: Routes.settings,
    icon: SettingsSvg,
  },
];
</script>

<style lang="scss">
.side-nav-container {
  text-transform: capitalize;
  margin-top: 1rem;

  .nav-button {
    border-radius: $medium;
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    padding: $small 0;
    position: relative;

    &.active::before {
      content: "•";
      position: absolute;
      left: -$small;
      top: $medium;
      opacity: 0.75;
    }

    &:hover {
      background-color: $darkestblue;
    }

    .in {
      display: flex;
      align-items: center;

      & > * {
        background-size: 1.5rem;
      }
    }
  }

  svg {
    margin: 0 $small 0 $small;
    border-radius: $small;
    transform: scale(0.9);
    opacity: 0.75;
  }
}
</style>
