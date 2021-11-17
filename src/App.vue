<template>
  <div class="l-container" :class="{ collapsed: collapsed }">
    <div class="l-sidebar">
      <div id="logo-container">
        <div id="toggle" @click="toggleNav"></div>
        <router-link :to="{ name: 'FolderView' }" v-if="!collapsed"
          ><div ref="logo" class="logo"></div
        ></router-link>
      </div>
      <hr class="seperator" />
      <Navigation :collapsed="collapsed" />
      <hr class="seperator" />
      <PinnedStuff :collapsed="collapsed" />
      <div id="settings-button">
        <div class="in">
          <div class="nav-icon" id="settings-icon"></div>
          <span id="text">Settings</span>
        </div>
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
import { ref } from "@vue/reactivity";
import Navigation from "./components/LeftSidebar/Navigation.vue";
import PinnedStuff from "./components/LeftSidebar/PinnedStuff.vue";

export default {
  components: {
    Navigation,
    PinnedStuff,
  },
  setup() {
    const collapsed = ref(false);

    const logo = ref(null);

    function toggleNav() {
      collapsed.value = !collapsed.value;
    }
    return { logo, toggleNav, collapsed };
  },
};
</script>

<style>
.logo {
  height: 30px;
  width: 150px;
  margin-left: 35px;
  background: url(./assets/logo.svg);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  animation: fadeIn;
  animation-duration: 2s;
  animation-iteration-count: 1;
}
.nav-container .in {
  display: flex;
  align-items: center;
}

.collapsed .in {
  flex-direction: column;
}

#logo-container {
  height: 60px;
  margin-left: 20px;
  display: flex;
  align-items: center;
}

.l-sidebar {
  position: relative;
}

.l-container .seperator {
  margin-left: -2em;
}

.l-container #toggle {
  position: fixed;
  top: 7px;
  width: 30px;
  height: 60px;
  background: url(./assets/icons/menu.svg);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
  margin-right: 5px;
}

.l-container #settings-button {
  position: absolute;
  bottom: 0;
  display: flex;
  color: #fff;
  height: 50px;
  width: 100%;
}

#settings-button  .in {
  display: flex;
  align-items: center;
  justify-content: center;
}

.l-container #settings-button:hover {
  background: #17c93d7c;
  cursor: pointer;
}

.l-container #settings-button #settings-icon {
  margin-left: 23px;
  margin-right: 5px;
  width: 24px;
  height: 24px;
  background-image: url(./assets/icons/settings.svg);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
}

.collapsed #settings-button #settings-icon {
  margin-right: 0;
}

.collapsed #settings-button #text {
  display: none;
}
</style>
