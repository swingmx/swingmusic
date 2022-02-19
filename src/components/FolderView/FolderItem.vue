<template>
  <router-link
    :to="{ name: 'FolderView', params: { path: props.folder.path } }"
  >
    <div class="f-item">
      <div class="icon image"></div>
      <div class="info">
        <div class="f-item-text ellip">{{ props.folder.name }}</div>
        <div class="separator no-border"></div>
        <div class="f-item-count">{{ props.folder.count }} tracks</div>
      </div>
    </div>
  </router-link>
</template>

<script setup>
const props = defineProps({
  folder: {
    type: Object,
    required: true,
  },
});
</script>

<style lang="scss">
.f-container .f-item {
  height: 5rem;
  display: flex;
  align-items: center;
  position: relative;
  background-color: #ffffff09;
  transition: all 0.2s ease;
  border-radius: .75rem;

  @include phone-only {
    height: 4rem;
  }

  .icon {
    background-image: url(../../assets/icons/folder.svg);
    width: 2rem;
    height: 1.5rem;
    margin-right: 1rem;
    margin-left: 1rem;
  }

  .info {
    width: 100%;

    .f-item-count {
      font-size: 0.8rem;
      color: rgba(219, 217, 217, 0.63);
    }

    .f-item-text {
      text-align: left;
    }
  }

  &:hover {
    background: #0575e6; /* fallback for old browsers */
    background: linear-gradient(
      to top right,
      #021b79,
      #0575e6
    ); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    background-size: 105% 105%;
    background-position-x: -$small;

    .f-item-count {
      color: #ffffff;
    }
  }
}
</style>
