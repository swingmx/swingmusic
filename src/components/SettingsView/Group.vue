<template>
  <div class="settingsgroup">
    <div v-if="group.title || group.desc" class="info">
      <h4 v-if="group.title">{{ group.title }}</h4>
      <div class="desc" v-if="group.desc">{{ group.desc }}</div>
    </div>
    <div class="setting rounded pad-lg">
      <div
        v-for="(setting, index) in group.settings"
        :key="index"
        :class="{ inactive: setting.inactive && setting.inactive() }"
      >
        <div
          class="title ellip"
          @click="
            setting.defaultAction ? setting.defaultAction() : setting.action()
          "
        >
          {{ setting.title }}
        </div>
        <div class="options">
          <Switch
            v-if="setting.type == SettingType.binary"
            @click="setting.action()"
            :state="setting.source()"
          />
          <Select
            v-if="setting.type === SettingType.select"
            :options="setting.options"
            :source="setting.source"
            :setterFn="setting.action"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { SettingType } from "@/settings/enums";
import { SettingGroup } from "@/interfaces/settings";

import Switch from "./Components/Switch.vue";
import Select from "./Components/Select.vue";

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

  .info {
    margin-left: $smaller;
  }

  h4 {
    margin: $small auto;
  }

  .desc {
    opacity: 0.5;
    font-size: 0.8rem;
  }

  .setting {
    background-color: $gray;
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
      user-select: none;
      cursor: pointer;
    }
  }
}
</style>
