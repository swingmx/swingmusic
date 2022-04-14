<template>
  <div id="nav-search">
    <form>
      <input
        type="search"
        name=""
        id=""
        placeholder="Search this playlist"
        class="rounded"
      />
    </form>
  </div>
</template>

<style lang="scss">
#nav-search {
  form {
    display: flex;
    gap: $small;

    input[type="search"] {
      background-color: $gray5;
      border: none;
      padding: $small;
      width: 100%;
      min-width: 24rem;
      color: $white;
      font-size: 1rem;

      &:focus {
        outline: solid $accent;
      }
    }
  }
}
</style>
