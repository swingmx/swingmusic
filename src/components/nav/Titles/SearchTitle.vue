<template>
  <div class="nav-search-input">
    <SearchInput />
  </div>
</template>

<script setup lang="ts">
import SearchInput from "@/components/RightSideBar/SearchInput.vue";
</script>

<style lang="scss">
.nav-search-input {
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
}
</style>
