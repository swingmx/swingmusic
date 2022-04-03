<template>
  <div class="p-header">
    <div class="carddd">
      <div class="art image shadow-sm"></div>
      <div class="info">
        <div class="btns">
          <PlayBtnRect :source="playSources.playlist" />
        </div>
        <div class="duration">{{props.info.count}} Tracks • 3 Hours</div>
        <div class="desc">
          {{ props.info.description }}
        </div>
        <div class="title ellip">{{ props.info.name }}</div>
        <div class="type">Playlist</div>
      </div>
    </div>
    <div class="last-updated">
      <span class="status"
        >Last updated {{ props.info.lastUpdated }} |&#160;</span
      >
      <span class="edit">Edit</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { playSources } from "../../composables/enums";
import { Playlist } from "../../interfaces";

import PlayBtnRect from "../shared/PlayBtnRect.vue";
const props = defineProps<{
  info: Playlist;
}>();
</script>

<style lang="scss">
.p-header {
  display: grid;
  grid-template-columns: 1fr;
  height: 14rem;
  background-image: linear-gradient(37deg, $black 4%, $accent, $black);
  position: relative;
  margin-top: $small;
  border-radius: 0.75rem;
  color: $white;

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
    grid-template-columns: 13rem 1fr;

    .art {
      width: 12rem;
      height: 12rem;
      background-color: red;
      background-image: url("../../assets/images/eggs.jpg");
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
    }
  }
}
</style>
