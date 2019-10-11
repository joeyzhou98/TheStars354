<template>
  <div id="header">
    <div id="logo">
      <router-link to="/"><img src="@/assets/temp-logo.png"></router-link>
    </div>
    <div id="search">
      <SearchBar></SearchBar>
    </div>
    <div id=info>
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
#info {
  float: right;
}
nav {
  margin: 5px;
  padding: 2px 20px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &:hover {
      color: #00a2e8;
    }
  }
}
</style>
