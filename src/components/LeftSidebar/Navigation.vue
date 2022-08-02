<template>
  <div class="side-nav-container">
    <router-link
      v-for="menu in menus"
      :key="menu.name"
      :to="{ name: menu.route_name, params: menu.params }"
    >
      <div class="nav-button" id="home-button">
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

const menus = [
  {
    name: "playlists",
    route_name: "Playlists",
    icon: PlaylistSvg,
  },
  {
    name: "folders",
    route_name: "FolderView",
    params: { path: "$home" },
    icon: FolderSvg,
  },
];
</script>

<style lang="scss">
.side-nav-container {
  color: #fff;
  margin: 1rem 0;
  text-transform: capitalize;

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
