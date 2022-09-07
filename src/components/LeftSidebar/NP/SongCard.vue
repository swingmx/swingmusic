<template>
  <div class="sidebar-songcard">
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
        <div id="bitrate" v-if="track?.bitrate">
          <span v-if="track.bitrate > 1500">MASTER</span>
          <span v-else-if="track.bitrate > 330">FLAC</span>
          <span v-else>MP3</span>
          • {{ track.bitrate }}
        </div>
      </div>
    </router-link>

    <div class="bottom">
      <div class="title ellip">{{ props.track?.title }}</div>
      <ArtistName
        :artists="track?.artists || ['Artist']"
        :albumartist="track?.albumartist"
        class="artists"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { paths } from "../../../config";
import { Track } from "../../../interfaces";
import ArtistName from "@/components/shared/ArtistName.vue";

const props = defineProps<{
  track: Track | null;
}>();

const imguri = paths.images.thumb;
</script>

<style lang="scss">
.sidebar-songcard {
  .art {
    width: 100%;
    aspect-ratio: 1;
    place-items: center;
    margin-bottom: $small;
    position: relative;

    img {
      width: 100%;
      height: auto;
      aspect-ratio: 1;
      object-fit: cover;
    }

    #bitrate {
      position: absolute;
      font-size: 0.75rem;
      width: max-content;
      padding: 0.2rem 0.35rem;
      bottom: 1rem;
      left: 1rem;
      background-color: $black;
      border-radius: $smaller;
      box-shadow: 0rem 0rem 1rem rgba(0, 0, 0, 0.438);
    }
  }

  .bottom {
    display: grid;
    gap: $smaller;
  }

  .title {
    font-weight: 900;
  }

  .artists {
    font-size: 0.85rem;
    opacity: 0.75;

    &:hover {
      text-decoration: underline 1px !important;
    }
  }
}
</style>
