<template>
  <div
    class="p-header image rounded no-scroll"
    ref="playlistheader"
    :style="[
      {
        backgroundImage: info.image ? `url(${imguri + info.image})` : undefined,
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
          {{ info.count + ` ${info.count == 1 ? "Track" : "Tracks"}` }}
          •
          {{ formatSeconds(info.duration, true) }}
        </div>
        <div class="title ellip">{{ info.name }}</div>
        <div class="type">PLAYLIST</div>
      </div>
    </div>
    <div class="last-updated" :class="{ lightbg: !info.image }">
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
import usePStore from "@/stores/pages/playlist";
import useModalStore from "../../stores/modal";

import { playSources } from "@/composables/enums";
import { formatSeconds, useVisibility } from "@/utils";
import { paths } from "../../config";
import { Playlist } from "../../interfaces";

import PlayBtnRect from "../shared/PlayBtnRect.vue";

const imguri = paths.images.playlist;
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
</script>

<style lang="scss">
.p-header {
  display: grid;
  grid-template-columns: 1fr;
  height: $banner-height;
  position: relative;
  background-color: $gray5;

  .gradient {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    // background-image: linear-gradient(
    //   rgba(0, 0, 0, 0.514),
    //   rgba(0, 0, 0, 0.651)
    // );
    background-color: $black;
    opacity: 0.5;
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

  .last-updated.lightbg {
    background-color: $gray2;
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
      font-size: small;
      font-weight: bold;
      color: rgba(255, 255, 255, 0.692);
    }

    .title {
      font-size: 4rem;
      font-weight: 1000;
      text-transform: capitalize;
      cursor: text;
    }

    .duration {
      font-size: 0.8rem;
      color: $white;
      padding: $smaller;
      padding-left: 0;
      font-weight: 900;
      cursor: text;
    }

    .btns {
      margin-top: $small;
      display: flex;
      gap: $small;
    }
  }
}
</style>
