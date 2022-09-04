<template>
  <div class="l-sidebar">
    <div class="withlogo">
      <Logo />
      <Navigation />
    </div>

    <nowPlaying v-if="settings.show_default_np" />
  </div>
</template>

<script setup lang="ts">
import Navigation from "@/components/LeftSidebar/Navigation.vue";
import nowPlaying from "@/components/LeftSidebar/nowPlaying.vue";
import Logo from "@/components/Logo.vue";

import useSettingsStore from "@/stores/settings";

const settings = useSettingsStore();
</script>
