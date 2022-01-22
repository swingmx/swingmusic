<template>
  <div class="xartist border">
    <div
      class="artist-image image"
      :style="{ backgroundImage: `url('${artist.image}')` }"
    ></div>
    <div>
    <p class="artist-name ellipsis">{{ artist.name }}</p>
    </div>
    <!-- <div class="a-circle"></div> -->
  </div>
</template>

<script>
export default {
  props: ["artist"],
};
</script>

<style lang="scss">
.xartist {
  flex: 0 0 auto;
  overflow: hidden;
  position: relative;
  margin: 0 $smaller 0 $smaller;
  width: 9em;
  height: 11em;
  border-radius: $small;
  background-color: #232452;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;

  .artist-image {
    width: 7em;
    height: 7em;
    border-radius: 50%;
    margin-bottom: $small;
    background: url("../../assets/images/null.webp");
    background-size: 7rem 7rem;
    background-repeat: no-repeat;
    background-position: center;
    transition: all 0.5s ease-in-out;
    border: solid 1px rgba(5, 5, 5, 0.055);
    box-shadow: 0px 0px 80px rgb(0, 0, 0);
  }

  &:hover {
    .artist-image {
      background-position: 50% 20%;
      border-radius: 20%;
      background-size: 10rem 10rem;
    }
  }

  .artist-name {
    margin: 0;
    text-align: center;
    font-size: 0.9rem;
    font-weight: 510;
    max-width: 7rem;
  }
}
</style>