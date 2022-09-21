<template>
  <div class="queue-view">
    <Layout :tracks="queue.tracklist">
      <template #header>
        <div>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Ab doloremque
          doloribus nostrum voluptas? Nobis ipsa cupiditate perspiciatis earum
          explicabo hic accusamus assumenda commodi, veritatis, nostrum nisi
          quod sequi exercitationem ducimus.Lorem ipsum dolor sit amet
          consectetur, adipisicing elit. Culpa facere recusandae dolorem sunt
          blanditiis natus delectus alias soluta facilis? Asperiores praesentium
          repellat magni rerum? Ratione reiciendis ut magni laborum itaque!
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Consequatur,
          ut. Iure ex nemo sunt. Nostrum, corporis! Asperiores omnis ducimus eum
          culpa quae nesciunt eius, soluta molestiae delectus quasi labore
          ex
          nemo sunt. Nostrum, corporis! Asperiores omnis ducimus eum culpa quae
          nesciunt eius, soluta molestiae delectus quasi labore ipsum! Lorem
          ipsum dolor sit amet consectetur adipisicing elit. Alias et ducimus
          consequuntur doloremque voluptate laboriosam, obcaecati eligendi!
          Mollitia cum, sint fuga facere sit minus modi quaerat quia nisi, earum
          ut! Lorem ipsum dolor sit amet consectetur adipisicing elit. Alias
          aliquam, sit laboriosam quidem minus ipsam consequatur deleniti
          architecto accusamus distinctio earum in suscipit eveniet temporibus
          obcaecati voluptas odit tenetur adipisci?
        </div>
      </template>
    </Layout>
  </div>
</template>

<script setup lang="ts">
import { computed, onUpdated, ref } from "vue";

import useQStore from "@/stores/queue";
import { onMounted } from "vue";
import SongItem from "@/components/shared/SongItem.vue";
import { useVirtualList } from "@vueuse/core";
import Layout from "@/layouts/HeaderAndVList.vue";

const queue = useQStore();
const height = ref(330);
const header = ref<HTMLElement>();
const source = computed(() => queue.tracklist);

// function playFromQueuePage(index: number) {
//   queue.play(index);
// }
// import SongList from "@/components/FolderView/SongList.vue";
// import { focusElem } from "@/utils";
</script>

<!-- <style lang="scss">
.queue-view {
}
</style> -->
