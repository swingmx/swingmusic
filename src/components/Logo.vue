<template>
  <div class="app-logo">
    <router-link :to="{ name: 'Home' }">
      <img
        class="app-logo rounded shadow-sm"
        src="../assets/images/logo.webp"
        alt="logo"
      />
    </router-link>
  </div>
</template>

<style lang="scss">
.app-logo {
  height: 5rem !important;
  width: 15rem;
  object-fit: cover;
  pointer-events: none;
}
</style>
