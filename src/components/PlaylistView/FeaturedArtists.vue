<template>
  <div class="f-artists">
    <div class="header">
      <div class="headin">Featured Artists</div>
      <div class="xcontrols">
        <div class="prev" @click="scrollLeft"></div>
        <div class="next" @click="scrollRight"></div>
      </div>
    </div>
    <div class="separator no-border"></div>
    <div class="artists" ref="artists_dom">
      <ArtistCard
        v-for="artist in artists"
        :key="artist"
        :artist="artist"
        :color="232452"
      />
    </div>
  </div>
</template>
<script>
import { ref } from "@vue/reactivity";
import ArtistCard from "@/components/shared/ArtistCard.vue";
import { computed, reactive } from "vue";

export default {
  props: ["artists"],
  components: {
    ArtistCard,
  },
  setup() {
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

    return {
      artists_dom,
      scrollLeft,
      scrollRight,
    };
  },
};
</script>

<style lang="scss">
.f-artists {
  height: 15.5em;
  width: calc(100%);
  padding: $small;
  border-radius: $small;
  user-select: none;
  background: linear-gradient(58deg, $gray 0%, rgba(5, 0, 7, 0.5) 100%);
  position: relative;

  .header {
    display: flex;
    height: 2.5rem;
    align-items: center;
    position: relative;

    .headin {
      font-size: 1.5rem;
      font-weight: 900;
      display: flex;
    }
  }
}

.f-artists .xcontrols {
  z-index: 1;
  width: 5rem;
  height: 2rem;
  position: absolute;
  top: 0;
  right: 0;
  display: flex;
  justify-content: space-between;

  &:hover {
    z-index: 1;
  }

  .next {
    background: url(../../assets/icons/right-arrow.svg) no-repeat center;
  }

  .prev {
    background: url(../../assets/icons/right-arrow.svg) no-repeat center;
    transform: rotate(180deg);
  }
  .next,
  .prev {
    width: 2em;
    height: 2em;
    border-radius: $small;
    cursor: pointer;
    transition: all 0.5s ease;
    background-color: rgb(51, 51, 51);
  }

  .next:hover,
  .prev:hover {
    background-color: $blue;
    transition: all 0.5s ease;
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
