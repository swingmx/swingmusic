<template>
  <div class="nav-search-input">
    <SearchInput />
    <div id="nav-tab-headers"></div>
  </div>
</template>

<script setup lang="ts">
import SearchInput from "@/components/RightSideBar/SearchInput.vue";
</script>

<style lang="scss">
.nav-search-input {
  display: flex;
  grid-template-columns: repeat(3, 1fr);
  align-items: center;
  justify-content: space-between;
  height: 2rem;

  #gsearch-input {
    display: unset;

    #ginner {
      max-width: 30rem;
      margin: 0 auto;
    }

    .buttons {
      display: none;
    }
  }

  .tabheaders {
    margin: 0;
  }
}
</style>
