<template>
  <div class="topnav">
    <div class="left">
      <div class="btn">
        <NavButtons />
      </div>

      <div class="info">
        <div class="title" v-if="$route.name == 'Playlists'">Playlists</div>
        <div class="folder" v-else-if="$route.name == 'FolderView'">
          <div class="fname">
            <div class="icon image"></div>
            <div class="ellip">
              {{ $route.params.path.split("/").splice(-1)[0] }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="center rounded">
      <Loader />
    </div>
    <div class="right">
      <div class="more image"></div>
      <Search />
    </div>
  </div>
</template>

<script setup>
import NavButtons from "./NavButtons.vue";
import Loader from "../shared/Loader.vue";
import Search from "./Search.vue";
</script>

<style lang="scss">
.topnav {
  display: grid;
  grid-template-columns: 1fr max-content max-content;
  padding-bottom: 1rem;
  margin: $small $small 0 $small;
  border-bottom: 1px solid $gray3;
  height: 3rem;

  .left {
    display: flex;
    align-items: center;

    .info {
      .title {
        font-size: 1.5rem;
        font-weight: bold;
      }

      .folder {
        display: flex;
        gap: $small;

        .playbtnrect {
          height: 2.25rem;
        }

        .drop-btn {
          width: 2.25rem;

          .drop-icon {
            height: 2.25rem;
            width: 2.25rem;
          }
        }

        .fname {
          padding-left: 0.5rem;
          background-color: $gray4;
          border-radius: $small;
          height: 2.25rem;
          display: flex;
          align-items: center;
          padding-right: $small;
          gap: 0.25rem;
          margin-left: $smaller;

          .icon {
            width: 1.5rem;
            height: 1.5rem;
            background-image: url("../../assets/icons/folder.fill.svg");
          }
        }
      }
    }
  }

  .center {
    display: grid;
    place-items: center;
    margin-right: 1rem;
  }

  .right {
    width: 100%;
    display: flex;
    gap: $small;

    .more {
      width: 2.25rem;
      aspect-ratio: 1;
      height: 100%;
      background-color: $gray5;
      background-image: url("../../assets/icons/more.svg");
      transform: rotate(90deg);
      border-radius: $small;
    }
  }
}
</style>
