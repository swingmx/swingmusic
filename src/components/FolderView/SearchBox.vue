<template>
  <div class="folder-top flex">
    <div class="fname">
      <span>Oldies Volume 1</span>
    </div>
    <div class="fsearch">
      <div>
        <input type="search" placeholder="Search here" />
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
.folder-top {
  padding-bottom: 1em;
  margin-bottom: 1em;
  border-bottom: 1px solid var(--seperator);
}

.folder-top .fname {
  width: 50%;
  color: rgba(255, 255, 255, 0.438);
  text-transform: uppercase;
  display: flex;
  align-items: center;
}

.folder-top .fsearch {
  width: 50%;
  display: flex;
  justify-content: flex-end;
  margin-right: 10px;
}

.folder-top .fsearch div {
  width: 100%;
}

.folder-top .fsearch input {
  width: 100%;
  border: none;
  border-radius: 2em;
  padding-left: 1em;
  background-color: #0101016c;
  color: rgba(255, 255, 255, 0.521);
  font-size: 1em;
  line-height: 3em;
  outline: none;
}
.folder-top .fsearch input::-webkit-search-cancel-button {
  position: relative;
  right: 20px;
  cursor: pointer;
  width: 50px;
  height: 50px;
  border: solid;
}

.folder-top .fsearch input:focus {
  color: rgb(75, 74, 74);
  outline: 0.1em solid var(--green);
}
</style>