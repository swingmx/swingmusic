<template>
  <div class="l-container">
    <div class="l-sidebar">
      <router-link :to="{ name: 'Home' }"><div id="logo"></div></router-link>
      <hr id="logo-seperator" />
      <Navigation />
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

export default {
  components: {
    Navigation,
  },
  setup() {},
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

.l-container #logo-seperator {
  margin-left: -1em;
  border: 1px solid;
  color: rgba(255, 255, 255, 0.514);
  margin-bottom: 1em;
}

.l-container #l-home-icon {
  height: 40px;
  width: 40px;
  background: red;
}
</style>
