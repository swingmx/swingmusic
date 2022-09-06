<template>
  <div class="nav-queue-title">
    <div class="first noscroll">
      <router-link :to="(getSourceUrlParams())">
        <button>Go to source</button>
      </router-link>
      <div class="playing-from">
        <div class="border rounded-sm pad-sm">
          <b class="ellip">{{ getSourceName() }}</b>
        </div>
      </div>
    </div>
    <QueueActions />
  </div>
</template>

<script setup lang="ts">
import QueueActions from "@/components/RightSideBar/Queue/QueueActions.vue";
import { FromOptions, Routes } from "@/composables/enums";
import useQueueStore from "@/stores/queue";
import { RouteLocationRaw, RouteRecordRaw } from "vue-router";

const queue = useQueueStore();

const { from: source } = queue;

function getSourceName(): RouteLocationRaw {
  switch (source.type) {
    case FromOptions.album:
      return source.name;

    case FromOptions.folder:
      return source.name;

    case FromOptions.playlist:
      return source.name;

    case FromOptions.search:
      return `Search for: "${source.query}"`;

    default:
      return "Ghost source";
  }
}

function getSourceUrlParams() {
  switch (source.type) {
    case FromOptions.album:
      return {
        name: Routes.album,
        params: {
          hash: source.hash,
        },
      };
    case FromOptions.folder:
      return {
        name: Routes.folder,
        params: {
          path: source.path,
        },
      };
    case FromOptions.playlist:
      return {
        name: Routes.playlist,
        params: {
          pid: source.playlistid,
        },
      };
    case FromOptions.search:
      return {
        name: Routes.search,
        params: {
          query: source.query,
        },
      };

    default:
      return "/";
  }
}

</script>

<style lang="scss">
.nav-queue-title {
  display: grid;
  grid-template-columns: 1fr max-content;
  gap: 1rem;
  align-items: center;

  .first {
    width: 100%;
    display: grid;
    grid-template-columns: max-content 1fr;
    gap: 1rem;

    .playing-from {
      display: flex;
      align-items: center;
      gap: $small;
      opacity: 0.75;
    }

    button {
      cursor: pointer;
    }
  }

  .queue-actions {
    margin: 0;
  }
}
</style>
