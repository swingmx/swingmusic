<template>
  <div class="folder-top flex">
    <div class="fname">
      <span>Oldies Volume 1</span>
    </div>
    <div class="fsearch">
      <div>
        <input type="search" placeholder="Search this directory" />
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
.folder-top {
  padding-bottom: 1rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--separator);
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
  margin-right: 1rem;
}

.folder-top .fsearch div {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}

.folder-top .fsearch input {
  width: 30rem;
  border: none;
  border-radius: .5rem;
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
  outline: 0.1rem solid #fafafa52;
}
</style>