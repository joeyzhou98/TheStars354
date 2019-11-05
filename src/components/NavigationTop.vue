<template>
  <div>
    <b-navbar id="navbar" toggleable="sm" class="fixed-top">
      <div id="categories">
        <CategoriesMenu></CategoriesMenu>
      </div>
      <div class="mx-auto" style="width: 200px;">
        <b-navbar-brand><router-link to="/">354 THE STARS</router-link></b-navbar-brand>
      </div>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-navbar-nav>
        <b-nav-item><router-link class="item-link" to="/bestsellers">Bestsellers</router-link></b-nav-item>
        <b-nav-item><router-link class="item-link" to="/deals">Deals</router-link></b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <div id="search">
            <SearchBar></SearchBar>
          </div>
          <div id="buttons"> <!-- Add event listener to login and logout events-->
            <b-button class="icon-button shadow-none" variant="outline"
                      title="Account"
                     @click="VerifyLoginStatus">
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
import Cookie from 'js-cookie'
import App from '../App'

export default {
  name: 'NavigationTop',
  components: {
    'SearchBar': SearchBar,
    'CategoriesMenu': CategoriesMenu
  },
  data () {
    return {
      toAccount: '/login', // by default, Account brings to Login page
      toCart: '/cart' // user is able to add to cart without being logged in
    }
  },
  methods: {
    onLogin () {
      const accessToken = Cookie.get('access_token')
      alert(accessToken)
      if (accessToken !== '') {
        this.toAccount = '/account'
      }
    },
    onLogout () {
      const accessToken = Cookie.get('access_token')
      if (accessToken === '') { this.toAccount = '/login' }
    },
    VerifyLoginStatus () {
      console.log('loginStatus', App.loginStatus.state)
      alert(App.loginStatus.state.login)
      if (App.loginStatus.state.login) {
        this.$router.push('/account')
      } else {
        this.$router.push('/login')
      }
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
.item-link {
  margin-right: 4px;
  &:hover {
    text-decoration: none;
  }
}
</style>
