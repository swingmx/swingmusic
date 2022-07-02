<template>
  <div class="al-view rounded">
    <div class="al-content">
      <div>
        <Header :album="album.info" />
      </div>
      <div class="songs rounded">
        <SongList :tracks="album.tracks" :on_album_page="true" />
      </div>
      <div
        id="bottom-items"
        class="rounded"
        ref="albumbottomcards"
        @click="expandBottom"
      >
        <FeaturedArtists :artists="album.artists" />
        <div v-if="album.bio">
          <div class="separator" id="av-sep"></div>
          <AlbumBio :bio="album.bio" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Header from "../components/AlbumView/Header.vue";
import AlbumBio from "../components/AlbumView/AlbumBio.vue";

import SongList from "../components/FolderView/SongList.vue";
import FeaturedArtists from "../components/PlaylistView/FeaturedArtists.vue";

import useAStore from "../stores/pages/album";
import { onBeforeRouteUpdate } from "vue-router";
import { ref } from "vue";

const album = useAStore();
const albumbottomcards = ref<HTMLElement>(null);

onBeforeRouteUpdate(async (to) => {
  await album.fetchTracksAndArtists(to.params.hash.toString());
  album.fetchBio(to.params.hash.toString());
});

function expandBottom() {
  const elem = albumbottomcards.value;
  elem.style.height = `${40}rem`;
}
</script>

<style lang="scss">
.al-view {
  scrollbar-width: none;
  height: 100%;
  position: relative;
  overflow: hidden;

  .al-content {
    height: 100%;
    overflow: auto;
    padding-bottom: 17rem;
  }

  .songs {
    min-height: calc(100% - 31.5rem);
    margin-top: $small;
  }

  &::-webkit-scrollbar {
    display: none;
  }

  #av-sep {
    border: none;
  }

  #bottom-items {
    z-index: 77;
    padding: $small;
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 15rem;
    max-height: 35rem;
    overflow: hidden;
    background-color: $gray;
    transition: all 0.5s ease;
    overscroll-behavior: contain;
  }
}
</style>
