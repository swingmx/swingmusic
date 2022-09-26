<template>
  <div class="nav-search-input">
    <SearchInput :on_nav="true" />
  </div>
</template>

<script setup lang="ts">
import SearchInput from "@/components/RightSideBar/SearchInput.vue";
</script>

<style lang="scss">
.nav-search-input {
  align-items: center;
  justify-content: space-evenly;

  & > div {
    width: 70%;
    margin: 0 auto;
  }
}
</style>
