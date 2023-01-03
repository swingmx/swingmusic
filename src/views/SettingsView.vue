<template>
  <div class="settingspage content-page" style="height: 100%; overflow: auto">
    <Content :current="0" />
  </div>
</template>

<script setup lang="ts">
import Content from "../components/SettingsView/Content.vue";
</script>
