<template>
    <input v-model="searchText" />
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
input {
  display: block;
  margin: 0px;
  padding: 6px;
  border-style:solid;
  border-color: lightgray;
  border-radius: 5px;
  color: #2c3e50;
  font-size: 17px;
  outline: none;
  width: 50vw;
  &:focus {
    border-color: #00a2e8;
  }
}
</style>
