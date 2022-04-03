<template>
  <div class="folder-top flex">
    <div class="fname">
      <button class="play image">
        <div class="icon"></div>
        Play
      </button>
      <div class="text">
        <div class="icon image"></div>
        <div class="ellip">
          {{ folder.path.split("/").splice(-1).join("") }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import useFStore from "../../stores/folder";

const folder = useFStore();
</script>

<style lang="scss">
.folder-top {
  border-bottom: 1px solid $separator;
  width: calc(100% - 0.5rem);
  padding-bottom: $small;
  height: 3rem;
}

.folder-top .fname {
  width: 100%;
  display: flex;
  align-items: center;

  .play {
    height: 100%;
    width: 5em;
    background-color: $blue;
    padding-left: $small;
    margin-right: $small;

    .icon {
      height: 1.5rem;
      width: 1.5rem;
      background-image: url(../../assets/icons/play.svg);
      background-size: 1.5rem;
      background-position: 10%;
      margin-right: $small;
    }
  }

  .text {
    position: relative;
    display: flex;
    align-items: center;

    border-radius: $small;
    background-color: $primary;
    padding: $small $small $small 2.25rem;

    .icon {
      position: absolute;
      left: $small;
      height: 1.5rem;
      width: 1.5rem;
      background-image: url(../../assets/icons/folder.fill.svg);
      margin-right: $small;
    }

    @include phone-only {
      display: none;
    }
  }
}
</style>
