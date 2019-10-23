<template>
  <div>
    <b-navbar id="navbar" toggleable="sm" class="fixed-top">
      <div id="categories">
        <CategoriesMenu></CategoriesMenu>
      </div>
      <div class="mx-auto" style="width: 200px;">
        <b-navbar-brand><router-link to="/#">354 THE STARS</router-link></b-navbar-brand>
      </div>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <!-- Right aligned nav items -->
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <div id="search">
            <SearchBar></SearchBar>
          </div>
          <div id="buttons"> <!-- Add event listener to login and logout events-->
            <b-button class="icon-button shadow-none" variant="outline"
                      title="Account"
                     :to="toAccount">
              <icon name="user"></icon>
            </b-button>
            <b-button class="icon-button shadow-none" variant="outline"
                      title="Cart"
                      :to="toCart">
              <icon name="shopping-cart"></icon>
            </b-button>
          </div>
          </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import CategoriesMenu from '@/components/CategoriesMenu.vue'
import SearchBar from '@/components/SearchBar.vue'
// import { bus } from '@/main'

export default {
  name: 'NavigationTop',
  components: {
    'SearchBar': SearchBar,
    'CategoriesMenu': CategoriesMenu
  },
  data () {
    return {
      toAccount: '/account', // by default, Account brings to Login page
      toCart: '/cart' // user is able to add to cart without being logged in
    }
  },
  methods: {
    onLogin () {
      this.toAccount = '/account'
    },
    onLogout () {
      this.toAccount = '/login'
    }
  }
}
</script>

<style scoped lang="scss">
#navbar {
  background-color: white;
  box-shadow: 0px 2px 2px lightgray;
  text-align: left;
}
#categories {
  display: inline-block;
  margin-left: 10px;
  margin-right: 30px;
}
#logo {
  margin: 0px 15px;
  text-align: left;
  width: 200px;
}
#buttons {
  margin: 0px 30px;
}
.icon-button {
  background: none;
  border: none;
  text-align: center;
  margin: 0px 3px;
  cursor: pointer;
  outline: none;
  color: $darkblue;
  &:hover {
    color: $mainblue;
  }
  &:active {
    position:relative;
    top:1px;
  }
}
#search {
  margin: 4px 0px;
}
</style>
