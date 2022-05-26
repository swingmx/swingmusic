<template>
  <div class="side-nav-container rounded hidden" id="pinned-container">
    <div>
      <div class="nav-button" id="pinned-button">
        <span id="text">Quick access</span>
      </div>
    </div>
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="album-button">
        <div class="nav-icon image" id="album-icon"></div>
        <span id="text">Legends Never Die</span>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="album-button">
        <div class="nav-icon image" id="album-icon"></div>
        <span id="text">The Party Never Ends</span>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="artists-button">
        <div class="nav-icon image" id="artists-icon"></div>
        <span id="text">Juice WRLD</span>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="playlists-button">
        <div class="nav-icon image" id="playlists-icon"></div>
        <span id="text" class="ellip">Juice WRLD Discography</span>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="mixes-button">
        <div class="nav-icon image" id="mixes-icon"></div>
        <span id="text">Lil Peep Radio</span>
      </div>
    </router-link>
    <hr />
    <router-link :to="{ name: 'Home' }">
      <div class="nav-button" id="folders-button">
        <div class="nav-icon image" id="folders-icon"></div>
        <span id="text">Ngogoyo ya Kamarú</span>
      </div>
    </router-link>
  </div>
</template>

<style lang="scss">
#pinned-container {
  background: #6e2c00;

  border-top: none;
  margin: $small;
  padding: $small;

  #text {
    font-size: 0.9rem;
  }

  .nav-icon {
    margin: 0 $small 0 0;
  }
}

#pinned-container .nav-button {
  border-radius: $small;
  color: rgba(255, 255, 255, 0.671);
  padding-left: $small;
}

#pinned-container .nav-button:hover {
  background-color: rgb(5, 80, 150);
}

#pinned-container .nav-button .nav-icon {
  height: 1.3rem;
  width: 1.3rem;
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
</style>
