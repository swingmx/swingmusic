<template>
  <div class="topnav">
    <div class="left">
      <div class="btn">
        <NavButtons />
      </div>

      <div class="info">
        <div
          class="title"
          v-show="$route.name == 'Playlists'"
          v-motion
          :initial="{
            opacity: 0,
            x: -20,
          }"
          :visible="{
            opacity: 1,
            x: 0,
            transition: {
              delay: 100,
            },
          }"
        >
          Playlists
        </div>
        <div
          class="folder"
          v-show="$route.name == 'FolderView'"
          v-motion
          :initial="{
            opacity: 0,
            x: -20,
          }"
          :visible="{
            opacity: 1,
            x: 0,
            transition: {
              delay: 100,
            },
          }"
        >
          <div class="fname">
            <div class="icon image"></div>
            <div class="paths">
              <!-- {{ $route.params.path.split("/").splice(-1)[0] }} -->
              <!-- {{ $route.params.path }} -->
              <div class="path" v-for="path in subPaths" :key="path.path">
                <span class="text">{{ path.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="center rounded">
      <Loader />
    </div>
    <div class="right">
      <div class="more image"></div>
      <Search />
    </div>
  </div>
</template>

<script setup lang="ts">
import NavButtons from "./NavButtons.vue";
import Loader from "../shared/Loader.vue";
import Search from "./Search.vue";
import { useRoute } from "vue-router";
import { onMounted, ref, watch } from "vue";
import { Routes } from "@/composables/enums";
import createSubPaths from "@/composables/createSubPaths";
import { subPath } from "@/interfaces";

const route = useRoute();

const subPaths = ref<subPath[]>();

function useSubRoutes() {
  watch(
    () => route.name,
    (newRoute: string) => {
      switch (newRoute) {
        case Routes.folder:
          console.log(newRoute);
          subPaths.value = createSubPaths(route.params.path);

          watch(
            () => route.params.path,
            (newPath) => {
              if (newPath == undefined) return;

              subPaths.value = createSubPaths(newPath);
            }
          );
          break;

        default:
          break;
      }
    }
  );
}

onMounted(() => {
  useSubRoutes();
});
</script>

<style lang="scss">
.topnav {
  display: grid;
  grid-template-columns: 1fr min-content max-content;
  padding-bottom: 1rem;
  margin: $small $small 0 $small;
  border-bottom: 1px solid $gray3;
  height: 3rem;

  .left {
    display: grid;
    grid-template-columns: max-content 1fr;

    .info {
      min-width: 15rem;

      .title {
        font-size: 1.5rem;
        font-weight: bold;
      }

      .folder {
        display: flex;
        gap: $small;

        .playbtnrect {
          height: 2.25rem;
        }

        .drop-btn {
          width: 2.25rem;

          .drop-icon {
            height: 2.25rem;
            width: 2.25rem;
          }
        }

        .fname {
          background-color: $gray4;
          border-radius: $small;
          height: 2.25rem;
          display: flex;
          align-items: center;
          margin-left: $smaller;
          overflow: auto;

          .icon {
            height: 2rem;
            aspect-ratio: 1;
            background-image: url("../../assets/icons/folder.fill.svg");
            background-size: 1.5rem;
            background-position: 75% 50%;
          }

          .paths {
            display: flex;
            gap: $smaller;
            overflow: auto;
            height: 100%;
            scrollbar-width: none;

            &::-webkit-scrollbar {
              display: none;
            }

            .path {
              white-space: nowrap;
              display: flex;
              align-items: center;
              cursor: default;

              .text {
                padding: $smaller;
                border-radius: $smaller;
              }

              &::before {
                content: "";
                height: $medium;
                margin-right: $smaller;
                border-right: solid 1px $white;
                transform: rotate(20deg);
              }

              &:first-child {
                &::before {
                  display: none;
                }
              }

              &:last-child {
                padding-right: $small;
              }

              &:hover {
                .text {
                  background-color: $gray;
                }
              }
            }
          }
        }
      }
    }
  }

  .center {
    display: grid;
    place-items: center;
    margin-right: 1rem;
  }

  .right {
    width: 100%;
    display: flex;
    gap: $small;

    .more {
      width: 2.25rem;
      aspect-ratio: 1;
      height: 100%;
      background-color: $gray5;
      background-image: url("../../assets/icons/more.svg");
      transform: rotate(90deg);
      border-radius: $small;
    }
  }
}
</style>
