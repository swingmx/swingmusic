<template>
  <div class="side-nav-container">
    <router-link
      v-for="menu in menus"
      :key="menu.name"
      :to="{ name: menu.route_name, params: menu?.params }"
    >
      <div v-if="menu.separator" :class="{ separator: menu.separator }"></div>
      <div class="nav-button" id="home-button" v-else>
        <div class="in">
          <component :is="menu.icon"></component>
          <span>{{ menu.name }}</span>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import PlaylistSvg from "../../assets/icons/playlist.svg";
import FolderSvg from "../../assets/icons/folder.svg";
import SettingsSvg from "../../assets/icons/settings.svg";
import SearchSvg from "../../assets/icons/search.svg";

import { Routes } from "@/composables/enums";

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
    name: "search",
    route_name: Routes.search,
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
  color: #fff;
  text-transform: capitalize;
  margin-top: 1rem;

  .nav-button {
    border-radius: $small;
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    padding: 0.6rem 0;

    &:hover {
      background-color: $gray3;
    }

    .nav-icon {
      height: 2rem;
      width: 2rem;
      margin: 0 $small 0 $small;
      border-radius: $small;
      background-color: rgb(26, 24, 24);
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
  }

  svg > path {
    fill: $accent;
  }
}
</style>
