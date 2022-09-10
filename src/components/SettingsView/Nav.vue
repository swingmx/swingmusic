<template>
  <div class="settingsnav">
    <div class="buttongroup rounded-sm bg-primary">
      <button v-for="(group, index) in settingGroups" :key="index">
        {{ group.title }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import settingGroups from "@/settings";
</script>

<style lang="scss">
.settingsnav {
  .buttongroup {
    display: grid;
    grid-auto-flow: column;
    width: max-content;
    margin: 0 auto;
    overflow: hidden;

    button {
      padding: 0 1rem;
      border-radius: 0;
      width: 5rem;
    }
  }
}
</style>
