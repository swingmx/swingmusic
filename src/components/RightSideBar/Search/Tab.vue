<template>
  <component :is="getComponent()?.component" v-bind="getComponent()?.props" />
</template>

<script setup lang="ts">
import ArtistGrid from "./ArtistGrid.vue";
import TracksGrid from "./TracksGrid.vue";

const props = defineProps<{
  name: string;
  isOnSearchPage?: boolean;
}>();

function getComponent() {
  switch (props.name) {
    case "tracks":
      return {
        component: TracksGrid,
        props: {
          isOnSearchPage: props.isOnSearchPage,
        },
      };
    case "albums":
      return {
        component: ArtistGrid,
        props: {
          album_grid: true,
        },
      };
    case "artists":
      return {
        component: ArtistGrid,
        props: {},
      };
    default:
      return null;
  }
}
</script>
