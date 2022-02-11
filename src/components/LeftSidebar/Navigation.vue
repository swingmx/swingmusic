<template>
  <div class="side-nav-container" :class="{ collapsed: props.collapsed }">
    <router-link
      v-for="menu in menus"
      :key="menu.name"
      :to="{ name: menu.route_name, params: { path: 'home' } }"
    >
      <div class="nav-button" id="home-button">
        <div class="in">
          <div class="nav-icon image" :id="`${menu.name}-icon`"></div>
          <span>{{ menu.name }}</span>
        </div>
      </div>
    </router-link>
    <hr />
  </div>
</template>

<script setup>
import { ref } from "vue";

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
    route_name: "PlaylistView",
  },
  {
    name: "folders",
    route_name: "FolderView",
  },
  {
    name: "settings",
    route_name: "SettingsView",
  },
];

const props = defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
});
</script>

<style lang="scss">
.collapsed {
  .nav-button {
    margin-top: 5px;

    span {
      display: none;
    }

    .in {
      width: 100%;
      flex-direction: column;
    }
  }
}

.side-nav-container {
  padding: $small;
  color: #fff;
  margin-bottom: 1rem;
  padding-top: 10px;
  margin-top: 1rem;
  text-transform: capitalize;

  .nav-button {
    border-radius: $small;
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    height: 100%;
    padding: 0.6rem 0 0.6rem 0;

    &:hover {
      #home-icon {
        background-color: rgba(145, 58, 58, 0.555);
      }

      #albums-icon {
        background-color: rgba(113, 58, 145, 0.555);
      }

      #artists-icon {
        background-color: rgba(13, 72, 139, 0.555);
      }

      #playlists-icon {
        background-color: rgba(206, 13, 132, 0.555);
      }

      #mixes-icon {
        background-color: rgba(0, 85, 81, 0.555);
      }

      #folders-icon {
        background-color: rgba(90, 89, 3, 0.596);
      }

      #settings-icon {
        background-color: rgba(129, 106, 106, 0.596);
      }
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
    }

    #home-icon,
    #albums-icon,
    #artists-icon,
    #playlists-icon,
    #mixes-icon,
    #folders-icon,
    #settings-icon {
      background-size: 1.5rem;
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
  }
}

.side-nav-container hr {
  display: none;
}
</style>
