<template>
  <div class="b-bar">
    <div class="centered">
      <div class="inner">
        <RouterLink
          title="go to album"
          :to="{
            name: Routes.album,
            params: {
              hash: queue.currenttrack.albumhash,
            },
          }"
        >
          <img
            class="rounded-sm"
            :src="paths.images.thumb.small + queue.currenttrack.image"
            alt=""
          />
        </RouterLink>

        <div class="info">
          <div class="with-title">
            <div class="time time-current">
              <span>
                {{ formatSeconds(queue.duration.current) }}
              </span>
            </div>
            <div class="tags">
              <div class="title ellip">
                {{ queue.currenttrack.title }}
              </div>
              <ArtistName
                :artists="queue.currenttrack.artist"
                :albumartist="queue.currenttrack.albumartist"
                class="artist"
              />
            </div>
            <div class="time time-full">
              <span>
                {{
                  formatSeconds(
                    queue.currenttrack ? queue.currenttrack.duration : 0
                  )
                }}
              </span>
            </div>
          </div>

          <Progress />
        </div>
        <div class="buttons">
          <HotKeys />
        </div>
      </div>
      <div class=""></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { paths } from "@/config";
import useQStore from "@/stores/queue";
import { formatSeconds } from "@/utils";

import { Routes } from "@/composables/enums";
import useSettingsStore from "@/stores/settings";

import ArtistName from "../shared/ArtistName.vue";
import HotKeys from "../LeftSidebar/NP/HotKeys.vue";
import Progress from "../LeftSidebar/NP/Progress.vue";

const queue = useQStore();
const settings = useSettingsStore();
</script>

<style lang="scss">
.b-bar {
  height: 65px;
  background-color: rgb(22, 22, 22);
  display: grid;
  align-items: center;
  z-index: 1;
  border-top: solid 1px $gray3;

  .centered {
    width: 50rem;
    display: grid;
    align-items: center;

    .inner {
      display: grid;
      height: 3rem;
      grid-template-columns: max-content 1fr max-content;
      gap: 1rem;
      align-items: center;
    }

    // background-color: $gray5;
    width: max-content;
    padding: $small $medium;
    margin: 0 auto;

    img {
      height: 2.75rem;
      width: 100%;
      aspect-ratio: 1;
      object-fit: cover;
      cursor: pointer;
    }

    .info {
      width: 30rem;
      // width: 100%;

      .with-title {
        display: grid;
        grid-template-columns: max-content 1fr max-content;
        align-items: flex-end;
        gap: $smaller;
      }

      .time {
        font-size: 12px;
        height: fit-content;
        width: 3rem;

        span {
          background-color: $gray3;
          border-radius: $smaller;
          padding: 0 $smaller;
        }
      }

      .time-full {
        text-align: end;
      }

      .tags {
        font-size: small;
        display: grid;
        grid-template-rows: 1fr 1fr;
        place-items: center;

        .title {
          font-weight: bold;
        }

        .artist {
          opacity: 0.75;
          margin-bottom: -$smaller;
          font-size: 12px;
        }
      }
    }

    .buttons {
      width: 9rem;
    }
  }
  // width: 100%;

  // .time {
  //   display: grid;
  //   grid-template-columns: repeat(3, 1fr);
  //   align-items: center;

  //   .full {
  //     text-align: end;
  //   }
  // }

  // .info {
  //   display: grid;
  //   grid-template-columns: max-content 1fr;
  //   gap: 1rem;

  //   img {
  //     height: 6rem;
  //     width: auto;
  //   }

  //   .tags {
  //     display: flex;
  //     flex-direction: column;
  //     justify-content: flex-end;
  //     gap: $smaller;

  //     .np-title {
  //       font-size: 1.15rem;
  //       font-weight: bold;
  //     }

  //     .np-artist {
  //       opacity: 0.75;
  //       font-size: 0.9rem;
  //     }
  //   }
  // }
}
</style>
