<template>
  <div class="rounded folder">
    <div class="folder-top flex">
      <div class="fname">
        <span>Oldies Volume 1</span>
      </div>
      <div class="fsearch">
        <div>
          <input type="text" placeholder="Search here" />
        </div>
      </div>
    </div>
    <div class="table">
      <div>
        <div class="theaders">
          <div>Track</div>
          <div>Artist</div>
          <div>Album</div>
          <div>Duration</div>
        </div>
        <hr />
        <div class="theaders">
          <div class="flex">
            <div class="album-art rounded"></div>
            <span>Some broken hearts never mend</span>
          </div>
          <div class="flex">Don Williams</div>
          <div class="flex">Best Of</div>
          <div class="flex">3:17</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style>
.theaders {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  grid-auto-columns: 1fr;
  gap: 0px 0px;
  grid-auto-flow: row;
}

.theaders .flex {
  align-items: center;
  /* border: solid; */
}

.theaders .flex span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  
}
.theaders .album-art {
  width: 50px;
  height: 50px;
  margin-right: 10px;
  background: rgb(172, 13, 13);
}

.folder {
  background-color: rgba(0, 0, 0, 0.144);
  padding: 20px 20px 20px 20px;
}

.folder-top {
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.445);
}

.folder-top .fname {
  width: 50%;
  color: rgba(255, 255, 255, 0.438);
  text-transform: uppercase;
  font-weight: bold;
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
  padding-right: 20px;
}

.folder-top .fsearch input {
  width: 100%;
  height: 50px;
  border: none;
  border-radius: 10px;
  outline: none;
  padding-left: 10px;
  background-color: #0101016c;
  color: rgba(255, 255, 255, 0.521);
  font-size: large;
  line-height: 50px;
}

.folder-top .fsearch input:focus {
  color: #fff;
}
</style>