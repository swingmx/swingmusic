<template>
  <div id="nav-search">
    <form>
      <input
        type="search"
        name=""
        id=""
        placeholder="Search here"
        class="rounded"
      />
    </form>
  </div>
</template>

<style lang="scss">
#nav-search {
  // border: solid 1px $gray2;

  form {
    display: flex;
    gap: $small;
    padding: 0;
    margin: 0;

    input[type="search"] {
      background-color: $gray5;
      border: none;
      padding: $small;
      width: 100%;
      color: $white;
      font-size: 1rem;

      &:focus {
        outline: solid $accent;
      }
    }
  }
}
</style>
