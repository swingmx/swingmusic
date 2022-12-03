<template>
  <div class="albums-list">
    <div class="section-title">
      <b>
        {{ title }}
      </b>
      <div class="see-all"><b>SEE ALL</b></div>
    </div>
    <div class="cars">
      <AlbumCard
        v-for="album in search.albums.value.slice(0, 6)"
        :album="album"
        :key="Math.random()"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import AlbumCard from "../shared/AlbumCard.vue";
import useSearchStore from "@/stores/search";

defineProps<{
  //   albums: Album[];
  title: string;
}>();

const search = useSearchStore();

// TODO: use AlbumView's ArtistAlbums component instead of this
</script>

<style lang="scss">
.albums-list {
  .section-title {
    margin: 0;
    margin-bottom: -$small;

    .see-all {
      float: right;
      font-size: small;
      opacity: 0.5;
    }
  }

  .cars {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
    // padding: 1rem 0;
    // gap: 2rem 0;
  }
}
</style>
