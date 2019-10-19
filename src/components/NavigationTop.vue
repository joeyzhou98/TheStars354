<template>
  <div id="full-header">
    <div id="top">
      <div id="promo">
        FREE WORLDWIDE SHIPPING ON EVERY ORDER!
      </div>
      <div id="login">
        <nav>
          <div v-if="loggedin">
            Hello Name! <!-- TODO: Replace {Name} with user's name when loggedin is true -->
          </div>
          <div v-else>
            Hello! <router-link to="/register">Register</router-link>
            or <router-link to="/login">Log in</router-link>
          </div>
        </nav>
      </div>
    </div>
    <div id="main-header" class="level">
      <div class="level-left">
        <div id="categories">
          <CategoriesMenu></CategoriesMenu>
        </div>
        <div id="logo">
          <router-link to="/"><img src="@/assets/temp-logo.png"></router-link>
        </div>
        <div id="search">
          <SearchBar></SearchBar>
        </div>
      </div>
      <div class="level-right">
        <div id="buttons"> <!-- Add event listener to login and logout events-->
          <b-button class="icon-button" type="is-link"
                  tag="router-link" icon-right="user icon-color" :to="`${toAccount}`">
                  ACCOUNT</b-button>
          <b-button class="icon-button" type="is-link" :to="`${toCart}`"
                  icon-right="shopping-cart icon-color">
                  CART</b-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CategoriesMenu from '@/components/CategoriesMenu.vue'
import SearchBar from '@/components/SearchBar.vue'
import { bus } from '@/main'

export default {
  name: 'NavigationTop',
  components: {
    'SearchBar': SearchBar,
    'CategoriesMenu': CategoriesMenu
  },
  data () {
    return {
      toAccount: '/login', // by default, Account brings to Login page
      toCart: '/cart', // user is able to add to cart without being logged in
      headerOffset: 40 // hardcoded :( otherwise won't work after refreshing page
    }
  },
  methods: {
    onLogin () {
      this.toAccount = '/account'
    },
    onLogout () {
      this.toAccount = '/login'
    },
    onScroll () {
      try {
        if (window.pageYOffset >= this.headerOffset) {
          document.getElementById('main-header').className = 'level navbar is-fixed-top'
          bus.$emit('doStickyHeader', this.headerOffset)
        } else {
          document.getElementById('main-header', this.headerOffset).className = 'level'
          bus.$emit('undoStickyHeader')
        }
      } catch (e) {
        alert(e)
      }
    }
  },
  mounted () {
    window.addEventListener('scroll', this.onScroll)
  },
  destroyed () {
    window.removeEventListener('scroll', this.onScroll)
  }
}
</script>

<style scoped lang="scss">
#full-header {
  display: inline-block;
  text-align: left;
  margin-left: calc(50% - 50vw);
  width: 100vw;
}
#main-header {
  box-shadow: 0px 3px 2px lightgray;
}
.is-fixed-top {
  margin-left: calc(50% - 50vw);
  width: 100vw;
}
#top {
  display: inline-block;
  background-color: $mainblue;
  color: white;
  width: 100%;
  vertical-align: middle;
}
#promo {
  display: inline-block;
  margin-left: 5em;
  padding-top: 10px;
  font-size: 80%;
  font-weight: 600;
}
#login {
  float: right;
  margin: 5px;
  padding: 2px 20px;
  a {
    font-weight: bold;
    color: white;
    &:hover {
      color: $darkblue;
    }
  }
}
#categories {
  display: inline-block;
  margin-left: 30px
}
#logo {
  margin: 0px 15px;
  text-align: left;
  width: 200px;
}
#search {
  width: 50vw;
  display: inline-block;
}
#buttons {
  margin: 0px 30px;
}
.icon-button {
  border: none;
  size: "is-size-6";
  text-align: center;
  margin: 4px 3px;
  padding: 0px 20px;
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
</style>
