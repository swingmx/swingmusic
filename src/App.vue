<template>
  <div class="l-container">
    <div class="l-sidebar">
      <div id="logo-container">
        <router-link :to="{ name: 'Home' }"><div id="logo"></div></router-link>
      </div>
      <hr class="seperator" />
      <Navigation />
      <hr class="seperator" />
      <PinnedStuff />
      <div id="settings-button">
        <div class="nav-icon" id="settings-icon"></div>
        <span id="text">Settings</span>
      </div>
    </div>
    <div class="nav">
      <div id="nav"></div>
    </div>
    <div class="content">
      <router-view />
    </div>
    <div class="r-sidebar"></div>
  </div>
</template>

<script>
import Navigation from "./components/LeftSidebar/Navigation.vue";
import PinnedStuff from "./components/LeftSidebar/PinnedStuff.vue";

export default {
  components: {
    Navigation,
    PinnedStuff,
  },
  setup() {
    let quick_access = null;

    return { quick_access };
  },
};
</script>

<style>
#logo {
  height: 60px;
  width: 200px;
  background: url(./assets/logo.svg);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

#logo-container {
  padding-left: 15px;
}

.l-sidebar {
  position: relative;
}

.l-container .seperator {
  margin-left: -2em;
}

.l-container #settings-button {
  position: absolute;
  bottom: 0;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  height: 50px;
  width: 100%;
}

.l-container #settings-button:hover {
  background: #17c93d7c;
  cursor: pointer;
}

.l-container #settings-button #settings-icon {
  margin-left: 10px;
  margin-right: 5px;
  width: 24px;
  height: 24px;
  background-image: url(./assets/icons/settings.svg);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

@media (max-width: 1000px) {
  #logo {
    height: 40px;
    width: 40px;
    background: url(./assets/icons/logo-small.svg);
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
  }
  .l-container #settings-button {
    flex-direction: column;
    justify-content: center;
  }

  .l-container #settings-button #settings-icon {
    margin-left: 0;
    margin-right: 0;
  }
  .l-container #settings-button #text {
    display: none;
  }
}
</style>
