<template>
  <div class="p-header">
    <div class="carddd">
      <div class="type">❤ Playlist</div>
      <div class="title ellip">{{ props.info.name }}</div>
      <div class="desc">
        {{ props.info.desc[0] }}
      </div>
      <div class="duration">4 Tracks • 3 Hours</div>
      <div class="btns">
        <PlayBtnRect />
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
  background-image: url("../../assets/images/eggs.jpg");
  position: relative;
  margin-top: $small;
  border-radius: 0.75rem;
  color: $white;

  .last-updated {
    position: absolute;
    bottom: $small;
    right: $small;
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
    position: absolute;
    bottom: $small;
    left: $small;
    width: 25rem;
    padding: 1rem;
    background-color: rgba(5, 4, 4, 0.829);
    border-radius: .75rem;

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
      position: absolute;
      right: 1rem;
      bottom: 1rem;
      font-size: 0.8rem;
      color: $white;
      padding: $smaller;
      border: solid 1px $gray1;
      user-select: none;
      border-radius: $smaller;
    }

    .btns {
      margin-top: $small;
    }
  }
}
</style>
