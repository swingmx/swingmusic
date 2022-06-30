<template>
  <div class="album-h" ref="albumheaderthing">
    <div
      class="a-header rounded"
      :style="{
        backgroundImage: `linear-gradient(
        37deg, ${album.colors[0]}, ${album.colors[3]}
      )`,
      }"
    >
      <div class="art">
        <div
          class="image shadow-lg rounded"
          :style="{
            backgroundImage: `url(&quot;${imguri + album.image}&quot;)`,
          }"
          v-motion-slide-from-left
        ></div>
      </div>
      <div class="info">
        <div class="top" v-motion-slide-from-top>
          <div class="h">
            <span v-if="album.is_soundtrack">Soundtrack</span>
            <span v-else-if="album.is_compilation">Compilation</span>
            <span v-else-if="album.is_single">Single</span>
            <span v-else>Album</span>
          </div>
          <div class="title ellip">
            {{ album.title }}
          </div>
        </div>
        <div class="bottom">
          <div class="stats">
            {{ album.count }} Tracks •
            {{ formatSeconds(album.duration, true) }} • {{ album.date }} •
            {{ album.artist }}
          </div>
          <PlayBtnRect :source="playSources.album" :store="useAlbumStore" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import useVisibility from "@/composables/useVisibility";
import useNavStore from "@/stores/nav";
import useAlbumStore from "@/stores/pages/album";
import { ref } from "vue";
import { playSources } from "../../composables/enums";
import { formatSeconds } from "../../composables/perks";
import { paths } from "../../config";
import { AlbumInfo } from "../../interfaces";
import PlayBtnRect from "../shared/PlayBtnRect.vue";

defineProps<{
  album: AlbumInfo;
}>();

const albumheaderthing = ref<HTMLElement>(null);
const imguri = paths.images.thumb;
const nav = useNavStore();

useVisibility(albumheaderthing, nav.toggleShowPlay);
</script>

<style lang="scss">
.album-h {
  height: auto;
}

.a-header {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 1rem;
  padding: 1rem;
  height: 100%;
  background-color: $black;
  background-image: linear-gradient(37deg, $black 20%, $gray, $black 90%);

  .art {
    width: 100%;
    height: 100%;
    left: 1rem;
    display: flex;
    align-items: flex-end;

    .image {
      width: 15rem;
      height: 15rem;
    }
  }

  .info {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;

    .top {
      .h {
        color: #ffffffcb;
      }

      .title {
        font-size: 2.5rem;
        font-weight: 600;
        color: white;
        text-transform: capitalize;
      }

      .artist {
        font-size: 1.15rem;
        color: #ffffffe0;
      }
    }

    .separator {
      width: 20rem;
    }

    .bottom {
      margin-top: $smaller;

      .stats {
        border-radius: $small;
        font-weight: bold;
        font-size: 0.8rem;
        margin-bottom: 0.75rem;
      }

      .play {
        height: 2.5rem;
        width: 6rem;
        display: flex;
        align-items: center;
        background: $blue;
        padding: $small;
        cursor: pointer;

        .icon {
          height: 1.5rem;
          width: 1.5rem;
          margin-right: $small;
          background: url(../../assets/icons/play.svg) no-repeat center/cover;
        }
      }
    }
  }
}
</style>
