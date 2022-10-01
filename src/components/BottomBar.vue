<template>
  <div class="b-bar">
    <div class="centered">
      <div class="inner">
        <div class="with-icons rounded-sm border">
          <!-- <button><PlusSvg /></button> -->
          <RouterLink
            title="go to album"
            :to="{
              name: Routes.album,
              params: {
                hash: queue.currenttrack?.albumhash || ' ',
              },
            }"
          >
            <img
              class="rounded-sm"
              :src="paths.images.thumb.small + queue.currenttrack?.image"
              alt=""
            />
          </RouterLink>
          <button><HeartSvg /></button>
        </div>

        <div class="info">
          <div class="with-title">
            <div class="time time-current">
              <span>
                {{ formatSeconds(queue.duration?.current) }}
              </span>
            </div>
            <div class="tags">
              <div v-tooltip class="title ellip">
                {{ queue.currenttrack?.title || "Hello there" }}
              </div>
              <ArtistName
                :artists="queue.currenttrack?.artist || []"
                :albumartist="
                  queue.currenttrack?.albumartist || 'Welcome to alice'
                "
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
        <div class="buttons rounded-sm border">
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

import HotKeys from "@/components/LeftSidebar/NP/HotKeys.vue";
import Progress from "@/components/LeftSidebar/NP/Progress.vue";
import ArtistName from "@/components/shared/ArtistName.vue";

import HeartSvg from "@/assets/icons/heart.svg";
// import PlusSvg from "@/assets/icons/plus.svg";

const queue = useQStore();
const settings = useSettingsStore();
</script>

<style lang="scss">
.b-bar {
  background-color: rgb(22, 22, 22);
  display: grid;
  align-items: center;
  z-index: 1;

  &:hover {
    ::-moz-range-thumb {
      height: 0.8rem;
    }

    ::-webkit-slider-thumb {
      height: 0.8rem;
    }

    ::-ms-thumb {
      height: 0.8rem;
    }
  }

  .centered {
    display: grid;
    align-items: center;
    width: max-content;
    padding: $small $medium;
    margin: 0 auto;

    .inner {
      display: grid;
      height: 3rem;
      grid-template-columns: max-content 1fr max-content;
      gap: 1rem;
      align-items: center;
    }

    .with-icons {
      background-color: rgba(255, 255, 255, 0.048);
      display: grid;
      gap: $small;
      grid-template-columns: repeat(3, max-content);
      align-items: center;
      padding: 0 5px;
      margin-top: -$smaller;

      button {
        height: 2rem;
        width: 2rem;
        background: transparent;
        padding: 0;

        &:last-child:hover {
          background: $red;
        }
      }
    }

    img {
      height: 2.75rem;
      width: 100%;
      aspect-ratio: 1;
      object-fit: cover;
      cursor: pointer;
      margin-top: $smaller;
    }

    .info {
      width: 30rem;

      .with-title {
        display: grid;
        grid-template-columns: max-content 1fr max-content;
        align-items: flex-end;
        gap: $smaller;
      }

      .time {
        font-size: $medium;
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
          font-size: $medium;
        }
      }
    }

    .buttons {
      height: 3.25rem;
      margin-top: -$smaller;
      background-color: rgba(255, 255, 255, 0.048);
      display: grid;
      place-items: center;
      padding: 0 $small;
    }
  }

  .right {
    display: grid;
    place-content: end;
  }
}
</style>
