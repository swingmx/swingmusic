<template>
  <div class="album-tracks rounded">
    <div v-for="(disc, key) in discs" class="album-disc">
      <SongList
        :key="key"
        :tracks="disc"
        :on_album_page="true"
        :disc="key"
        :copyright="isLastDisc(key) ? copyright : null"
        @playFromPage="playFromAlbumPage"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
// @stores
import useQueueStore from "@/stores/queue";
import useAlbumStore from "@/stores/pages/album";

// @utils
import { Track } from "@/interfaces";

// @components
import SongList from "@/components/FolderView/SongList.vue";

// @setup

const props = defineProps<{
  discs: {
    [key: string]: Track[];
  };
  copyright?: string;
}>();

const queue = useQueueStore();
const album = useAlbumStore();

// check if the disc is the last disc
const isLastDisc = (disc: string | number) => {
  const discs = Object.keys(props.discs);
  return discs[discs.length - 1] === disc;
};

function playFromAlbumPage(index: number) {
  const { title, artist, hash } = album.info;
  queue.playFromAlbum(title, artist, hash, album.allTracks);
  queue.play(index);
}
</script>

<style lang="scss">
.album-tracks {
  display: grid;
  gap: 1rem;
}
</style>
