<template>
  <div class="settingsgroup">
    <div>
      <h4>{{ group.title }}</h4>
      <div class="desc">{{ group.desc }}</div>
    </div>
    <div class="setting rounded bg-black pad-lg">
      <div v-for="(setting, index) in group.settings" :key="index">
        <div class="title">
          {{ setting.title }}
        </div>
        <div class="options"><Switch /></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { SettingGroup } from "@/interfaces/settings";
import Switch from "./Components/Switch.vue";

defineProps<{
  group: SettingGroup;
}>();
</script>

<style lang="scss">
.settingsgroup {
  display: grid;
  gap: $small;
  margin-top: 2rem;

  h4 {
    margin: $small auto;
  }

  .desc {
    opacity: 0.5;
    font-size: 0.9rem;
  }

  .setting > * {
    display: grid;
    grid-template-columns: 1fr max-content;

    .title {
      margin: auto 0;
    }
  }
}
</style>
