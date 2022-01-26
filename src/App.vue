<template>
  <div id="bg-blur"></div>
  <div class="l-container" :class="{ collapsed: collapsed }">
    <div class="l-sidebar">
      <div id="logo-container">
        <div id="toggle" @click="toggleNav"></div>
        <router-link :to="{ name: 'Home' }" v-if="!collapsed"
          ><div class="logo"></div
        ></router-link>
      </div>
      <Navigation :collapsed="collapsed" />
      <PinnedStuff :collapsed="collapsed" />
    </div>
    <div class="content">
      <div class="search-box">
        <Search
          v-model:search="search"
          @expandSearch="expandSearch"
          @collapseSearch="collapseSearch"
        />
      </div>
      <router-view />
    </div>
    <div class="r-sidebar">
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

import Search from "./components/Search.vue";
import NowPlaying from "./components/RightSideBar/NowPlaying.vue";
import UpNext from "./components/RightSideBar/UpNext.vue";
import RecommendedArtist from "./components/RightSideBar/Recommendation.vue";

import perks from "@/composables/perks.js";

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

    perks.readQueue();

    function toggleNav() {
      collapsed.value = !collapsed.value;
    }

    let up_next = ref(true);
    let search = ref(false);

    const expandQueue = () => {
      up_next.value = !up_next.value;
    };

    const expandSearch = () => {
      search.value = true;
    };

    const collapseSearch = () => {
      search.value = false;
    };

    return {
      toggleNav,
      expandSearch,
      collapseSearch,
      expandQueue,
      collapsed,
      up_next,
      search,
    };
  },
};
</script>

<style lang="scss">
#logo-container {
  position: relative;
  height: 3.6rem;
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;

  #toggle {
    position: absolute;
    left: 0.2rem;
    width: 4rem;
    height: 100%;
    background: url(./assets/icons/menu.svg);
    background-size: 50%;
    background-repeat: no-repeat;
    background-position: center;
    cursor: pointer;
  }
}
.logo {
  height: 2rem;
  width: 9rem;
  margin-left: 4rem;
  background: url(./assets/logo.svg);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  animation: fadeIn;
  animation-duration: 2s;
  animation-iteration-count: 1;
}

.r-sidebar {
  &::-webkit-scrollbar {
    display: none;
  }
}

.content {
  width: 100%;
  padding: 0 $small;
  display: grid;
  grid-template-rows: auto 1fr;
}
</style>
