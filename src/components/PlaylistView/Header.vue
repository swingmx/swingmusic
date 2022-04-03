<template>
  <div class="p-header">
    <div class="carddd">
      <div class="art image"></div>
      <div class="info">
        <div class="btns">
          <PlayBtnRect :source="playSources.playlist" />
        </div>
        <div class="duration">4 Tracks • 3 Hours</div>
        <div class="desc">
          {{ props.info.desc[0] }}
          Juice is a drink made from the extraction or pressing of the natural
          liquid contained in fruit and vegetables. It can also refer to liquids
          that are flavored with concentrate or other biological food sources,
          such as meat or seafood, such as clam juice
        </div>
        <div class="title ellip">{{ props.info.name }}</div>
        <div class="type">❤ Playlist</div>
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

import PlayBtnRect from "../shared/PlayBtnRect.vue";
const props = defineProps<{
  info: {
    name: string;
    count: number;
    duration: string;
    desc: string;
    lastUpdated: string;
  };
}>();
</script>

<style lang="scss">
.p-header {
  display: grid;
  grid-template-columns: 1fr;
  height: 14rem;
  // background-image: url("../../assets/images/eggs.jpg");

  background-image: linear-gradient(23deg, $black 40%, rgb(141, 11, 2), $black);
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
