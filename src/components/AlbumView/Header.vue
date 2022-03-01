<template>
  <div class="album-h">
    <div class="a-header rounded">
      <div
        class="image art shadow-lg"
        :style="{ backgroundImage: `url(&quot;${encodeURI(props.album_info.image)}&quot;)` }"
      ></div>
      <div class="info">
        <div class="top">
          <div class="h">Album</div>
          <div class="separator no-border"></div>
          <div class="title">{{ props.album_info.name }}</div>
          <div class="artist">{{ props.album_info.artist }}</div>
        </div>
        <div class="separator no-border"></div>
        <div class="bottom">
          <div class="stats shadow-sm">
            {{ props.album_info.count }} Tracks • {{ props.album_info.duration }} •
            {{ props.album_info.date }}
          </div>
          <div class="play rounded" @click="playAlbum">
            <div class="icon"></div>
            <div>Play</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import state from "@/composables/state.js";
import perks from "@/composables/perks.js";

const props = defineProps({
  album_info: {
    type: Object,
    default: () => ({}),
  },
});

function playAlbum() {
  perks.updateQueue(state.album.tracklist[0], "album");
}
</script>

<style lang="scss">
.album-h {
  @include tablet-landscape {
    grid-template-columns: 1fr;
  }

  gap: $small;
  position: relative;
  overflow: hidden;
  height: 14rem;
}

.a-header {
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  padding: 1rem;
  height: 100%;
  background-image: linear-gradient(
    56deg,
    $gray 0%,
    $gray4 25%,
    $gray1 50%,
    $gray1 75%,
    $gray 100%
  );
  background-position: 0% 60%;
  background-repeat: no-repeat;
  background-size: cover;

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
        background-color: $gray;
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
        background: $highlight-blue;
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
