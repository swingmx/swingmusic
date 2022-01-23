<template>
  <div class="options" v-if="magic_flag">
    <div class="item info">Filter by:</div>
    <div
      class="item"
      v-for="option in options"
      :key="option"
      @click="addFilter(option.icon)"
    >
      {{ option.title }}
    </div>
  </div>
</template>

<script>
export default {
  props: ["magic_flag"],
  setup(props, { emit }) {
    const options = [
      {
        title: "🎵 Track",
        icon: "🎵",
      },
      {
        title: "💿 Album",
        icon: "💿",
      },
      {
        title: "🙄 Artist",
        icon: "🙄",
      },
      {
        title: "😍 Playlist",
        icon: "😍",
      },
      {
        title: "📁 Folder",
        icon: "📁",
      },
    ];

    function addFilter(value) {
      emit("addFilter", value);
    }

    return {
      options,
      addFilter,
    };
  },
};
</script>

<style lang="scss">
.right-search .options {
  display: flex;

  .item {
    margin: $small;
  }
}
</style>