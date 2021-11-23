<template>
  <div class="f-container rounded">
    <p>folders in this directory</p>
    <div id="f-items">
      <router-link :to="{ path: '/' }" v-for="folder in folders" :key="folder">
        <div class="f-item rounded">
          <span class="f-item-text">{{ folder.name }}</span>
        </div>
      </router-link>
    </div>
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
  margin-bottom: 1em;
  background: rgba(31, 30, 30, 0.521);
  padding: 1em;
}

#f-items {
  display: flex;
  flex-wrap: wrap;
  border-top: 1px solid var(--seperator);
  gap: 1em;
  padding-top: 1em;
}

.f-container p {
  text-transform: uppercase;
  font-weight: normal;
  color: rgba(255, 255, 255, 0.438);
  margin-bottom: 1em;
}

.f-container .f-item {
  min-width: 15em;
  min-height: 5em;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  background-image: url(../../assets/icons/folder.svg);
  background-repeat: no-repeat;
  background-position: 1em;
  background-size: 10% 100%;
  background-color: rgba(80, 80, 80, 0.247);
}

.f-container .f-item:hover {
  background-color: rgba(0, 0, 0, 0.527);
}

.f-container .f-item-text {
  position: absolute;
  left: 3em;
  text-align: left;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
}
</style>