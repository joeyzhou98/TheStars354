<template>
<div>
  <b-nav-form>
    <b-input-group>
      <b-form-input id="bar" class="mr-sm-2"  size="sm" placeholder="Search" v-model="query" @keyup.enter="onSearch">
        </b-form-input>
      <b-button id="submit" variant="outline-primary" class="shadow-none" size="sm" type="submit"
        to="/search" @click="onSearch">Search</b-button>
    </b-input-group>
  </b-nav-form>
</div>
</template>

<script>
import { bus } from '../main'

export default {
  name: 'SearchBar',
  data () {
    return {
      filterSelection: 0,
      query: null
    }
  },
  methods: {
    onSearch () {
      bus.$emit('search', this.query)
    }
  }
}
</script>

<style scoped lang="scss">
#bar {
  color: $darkblue;
  outline: none;
  padding: 0px 10px;
}
.icon-color {
  color: lightgray;
}
#submit {
  border-top-left-radius: 0%;
  border-bottom-left-radius: 0%;
  &:active {
    position:relative;
    top:1px;
  }
}
</style>
