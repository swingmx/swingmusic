<template>
  <div class="card-grid-view v-scroll-page">
    <div class="scrollable">
      <AlbumCard
        v-for="album in albums"
        :album="album"
        :key="album.albumhash"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { getFavAlbums } from "@/composables/fetch/favorite";
import { onMounted, Ref, ref } from "vue";

import AlbumCard from "@/components/shared/AlbumCard.vue";
import { Album } from "@/interfaces";

const albums: Ref<Album[]> = ref([]);

onMounted(() => {
  getFavAlbums(0).then((data) => (albums.value = data));
});
</script>