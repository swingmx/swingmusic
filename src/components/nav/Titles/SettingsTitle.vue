<template>
  <div class="settings-nav">
    <SimpleTitle :text="'Settings'" />
    <Nav />
  </div>
</template>

<script setup lang="ts">
import SimpleTitle from "./SimpleTitle.vue";
import Nav from "@/components/SettingsView/Nav.vue";
</script>

<style lang="scss">
.settings-nav {
  display: grid;
  grid-template-columns: 1fr max-content;
}
</style>
