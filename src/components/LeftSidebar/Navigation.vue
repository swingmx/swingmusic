<template>
  <div class="side-nav-container">
    <router-link
      v-for="menu in menus"
      :key="menu.name"
      :to="{ name: menu.route_name, params: menu.params }"
    >
      <div class="nav-button" id="home-button" v-motion-slide-from-left-100>
        <div class="in">
          <div class="nav-icon image" :id="`${menu.name}-icon`"></div>
          <span>{{ menu.name }}</span>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";

const menus = [
  {
    name: "home",
    route_name: "Home",
  },
  {
    name: "albums",
    route_name: "AlbumsView",
  },
  {
    name: "artists",
    route_name: "ArtistsView",
  },
  {
    name: "playlists",
    route_name: "Playlists",
  },
  {
    name: "folders",
    route_name: "FolderView",
    params: { path: "$home" },
  },
  {
    name: "tags",
  },
  {
    name: "settings",
    route_name: "SettingsView",
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

    #home-icon {
      background-image: url(../../assets/icons/home.svg);
    }

    #albums-icon {
      background-image: url(../../assets/icons/album.svg);
    }

    #artists-icon {
      background-image: url(../../assets/icons/artist.svg);
    }

    #playlists-icon {
      background-image: url(../../assets/icons/playlist.svg);
    }

    #mixes-icon {
      background-image: url(../../assets/icons/mix.svg);
    }

    #folders-icon {
      background-image: url(../../assets/icons/folder.svg);
    }
    #settings-icon {
      background-image: url(../../assets/icons/settings.svg);
    }
    #tags-icon {
      background-image: url(../../assets/icons/tag.svg);
    }
  }
}
</style>
