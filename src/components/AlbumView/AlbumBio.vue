<template>
  <div class="al-bio rounded">
    <div class="separator" id="av-sep"></div>
    <div class="grid albumbio">
      <div class="left rounded">
        <img
          class="rect rounded"
          :src="paths.images.thumb + images.album"
          alt=""
        />
        <div class="circle"></div>
        <img class="circle" :src="paths.images.artist + images.artist" alt="" />
      </div>
      <div class="bio rounded border" v-html="bio" v-if="bio"></div>
      <div class="bio rounded border" v-else>No bio found</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { paths } from "@/config";

defineProps<{
  bio: string;
  images: {
    artist: string;
    album: string;
  };
}>();
</script>

<style lang="scss">
.al-bio {
  padding: $small;

  .albumbio {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: $small;
    min-height: 15rem;
  }

  @include tablet-portrait {
    grid-template-columns: 1fr;
  }

  @include tablet-landscape {
    grid-template-columns: 1fr auto;
  }

  .left {
    position: relative;
    height: 100%;
    width: 100%;
    margin-right: $small;
    overflow: hidden;
    border: solid 1px $gray5;
    background-image: linear-gradient(37deg, $gray5 20%, $gray4);

    @include tablet-portrait {
      display: none;
    }

    @include tablet-landscape {
      width: 10rem;
    }

    .rect {
      width: 10rem;
      height: 10rem;
      position: absolute;
      bottom: 0rem;
      left: 7rem;
      transform: rotate(15deg) translate(-1rem, 1rem);
      z-index: 1;
      transition: all 0.5s ease-in-out;

      &:hover {
        transform: rotate(0deg) translate(-1rem, 0) scale(1.1);
        transition: all 0.5s ease-in-out;
      }
    }

    .circle {
      position: absolute;
      width: 7rem;
      height: 7rem;
      left: 15rem;
      bottom: 0;
      border-radius: 50%;
      box-shadow: 0 0 2rem rgb(0, 0, 0);
      transition: all 0.25s ease-in-out;

      &:hover {
        transform: scale(1.5);
      }
    }
  }
  .bio {
    border: solid 1px $gray5;
    padding: $small;
    line-height: 1.5rem;

    &::after {
      content: " ...";
    }
  }
}
</style>
