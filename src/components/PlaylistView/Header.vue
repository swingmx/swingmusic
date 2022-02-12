<template>
  <div class="p-header rounded">
    <div class="info rounded card-dark">
      <div>
        <div class="name">Makaveli Radio</div>
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

  .last-updated {
    position: absolute;
    bottom: $small;
    right: $small;
    padding: 0.5rem;
    background-color: rgba(0, 0, 0, 0.699);
    color: rgb(255, 255, 255);
    font-size: 0.9rem;
    border-radius: $smaller;
    box-shadow: 0px 0px 1rem rgba(0, 0, 0, 0.479);

    @include phone-only {
      // border: solid;
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
    padding: $small;
    display: flex;
    flex-direction: row;
    align-items: flex-end;
    padding-bottom: 3.5rem;
    box-shadow: 0px 0px 1.5rem rgba(0, 0, 0, 0.658);

    @include phone-only {
      width: calc(100% - 1rem);
    }

    .name {
      font-size: 1.5rem;
      font-weight: bold;

      &::before {
        content: "😎 ";
      }
    }

    .metrics {
      margin-top: $small;
      background-color: rgba(47, 55, 129, 0.233);
      color: rgb(0, 60, 255);
      padding: $small;
      width: fit-content;
      border-radius: $smaller;
    }

    .buttons {
      position: absolute;
      bottom: $small;
      left: $small;
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
