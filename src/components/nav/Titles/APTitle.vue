<template>
  <div
    class="title grid albumnavtitle"
    :class="{
      hide_play: header_shown,
    }"
  >
    <div class="first grid">
      <PlayBtn :source="things.source" :store="things.store" />
      <div class="ellip">
        {{ things.text }}
      </div>
    </div>
    {{ usePStore().query }}
    <Input :ref_value="usePStore().query" />
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";
import { computed } from "@vue/reactivity";

import PlayBtn from "@/components/shared/PlayBtn.vue";
import { playSources, Routes } from "@/composables/enums";
import useAlbumStore from "@/stores/pages/album";
import usePStore from "@/stores/pages/playlist";
import Input from "@/components/shared/Input.vue";

defineProps<{
  header_shown: boolean;
}>();

const things = computed(() => {
  const route = useRoute();
  let thing = {
    text: "",
    store: null as any,
    source: playSources.album,
  };

  switch (route.name) {
    case Routes.album:
      thing = {
        source: playSources.album,
        text: useAlbumStore().info.title,
        store: useAlbumStore,
      };
      break;
    case Routes.playlist:
      thing = {
        source: playSources.playlist,
        text: usePStore().info.name,
        store: usePStore,
      };
      break;
  }

  return thing;
});
</script>

<style lang="scss">
.albumnavtitle {
  grid-template-columns: max-content 1fr;
  align-items: center;
  justify-content: space-between;
  gap: $small;
  height: 100%;

  .first {
    grid-template-columns: max-content 1fr;
    gap: $small;
    align-items: center;
  }
}

.albumnavtitle.hide_play {
  .first {
    visibility: hidden;
  }
}
</style>
