<template>
<div>
  <b-nav-form>
    <b-input-group>
      <b-form-input id="bar" class="shadow-none mr-sm-2"  size="sm" placeholder="Search" v-model="query" @keyup.enter="onSearch">
        </b-form-input>
      <b-button id="submit" variant="outline-primary" class="shadow-none" size="sm" type="submit"
        @click="onSearch">Search</b-button>
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
      query: '',
      sendQuery: false
    }
  },
  computed: {
    onSearchPage () {
      return this.$route.path === '/search'
    }
  },
  methods: {
    onSearch () {
      if (this.onSearchPage) {
        bus.$emit('search', this.query)
      } else { // delay until we are on search page before sending search event
        this.$router.push('/search')
        this.sendQuery = true
      }
    }
  },
  watch: {
    sendQuery () {
      if (this.sendQuery && this.onSearchPage) {
        bus.$emit('search', this.query)
        this.sendQuery = false
      }
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
