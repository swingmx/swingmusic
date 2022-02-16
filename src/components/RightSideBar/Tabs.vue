<template>
  <div class="r-tabs">
    <div v-for="tab in props.tabs"
         @click="changeTab(tab)"
         :key="tab"
         class="image t-item"
         :class="{ active_tab: props.current_tab === tab }, `${tab}`"
    ></div>
    <div>
    </div>
  </div>
</template>

<script setup>

const props = defineProps({
  current_tab: String,
  tabs: Object,
});

const emit = defineEmits(['changeTab'])

function changeTab(tab) {
  if (tab === props.current_tab) return;

  emit('changeTab', tab)
}

</script>

<style lang="scss">
.r-tabs {
  display: flex;
  flex-direction: column;
  gap: $small;
  margin-top: $small;
  margin-left: $small;

  .t-item {
    float: right;
    width: 100%;
    height: 2.45rem;
    background-size: 1.5rem;
    border-radius: $small 0 0 $small;

    &:hover {
      background-color: rgba(128, 128, 128, 0.281);
    }
  }

  .active_tab {
    border-right: solid;
    background-color: rgba(17, 123, 223, 0.192);
  }

  .search {
    background-image: url("../../assets/icons/search.svg");
    // background-color: rgba(35, 35, 66, 0.247);
  }

  .queue {
    background-image: url("../../assets/icons/queue.svg");
    // background-color: rgba(46, 25, 33, 0.445);
  }

  .home {
    background-image: url("../../assets/icons/dashboard.svg");
    // background-color: rgba(148, 102, 50, 0.445);
  }
}
</style>
