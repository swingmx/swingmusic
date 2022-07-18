<template>
  <ContextMenu />
  <Modal />
  <Notification />
  <div class="l-container">
    <div class="l-sidebar rounded">
      <Logo />
      <Navigation />
      <div class="l-album-art">
        <nowPlaying />
      </div>
    </div>
    <NavBar />
    <div id="acontent">
      <router-view />
    </div>
    <SearchInput />
    <RightSideBar />
    <Tabs />
  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute, RouteLocationNormalized } from "vue-router";
import { onStartTyping } from "@vueuse/core";

import Navigation from "@/components/LeftSidebar/Navigation.vue";
import RightSideBar from "@/components/RightSideBar/Main.vue";
import nowPlaying from "@/components/LeftSidebar/nowPlaying.vue";
import NavBar from "@/components/nav/NavBar.vue";
import Tabs from "@/components/RightSideBar/Tabs.vue";
import SearchInput from "@/components/RightSideBar/SearchInput.vue";
import useContextStore from "@/stores/context";
import ContextMenu from "@/components/contextMenu.vue";
import Modal from "@/components/modal.vue";
import Notification from "@/components/Notification.vue";
import useQStore from "@/stores/queue";
import Logo from "@/components/Logo.vue";

import useShortcuts from "@/composables/useKeyboard";
import { isSameRoute } from "@/composables/perks";

const context_store = useContextStore();
const queue = useQStore();
const app_dom = document.getElementById("app");
const route = useRoute();
const router = useRouter();

// function to add the 

queue.readQueue();
useShortcuts(useQStore);

app_dom.addEventListener("click", (e) => {
  if (context_store.visible) {
    context_store.hideContextMenu();
  }
});

function removeHighlight(route: RouteLocationNormalized) {
  setTimeout(() => {
    router.push({ name: route.name, params: route.params });
  }, 5000);
}

router.afterEach((to, from) => {
  const h_hash = to.query.highlight as string;

  if (h_hash) removeHighlight(to);
  if (isSameRoute(to, from)) return;

  document.getElementById("acontent")?.scrollTo(0, 0);
});

onStartTyping(() => {
  document.getElementById("globalsearch").focus();
});
</script>

<style lang="scss">
@import "./assets/css/mixins.scss";

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

.content {
  padding: 0 $small;
  margin-top: $small;
  overflow: auto;
  padding-right: $small !important;
}
</style>
