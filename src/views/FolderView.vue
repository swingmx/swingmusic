<template>
  <div
    class="folder-view v-scroll-page"
    style="height: 100%"
    :class="{ isSmall, isMedium }"
  >
    <DynamicScroller
      :items="scrollerItems"
      :min-item-size="64"
      class="scroller"
      style="height: 100%"
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
import { isMedium, isSmall } from "@/stores/content-width";
import useLoaderStore from "@/stores/loader";
import useFolderStore from "@/stores/pages/folder";
import useQueueStore from "@/stores/queue";

import FolderList from "@/components/FolderView/FolderList.vue";
import SongItem from "@/components/shared/SongItem.vue";
import { createTrackProps } from "@/utils";

const loader = useLoaderStore();
const folder = useFolderStore();
const queue = useQueueStore();

interface ScrollerItem {
  id: string | number;
  component: typeof FolderList | typeof SongItem;
  props: any;
}

class songItem {
  id: number;
  props: any;
  component = SongItem;

  constructor(track: Track) {
    this.id = Math.random();
    this.props = createTrackProps(track)
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
// .folder-view {
//   background-color: $red;
//   padding-left: 0 !important;
// }
</style>
