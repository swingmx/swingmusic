<template>
  <div class="f-container rounded" :class="{ no_f: !folders.length }">
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
  </div>
</template>

<script>
export default {
  props: ["folders"],
};
</script>

<style lang="scss">
.f-container {
  padding: $small 1rem 1rem 1rem;
}

.no_f {
  display: none;
}

#f-items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(13rem, 1fr));
  grid-gap: 1rem;
  gap: 1rem;
}

.f-container p {
  text-transform: uppercase;
  font-weight: normal;
  color: rgba(255, 255, 255, 0.438);
  margin-bottom: 1rem;
}

.f-container .f-item {
  min-height: 5rem;
  display: flex;
  align-items: center;
  position: relative;
  background-image: url(../../assets/icons/folder.svg);
  background-repeat: no-repeat;
  background-position: 1rem;
  background-size: 10% 100%;
  background-color: rgb(22, 36, 85);
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
  background-color: $blue;
}
</style>