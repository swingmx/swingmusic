<template>
  <div id="bg-blur"></div>
  <div class="l-container" :class="{ collapsed: collapsed }">
    <div class="l-sidebar">
      <div id="logo-container">
        <div id="toggle" @click="toggleNav"></div>
        <router-link :to="{ name: 'FolderView' }" v-if="!collapsed"
          ><div ref="logo" class="logo"></div
        ></router-link>
      </div>
      <Navigation :collapsed="collapsed" />
      <PinnedStuff :collapsed="collapsed" />
      <div id="settings-button">
        <div class="in">
          <div class="nav-icon image" id="settings-icon"></div>
          <span id="text">Settings</span>
        </div>
      </div>
    </div>
    <div class="content">
      <router-view />
    </div>
    <div class="r-sidebar">
      <Search :collapser="collapser"/>
      <NowPlaying />
      <UpNext :collapser="collapser" @updateCollapser="updateCollapser"/>
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";

import Navigation from "./components/LeftSidebar/Navigation.vue";
import PinnedStuff from "./components/LeftSidebar/PinnedStuff.vue";

import Search from "./components/RightSideBar/Search.vue";
import NowPlaying from "./components/RightSideBar/NowPlaying.vue";
import UpNext from "./components/RightSideBar/UpNext.vue";

export default {
  components: {
    Navigation,
    PinnedStuff,
    Search,
    NowPlaying,
    UpNext
  },
  setup() {
    const collapsed = ref(true);

    const logo = ref(null);

    function toggleNav() {
      collapsed.value = !collapsed.value;
    }

    const collapser = ref(false)
    const updateCollapser = ()=> {
      collapser.value = !collapser.value
      console.log(collapser.value);
    }

    return { logo, toggleNav, collapsed, collapser, updateCollapser };
  },
};
</script>

<style>
.logo {
  height: 2em;
  width: 9em;
  margin-left: 2.25em;
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
  height: 3.6em;
  margin-left: 1em;
  display: flex;
  align-items: center;
  margin-bottom: 0.5em;
}

.l-sidebar {
  position: relative;
}

.l-container #toggle {
  position: fixed;
  top: 1em;
  width: 1.75em;
  height: 3.75em;
  background: url(./assets/icons/menu.svg);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
  margin-left: 0.25em;
}

.l-container #settings-button {
  position: absolute;
  bottom: 0;
  display: flex;
  color: #fff;
  height: 50px;
  width: 100%;
  border-top: 1px solid var(--seperator);
}

#settings-button .in {
  display: flex;
  align-items: center;
  justify-content: center;
}

.l-container #settings-button:hover {
  background: #17c93d7c;
  cursor: pointer;
}

.l-container #settings-button #settings-icon {
  margin-left: 1em;
  margin-right: 0.25em;
  width: 1.5em;
  height: 1.5em;
  background-image: url(./assets/icons/settings.svg);
  /* background-size: contain;
  background-repeat: no-repeat;
  background-position: center; */
}

.collapsed #settings-button #settings-icon {
  margin-right: 0;
}

.collapsed #settings-button #text {
  display: none;
}
</style>
