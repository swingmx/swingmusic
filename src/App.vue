<template>
  <ContextMenu />
  <Modal />
  <Notification />
  <div id="tooltip"></div>
  <section
    id="app-grid"
    :class="{
      noSidebar: !settings.use_sidebar || !xl,
      extendWidth: settings.extend_width && settings.extend_width_enabled,
      addBorderRight: xxl && !settings.extend_width,
    }"
  >
    <LeftSidebar />
    <NavBar />
    <div id="acontent" v-element-size="updateContentElemSize">
      <router-view />
    </div>
    <!-- <SearchInput v-if="settings.use_sidebar && xl" /> -->
    <RightSideBar v-if="settings.use_sidebar && xl" />
    <BottomBar />
  </section>
</template>

<script setup lang="ts">
// @libraries
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { onStartTyping } from "@vueuse/core";
import { vElementSize } from "@vueuse/components";

// @stores
import useQStore from "@/stores/queue";
import useModalStore from "@/stores/modal";
import useContextStore from "@/stores/context";
import useSettingsStore from "@/stores/settings";
import { content_width } from "@/stores/content-width";

// @utils
import { xl, xxl } from "./composables/useBreakpoints";
import handleShortcuts from "@/composables/useKeyboard";
import { readLocalStorage, writeLocalStorage } from "@/utils";

// @small-components
import Modal from "@/components/modal.vue";
import ContextMenu from "@/components/ContextMenu.vue";
import Notification from "@/components/Notification.vue";

// @app-grid-components
import NavBar from "@/components/nav/NavBar.vue";
import LeftSidebar from "./components/LeftSidebar/index.vue";
import RightSideBar from "@/components/RightSideBar/Main.vue";
import BottomBar from "@/components/BottomBar.vue";

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

onStartTyping((e) => {
  if (e.ctrlKey) {
    console.log("ctrl pressed");
  }

  const elem = document.getElementById("globalsearch") as HTMLInputElement;
  elem.focus();
  elem.value = "";
});

function updateContentElemSize({
  width,
  height,
}: {
  width: number;
  height: number;
}) {
  content_width.value = width;
}

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
