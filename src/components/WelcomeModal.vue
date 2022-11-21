<template>
  <div class="welcome-to-alice">
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
    <p>
      To get started, you need to have
      <a href="https://github.com/geoffrey45/alice-core" target="_blank"
        ><span class="inline-code">alice server </span></a
      >
      running on your computer, and accessible via
      <a href="http://localhost:1970"
        ><span class="inline-code">localhost:1970</span></a
      >.
    </p>
    <p>
      On top of that, you need to enable loading mixed content in your browser
      to to load local images 🖼️. Firefox usually supports this by default, but
      you may need to enable it in Chrome.
    </p>
    <hr />
    <br />
    <div class="instructions rounded">
      <div class="t-center">How to enable loading mixed content in</div>
      <div class="button-group">
        <a
          href="https://support.mozilla.org/en-US/kb/mixed-content-blocking-firefox"
          target="_blank"
        >
          <button>🦊 Firefox</button>
        </a>
        <a
          href="https://support.google.com/chrome/answer/95617?hl=en"
          target="_blank"
        >
          <button>🦝 Chrome</button>
        </a>
      </div>
    </div>

    <div class="bottom-banner">
      <div class="creator t-center">
        Designed and developed by
        <span class="name"
          ><a href="https://github.com/geoffrey45">Geoffrey Mungai</a>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts"></script>

<style lang="scss">
.welcome-to-alice {
  p {
    line-height: 1.5rem;
  }

  .inline-code {
    font-size: 0.9rem;
    color: $red;
    border-radius: $smaller;
    font-family: "ui-monospace", "SFMono-Regular", "SF Mono", "Menlo",
      "Consolas", "Liberation Mono";
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
    }
  }

  .instructions {
    background-color: $gray4;
    padding: $small;

    .button-group {
      margin-top: 1rem;
      display: flex;
      justify-content: space-evenly;
      gap: 1rem;

      button {
        padding: 0 $medium;
      }
    }
  }
}
</style>
