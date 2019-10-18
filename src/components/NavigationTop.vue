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
    <div class="level">
      <div class="level-left">
        <div id="logo">
          <router-link to="/"><img src="@/assets/temp-logo.png"></router-link>
        </div>
        <div id="search">
          <SearchBar></SearchBar>
        </div>
      </div>
      <div class="level-right">
        <div id="buttons">
          <div v-if="loggedin"> <!--login or account-->
            <b-button class="icon-button" type="is-link"
                    size="is-medium" tag="router-link" icon-right="user icon-color" to="/account" />
            <b-button class="icon-button" type="is-link"
                    size="is-medium"
                    icon-right="shopping-cart icon-color" />
          </div>
          <div v-else>
            <b-button class="icon-button" type="is-link"
                    size="is-medium" tag="router-link" icon-right="user icon-color" to="/login" />
            <b-button class="icon-button" type="is-link"
                    size="is-medium"
                    icon-right="shopping-cart icon-color" />
          </div>
        </div>
      </div>
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
      color: $blueblack;
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
  width: 50vw;
  display: inline-block;
}
#buttons {
  margin: 0px 30px;
}
.icon-button {
  border: none;
  text-align: center;
  margin: 4px 3px;
  padding: 0px 20px;
  cursor: pointer;
  outline: none;
  color: lightgray;
  &:hover {
    color: $mainblue;
  }
  &:active {
    position:relative;
    top:1px;
  }
}
</style>
