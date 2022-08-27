<template>
  <div class="settingsgroup">
    <div>
      <h4 v-if="group.title">{{ group.title }}</h4>
      <div class="desc" v-if="group.desc">{{ group.desc }}</div>
    </div>
    <div class="setting rounded bg-primary pad-lg">
      <div
        v-for="(setting, index) in group.settings"
        :key="index"
        :class="{ inactive: setting.inactive && setting.inactive() }"
      >
        <div class="title">
          {{ setting.title }}
        </div>
        <div class="options">
          <Switch
            v-if="setting.type == SettingType.switch"
            @click="setting.action()"
            :state="setting.source()"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { SettingGroup, SettingType } from "@/interfaces/settings";
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

  &:first-child {
    margin-top: 0;
  }

  h4 {
    margin: $small auto;
  }

  .desc {
    opacity: 0.5;
    font-size: 0.9rem;
  }

  .setting {
    display: grid;
    gap: 1rem;

    .inactive {
      opacity: 0.5;
      pointer-events: none;
    }
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
