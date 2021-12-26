<template>
  <div class="f-container rounded" :class="{ no_f: !folders.length }">
    <p v-if="folders.length">folders in this directory</p>
    <div id="f-items" v-if="folders.length">
      <router-link
        :to="{ name: 'FolderView', params: { path: folder.path } }"
        v-for="folder in folders"
        :key="folder"
      >
        <div class="f-item rounded">
          <div class="f-item-text ellip">{{ folder.name }}</div>
          <div class="f-item-count">{{ folder.count }} tracks</div>
        </div>
      </router-link>
    </div>
    <div v-else>
      <p>No folders in this directory</p>
    </div>
  </div>
</template>

<script>
export default {
  props: ["folders"],
};
</script>

<style lang="scss">
.f-container {
  margin-bottom: 1rem;
  background: rgba(31, 30, 30, 0.521);
  padding: 1rem;
}

.no_f {
  background-image: url(../../assets/icons/info.svg);
  background-repeat: no-repeat;
  background-position: 1rem;
  background-size: 2rem 2rem;
  padding-left: 4rem;
}

#f-items {
  display: flex;
  flex-wrap: wrap;
  border-top: 1px solid var(--separator);
  gap: 1rem;
  padding-top: 1rem;
}

.f-container p {
  text-transform: uppercase;
  font-weight: normal;
  color: rgba(255, 255, 255, 0.438);
  margin-bottom: 1rem;
}

.f-container .f-item {
  min-width: 14.4rem;
  min-height: 5rem;
  display: flex;
  align-items: center;
  position: relative;
  background-image: url(../../assets/icons/folder.svg);
  background-repeat: no-repeat;
  background-position: 1rem;
  background-size: 10% 100%;
  background-color: rgba(80, 80, 80, 0.247);
  transition: all 0.2s ease;

  .f-item-count {
    position: absolute;
    top: 70%;
    left: 3rem;
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.5);
  }

  .f-item-text {
    position: absolute;
    left: 3rem;
    text-align: left;
  }
}

.f-container .f-item:hover {
  transition: all 0.2s ease;
  background: #000000; /* fallback for old browsers */
  background: no-repeat 8%/100% url(../../assets/icons/folder.svg),
    -webkit-linear-gradient(to bottom, #434343, #000000); /* Chrome 10-25, Safari 5.1-6 */
  background: no-repeat 8%/10% url(../../assets/icons/folder.svg),
    linear-gradient(to bottom, #434343, #000000); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
</style>