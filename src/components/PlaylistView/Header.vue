<template>
  <div
    class="p-header image"
    ref="playlistheader"
    :style="[
      {
        backgroundImage: `url(${imguri + props.info.image})`,
      },
    ]"
  >
    <div class="gradient"></div>
    <div class="carddd">
      <div class="info">
        <div class="btns">
          <PlayBtnRect
            :source="playSources.playlist"
            :store="usePStore"
            :background="{
              color: '#fff',
              isDark: true,
            }"
          />
          <Option @showDropdown="showDropdown" :src="context.src" />
        </div>
        <div class="duration">
          <span v-if="props.info.count == 0">No Tracks</span>
          <span v-else-if="props.info.count == 1"
            >{{ props.info.count }} Track</span
          >
          <span v-else>{{ props.info.count }} Tracks</span> •
          {{ formatSeconds(props.info.duration, true) }}
        </div>
        <div class="desc">
          {{ props.info.description }}
        </div>
        <div class="title ellip">{{ props.info.name }}</div>
        <div class="type">Playlist</div>
      </div>
    </div>
    <div class="last-updated">
      <span class="status"
        >Last updated {{ props.info.lastUpdated }} &#160;|&#160;&#160;</span
      >
      <span class="edit" @click="editPlaylist">Edit</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import useVisibility from "@/composables/useVisibility";
import useNavStore from "@/stores/nav";
import usePStore from "@/stores/pages/playlist";
import { ref } from "vue";
import { ContextSrc, playSources } from "../../composables/enums";
import { paths } from "../../config";
import pContext from "../../contexts/playlist";
import { Playlist } from "../../interfaces";
import useContextStore from "../../stores/context";
import useModalStore from "../../stores/modal";
import Option from "../shared/Option.vue";
import PlayBtnRect from "../shared/PlayBtnRect.vue";
import { formatSeconds } from "@/composables/perks";

const imguri = paths.images.playlist;
const context = useContextStore();
const modal = useModalStore();
const nav = useNavStore();
const playlistheader = ref(null);

useVisibility(playlistheader, nav.toggleShowPlay);

const props = defineProps<{
  info: Playlist;
}>();

function editPlaylist() {
  modal.showEditPlaylistModal(props.info);
}

function showDropdown(e: any) {
  context.showContextMenu(e, pContext(), ContextSrc.PHeader);
}
</script>

<style lang="scss">
.p-header {
  display: grid;
  grid-template-columns: 1fr;
  height: 100%;
  position: relative;
  border-radius: 0.75rem;
  color: $white;
  background-color: transparent;
  z-index: 0;

  .gradient {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: linear-gradient(
      37deg,
      $black 20%,
      transparent,
      $black 90%
    );
    border-radius: 0.5rem;
  }

  .last-updated {
    position: absolute;
    bottom: 1rem;
    right: 1rem;
    padding: 0.5rem;
    background-color: $body;
    color: rgb(255, 255, 255);
    font-size: 0.9rem;
    border-radius: $smaller;
    box-shadow: 0 0 1rem rgba(0, 0, 0, 0.479);
    z-index: 12;

    @include phone-only {
      bottom: 1rem;
      right: 1rem;
      font-size: small;

      .status {
        display: none;
      }
    }

    .edit {
      cursor: pointer;
    }
  }

  .carddd {
    width: 100%;
    padding: 1rem;
    display: grid;
    z-index: 10;

    .art {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: flex-end;

      .image {
        width: 12rem;
        height: 12rem;
        background-image: url("../../assets/images/eggs.jpg");
      }
    }

    .info {
      display: flex;
      flex-direction: column-reverse;
    }

    .type {
      color: rgba(255, 255, 255, 0.692);
    }

    .title {
      font-size: 2.5rem;
      font-weight: 900;
      text-transform: capitalize;
    }

    .desc {
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: initial;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      max-width: 50%;
    }

    .duration {
      font-size: 0.8rem;
      color: $white;
      padding: $smaller;
      padding-left: 0;
      font-weight: 900;
    }

    .btns {
      margin-top: $small;
      display: flex;
      gap: $small;
    }
  }
}
</style>
