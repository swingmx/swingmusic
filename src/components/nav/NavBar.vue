<template>
  <div class="topnav rounded">
    <div class="left">
      <div class="btn">
        <PlayBtn />
      </div>
      <div class="info">
        <div class="title">Playlists</div>
      </div>
    </div>
    <div class="center rounded"></div>
    <div class="right"></div>
  </div>
</template>

<script setup>
import PlayBtn from "../shared/PlayBtn.vue";
</script>

<style lang="scss">
.topnav {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  padding: 0 $small;
  margin: $small $small 0 $small;

  .left {
    display: flex;
    align-items: center;
    gap: $small;

    .info {
      .title {
        font-size: 1.5rem;
        font-weight: bold;
      }
    }
  }

  .center {
    display: grid;

    .songcard {
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
}
</style>
