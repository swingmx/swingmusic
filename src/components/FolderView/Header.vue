<template>
  <div class="folder-top flex">
    <div class="fname">
      <button class="play image">
        <div class="icon"></div>
        Play
      </button>
      <div class="ellip text">
        <div class="icon image"></div>
        {{ path.split("/").splice(-1) + "" }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["path"],
};
</script>

<style lang="scss">
.folder-top {
  border-bottom: 1px solid $separator;
  width: calc(100% - 0.5rem);
  padding-bottom: $small;
  height: 3rem;
}

.folder-top .fname {
  // width: 50%;
  display: flex;
  align-items: center;

  .play {
    height: 100%;
    width: 5em;
    background-color: rgb(5, 74, 131);
    border-radius: $small;
    display: flex;
    align-items: center;
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
    display: flex;
    align-items: center;

    border-radius: $small;
    background-color: rgb(24, 22, 22);
    padding: $small;

    .icon {
      height: 1.5rem;
      width: 1.5rem;
      background-image: url(../../assets/icons/folder.svg);
      margin-right: $small;
    }
  }
}
</style>