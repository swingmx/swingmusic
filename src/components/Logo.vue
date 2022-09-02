<template>
  <div id="logo-container"
  >
    <router-link :to="{ name: 'Home' }">
      <div id="logo"></div
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
  background-image: url(./../assets/images/logo.webp);
  background-size: contain;
  @include ximage;
  border-radius: $medium;
}
</style>
