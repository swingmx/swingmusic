<template>
  <div class="settingspage">
    <div class="scrollable">
      <Content :current="0" />
    </div>
    <Nav />
  </div>
</template>

<script setup lang="ts">
import Nav from "@/components/SettingsView/Nav.vue";
import Content from "../components/SettingsView/Content.vue";
</script>

<style lang="scss">
.settingspage {
  height: 100%;
  padding: 1rem;
  display: grid;
  grid-template-rows: 1fr max-content;
  gap: 1rem;
  background-color: $black;

  .scrollable {
    overflow: auto;
    margin-top: 1rem;

    @include for-desktop-down {
      margin-top: 0;
    }
  }
}
</style>
