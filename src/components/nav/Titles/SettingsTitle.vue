<template>
  <div class="settings-nav">
    <SimpleNav :text="'Settings'" />
    <Nav />
  </div>
</template>

<script setup lang="ts">
import SimpleNav from "./SimpleNav.vue";
import Nav from "@/components/SettingsView/Nav.vue";
</script>

<style lang="scss">
.settings-nav {
  display: grid;
  grid-template-columns: 1fr max-content;
}
</style>
