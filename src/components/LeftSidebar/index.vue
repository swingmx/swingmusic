<template>
  <div class="l-sidebar no-scroll">
    <div class="withlogo">
      <Logo />
      <Navigation />
    </div>

    <NowPlayingImage v-if="settings.use_np_img" />
  </div>
</template>

<script setup lang="ts">
import Navigation from "@/components/LeftSidebar/Navigation.vue";
import Logo from "@/components/Logo.vue";
import NowPlayingImage from "./NowPlayingImg.vue";

import useSettingsStore from "@/stores/settings";

const settings = useSettingsStore();
</script>