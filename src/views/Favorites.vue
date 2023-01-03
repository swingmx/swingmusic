<template>
  <div class="content-page favorites-page">
    <div class="fav-albums" v-if="favAlbums.length">
      <ArtistAlbums
        :albums="favAlbums"
        :albumType="discographyAlbumTypes.albums"
        :title="'Albums ❤️'"
        :route="'/favorites/albums'"
      />
    </div>
    <div class="fav-tracks" v-if="favTracks.length">
      <TopTracks
        :tracks="favTracks"
        :route="'/favorites/tracks'"
        :title="'Tracks ❤️'"
        :playHandler="handlePlay"
      />
    </div>

    <div class="fav-artists" v-if="favArtists.length">
      <FeaturedArtists :artists="favArtists" :title="'Artists ❤️'" :route="'/favorites/artists'"/>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, Ref, ref } from "vue";

import ArtistAlbums from "@/components/AlbumView/ArtistAlbums.vue";
import TopTracks from "@/components/ArtistView/TopTracks.vue";
import FeaturedArtists from "@/components/PlaylistView/ArtistsList.vue";
import { discographyAlbumTypes } from "@/composables/enums";
import { getAllFavs, getFavTracks } from "@/composables/fetch/favorite";
import { Album, Artist, Track } from "@/interfaces";
import useQueueStore from "@/stores/queue";
import { maxAbumCards } from "@/stores/content-width";

const queue = useQueueStore();

const favAlbums: Ref<Album[]> = ref([]);
const favTracks: Ref<Track[]> = ref([]);
const favArtists: Ref<Artist[]> = ref([]);

onMounted(() => {
  const max = maxAbumCards.value;
  getAllFavs(5, max, max).then((favs) => {
    favAlbums.value = favs.albums;
    favTracks.value = favs.tracks;
    favArtists.value = favs.artists;
  });
});

async function handlePlay(index: number) {
  const tracks = await getFavTracks(0);
  queue.playFromFav(tracks);
  queue.play(index);
}
</script>

<style lang="scss">
.favorites-page {
  height: 100%;
  overflow: auto;
  padding-bottom: 4rem;
  padding-right: 1rem;

  h3 {
    margin-top: 0;
  }

  .fav-tracks {
    margin-bottom: 2rem;

    h3 {
      margin-top: 0;
    }

    .artist-top-tracks {
      margin-top: 0;
    }
  }

  .fav-albums {
    .album-list {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
    }
    margin-bottom: 2rem;
  }
}
</style>
