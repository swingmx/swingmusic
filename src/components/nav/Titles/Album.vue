<template>
  <div class="title albumnavtitle" v-motion-slide-from-left-100>
    <PlayBtn />
    <div class="ellip">
      {{ store.info.title }}
    </div>
  </div>
</template>

<script setup lang="ts">
import useAlbumStore from "@/stores/album";
import PlayBtn from "@/components/shared/PlayBtn.vue";

const store = useAlbumStore();
</script>

<style lang="scss">
.albumnavtitle {
  padding-left: 3rem;

  .play-btn {
    position: absolute;
    left: $smaller;
    top: -$smaller;
    height: 2.25rem;
    aspect-ratio: 1;
  }
}
</style>
