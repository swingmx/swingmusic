<template>
  <div class="side-nav-container border" :class="{ collapsed: collapsed }">
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="home-button">
        <div class="in">
          <div class="nav-icon image" id="home-icon"></div>
          <span>Home</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'AlbumsExplorer' }">
      <div class="nav-button" id="album-button">
        <div class="in">
          <div class="nav-icon image" id="album-icon"></div>
          <span>Albums</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'ArtistsExplorer' }">
      <div class="nav-button" id="artists-button">
        <div class="in">
          <div class="nav-icon image" id="artists-icon"></div>
          <span>Artists</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'PlaylistView' }">
      <div class="nav-button" id="playlists-button">
        <div class="in">
          <div class="nav-icon image" id="playlists-icon"></div>
          <span>Playlist</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="mixes-button">
        <div class="in">
          <div class="nav-icon image" id="mixes-icon"></div>
          <span>Mixes</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'FolderView', params: { path: 'home' } }">
      <div class="nav-button" id="folders-button">
        <div class="in">
          <div class="nav-icon image" id="folders-icon"></div>
          <span>Folders</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'FolderView', params: { path: 'home' } }">
      <div class="nav-button" id="folders-button">
        <div class="in">
          <div class="nav-icon image" id="settings-icon"></div>
          <span>Settings</span>
        </div>
      </div>
    </router-link>
  </div>
</template>

<script>
export default {
  props: ["collapsed"],
  setup() {},
};
</script>

<style lang="scss">
.collapsed {
  .nav-button {
    font-size: smaller;
    margin-top: 5px;
    align-items: center;
    justify-content: center;

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
  margin-bottom: 10px;
  padding-top: 10px;

  .nav-button {
    border-radius: $small;
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    height: 100%;
    padding: 0.6rem 0 0.6rem 0;

    &:hover {
      background-color: rgb(5, 80, 150);
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
    #album-icon,
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

    #album-icon {
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