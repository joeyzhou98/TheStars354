<template>
<div>
    <input id="bar" v-model="searchText" />
    <button id="submit">SEARCH</button>
</div>
</template>

<script>
export default {
  name: 'SearchBar',
  data () {
    return {
      searchText: ''
    }
  }
}
</script>

<style lang="scss">
#bar {
  display: inline-block;
  margin: 0px 8px;
  padding: 6px;
  border-radius: 5px;
  border: solid lightgray;
  color: #2c3e50;
  font-size: 17px;
  outline: none;
  width: 50vw;
  &:focus {
    border-color: #d6ebff;
  }
}
#submit {
  display:inline-block;
  box-shadow:inset 0px 1px 0px 0px #bbdaf7;
  background:linear-gradient(to bottom, #79bbff 5%, #00a2e8 100%);
  background-color:#79bbff;
  border-radius:6px;
  border:1px solid #d6ebff;
  cursor:pointer;
  color:#ffffff;
  font-size:15px;
  font-weight:bold;
  padding:9px 24px 7px 24px;
  text-decoration:none;
  text-shadow:0px 1px 0px #528ecc;
  outline: none;
  &:hover {
    background:linear-gradient(to bottom, #00a2e8 5%, #79bbff 100%);
    background-color:#378de5;
  }
  &:active {
    position:relative;
    top:1px;
  }
}
</style>
