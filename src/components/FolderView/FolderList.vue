<template>
  <div class="f-container">
    <h3>folders in this directory</h3>
    <router-link :to="{ path: '/' }" v-for="folder in folders" :key="folder">
      <div class="f-item circular">
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
.f-container {
  margin-bottom: 20em;
}
.f-container h3 {
  text-transform: uppercase;
  font-weight: normal;
  color: rgba(255, 255, 255, 0.438);
  margin-bottom: 0em;
}
.f-container .f-item {
  float: left;
  width: 9em;
  height: 8em;
  /* background-color: #9d020781; */
  display: flex;
  justify-content: center;
  position: relative;
  background-image: url(../../assets/icons/folder.svg);
  background-repeat: no-repeat;
  background-position: center;
  background-size: 30%;
  margin: 2em 2em 0em 0;
  padding: 1em;
  /* border: .1em solid var(--seperator); */
  background-color: rgba(80, 80, 80, 0.247);
}

.f-container .f-item:hover {
  background-color: rgba(0, 0, 0, 0.527);
}

.f-container .f-item-text {
  width: calc(100% - 10%);
  line-height-step: 2;
  position: absolute;
  bottom: 0.5em;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
}
</style>