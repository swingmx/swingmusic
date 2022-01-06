<template>
  <div class="folder-top flex">
    <div class="fname">
      <div>
        <div class="ellip">{{ path.split("/").splice(-1) + "" }}</div>
      </div>
    </div>
    <div class="fsearch">
      <div>
        <input type="search" placeholder="Search this directory" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ["path"],
};
</script>

<style lang="scss">
.folder-top {
  padding-bottom: 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid $separator;
  width: calc(100% - 2rem);
  margin-left: 1rem;
}

.folder-top .fname {
  width: 50%;
  color: rgba(255, 255, 255, 0.438);
  text-transform: uppercase;
  display: flex;
  align-items: center;
}

.folder-top .fsearch {
  position: relative;
  width: 50%;
  padding-right: 3rem;
}

.folder-top .fsearch div {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}

.folder-top .fsearch input {
  width: 30rem;
  border: none;
  border-radius: 0.5rem;
  padding-left: 1rem;
  background-color: #4645456c;
  color: rgba(255, 255, 255, 0.521);
  font-size: 1rem;
  line-height: 3rem;
  outline: none;
}

.folder-top .fsearch input::-webkit-search-cancel-button {
  position: relative;
  right: 20px;
  cursor: pointer;
  width: 50px;
  height: 50px;
}

.folder-top .fsearch input:focus {
  color: rgb(255, 255, 255);
  outline: 1px solid #fafafa52;
}
</style>