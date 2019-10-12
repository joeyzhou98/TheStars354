<template>
<div>
    <input id="bar" v-model="searchText" />
     <b-button id="submit" type="is-info">SEARCH</b-button>
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
  color: $black;
  font-size: 17px;
  outline: none;
  width: 50vw;
  &:focus {
    border-color: $lightblue;
  }
}
#submit {
  background-color: $mainblue;
  &:active {
    position:relative;
    top:1px;
  }
  &:hover {
    background-color:$darkblue;
  }
}
</style>
