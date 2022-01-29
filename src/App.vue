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
      <div class="search-box"></div>
      <router-view />
    </div>
    <RightSideBar />
    <div class="bottom-bar">
      <BottomBar />
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";

import Navigation from "./components/LeftSidebar/Navigation.vue";
import PinnedStuff from "./components/LeftSidebar/PinnedStuff.vue";
import BottomBar from "@/components/BottomBar/BottomBar.vue";

import perks from "@/composables/perks.js";
import Main from "./components/RightSideBar/Main.vue";

export default {
  components: {
    Navigation,
    PinnedStuff,
    BottomBar,
    RightSideBar: Main,
  },

  setup() {
    const collapsed = ref(true);

    perks.readQueue();

    function toggleNav() {
      collapsed.value = !collapsed.value;
    }

    return {
      toggleNav,
      collapsed,
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
    width: 3rem;
    height: 100%;
    background: url(./assets/icons/menu.svg);
    background-size: 2rem;
    background-repeat: no-repeat;
    background-position: center;
    cursor: pointer;
  }
}
.logo {
  height: 2rem;
  width: 9rem;
  margin-left: 3rem;
  background: url(./assets/logo.svg);
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
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
