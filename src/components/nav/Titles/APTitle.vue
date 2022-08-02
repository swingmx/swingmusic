<template>
  <div class="title albumnavtitle">
    <PlayBtn :source="things.source" :store="things.store" />
    <div class="ellip">
      {{ things.text }}
    </div>
  </div>
</template>

<script setup lang="ts">
import PlayBtn from "@/components/shared/PlayBtn.vue";
import { playSources, Routes } from "@/composables/enums";
import useAlbumStore from "@/stores/pages/album";
import usePStore from "@/stores/pages/playlist";
import { computed } from "@vue/reactivity";
import { useRoute } from "vue-router";


const things = computed(() => {
  const route = useRoute();
  let thing = {
    text: "",
    store: null,
    source: playSources.album,
  };

  if (route.name == Routes.album) {
    thing = {
      source: playSources.album,
      text: useAlbumStore().info.title,
      store: useAlbumStore,
    };
  } else if (route.name == Routes.playlist) {
    thing = {
      source: playSources.playlist,
      text: usePStore().info.name,
      store: usePStore,
    };
  }

  return thing;
});
</script>

<style lang="scss">
.albumnavtitle {
  display: flex;
  align-items: center;
  gap: $small;
}
</style>
