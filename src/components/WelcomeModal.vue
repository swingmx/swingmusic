<template>
  <div class="welcome-to-swing">
    <h3 class="t-center">
      Welcome to
      <span class="app-name">Alice</span>
      <span class="release">0.1.0</span>
    </h3>
    <p>
      Alice is a web based music player that is designed to provide a home 🏡
      for all your local music files 💿️.
    </p>
    <hr />
    <p class="t-center">Let there be music!</p>
    <hr />
    <br />

    <div class="bottom-banner">
      <div class="creator t-center">
        Designed and developed by
        <span class="name"
          ><a href="https://github.com/geoffrey45">Mungai Njoroge</a>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style lang="scss">
.welcome-to-swing {
  p {
    line-height: 1.5rem;
  }

  hr {
    border: none;
    border-bottom: 1px $gray3 solid;
  }

  .app-name {
    font-size: 1.5rem;
    color: $red;
  }

  .release {
    margin-left: $smaller;
    font-size: 0.7rem;
    color: $gray1;
  }

  .bottom-banner {
    font-size: small;
    margin-top: 1rem;
    opacity: 0.4;

    a {
      color: $red;
      cursor: pointer !important;
    }
  }
}
</style>
