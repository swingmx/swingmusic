<template>
  <div class="a-header rounded">
    <div class="art rounded"></div>
    <div class="info">
      <div class="top">
        <div class="title">{{ album.title }}</div>
        <div class="artist">{{ album.artist }}</div>
      </div>
      <div class="separator"></div>
      <div class="bottom">
        <div class="stats">
          {{ album.count }} Tracks • {{ album.duration }} • {{ album.date }}
        </div>
        <div class="play rounded">
          <div class="icon"></div>
          <div>Play</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "@vue/reactivity";

export default {
  setup() {
    const album = ref({
      title: "Fighting Demons",
      artist: "Juice Wrld",
      count: 17,
      duration: "54 min",
      date: 2021,
    });

    return {
      album,
    };
  },
};
</script>

<style lang="scss">
.a-header {
  height: 14rem;
  background: rgb(0, 0, 0);
  display: flex;
  align-items: center;
  padding: 0 1rem 0 1rem;

  .art {
    width: 12rem;
    height: 12rem;
    background: no-repeat center/cover url(../../assets/images/jw.jpeg);
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
        font-size: 2rem;
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
        background: rgb(33, 145, 61);
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