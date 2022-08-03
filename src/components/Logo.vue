<template>
  <div id="logo-container"
  >
    <router-link :to="{ name: 'Home' }">
      <div id="logo" class="rounded"></div
    ></router-link>
  </div>
</template>

<style lang="scss">
@import "../assets/scss/mixins.scss";

#logo-container {
  overflow: hidden;
}

#logo {
  height: 4.5rem !important;
  width: 15rem;
  background-image: url(./../assets/images/logo.webp);
  background-size: contain;
  @include ximage;
}
</style>
