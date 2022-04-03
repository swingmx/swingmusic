<template>
  <div class="album-h">
    <div class="a-header rounded">
      <div
        class="image art shadow-lg rounded"
        :style="{
          backgroundImage: `url(&quot;${props.album.image}&quot;)`,
        }"
      ></div>
      <div class="info">
        <div class="top">
          <div class="h">Album</div>
          <div class="separator no-border"></div>
          <div class="title">{{ props.album.album }}</div>
          <div class="artist">{{ props.album.artist }}</div>
        </div>
        <div class="separator no-border"></div>
        <div class="bottom">
          <div class="stats shadow-sm">
            {{ props.album.count }} Tracks •
            {{ perks.formatSeconds(props.album.duration, "long") }} •
            {{ props.album.date }}
          </div>
          <PlayBtnRect :source="playSources.album" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import perks from "../../composables/perks.js";
import { AlbumInfo } from "../../interfaces.js";
import PlayBtnRect from "../shared/PlayBtnRect.vue";
import { playSources } from "../../composables/enums";
const props = defineProps<{
  album: AlbumInfo;
}>();
</script>

<style lang="scss">
.album-h {
  height: 14rem;
}

.a-header {
  position: relative;
  display: flex;
  align-items: center;
  padding: 1rem;
  height: 100%;
  background-color: $gray4;
  background-image: linear-gradient(
    to bottom,
    $gray3 0%,
    $gray3 25%,
    $gray3 35%,
    $gray4 50%,
    $gray 75%,
    $black 100%
  );

  .art {
    position: absolute;
    width: 12rem;
    height: 12rem;
    left: 1rem;
  }

  .info {
    width: 100%;
    height: calc(100%);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    margin-left: 13rem;

    .top {
      .h {
        color: #ffffffcb;
      }
      .title {
        font-size: 2rem;
        font-weight: 1000;
        color: white;
        text-transform: capitalize;
      }

      .artist {
        margin-top: $small;
        font-size: 1.5rem;
        color: #fffffff1;
      }
    }

    .separator {
      width: 20rem;
    }

    .bottom {
      position: relative;

      .stats {
        background-color: $red;
        padding: $small;
        border-radius: $small;
        position: absolute;
        right: 0;
        bottom: 0;
        font-weight: bold;
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
