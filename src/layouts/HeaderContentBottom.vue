<template>
  <div class="ap-container noscroll rounded">
    <div id="ap-page">
      <header class="ap-page-header" ref="apheader">
        <slot name="header"></slot>
      </header>
      <main class="ap-page-content">
        <slot name="content"></slot>
      </main>
    </div>
    <div
      class="ap-page-bottom-container rounded"
      ref="apbottomcontainer"
      :class="{
        bottomexpanded: bottomContainerRaised,
      }"
    >
      <div class="click-to-expand" @click="toggleBottom">
        <div>
          <div class="arrow">↑</div>
          <span>tap here</span>
        </div>
      </div>
      <div class="bottom-content">
        <slot name="bottom"></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import useVisibility from "@/composables/useVisibility";
import useNavStore from "@/stores/nav";
import { onBeforeRouteUpdate, RouteParams, useRoute } from "vue-router";

const nav = useNavStore();

const props = defineProps<{
  /**
   *  Called when the bottom container is raised.
   */
  bottomRaisedCallback?: (routeparams?: RouteParams) => void;
}>();

let elem: HTMLElement = null;
let classlist: DOMTokenList = null;

const route = useRoute();
const apheader = ref<HTMLElement>(null);
const apbottomcontainer = ref(null);
const bottomContainerRaised = ref(false);

onMounted(() => {
  elem = document.getElementById("ap-page");
  classlist = elem.classList;
});

onBeforeRouteUpdate((to) => {
  if (bottomContainerRaised.value) {
    if (!props.bottomRaisedCallback) return;
    props.bottomRaisedCallback(to.params);
  }
});

function handleVisibilityState(state: boolean) {
  resetBottomPadding();

  nav.toggleShowPlay(state);
}

useVisibility(apheader, handleVisibilityState);

function resetBottomPadding() {
  if (bottomContainerRaised.value) return;

  classlist.remove("addbottompadding");
}

let bottomRaisedCallbackExecuted = false;

function toggleBottom() {
  bottomContainerRaised.value = !bottomContainerRaised.value;

  if (bottomContainerRaised.value) {
    classlist.add("addbottompadding");
    if (!bottomRaisedCallbackExecuted) {
      bottomRaisedCallbackExecuted = true;
      if (!props.bottomRaisedCallback) return;
      props.bottomRaisedCallback(route.params);
    }
    return;
  }
  if (elem.scrollTop == 0) {
    classlist.remove("addbottompadding");
  }
}
</script>

<style lang="scss">
.ap-container {
  height: 100%;
  position: relative;

  #ap-page {
    overflow: auto;
    height: 100%;
    position: relative;
    display: grid;
    grid-template-rows: 18rem 1fr;
    gap: 1rem;

    .ap-page-content {
      padding-bottom: 16rem;
    }
  }

  .ap-page-bottom-container {
    position: absolute;
    bottom: 0;
    height: 15rem;
    width: 100%;
    background-color: $gray;
    transition: all 0.5s ease !important;
    overscroll-behavior: contain;
    display: grid;
    grid-template-rows: 2rem 1fr;

    .bottom-content {
      overflow: hidden;
      scroll-behavior: contain;
    }

    .click-to-expand {
      height: 1.5rem;
      display: flex;
      align-items: center;
      color: $gray1;

      div {
        margin: 0 auto;
        font-size: small;
        cursor: default;
        user-select: none;
        display: flex;
        gap: $small;
      }

      .arrow {
        max-width: min-content;
        transition: all 0.2s ease-in-out;
      }

      &:hover {
        color: $accent !important;
      }
    }
  }

  .bottomexpanded {
    height: 32rem !important;
    scroll-behavior: contain;

    .arrow {
      transform: rotate(180deg) !important;
    }

    .bottom-content {
      overflow: auto !important;
      scrollbar-width: none;

      &::-webkit-scrollbar {
        display: none;
      }
    }
  }

  .addbottompadding {
    padding-bottom: 16rem;
  }
}
</style>
