<template>
  <ContextMenu />
  <Modal />
  <Notification />
  <section
    id="app-grid"
    :class="{
      noSidebar: !settings.use_sidebar || !xl,
      NoSideBorders: !xxl,
      extendWidth: settings.extend_width && settings.can_extend_width,
    }"
  >
    <LeftSidebar />
    <NavBar />
    <div id="acontent" v-element-size="updateContentElemSize">
      <router-view />
    </div>
    <RightSideBar v-if="settings.use_sidebar && xl" />
    <BottomBar />
  </section>
</template>

<script setup lang="ts">
// @libraries
import { vElementSize } from "@vueuse/components";
import { onStartTyping } from "@vueuse/core";
import { onMounted } from "vue";
import { useRouter } from "vue-router";

// @stores
import { content_width } from "@/stores/content-width";
import useContextStore from "@/stores/context";
import useModalStore from "@/stores/modal";
import useQStore from "@/stores/queue";
import useSettingsStore from "@/stores/settings";

// @utils
import handleShortcuts from "@/composables/useKeyboard";
import { readLocalStorage, writeLocalStorage } from "@/utils";
import { xl, xxl } from "./composables/useBreakpoints";

// @small-components
import ContextMenu from "@/components/ContextMenu.vue";
import Modal from "@/components/modal.vue";
import Notification from "@/components/Notification.vue";

// @app-grid-components
import BottomBar from "@/components/BottomBar.vue";
import NavBar from "@/components/nav/NavBar.vue";
import RightSideBar from "@/components/RightSideBar/Main.vue";
import LeftSidebar from "./components/LeftSidebar/index.vue";

const queue = useQStore();
const router = useRouter();
const modal = useModalStore();
const settings = useSettingsStore();

queue.readQueue();
handleShortcuts(useQStore);

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

function updateContentElemSize({ width }: { width: number }) {
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
