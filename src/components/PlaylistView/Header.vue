<template>
  <div class="p-header">
    <div class="info">
      <div>
        <div class="title">Makaveli Radio</div>
        <div class="metrics rounded border">45 Tracks • 3 Hours 4 Minutes</div>
      </div>
      <div class="buttons">
        <button class="play">
          <div class="icon"></div>
          Play
        </button>
        <button class="menu">
          <div class="icon"></div>
        </button>
      </div>
    </div>
    <div class="last-updated">
      <span class="status">Last updated yesterday |&#160;</span>
      <span class="edit">Edit</span>
    </div>
  </div>
</template>

<style lang="scss">
.p-header {
  display: grid;
  grid-template-columns: 1fr;
  height: 14rem;
  background-image: url("../../assets/images/eggs.jpg");
  position: relative;
  margin-top: $small;
    border-radius: .75rem;

  .last-updated {
    position: absolute;
    bottom: $small;
    right: $small;
    padding: 0.5rem;
    background-color: rgba(0, 0, 0, 0.699);
    color: rgb(255, 255, 255);
    font-size: 0.9rem;
    border-radius: $smaller;
    box-shadow: 0 0 1rem rgba(0, 0, 0, 0.479);

    @include phone-only {
      bottom: 1rem;
      right: 1rem;
      font-size: small;

      .status {
        display: none;
      }
    }

    .edit {
      cursor: pointer;
    }
  }

  .info {
    position: absolute;
    width: 25rem;
    height: 10rem;
    bottom: $small;
    left: $small;
    display: flex;
    flex-direction: row;
    align-items: flex-end;
    padding: 1rem 1rem 4rem 1rem;
    box-shadow: 0 0 1.5rem rgba(0, 0, 0, 0.658);
    border-radius: .75rem;
    background-color: $black;

    @include phone-only {
      width: calc(100% - 1rem);
    }

    .title {
      font-size: 1.5rem;
      font-weight: bold;
      color: $white;
    }

    .metrics {
      margin-top: $small;
      color: $blue;
      padding: $small;
    }

    .buttons {
      position: absolute;
      bottom:1rem;
      left:1rem;
      display: flex;
      gap: $small;

      .play {
        width: 5rem;
        height: 2.5rem;
        padding: 0.25rem $small;

        .icon {
          width: 1.5rem;
          height: 1.5rem;
          background-image: url("../../assets/icons/play.svg");
          background-size: 1.5rem;
          background-position: center;
          margin-right: 0.25rem;
        }
      }

      .menu {
        width: 2.5rem;
        height: 2.5rem;
        background-image: url("../../assets/icons/options.svg");
        background-size: 2rem;
        background-repeat: no-repeat;
        background-position: center;
      }
    }
  }
}
</style>
