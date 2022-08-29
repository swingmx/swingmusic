<template>
  <div class="side-nav-container">
    <router-link
      v-for="menu in filtered_menus"
      :key="menu.name"
      :to="{ name: menu.route_name, params: menu?.params }"
    >
      <div
        v-if="menu.separator"
        :class="{
          separator: menu.separator,
        }"
      ></div>
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
import { computed } from "@vue/reactivity";

import { Routes } from "@/composables/enums";
import useSettingsStore from "@/stores/settings";

import PlaylistSvg from "../../assets/icons/playlist.svg";
import FolderSvg from "../../assets/icons/folder.svg";
import SettingsSvg from "../../assets/icons/settings.svg";
import SearchSvg from "../../assets/icons/search.svg";

const settings = useSettingsStore();

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
    name: "queue",
    route_name: Routes.queue,
    icon: PlaylistSvg,
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

const filtered_menus = computed(() => {
  if (settings.hide_queue_page) {
    return menus.filter((menu) => menu.route_name !== Routes.queue);
  }

  return menus;
});
</script>

<style lang="scss">
.side-nav-container {
  text-transform: capitalize;
  margin-top: 1rem;

  .nav-button {
    border-radius: $small;
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    padding: $smaller 0;

    &:hover {
      background-color: $gray3;
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
  }

  svg > path {
    fill: $accent;
  }
}
</style>
