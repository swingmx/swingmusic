<template>
  <div class="r-tabs">
    <button v-for="tab in props.tabs"
    @click="changeTab(tab)"
    :key="tab"
      class="image t-item rounded"
      :class="{ active_tab: props.current_tab == tab }, `${tab}`"
    ></button>
    <div>
    </div>
  </div>
</template>

<script setup>import { onMounted } from 'vue';

const props = defineProps({
  current_tab: String,
  tabs: Object,
});

const emit = defineEmits(['changeTab'])

function changeTab(tab) {
  if (tab == props.current_tab) return;

  emit('changeTab', tab)
}

</script>

<style lang="scss">
.r-tabs {
  display: flex;
  flex-direction: column;
  gap: $small;

  .t-item {
    width: 2rem;
    height: 2rem;
    background-size: 1.5rem;
  }

  .active_tab {
    border-right: solid;
    border-radius: $small 0 0 $small;
  }

  .search {
    background-image: url("../../assets/icons/search.svg");
    background-color: rgba(35, 35, 66, 0.247);
  }

  .queue {
    background-image: url("../../assets/icons/queue.svg");
    background-color: rgba(46, 25, 33, 0.445);
  }

  .home {
    background-image: url("../../assets/icons/dashboard.svg");
    background-color: rgba(148, 102, 50, 0.445);
  }
}
</style>
