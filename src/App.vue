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
    <div class="content" :class="{ isMagicFlag: isMagicFlag }">
      <div class="search-box">
        <Search
          v-model:search="search"
          @expandSearch="expandSearch"
          @collapseSearch="collapseSearch"
        />
      </div>

      <div class="separator" style="border: none"></div>
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
import { computed, ref } from "@vue/reactivity";

import Navigation from "./components/LeftSidebar/Navigation.vue";
import PinnedStuff from "./components/LeftSidebar/PinnedStuff.vue";

import Search from "./components/Search.vue";
import NowPlaying from "./components/RightSideBar/NowPlaying.vue";
import UpNext from "./components/RightSideBar/UpNext.vue";
import RecommendedArtist from "./components/RightSideBar/Recommendation.vue";

import state from "@/composables/state.js";
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

    const isMagicFlag = computed(() => {
      return state.magic_flag.value;
    });
    
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
      expandSearch,
      collapseSearch,
      isMagicFlag,
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

.l-container #toggle {
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

.r-sidebar {
  &::-webkit-scrollbar {
    display: none;
  }
}

.content {
  position: relative;
  padding: 0.5rem;
  padding-top: 3.75rem;

  .search-box {
    width: calc(100% - 1rem);
    position: absolute;
    top: 0;
    z-index: 1;
  }
}
.isMagicFlag {
  padding-top: 7.5rem;
}
</style>
