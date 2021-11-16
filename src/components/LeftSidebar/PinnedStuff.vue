<template>
  <div class="nav-container hidden" id="pinned-container">
    <div>
      <div class="nav-button" id="pinned-button">
        <!-- <div class="nav-icon" id="pinned-icon"></div> -->
        <span id="text">Quick access</span>
      </div>
    </div>
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="album-button">
        <div class="nav-icon" id="album-icon"></div>
        <span id="text">Legends Never Die</span>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="album-button">
        <div class="nav-icon" id="album-icon"></div>
        <span id="text">The Party Never Ends</span>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="artists-button">
        <div class="nav-icon" id="artists-icon"></div>
        <span id="text">Juice WRLD</span>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="playlists-button">
        <div class="nav-icon" id="playlists-icon"></div>
        <span id="text">Juice WRLD Discography</span>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="mixes-button">
        <div class="nav-icon" id="mixes-icon"></div>
        <span id="text">Lil Peep Radio</span>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="folders-button">
        <div class="nav-icon" id="folders-icon"></div>
        <span id="text">Ngogoyo ya Kamarú</span>
      </div>
    </router-link>
  </div>
</template>

<style>
.hidden {
  display: none;
}

#pinned-container .nav-button {
  color: rgba(255, 255, 255, 0.671);
}

#pinned-container .nav-button:hover {
  background-color: rgba(5, 80, 150, 0.322);
}

#pinned-container .nav-button .nav-icon {
  height: 20px;
  width: 20px;
}

#pinned-container #album-button #album-icon {
  background-image: url(../../assets/icons/album.svg);
}

#pinned-container #home-button #text {
  margin-top: 5px;
}

#pinned-container #artists-button #artists-icon {
  background-image: url(../../assets/icons/artist.svg);
}

#pinned-container #playlists-button #playlists-icon {
  background-image: url(../../assets/icons/playlist.svg);
}

#pinned-container #mixes-button #mixes-icon {
  background-image: url(../../assets/icons/mix.svg);
}

#pinned-container #folders-button #folders-icon {
  background-image: url(../../assets/icons/folder.svg);
}

#pinned-container #pinned-button #pinned-icon {
  background-image: url(../../assets/icons/pin.svg);
  width: 20px;
  height: 20px;
}

#pinned-container #pinned-button #text {
  text-transform: uppercase;
  font-weight: 1000;
  font-size: small;
  font-style: italic;
}

#pinned-container #pinned-button:hover {
  background-color: transparent;
}

#pinned-container #folders-button #text {
  margin-top: 5px;
}

#pinned-container hr {
  color: transparent;
}

#pinned-container .seperator {
  color: var(--grey);
}
</style>