<template>
  <div
    class="artist-page v-scroll-page"
    style="height: 100%"
    :class="{ isSmall, isMedium }"
  >
    <RecycleScroller
      class="scroller"
      :items="scrollerItems"
      :item-size="null"
      key-field="id"
      v-slot="{ item }"
      style="height: 100%"
    >
      <component :is="item.component" v-bind="item.props" />
    </RecycleScroller>
  </div>
</template>

<script setup lang="ts">
import { isMedium, isSmall } from "@/stores/content-width";

import Header from "@/components/ArtistView/Header.vue";
import { computed } from "vue";

interface ScrollerItem {
  id: string | number;
  component: typeof Header;
  // props: Record<string, unknown>;
  size: number;
}

const header: ScrollerItem = {
  id: "artist-header",
  component: Header,
  size: 19 * 16,
};

const scrollerItems = computed(() => {
  return [header];
});
</script>

<style lang="scss">
.artist-page {
  border: solid 1px;

}
</style>
