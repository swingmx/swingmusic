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
    <router-link :to="{ name: 'FolderView', params: { path: '/' } }">
      <div class="nav-button" id="folders-button">
        <div class="in">
          <div class="nav-icon image" id="folders-icon"></div>
          <span id="text">Folders</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'FolderView', params: { path: '/' } }">
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
.side-nav-container .in {
  display: flex;
  align-items: center;
}

.collapsed .in {
  flex-direction: column;
}

.side-nav-container {
  color: #fff;
  border-top: 1px solid var(--separator);
  margin-bottom: 10px;
  padding-top: 10px;
}

.side-nav-container .nav-button {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  background-color: transparent;
  height: 100%;
  padding: 10px;
  transition: all 0.3s ease-in-out;
}

.collapsed .nav-button {
  font-size: smaller;
  margin-top: 5px;
  transition: all 0.2s ease-in-out;
}

.side-nav-container .nav-button:hover {
  background-color: rgba(220, 20, 60, 0.5);
}

.side-nav-container .nav-button .nav-icon {
  height: 24px;
  width: 24px;
  margin-right: 0.5rem;
  margin-left: 10px;
}

.side-nav-container #home-button #home-icon {
  background-image: url(../../assets/icons/home.svg);
}

.side-nav-container #album-button #album-icon {
  background-image: url(../../assets/icons/album.svg);
}

.side-nav-container #home-button #text {
  margin-top: 5px;
}

.side-nav-container #artists-button #artists-icon {
  background-image: url(../../assets/icons/artist.svg);
}

.side-nav-container #playlists-button #playlists-icon {
  background-image: url(../../assets/icons/playlist.svg);
}

.side-nav-container #mixes-button #mixes-icon {
  background-image: url(../../assets/icons/mix.svg);
}

.side-nav-container #folders-button #folders-icon {
  background-image: url(../../assets/icons/folder.svg);
}
.side-nav-container #folders-button #settings-icon {
  background-image: url(../../assets/icons/settings.svg);
}

.side-nav-container #folders-button #text {
  margin-top: 5px;
}

.side-nav-container hr {
  display: none;
}
</style>