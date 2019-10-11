<template>
  <div id="top_bar">
    <nav>
      <div v-if="loggedin">
        Hello Name!
      </div>
      <div v-else>
        Hello! <router-link to="/register">Register</router-link>
        or <router-link to="/login">Log in</router-link>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'NavigationTop'
}
</script>

<style scoped lang="scss">
nav {
  margin: 5px;
  padding: 30px;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
