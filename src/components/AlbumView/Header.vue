<template>
  <div class="album-h">
    <div class="a-header rounded">
      <div class="info">
        <div class="top">
          <div class="h">Album</div>
          <div class="separator no-border"></div>
          <div class="title">{{ album_info.name }}</div>
          <div class="artist">{{ album_info.artist }}</div>
        </div>
        <div class="separator no-border"></div>
        <div class="bottom">
          <div class="stats">
            {{ album_info.count }} Tracks • {{ album_info.duration }} • 2021
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

<script>
import state from "@/composables/state.js";
import perks from "@/composables/perks.js";

export default {
  props: ["album_info"],
  setup() {
    function playAlbum() {
      perks.updateQueue(state.album_song_list.value[0], "album");
    }

    return {
      playAlbum,
    };
  },
};
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
  background-image: url("../../assets/images/abg.webp");
  background-position: 0% 60%;
  background-repeat: no-repeat;
  background-size: cover;

  .info {
    width: 100%;
    height: calc(100%);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;

    .top {
      .h {
        color: rgba(255, 255, 255, 0.795);
      }
      .title {
        font-size: 2rem;
        font-weight: 1000;
        color: white;
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
      .stats {
        font-weight: bold;
        display: none;
      }

      .play {
        height: 2.5rem;
        width: 6rem;
        display: flex;
        align-items: center;
        background: $highlight-blue;
        padding: $small;
        margin: $small 0;
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
