<template>
  <ContextMenu />
  <Modal />
  <Notification />
  <div class="l-container" :class="{ collapsed: collapsed }">
    <div class="l-sidebar">
      <div id="logo-container">
        <router-link :to="{ name: 'Home' }" v-if="!collapsed"
          ><div class="logo"></div
        ></router-link>
      </div>
      <Navigation />
      <div class="l-album-art">
        <nowPlaying />
      </div>
    </div>
    <NavBar />
    <div class="content">
      <router-view />
    </div>
    <SearchInput />
    <RightSideBar />
    <Tabs />
  </div>
</template>

<script setup>
import { ref } from "vue";
import Navigation from "./components/LeftSidebar/Navigation.vue";

import perks from "@/composables/perks.js";

import Main from "./components/RightSideBar/Main.vue";
import nowPlaying from "./components/LeftSidebar/nowPlaying.vue";
import NavBar from "./components/nav/NavBar.vue";
import Tabs from "./components/RightSideBar/Tabs.vue";
import SearchInput from "./components/RightSideBar/SearchInput.vue";
import useContextStore from "./stores/context";
import ContextMenu from "./components/contextMenu.vue";
import Modal from "./components/modal.vue";
import Notification from "./components/Notification.vue";
import useQStore from "./stores/queue";
import shortcuts from "./composables/keyboard";

const context_store = useContextStore();
const queue = useQStore();

queue.readQueueFromLocalStorage();

const RightSideBar = Main;

shortcuts(queue);

const app_dom = document.getElementById("app");

app_dom.addEventListener("click", (e) => {
  if (context_store.visible) {
    context_store.hideContextMenu();
  }
});
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
  margin-top: $small;
}
</style>
