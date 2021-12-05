<template>
  <div class="p-header rounded">
    <div class="album-art rounded"></div>
    <div></div>
  </div>
</template>

<script>
export default {

}
</script>

<style lang="scss">
.p-header {
  display: flex;
  padding: 0.5rem;
  background-color: $card-dark;
  height: calc(100% - 1rem);
}

.p-header > * {
  // border: solid;
}

.p-header .album-art {
  width: 15rem;
  height: 15rem;
  background: $red;
}
</style>
