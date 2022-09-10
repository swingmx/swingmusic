<template>
  <div class="artists-view rounded">
    <div class="al-header">
      <div class="heading">ALL ARTISTS</div>
      <div class="search">
        <input type="search" placeholder="Search artists" />
      </div>
    </div>
    <div class="all-albums">
      <div class="item rounded" v-for="artist in artists" :key="artist">
        <div class="album-art image rounded"></div>
        <div class="name t-center ellip">{{ artist.name }}</div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  setup() {
    const artists = [
      {
        name: "Juice Wrld",
      },
      {
        name: "Eminem",
      },
      {
        name: "Sting",
      },
      {
        name: "Juice Wrld",
      },
      {
        name: "Eminem",
      },
      {
        name: "Sting",
      },
      {
        name: "Juice Wrld",
      },
    ];

    return {
      artists,
    };
  },
};
</script>

<style lang="scss">
.artists-view {
  height: calc(100% - 14.5rem);
  padding: $small;
  margin-top: $small;
  overflow: hidden;

  .all-albums {
    height: calc(100% - 4rem);
    border-top: 1px solid $separator;
    padding: $small 0 0 0;
    overflow-y: auto;

    .item {
      position: relative;
      width: 10.9rem;
      height: 12rem;
      padding: $small 0.95rem $small 0.95rem;
      margin: $smaller;
      transition: all 0.2s ease-in-out;
      cursor: default;
      float: left;

      &:hover {
        background-color: rgb(74, 84, 87);
        // border: solid
      }

      .album-art {
        height: 9em;
        width: 9em;
        border-radius: 50%;
        background-image: url(../../assets/images/null.webp);
      }

      .name {
        margin-top: $small;
      }
    }
  }

  .al-header {
    display: flex;
    align-items: center;
    position: relative;
    height: 4em;
    padding: 0 $small 0 $small;

    .search {
      position: absolute;
      right: 0;
      padding-right: $small;

      input {
        width: 30rem;
        border: none;
        border-radius: 2rem;
        padding-left: 1rem;
        background-color: #4645456c;
        color: rgba(255, 255, 255, 0.521);
        font-size: 1rem;
        line-height: 3rem;
        outline: none;
      }

      input::-webkit-search-cancel-button {
        position: relative;
        right: 20px;
        cursor: default;
        width: 50px;
        height: 50px;
      }
    }
  }
}
</style>
