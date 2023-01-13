<template>
  <div id="folder-nav-title">
    <div class="folder">
      <div class="fname-wrapper">
        <div class="fname">
          <div
            class="icon image"
            @click="
              $router.push({ name: Routes.folder, params: { path: '$home' } })
            "
          ></div>
          <div class="paths">
            <div
              class="path"
              v-for="path in subPaths.slice(1)"
              :key="path.path"
              :class="{ inthisfolder: path.active }"
            >
              <router-link
                class="text"
                :to="{ name: Routes.folder, params: { path: path.path } }"
                >{{ path.name }}</router-link
              >
            </div>
          </div>
        </div>
      </div>
      <SearchInput :page="Routes.folder" />
      <!-- <div>
      </div> -->
    </div>
  </div>
</template>

<script setup lang="ts">
import SearchInput from "@/components/shared/NavSearchInput.vue";
import { subPath } from "@/interfaces";
import { Routes } from "@/router/routes";
import { focusElemByClass } from "@/utils";
import { onUpdated } from "vue";

defineProps<{
  subPaths: subPath[];
}>();

onUpdated(() => {
  focusElemByClass("inthisfolder");
});
</script>

<style lang="scss">
#folder-nav-title {
  width: 100%;

  .folder {
    display: grid;
    grid-template-columns: 1fr max-content;

    .fname-wrapper {
      width: 100%;
      overflow: hidden;
    }

    .fname {
      background-color: $gray4;
      border-radius: $small;
      height: 2.25rem;
      display: flex;
      align-items: center;
      padding-right: $smaller;
      width: fit-content;
      max-width: 100%;
      overflow: scroll;
      scrollbar-width: none;

      &::-webkit-scrollbar {
        display: none;
      }

      .icon {
        height: 2rem;
        aspect-ratio: 1;
        background-image: url("../../../assets/icons/folder.fill.svg");
        background-size: 1.5rem;
        margin-left: $smaller;
      }

      .paths {
        display: flex;
        gap: $smaller;

        &::-webkit-scrollbar {
          display: none;
        }

        .path {
          white-space: nowrap;
          margin: auto 0;

          .text {
            padding: $smaller;
            border-radius: $smaller;
          }

          &::before {
            content: "∕";
            margin-right: $smaller;
            color: $gray2;
            font-size: 1rem;
          }

          &:first-child {
            display: none;
          }

          &:last-child {
            padding-right: $smaller;
          }

          &:hover {
            .text {
              background-color: $gray;
            }
          }
        }

        .inthisfolder > .text {
          background-color: $gray;
          transition: all 0.5s;
        }
      }
    }
  }
}
</style>
