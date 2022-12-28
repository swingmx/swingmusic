<template>
  <div class="content-page favorites-page">
    <div class="header">
      <div class="tracks">Tracks</div>
      <div class="albums">Albums</div>
      <div class="artists">Artists</div>
      <div class="folders">Folders</div>
    </div>
    <div class="fav-tracks">
      <TopTracks
        :tracks="favTracks"
        :route="'/home'"
        :title="'Favorite tracks'"
        :playHandler="handlePlay"
      />
    </div>

    <div class="fav-albums">
      <ArtistAlbums
        :albums="favAlbums"
        :albumType="discographyAlbumTypes.albums"
        :title="'Favorite albums'"
        :route="'some'"
      />
    </div>
    <div class="fav-artists">
      <FeaturedArtists :artists="favArtists" :title="'Favorite artists'" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, Ref, ref } from "vue";

import ArtistAlbums from "@/components/AlbumView/ArtistAlbums.vue";
import TopTracks from "@/components/ArtistView/TopTracks.vue";
import FeaturedArtists from "@/components/PlaylistView/ArtistsList.vue";
import { discographyAlbumTypes } from "@/composables/enums";
import {
  getFavAlbums,
  getFavArtists,
  getFavTracks,
} from "@/composables/fetch/favorite";
import { Album, Artist, Track } from "@/interfaces";
import useQueueStore from "@/stores/queue";
import { maxAbumCards } from "@/stores/content-width";

const queue = useQueueStore();

const favAlbums: Ref<Album[]> = ref([]);
const favTracks: Ref<Track[]> = ref([]);
const favArtists: Ref<Artist[]> = ref([]);

onMounted(() => {
  getFavTracks().then((tracks) => (favTracks.value = tracks));
  getFavAlbums(maxAbumCards.value).then((albums) => (favAlbums.value = albums));
  getFavArtists(maxAbumCards.value).then(
    (artists) => (favArtists.value = artists)
  );
});

async function handlePlay(index: number) {
  console.log(index);

  const tracks = await getFavTracks(0);
  queue.playFromFav(tracks);
  queue.play(index);
}
</script>

<style lang="scss">
$tracksbg: rgb(55, 74, 243);
$albumsbg: rgb(255, 123, 0);
$artistsbg: rgb(0, 255, 21);

.favorites-page {
  height: 100%;
  overflow: scroll;
  padding-bottom: 4rem;

  .header > * {
    padding: 1rem;
    display: grid;
    place-content: center;
    border-radius: $small;
    font-weight: bold;
    width: 10rem;
  }

  .header {
    width: 100%;
    display: flex;
    gap: 1rem;

    .albums {
      background: $orange;
    }

    .tracks {
      background-color: $pink;
    }

    .artists {
      background-color: $blue;
    }

    .folders {
      background-color: $gray2;
    }
  }

  .fav-tracks {
    h3 {
      padding-left: 2rem;
      display: flex;
      justify-content: space-between;

      .see-all {
        font-size: $medium;
      }
    }
    margin: 1rem 0;
  }

  .fav-albums {
    // margin-top: 3rem;
    .album-list {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(10rem, 1fr));
    }
  }

  .fav-artists {
    margin-top: 3rem;
  }
}
</style>
