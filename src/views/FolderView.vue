<template>
  <div class="folder-view v-scroll-page">
    <DynamicScroller
      :items="scrollerItems"
      :min-item-size="64"
      class="scroller"
    >
      <template v-slot="{ item, index, active }">
        <DynamicScrollerItem
          :item="item"
          :active="active"
          :size-dependencies="[item.props]"
          :data-index="index"
        >
          <component
            :key="index"
            :is="item.component"
            v-bind="item.props"
            @playThis="playFromPage(item.props.index - 1)"
          ></component>
        </DynamicScrollerItem>
      </template>
    </DynamicScroller>
  </div>
</template>

<script setup lang="ts">
import { computed } from "@vue/reactivity";
import { onBeforeRouteLeave, onBeforeRouteUpdate } from "vue-router";

import { Track } from "@/interfaces";
import useQueueStore from "@/stores/queue";
import useLoaderStore from "@/stores/loader";
import useFolderStore from "@/stores/pages/folder";

import SongItem from "@/components/shared/SongItem.vue";
import FolderList from "@/components/FolderView/FolderList.vue";

const loader = useLoaderStore();
const folder = useFolderStore();
const queue = useQueueStore();

interface ScrollerItem {
  id: string;
  component: typeof FolderList | typeof SongItem;
  props: any;
}

class songItem {
  id: string;
  component = SongItem;
  props: any;

  constructor(track: Track) {
    this.id = track.trackid;
    this.props = {
      track,
      index: track.index + 1,
      isCurrent: queue.currenttrack?.hash === track.hash,
      isCurrentPlaying:
        queue.currenttrack?.hash === track.hash && queue.playing,
    };
  }
}

const scrollerItems = computed(() => {
  const items: ScrollerItem[] = [];

  if (folder.dirs.length) {
    items.push({
      id: "folder-list",
      component: FolderList,
      props: {
        folders: folder.dirs,
      },
    });
  }

  folder.tracks.forEach((track) => {
    items.push(new songItem(track));
  });

  return items;
});

function playFromPage(index: number) {
  queue.playFromFolder(folder.path, folder.allTracks);
  queue.play(index);
}

onBeforeRouteUpdate((to, from) => {
  loader.startLoading();
  folder
    .fetchAll(to.params.path as string)

    .then(() => {
      folder.resetQuery();
    })
    .then(() => {
      loader.stopLoading();
    });
});

onBeforeRouteLeave(() => {
  setTimeout(() => folder.resetQuery(), 500);
});
</script>

<style lang="scss">
.folder-view {
  height: 100%;

  .scroller {
    height: 100%;
    padding-bottom: $content-padding-bottom !important;
  }
}
</style>
