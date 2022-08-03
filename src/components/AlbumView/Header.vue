<template>
  <div
    class="a-header rounded"
    ref="albumheaderthing"
    :style="{
      backgroundImage: `linear-gradient(
        37deg, ${props.album.colors[0]}, ${props.album.colors[3]}
      )`,
    }"
  >
    <div class="art rounded">
      <img :src="imguri + album.image" alt="" class="rounded shadow-lg" />
    </div>
    <div class="info" :class="{ nocontrast: isLight(album.colors[0]) }">
      <div class="top">
        <div class="h">
          <span v-if="album.is_soundtrack">Soundtrack</span>
          <span v-else-if="album.is_compilation">Compilation</span>
          <span v-else-if="album.is_single">Single</span>
          <span v-else>Album</span>
        </div>
        <div class="title ellip cap-first">
          {{ album.title }}
        </div>
      </div>
      <div class="bottom">
        <div class="stats">
          {{ album.count }} Tracks • {{ formatSeconds(album.duration, true) }} •
          {{ album.date }} •
          {{ album.artist }}
        </div>
        <PlayBtnRect
          :source="playSources.album"
          :store="useAlbumStore"
          :background="getButtonColor(album.colors)"
        />
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
import { paths } from "@/config";
import { AlbumInfo } from "../../interfaces";
import PlayBtnRect from "../shared/PlayBtnRect.vue";
import { getButtonColor, isLight } from "../../composables/colors/album";

const props = defineProps<{
  album: AlbumInfo;
}>();

const emit = defineEmits<{
  (event: "resetBottomPadding"): void;
}>();

const albumheaderthing = ref<HTMLElement>(null);
const imguri = paths.images.thumb;
const nav = useNavStore();

/**
 * Calls the `toggleShowPlay` method which toggles the play button in the nav.
 * Emits the `resetBottomPadding` event to reset the album page content bottom padding.
 *
 * @param {boolean} state the new visibility state of the album page header.
 */
function handleVisibilityState(state: boolean) {
  if (state) {
    emit("resetBottomPadding");
  }

  nav.toggleShowPlay(state);
}

useVisibility(albumheaderthing, handleVisibilityState);
</script>

<style lang="scss">
.a-header {
  display: grid;
  grid-template-columns: max-content 1fr;
  gap: 1rem;
  padding: 1rem;
  height: 100% !important;
  background-color: $black;
  background-image: linear-gradient(37deg, $black 20%, $gray, $black 90%);

  .art {
    display: flex;
    align-items: flex-end;
    position: relative;

    img {
      height: 16rem;
      aspect-ratio: 1;
      object-fit: cover;
      transition: all 0.2s ease-in-out;
      user-select: none;
    }
  }

  .nocontrast {
    color: $black;
  }

  .info {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;

    .top {
      .title {
        font-size: 2.5rem;
        font-weight: 600;
      }

      .artist {
        font-size: 1.15rem;
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
    }
  }
}
</style>
