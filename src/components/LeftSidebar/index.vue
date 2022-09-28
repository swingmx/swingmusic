<template>
  <div class="l-sidebar noscroll">
    <div class="withlogo">
      <Logo />
      <Navigation />
    </div>

    <NPImg v-if="settings.use_np_img" />
  </div>
</template>

<script setup lang="ts">
import Navigation from "@/components/LeftSidebar/Navigation.vue";
import NPImg from "./NowPlayingImg.vue";
import Logo from "@/components/Logo.vue";

import useSettingsStore from "@/stores/settings";

const settings = useSettingsStore();
</script>
