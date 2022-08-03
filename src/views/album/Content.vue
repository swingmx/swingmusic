<template>
  <div class="album-tracks rounded">
    <div v-for="(disc, key) in discs" class="album-disc">
      <SongList
        :key="key"
        :tracks="disc"
        :on_album_page="true"
        :disc="key"
        :copyright="
          () => {
            if (isLastDisc(key)) {
              return copyright;
            }
          }
        "
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { Track } from "@/interfaces";
import SongList from "@/components/FolderView/SongList.vue";

const props = defineProps<{
  discs: {
    [key: string]: Track[];
  };
  copyright: string;
}>();

// check if the disc is the last disc
const isLastDisc = (disc: string | number) => {
  const discs = Object.keys(props.discs);
  return discs[discs.length - 1] === disc;
};
</script>

<style lang="scss">
.album-tracks {
  display: grid;
  gap: 1rem;
}
</style>
