<template>
  <div class="album-h">
    <div class="a-header rounded card-dark border">
      <div
          :style="{
          backgroundImage: `url(&quot;${album_info.image}&quot;)`,
        }"
          class="art rounded border"
      ></div>
      <div class="info">
        <div class="top">
          <div class="title">{{ album_info.name }}</div>
          <div class="artist">{{ album_info.artist }}</div>
        </div>
        <div class="separator no-border"></div>
        <div class="bottom">
          <div class="stats">
            {{ album_info.count }} Tracks • {{ album_info.duration }} • 2021
          </div>
          <button class="play rounded" @click="playAlbum">
            <div class="icon"></div>
            <div>Play</div>
          </button>
        </div>
      </div>
    </div>
    <div class="right rounded card-dark border">
      <div class="circle circular"></div>
      <div class="rect rounded"></div>
      <div
          :style="{
          backgroundImage: `url(&quot;${album_info.artist_image}&quot;)`,
        }"
          class="avatar image"
      ></div>
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
  display: grid;
  grid-template-columns: 1fr 1fr;

  @include tablet-landscape {
    grid-template-columns: 1fr;
  }

  gap: $small;
  position: relative;
  overflow: hidden;
  height: 14rem;

  .right {
    @include tablet-landscape {
      display: none;
    }

    padding: $small;
    position: relative;

    .avatar {
      height: 8rem;
      width: 8rem;
      border-radius: 50%;
      background-image: url("../../assets/images/null.webp");
      position: absolute;
      left: -4.2rem;
      top: 3rem;
      box-shadow: 0px 0px 1.5rem rgb(0, 0, 0);
    }

    .rect {
      width: 20rem;
      height: 10rem;
      position: absolute;
      right: 0;
      background-color: rgb(196, 58, 58);
      transform: rotate(-45deg) translate(20%, -50%);
      z-index: 1;
      box-shadow: 0px 0px 2rem rgb(0, 0, 0);
      transition: all 0.5s ease-in-out;

      &:hover {
        transition: all 0.5s ease-in-out;

        right: 2rem;
      }
    }

    .circle {
      width: 7rem;
      height: 7rem;
      position: absolute;
      right: 0;
      background-color: $blue;
      border-radius: 50%;
      transform: translateX(-11rem) translateY(7rem);
      box-shadow: 0px 0px 2rem rgba(0, 0, 0, 0.164);
      transition: all 0.5s ease-in-out;

      &:hover {
        transition: all 0.5s ease-in-out;

        right: 1rem;
      }
    }

    &:hover {
      transition: all 0.5s ease-in-out;

      .circle {
        border-radius: 0;
        transform: translateX(-11rem) translateY(7rem) rotate(360deg);
      }

      .rect {
        border-radius: 0;
        transform: translate(20%, -50%) rotate(360deg);
      }
    }
  }
}

.a-header {
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  padding: 0 1rem 0 1rem;

  .art {
    width: 14rem;
    height: 13rem;
    background: no-repeat center/cover;
    margin-right: 1rem;
  }

  .info {
    width: calc(100% - 13rem);
    height: calc(100% - 1rem);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;

    .top {
      .title {
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
      }

      .artist {
        margin-top: $small;

        color: rgba(255, 255, 255, 0.856);
      }
    }

    .separator {
      width: 20rem;
    }

    .bottom {
      .stats {
        font-weight: bold;
      }

      .play {
        height: 2.5rem;
        width: 6rem;
        display: flex;
        align-items: center;
        background: $blue;
        padding: $small;
        margin: $small 0;

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