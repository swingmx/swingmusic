<template>
  <div class="settingscontent">
    <Group
      v-for="(group, index) in settingGroups[current].groups"
      :key="index"
      :group="group"
    />
  </div>
</template>

<script setup lang="ts">
import settingGroups from "@/settings";
import Group from "./Group.vue";

defineProps<{
  current: number;
}>();
</script>

<style lang="scss">
.settingscontent {
  width: 100%;
  // max-width: 40rem;
  margin: 0 auto;
}
</style>
