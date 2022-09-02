<template>
  <div
    class="p-header image rounded noscroll"
    ref="playlistheader"
    :style="[
      {
        backgroundImage: info.image ? `url(${imguri + info.image})` : '',
      },
    ]"
    :class="{ border: !info.image }"
  >
    <div class="gradient" v-if="info.image"></div>
    <div class="carddd">
      <div class="info">
        <div class="btns">
          <PlayBtnRect :source="playSources.playlist" :store="usePStore" />
        </div>
        <div class="duration">
          <span v-if="info.count == 0">No Tracks</span>
          <span v-else-if="info.count == 1">{{ info.count }} Track</span>
          <span v-else>{{ info.count }} Tracks</span> •
          {{ formatSeconds(info.duration, true) }}
        </div>
        <div class="title ellip">{{ info.name }}</div>
        <div class="type">Playlist</div>
      </div>
    </div>
    <div class="last-updated">
      <span class="status"
        >Last updated {{ info.lastUpdated }} &#160;|&#160;&#160;</span
      >
      <span class="edit" @click="editPlaylist">Edit</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import useNavStore from "@/stores/nav";
import useModalStore from "../../stores/modal";
import pContext from "../../contexts/playlist";
import usePStore from "@/stores/pages/playlist";
import useContextStore from "../../stores/context";

import { paths } from "../../config";
import { Playlist } from "../../interfaces";
import { useVisibility, formatSeconds } from "@/utils";
import { ContextSrc, playSources } from "@/composables/enums";

import PlayBtnRect from "../shared/PlayBtnRect.vue";

const imguri = paths.images.playlist;
const context = useContextStore();
const modal = useModalStore();
const nav = useNavStore();
const playlistheader = ref<HTMLElement | null>(null);

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


  .gradient {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: linear-gradient(
      20deg,
      rgba(0, 0, 0, 0.25) 40%,
      rgba(0, 0, 0, 0.1),
      rgba(0, 0, 0, 0.1) 70%
    );
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
