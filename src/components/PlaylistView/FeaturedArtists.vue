<template>
  <div class="f-artists">
    <div class="header">
      <div class="headin">Featured Artists</div>
      <div class="xcontrols">
        <div class="prev icon" @click="scrollLeft()"><ArrowSvg /></div>
        <div class="next icon" @click="scrollRight()"><ArrowSvg /></div>
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
import ArrowSvg from "../../assets/icons/right-arrow.svg";

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
  width: 100%;
  padding: 0 $small;
  border-radius: $small;
  user-select: none;
  position: relative;

  .header {
    display: flex;
    align-items: center;
    position: relative;

    .headin {
      font-size: 1.5rem;
      font-weight: 900;
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

  .prev {
    transform: rotate(180deg);
  }

  .icon {
    border-radius: $small;
    cursor: pointer;
    transition: all 0.5s ease;
    background-color: rgb(51, 51, 51);
    padding: $smaller;

    svg {
      display: flex;
    }

    &:hover {
      background-color: $accent;
      transition: all 0.5s ease;
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
