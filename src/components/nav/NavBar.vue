<template>
  <div class="topnav rounded">
    <div class="left">
      <!-- <div class="btn">
        <PlayBtn />
      </div> -->
      <div class="info">
        <div class="title">Album</div>
      </div>
    </div>
    <div class="center"></div>
    <div class="right"></div>
  </div>
</template>

<script setup>
import PlayBtn from '../shared/PlayBtn.vue';

</script>

<style lang="scss">
.topnav {
  background-color: $gray3;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  padding: 0 $small;
  margin: $small $small 0 $small;

  .left {
    display: flex;
    // border: solid 1px $gray;
    align-items: center;
    gap: $small;

    .info {
      .title {
        font-size: 1.5rem;
        font-weight: bold;
      }
    }
  }
}
</style>
