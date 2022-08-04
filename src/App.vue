<template>
  <ContextMenu />
  <Modal />
  <Notification />
  <div id="app-grid">
    <div class="l-sidebar rounded">
      <Logo />
      <Navigation />
      <div class="l-album-art">
        <nowPlaying />
      </div>
    </div>
    <NavBar />
    <div id="acontent" class="rounded">
      <router-view />
    </div>
    <SearchInput />
    <RightSideBar />
    <Tabs />
  </div>
</template>

<script setup lang="ts">
import { onStartTyping } from "@vueuse/core";
import { useRouter } from "vue-router";

import useContextStore from "@/stores/context";
import useQStore from "@/stores/queue";
import useModalStore from "@/stores/modal";
import useShortcuts from "@/composables/useKeyboard";

import ContextMenu from "@/components/contextMenu.vue";
import Navigation from "@/components/LeftSidebar/Navigation.vue";
import nowPlaying from "@/components/LeftSidebar/nowPlaying.vue";
import Logo from "@/components/Logo.vue";
import Modal from "@/components/modal.vue";
import NavBar from "@/components/nav/NavBar.vue";
import Notification from "@/components/Notification.vue";
import RightSideBar from "@/components/RightSideBar/Main.vue";
import SearchInput from "@/components/RightSideBar/SearchInput.vue";
import Tabs from "@/components/RightSideBar/Tabs.vue";
import { onMounted } from "vue";

const queue = useQStore();
const router = useRouter();
const modal = useModalStore();
const context_store = useContextStore();
const app_dom = document.getElementById("app");

queue.readQueue();
useShortcuts(useQStore);

app_dom.addEventListener("click", (e) => {
  if (context_store.visible) {
    context_store.hideContextMenu();
  }
});

router.afterEach(() => {
  document.getElementById("acontent")?.scrollTo(0, 0);
});

onStartTyping(() => {
  const elem = document.getElementById("globalsearch") as HTMLInputElement;
  elem.focus();
  elem.value = "";
});

onMounted(() => {
  modal.showWelcomeModal();
});
</script>

<style lang="scss">
@import "./assets/scss/mixins.scss";

.l-sidebar {
  position: relative;

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
