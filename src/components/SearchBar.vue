<template>
<div>
    <b-field>
      <b-select id="filter" placeholder="All">
        <option
            v-for="category in categories"
            :key="category.id">
            {{ category.name }}
        </option>
      </b-select>
      <b-input id="bar" v-model="searchText"
               icon="search fa-flip-horizontal icon-color"
               placeholder="Search..." expanded>
      </b-input>
      <b-button id="submit" type="is-primary">SEARCH</b-button>
    </b-field>
</div>
</template>

<script>
export default {
  name: 'SearchBar',
  data () {
    return {
      searchText: '',
      categories: [
        {
          id: 0,
          name: 'All'
        },
        {
          id: 1,
          name: 'Category 1'
        },
        {
          id: 2,
          name: 'Category 2'
        }
      ]
    }
  }
}
</script>

<style scoped lang="scss">
#bar {
  color: $darkblue;
  outline: none;
  padding: 0px 40px;
}
.icon-color {
  color: lightgray;
}
#submit {
  background-color: $mainblue;
  border-top-left-radius: 0%;
  border-bottom-left-radius: 0%;
  &:active {
    position:relative;
    top:1px;
  }
  &:hover {
    background-color:$darkblue;
  }
}
</style>
