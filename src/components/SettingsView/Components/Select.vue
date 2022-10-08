<template>
  <div class="setting-select rounded-sm no-scroll">
    <div
      class="option"
      v-for="option in optionsWithActive"
      :key="option.title"
      :class="{ active: option.active }"
      @click="setterFn(option.value)"
    >
      {{ option.title }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { SettingOption } from "@/interfaces/settings";
import { computed } from "vue";

const props = defineProps<{
  options: SettingOption[] | undefined;
  source: () => string;
  setterFn: (value: any) => void;
}>();

const optionsWithActive = computed(() => {
  return props.options?.map((option) => {
    return {
      ...option,
      active: option.value === props.source(),
    };
  });
});
</script>

<style lang="scss">
.setting-select {
  display: flex;
  background-color: $gray3;

  .option {
    padding: 0.5rem;
    cursor: pointer;
    user-select: none;
    min-width: 4rem;
    text-align: center;
  }

  .option.active {
    background-color: $darkestblue;
  }
}
</style>
