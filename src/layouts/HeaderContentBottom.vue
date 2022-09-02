<template>
  <div id="ap-page">
    <header class="ap-page-header" ref="apheader">
      <slot name="header"></slot>
    </header>
    <main class="ap-page-content">
      <slot name="content"></slot>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useVisibility } from "@/utils";
import useNavStore from "@/stores/nav";

const nav = useNavStore();
const apheader = ref<any>(null);

function handleVisibilityState(state: boolean) {
  nav.toggleShowPlay(state);
}

useVisibility(apheader, handleVisibilityState);
</script>

<style lang="scss">
#ap-page {
  display: grid;
  grid-template-rows: 18rem 1fr;
  gap: 1rem;
}
</style>
