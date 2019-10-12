<template>
  <div id="header">
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
    <div id="logo">
      <router-link to="/"><img src="@/assets/temp-logo.png"></router-link>
    </div>
    <div id="search">
      <SearchBar></SearchBar>
    </div>
    <div id=buttons>
      <button class="iconbutton">ACC.</button>
      <button class="iconbutton">CART</button>
    </div>
  </div>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue'
export default {
  name: 'NavigationTop',
  components: {
    'SearchBar': SearchBar
  }
}
</script>

<style scoped lang="scss">
#header {
  display: inline-block;
  text-align: left;
  margin-left: calc(50% - 50vw);
  width: 100vw;
  box-shadow: 0px 3px 2px lightgray;
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
  font-size: 90%;
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
      color: $black;
    }
  }
}
#logo {
  text-align: left;
  float: left;
  width: 250px;
  img {
    width: 100%;
    height: 100%;
    object-fit: contain
  }
}
#search {
  margin: 32px 0px;
  display: inline-block;
}
#buttons {
  float: right;
  margin: 15px;
}
.iconbutton {
  display: inline-block;
  margin: 0px 15px;
  background-color: white;
  border: none;
  color: darkgray;
  padding: 20px;
  text-align: center;
  text-decoration: none;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  outline: none;
  &:hover {
    color: $mainblue;
  }
  &:active {
    position:relative;
    top:1px;
  }
}
</style>
