<template>
  <div class="f-artists">
    <div class="header">
      <div class="headin">Featured Artists</div>
      <div class="xcontrols">
        <div class="expand rounded">
          EXPAND
        </div>
        <div class="prev icon" @click="scrollLeft()"></div>
        <div class="next icon" @click="scrollRight()"></div>
      </div>
    </div>
    <div class="separator no-border"></div>
    <div class="artists" ref="artists_dom">
      <ArtistCard
        v-for="artist in artists"
        :key="artist.image"
        :artist="artist"
        :color="'ffffff00'"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from "@vue/reactivity";
import ArtistCard from "@/components/shared/ArtistCard.vue";
import { Artist } from "@/interfaces";

defineProps<{
  artists: Artist[];
}>();

const artists_dom = ref(null);

const scrollLeft = () => {
  const dom = artists_dom.value;
  dom.scrollBy({
    left: -700,
    behavior: "smooth",
  });
};

const scrollRight = () => {
  const dom = artists_dom.value;
  dom.scrollBy({
    left: 700,
    behavior: "smooth",
  });
};
</script>

<style lang="scss">
.f-artists {
  height: 14.5em;
  width: calc(100%);
  padding: $small;
  padding-bottom: 0;
  border-radius: $small;
  user-select: none;
  // background: linear-gradient(0deg, transparent, $black);
  position: relative;
  // background-color: #ffffff00;

  .header {
    display: flex;
    height: 2.5rem;
    align-items: center;
    position: relative;

    .headin {
      font-size: 1.5rem;
      font-weight: 900;
      // border: solid;
      margin-left: $small;
    }
  }
}

.f-artists .xcontrols {
  z-index: 1;
  position: absolute;
  top: 0;
  right: 0;
  display: flex;
  gap: 1rem;
  justify-content: space-between;

  .prev {
    transform: rotate(180deg);
  }
  .icon {
    background: url(../../assets/icons/right-arrow.svg) no-repeat center;
    width: 2rem;
    height: 2rem;
    border-radius: $small;
    cursor: pointer;
    transition: all 0.5s ease;
    background-color: rgb(51, 51, 51);

    &:hover {
      background-color: $blue;
      transition: all 0.5s ease;
    }
  }

  .expand {
    background-color: $gray3;
    padding: $smaller 1rem;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    justify-content: center;

    .icon {
      height: 1rem;
      aspect-ratio: 1;
      background-color: transparent;
      transform: rotate(-90deg);
    }
  }
}

.f-artists > .artists {
  display: flex;
  align-items: flex-end;
  flex-wrap: nowrap;
  overflow-x: scroll;
  gap: $small;
  scrollbar-width: none;

  &::-webkit-scrollbar {
    display: none;
  }
}
</style>
