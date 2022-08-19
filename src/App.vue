<template>
  <ContextMenu />
  <Modal />
  <Notification />
  <div id="app-grid">
    <div class="l-sidebar rounded">
      <div class="withlogo">
        <Logo />
        <Navigation />
      </div>

      <nowPlaying />
      <!-- <Playlists /> -->
    </div>
    <NavBar />
    <div id="acontent" class="rounded">
      <router-view />
    </div>
    <BottomBar />
    <SearchInput />
    <RightSideBar />
    <!-- <Tabs /> -->
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { onStartTyping } from "@vueuse/core";

import useQStore from "@/stores/queue";
import useModalStore from "@/stores/modal";
import useContextStore from "@/stores/context";
import handleShortcuts from "@/composables/useKeyboard";

import Logo from "@/components/Logo.vue";
import Modal from "@/components/modal.vue";
import NavBar from "@/components/nav/NavBar.vue";
// import Tabs from "@/components/RightSideBar/Tabs.vue";
import ContextMenu from "@/components/contextMenu.vue";
import Notification from "@/components/Notification.vue";
import Navigation from "@/components/LeftSidebar/Navigation.vue";
import nowPlaying from "@/components/LeftSidebar/nowPlaying.vue";
import RightSideBar from "@/components/RightSideBar/Main.vue";
import SearchInput from "@/components/RightSideBar/SearchInput.vue";
import BottomBar from "@/components/BottomBar/BottomBar.vue";

import { readLocalStorage, writeLocalStorage } from "@/utils";
import Playlists from "./components/LeftSidebar/Playlists.vue";

const queue = useQStore();
const router = useRouter();
const modal = useModalStore();
const context_store = useContextStore();
const app_dom = document.getElementById("app") as HTMLElement;

queue.readQueue();
handleShortcuts(useQStore);

app_dom.addEventListener("click", (e) => {
  if (context_store.visible) {
    context_store.hideContextMenu();
  }
});

router.afterEach(() => {
  (document.getElementById("acontent") as HTMLElement).scrollTo(0, 0);
});

onStartTyping(() => {
  const elem = document.getElementById("globalsearch") as HTMLInputElement;
  elem.focus();
  elem.value = "";
});

function handleWelcomeModal() {
  let welcomeShowCount = readLocalStorage("shown-welcome-message");

  if (!welcomeShowCount) {
    welcomeShowCount = 0;
  }

  if (welcomeShowCount < 2) {
    modal.showWelcomeModal();
    writeLocalStorage("shown-welcome-message", welcomeShowCount + 1);
  }
}

onMounted(() => {
  handleWelcomeModal();
});
</script>

<style lang="scss">
@import "./assets/scss/mixins.scss";

.l-sidebar {
  position: relative;


  .withlogo {
    padding: 1rem;
  }

  .l-album-art {
    width: calc(100% - 2rem);
    position: absolute;
    bottom: 0;
    margin-bottom: 1rem;
  }
}

.r-sidebar {
  &::-webkit-scrollbar {
    display: none;
  }
}
</style>
