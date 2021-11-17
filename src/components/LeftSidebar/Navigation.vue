<template>
  <div class="nav-container" :class="{ collapsed: collapsed }">
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="home-button">
        <div class="in">
          <div class="nav-icon" id="home-icon"></div>
          <span id="text">Home</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="album-button">
        <div class="in">
          <div class="nav-icon" id="album-icon"></div>
          <span id="text">Albums</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="artists-button">
        <div class="in">
          <div class="nav-icon" id="artists-icon"></div>
          <span id="text">Artists</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="playlists-button">
        <div class="in">
          <div class="nav-icon" id="playlists-icon"></div>
          <span id="text">Playlist</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="mixes-button">
        <div class="in">
          <div class="nav-icon" id="mixes-icon"></div>
          <span id="text">Mixes</span>
        </div>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="folders-button">
        <div class="in">
          <div class="nav-icon" id="folders-icon"></div>
          <span id="text">Folders</span>
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



<style>
.nav-container .in {
  display: flex;
  align-items: center;
}

.collapsed .in {
  flex-direction: column;
}

.nav-container {
  color: #fff;
}

.nav-container .nav-button {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  background-color: transparent;
  height: 100%;
  padding: 10px;
}


.collapsed span {
  font-size: small;
  margin-top: 5px;
}

.nav-container .nav-button:hover {
  background-color: rgba(220, 20, 60, 0.5);
}

.nav-container .nav-button .nav-icon {
  height: 24px;
  width: 24px;
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  margin-right: 0.5em;
  margin-left: 10px;
}

.nav-container #home-button #home-icon {
  background-image: url(../../assets/icons/home.svg);
}

.nav-container #album-button #album-icon {
  background-image: url(../../assets/icons/album.svg);
}

.nav-container #home-button #text {
  margin-top: 5px;
}

.nav-container #artists-button #artists-icon {
  background-image: url(../../assets/icons/artist.svg);
}

.nav-container #playlists-button #playlists-icon {
  background-image: url(../../assets/icons/playlist.svg);
}

.nav-container #mixes-button #mixes-icon {
  background-image: url(../../assets/icons/mix.svg);
}

.nav-container #folders-button #folders-icon {
  background-image: url(../../assets/icons/folder.svg);
}

.nav-container #folders-button #text {
  margin-top: 5px;
}

.nav-container hr {
  display: none;
}
</style>