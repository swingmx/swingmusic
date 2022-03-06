<template>
  <div id="bg-blur"></div>
  <div class="l-container" :class="{ collapsed: collapsed }">
    <div class="l-sidebar">
      <div id="logo-container">
        <router-link :to="{ name: 'Home' }" v-if="!collapsed"
          ><div class="logo"></div
        ></router-link>
      </div>
      <Navigation :collapsed="collapsed" />
      <div class="l-album-art">
        <AlbumArt :collapsed="collapsed" />
      </div>
    </div>
    <NavBar />
    <div class="content">
      <router-view />
    </div>
    <RightSideBar />
    <Tabs />
    <div class="bottom-bar">
      <BottomBar :collapsed="collapsed" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Navigation from "./components/LeftSidebar/Navigation.vue";
import BottomBar from "@/components/BottomBar/BottomBar.vue";

import perks from "@/composables/perks.js";

import Main from "./components/RightSideBar/Main.vue";
import AlbumArt from "./components/LeftSidebar/AlbumArt.vue";
import NavBar from "./components/nav/NavBar.vue";
import Tabs from "./components/RightSideBar/Tabs.vue";

const RightSideBar = Main;
perks.readQueue();
const collapsed = ref(false);
</script>

<style lang="scss">
.l-sidebar {
  position: relative;

  .l-album-art {
    position: absolute;
    bottom: 0;
  }
}

#logo-container {
  position: relative;
  height: 3.6rem;
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;

  #toggle {
    position: absolute;
    width: 3rem;
    height: 100%;
    background: url(./assets/icons/menu.svg) no-repeat center;
    background-size: 2rem;
    cursor: pointer;
  }
}
.logo {
  height: 4.5rem;
  width: 15rem;
  background: url(./assets/icons/logo.svg) no-repeat 1rem;
  background-size: 9rem;
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
  grid-template-rows: 1fr;
}
</style>
