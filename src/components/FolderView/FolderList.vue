<template>
  <div class="f-container" v-for="folder in folders" :key="folder">
    <router-link :to="{ path: '/' }">
      <div class="f-item circular">
        <div class="f-item-bg"></div>
        <span class="f-item-text">{{ folder.name }}</span>
      </div>
    </router-link>
  </div>
</template>

<script>
import Folders from "../../data/folders.js";

export default {
  setup() {
    const folders = Folders.folders;

    return { folders };
  },
};
</script>

<style>
.f-item {
  width: 10em;
  height: 10em;
  background-color: var(--green);
  display: flex;
  justify-content: center;
  position: relative;
  background-image: url(../../assets/icons/folder.svg);
  background-repeat: no-repeat;
  background-position: center;
  background-size: 50%;
}

.f-item-text {
  width: calc(100% - 10%);
  line-height-step: 2;
  position: absolute;
  bottom: -3em;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}

.f-item-bg {
  height: 100px;
  width: 100%;
  color: red;
}
</style>