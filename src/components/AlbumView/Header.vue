<template>
  <div class="album-h">
    <div class="a-header rounded">
      <div class="art">
        <div
          class="image shadow-lg"
          :style="{
            backgroundImage: `url(&quot;${props.album.image}&quot;)`,
          }"
        ></div>
      </div>
      <div class="info">
        <div class="top">
          <div class="h">Album</div>
          <div class="title ellip">{{ props.album.album }}</div>
        </div>
        <div class="bottom">
          <div class="stats">
            {{ props.album.count }} Tracks •
            {{ perks.formatSeconds(props.album.duration, "long") }} •
            {{ props.album.date }} • {{ props.album.artist }}
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
  height: 16rem;
}

.a-header {
  display: grid;
  grid-template-columns: 15rem 1fr;
  padding: 1rem;
  height: 100%;
  background-color: $black;
background-color: #000000;
background-image: linear-gradient(147deg, #436a91 0%, #2c3e50 74%);
  .art {
    width: 100%;
    height: 100%;
    left: 1rem;
    display: flex;
    align-items: flex-end;

    .image {
      width: 14rem;
      height: 14rem;
    }
  }

  .info {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;

    .top {
      .h {
        color: #ffffffcb;
      }

      .title {
        font-size: 2.5rem;
        font-weight: 1000;
        color: white;
        text-transform: capitalize;
      }

      .artist {
        font-size: 1.15rem;
        color: #ffffffe0;
      }
    }

    .separator {
      width: 20rem;
    }

    .bottom {
      margin-top: $smaller;

      .stats {
        border-radius: $small;
        font-weight: bold;
        font-size: 0.8rem;
        margin-bottom: 0.75rem;
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
