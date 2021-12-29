<template>
  <div class="side-nav-container" :class="{ collapsed: collapsed }">
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="home-button">
        <div class="in">
          <div class="nav-icon image" id="home-icon"></div>
          <span id="text">Home</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'AlbumsExplorer' }">
      <div class="nav-button" id="album-button">
        <div class="in">
          <div class="nav-icon image" id="album-icon"></div>
          <span id="text">Albums</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'ArtistsExplorer' }">
      <div class="nav-button" id="artists-button">
        <div class="in">
          <div class="nav-icon image" id="artists-icon"></div>
          <span id="text">Artists</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'PlaylistView' }">
      <div class="nav-button" id="playlists-button">
        <div class="in">
          <div class="nav-icon image" id="playlists-icon"></div>
          <span id="text">Playlist</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="mixes-button">
        <div class="in">
          <div class="nav-icon image" id="mixes-icon"></div>
          <span id="text">Mixes</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'FolderView', params: { path: 'home' } }">
      <div class="nav-button" id="folders-button">
        <div class="in">
          <div class="nav-icon image" id="folders-icon"></div>
          <span id="text">Folders</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'FolderView', params: { path: 'home' } }">
      <div class="nav-button" id="folders-button">
        <div class="in">
          <div class="nav-icon image" id="settings-icon"></div>
          <span id="text">Settings</span>
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
.collapsed .nav-button {
  font-size: smaller;
  margin-top: 5px;
  align-items: center;
  justify-content: center;

  .in {
    width: 100%;
    flex-direction: column;
  }
}

.side-nav-container {
  padding: $small;
  color: #fff;
  border-top: 1px solid var(--separator);
  margin-bottom: 10px;
  padding-top: 10px;

  .nav-button {
    border-radius: $small;
    display: flex;
    align-items: flex-start;
    justify-content: flex-start;
    background-color: transparent;
    height: 100%;
    padding: 0.6rem 0 0.6rem 0;

    &:hover {
      background-color: rgb(5, 80, 150);
    }

    .nav-icon {
      height: 1.5rem;
      width: 1.5rem;
      margin-right: 0.5rem;
      margin-left: 10px;
    }

    .in {
      display: flex;
      align-items: center;
    }

    #home-icon {
      background-image: url(../../assets/icons/home.svg);
    }

    #album-icon {
      background-image: url(../../assets/icons/album.svg);
    }

    #text {
      margin-top: 5px;
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