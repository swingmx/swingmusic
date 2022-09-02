<template>
  <ContextMenu />
  <Modal />
  <Notification />
  <div
    id="app-grid"
    :class="{
      showAltNP: settings.use_sidebar && settings.use_alt_np,
      disableSidebar: !settings.use_sidebar,
    }"
  >
    <LeftSidebar />
    <NavBar />
    <div id="acontent">
      <router-view />
    </div>
    <NowPlayingRight />
    <SearchInput v-if="settings.use_sidebar" />
    <RightSideBar v-if="settings.use_sidebar" />
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

import Modal from "@/components/modal.vue";
import NavBar from "@/components/nav/NavBar.vue";
import ContextMenu from "@/components/contextMenu.vue";
import Notification from "@/components/Notification.vue";

import RightSideBar from "@/components/RightSideBar/Main.vue";
import SearchInput from "@/components/RightSideBar/SearchInput.vue";
import NowPlayingRight from "@/components/RightSideBar/NowPlayingRight.vue";
import LeftSidebar from "./components/LeftSidebar/index.vue";
import useSettingsStore from "@/stores/settings";

import { readLocalStorage, writeLocalStorage } from "@/utils";

const queue = useQStore();
const router = useRouter();
const modal = useModalStore();
const context_store = useContextStore();
const settings = useSettingsStore();
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
