<template>
  <div class="queue-view">
    <div
      v-bind="containerProps"
      style="height: calc(100vh - 4.25rem)"
      :style="{ paddingTop: height - 64 + 16 + 'px' }"
      @scroll="handleScroll"
    >
      <div v-bind="wrapperProps">
        <div class="header rounded pad-sm" style="height: 64px">
          <div ref="header" :style="{ top: -height + 64 - 16 + 'px' }">
            Lorem ipsum dolor sit amet consectetur, adipisicing elit. Culpa
            facere recusandae dolorem sunt blanditiis natus delectus alias
            soluta facilis? Asperiores praesentium repellat magni rerum? Ratione
            reiciendis ut magni laborum itaque! Lorem ipsum dolor sit amet
            consectetur adipisicing elit. Consequatur, ut. Iure ex nemo sunt.
            Nostrum, corporis! Asperiores omnis ducimus eum culpa quae nesciunt
            eius, soluta molestiae delectus quasi labore ipsum! Lorem ipsum
            dolor sit amet consectetur adipisicing elit. Alias et ducimus
            consequuntur doloremque voluptate laboriosam, obcaecati eligendi!
            Mollitia cum, sint fuga facere sit minus modi quaerat quia nisi,
            earum ut! Lorem ipsum dolor sit amet consectetur adipisicing elit.
            Alias aliquam, sit laboriosam quidem minus ipsam consequatur
            deleniti architecto accusamus distinctio earum in suscipit eveniet
            temporibus obcaecati voluptas odit tenetur adipisci?Lorem ipsum
            dolor sit amet consectetur, adipisicing elit. Culpa facere
            recusandae dolorem sunt blanditiis natus delectus alias soluta
            facilis? Asperiores praesentium repellat magni rerum? Ratione
            reiciendis ut magni laborum itaque! Lorem ipsum dolor sit amet
            consectetur adipisicing elit. Consequatur, ut. Iure ex nemo sunt.
            Nostrum, corporis! Asperiores omnis ducimus eum culpa quae nesciunt
            eius, soluta molestiae delectus quasi labore ipsum! Lorem ipsum
            dolor sit amet consectetur adipisicing elit. Alias et ducimus
            consequuntur doloremque voluptate laboriosam, obcaecati eligendi!
            Mollitia cum, sint fuga facere sit minus modi quaerat quia nisi,
            earum ut! Lorem ipsum dolor sit amet consectetur adipisicing elit.
            Alias aliquam, sit laboriosam quidem minus ipsam consequatur
            deleniti architecto accusamus distinctio earum in suscipit eveniet
            temporibus obcaecati voluptas odit tenetur adipisci?Lorem ipsum
            dolor sit amet consectetur, adipisicing elit. Culpa facere
            recusandae dolorem sunt blanditiis natus delectus alias soluta
            facilis? Asperiores praesentium repellat magni rerum? Ratione
            reiciendis ut magni laborum itaque! Lorem ipsum dolor sit amet
            consectetur adipisicing elit. Consequatur, ut. Iure ex nemo sunt.
            Nostrum, corporis! Asperiores omnis ducimus eum culpa quae nesciunt
            eius, soluta molestiae delectus quasi labore ipsum! Lorem ipsum
            dolor sit amet consectetur adipisicing elit. Alias et ducimus
            consequuntur doloremque voluptate laboriosam, obcaecati eligendi!
            Mollitia cum, sint fuga facere sit minus modi quaerat quia nisi,
            earum ut! Lorem ipsum dolor sit amet consectetur adipisicing elit.
            Alias aliquam, sit laboriosam quidem minus ipsam consequatur
            deleniti architecto accusamus distinctio earum in suscipit eveniet
            temporibus obcaecati voluptas odit tenetur adipisci?
          </div>
        </div>
        <SongItem
          style="height: 60px"
          v-for="(t, index) in tracks"
          :key="t.data.trackid"
          :track="t.data"
          :index="0"
          :isPlaying="queue.playing"
          :isCurrent="queue.currentid == t.data.trackid"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";

import useQStore from "@/stores/queue";
import { focusElem } from "@/utils";
import SongList from "@/components/FolderView/SongList.vue";
import { onMounted } from "vue";
import SongItem from "@/components/shared/SongItem.vue";
import { useVirtualList } from "@vueuse/core";

const queue = useQStore();
const height = ref(330);

function playFromQueuePage(index: number) {
  queue.play(index);
}

const header = ref<HTMLElement>();
onMounted(() => {
  height.value = header.value.offsetHeight;
  console.log(height.value);
  // height.value = 370;
});
const source = computed(() => queue.tracklist);
function handleScroll(e: Event) {
  // check if header is visible
  const headerHeight = header.value?.offsetHeight || 0;
  const scrollTop = (e.target as HTMLElement).scrollTop;

  if (scrollTop > headerHeight) {
    // console.log("header is not visible");
    header.value.style.opacity = "0";
  } else {
    // console.log("header is visible");
    header.value.style.opacity = "1";
  }
}

const {
  list: tracks,
  containerProps,
  wrapperProps,
  scrollTo,
} = useVirtualList(source, {
  itemHeight: 60,
  overscan: 15,
});
</script>

<style lang="scss">
.queue-view {
  .header {
    // background-color: $gray3;
    // margin-bottom: 2rem;
    position: relative;
    overflow: visible;

    div {
      position: absolute;
      top: -25rem;
    }
  }
}
</style>
