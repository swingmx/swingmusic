<template>
  <div class="info">
    <div class="desc">
      <div>
        <router-link
          :to="{
            name: 'AlbumView',
            params: {
              hash: track?.albumhash ? track.albumhash : ' ',
            },
          }"
        >
          <div class="art">
            <img
              :src="imguri + track?.image"
              alt=""
              class="l-image rounded force-lm"
              loading="lazy"
            />
          </div>
        </router-link>

        <div id="bitrate" v-if="track?.bitrate">
          <span v-if="track.bitrate > 1500">MASTER</span>
          <span v-else-if="track.bitrate > 330">FLAC</span>
          <span v-else>MP3</span>
          • {{ track.bitrate }}
        </div>
        <div class="title ellip">{{ props.track?.title }}</div>
        <div class="separator no-border"></div>
        <div
          class="artists ellip"
          v-if="track?.artists && track?.artists[0] !== ''"
        >
          <span v-for="artist in putCommas(track.artists)" :key="artist">{{
            artist
          }}</span>
        </div>
        <div class="artists" v-else-if="track?.artists">
          <span>{{ track.albumartist }}</span>
        </div>
        <div class="artists" v-else>
          <span>Meh</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { putCommas } from "@/utils";
import { paths } from "../../../config";
import { Track } from "../../../interfaces";
const imguri = paths.images.thumb;

const props = defineProps<{
  track: Track | null;
}>();
</script>
