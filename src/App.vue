<template>
  <div id="bg-blur"></div>
  <div class="l-container" :class="{ collapsed: collapsed }">
    <div class="l-sidebar">
      <div id="logo-container">
        <div id="toggle" @click="toggleNav"></div>
        <router-link :to="{ name: 'FolderView' }" v-if="!collapsed"
          ><div class="logo"></div
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
      <Search
        v-model:search="search"
        @expandSearch="expandSearch"
        @collapseSearch="collapseSearch"
      />
      <div class="m-np">
        <NowPlaying />
      </div>
      <UpNext v-model:up_next="up_next" @expandQueue="expandQueue" />
      <RecommendedArtist />
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
import RecommendedArtist from "./components/RightSideBar/Recommendation.vue";

export default {
  components: {
    Navigation,
    PinnedStuff,
    Search,
    NowPlaying,
    UpNext,
    RecommendedArtist,
  },

  setup() {
    const collapsed = ref(true);

    function toggleNav() {
      collapsed.value = !collapsed.value;
    }

    let up_next = ref(false);
    let search = ref(false);

    const expandQueue = () => {
      up_next.value = !up_next.value;
      search.value = false;
    };

    const expandSearch = () => {
      search.value = true;
      up_next.value = false;
    };

    const collapseSearch = () => {
      search.value = false;
    };

    return {
      toggleNav,
      collapsed,
      up_next,
      expandQueue,
      expandSearch,
      collapseSearch,
      search,
    };
  },
};
</script>

<style>
.logo {
  height: 2rem;
  width: 9rem;
  margin-left: 2.25rem;
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
  height: 3.6rem;
  margin-left: 1rem;
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.l-sidebar {
  position: relative;
}

.l-container #toggle {
  position: fixed;
  top: 1rem;
  width: 1.75rem;
  height: 3.75rem;
  background: url(./assets/icons/menu.svg);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  cursor: pointer;
  margin-left: 0.25rem;
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
  margin-left: 1rem;
  margin-right: 0.25rem;
  width: 1.5rem;
  height: 1.5rem;
  background-image: url(./assets/icons/settings.svg);
}

.collapsed #settings-button #settings-icon {
  margin-right: 0;
}

.collapsed #settings-button #text {
  display: none;
}
.r-sidebar {
  position: relative;
  margin-bottom: 0.5em;
}
.m-np {
  position: absolute;
  bottom: 0;
}
</style>
