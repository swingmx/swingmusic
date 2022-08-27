<template>
  <div id="folder-nav-title">
    <div class="folder">
      <div class="fname">
        <div class="icon image"></div>
        <div class="paths">
          <div
            class="path"
            v-for="path in subPaths"
            :key="path.path"
            :class="{ inthisfolder: path.active }"
            @click="
              $router.push({ name: 'FolderView', params: { path: path.path } })
            "
          >
            <span class="text">{{ path.name }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { focusElem } from "@/utils";
import { subPath } from "@/interfaces";
import { onUpdated } from "vue";

defineProps<{
  subPaths: subPath[];
}>();

onUpdated(() => {
  focusElem("inthisfolder");
});
</script>

<style lang="scss">
#folder-nav-title {
  overflow: hidden;
  width: 100%;

  .folder {
    display: flex;
    gap: $small;
    width: inherit;

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
      width: 100%;
      overflow: auto;
      padding-right: $smaller;

      .icon {
        height: 2rem;
        aspect-ratio: 1;
        background-image: url("../../../assets/icons/folder.fill.svg");
        background-size: 1.5rem;
        margin-left: $smaller;
        background-position: 65% 50%;
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
          margin: auto 0;
          cursor: default;

          .text {
            padding: $smaller;
            border-radius: $smaller;
          }

          &::before {
            content: "/";
            font-size: small;
            margin-right: $smaller;
            opacity: .25;
          }

          &:first-child {
            &::before {
              display: none;
            }
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
          color: #fff;
          font-weight: bold;
          background-color: $gray;

          transition: all 0.5s;
        }
      }
    }
  }
}
</style>
