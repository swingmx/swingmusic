<template>
  <div class="artist-top-tracks">
    <h3 class="section-title">
      Tracks
      <span class="see-more">
        <RouterLink
          :to="{
            name: Routes.artistTracks,
            params: {
              hash: artist.info.artisthash,
            },
            query: {
              artist: artist.info.name,
            },
          }"
          >SEE ALL</RouterLink
        >
      </span>
    </h3>
    <div class="tracks">
      <SongItem
        v-for="(song, index) in artist.tracks"
        :track="song"
        :index="index + 1"
        @playThis="playFromPage(index)"
      />
    </div>
    <div class="error" v-if="!artist.tracks.length">No tracks</div>
  </div>
</template>

<script setup lang="ts">
import SongItem from "../shared/SongItem.vue";
import useArtistPageStore from "@/stores/pages/artist";
import useQueueStore from "@/stores/queue";
import { FromOptions, playSources } from "@/composables/enums";

import { getArtistTracks } from "@/composables/fetch/artists";
import { Routes } from "@/router/routes";

const artist = useArtistPageStore();
const queue = useQueueStore();

async function playFromPage(index: number) {
  if (
    queue.from.type == FromOptions.artist &&
    queue.from.artisthash == artist.info.artisthash
  ) {
    queue.play(index);
    return;
  }

  const tracks = await getArtistTracks(artist.info.artisthash);
  queue.playFromArtist(artist.info.artisthash, artist.info.name, tracks);
  queue.play(index);
}
</script>

<style lang="scss">
.artist-top-tracks {
  margin-top: 2rem;

  .section-title {
    margin-left: 0;
  }

  .error {
    padding-left: 1rem;
    color: $red;
  }

  h3 {
    display: flex;
    justify-content: space-between;
  }

  .see-more {
    font-size: $medium;

    a:hover {
      text-decoration: underline;
      cursor: pointer !important;
    }
  }
}
</style>
