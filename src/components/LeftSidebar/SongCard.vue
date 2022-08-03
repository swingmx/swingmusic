<template>
  <div class="info">
    <div class="desc">
      <div>
        <router-link
          :to="{
            name: 'AlbumView',
            params: {
              hash: track.albumhash,
            },
          }"
        >
          <div class="art">
            <img :src="imguri + track.image" alt="" class="l-image rounded" />
          </div>
        </router-link>

        <div id="bitrate">
          <span v-if="track.bitrate > 1500">MASTER</span>
          <span v-else-if="track.bitrate > 330">FLAC</span>
          <span v-else>MP3</span>
          • {{ track.bitrate }}
        </div>
        <div class="title ellip cap-first">{{ props.track.title }}</div>
        <div class="separator no-border"></div>
        <div class="artists ellip cap-first" v-if="props.track.artists[0] !== ''">
          <span
            v-for="artist in putCommas(props.track.artists)"
            :key="artist"
            >{{ artist }}</span
          >
        </div>
        <div class="artists" v-else>
          <span>{{ props.track.albumartist }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { putCommas } from "../../composables/perks";
import { Track } from "../../interfaces";
import { paths } from "../../config";
const imguri = paths.images.thumb;

const props = defineProps<{
  track: Track;
}>();
</script>
