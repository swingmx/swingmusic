<template>
  <div
    class="settingspage content-page"
    style="height: 100%; overflow: auto; padding-right: 1.25rem"
  >
    <Content :current="0" />
  </div>
</template>

<script setup lang="ts">
import Content from "../components/SettingsView/Content.vue";
</script>
