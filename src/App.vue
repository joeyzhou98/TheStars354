<template>
  <b-container id="app" fluid class="p-0">
    <NavigationTop></NavigationTop>
    <div id="content">
      <router-view/>
    </div>
    <NavigationBottom></NavigationBottom>
  </b-container>
</template>

<script>
import store from '@/store.js'
import NavigationTop from '@/components/NavigationTop.vue'
import NavigationBottom from '@/components/NavigationBottom.vue'

export default {
  name: 'App',
  store,
  components: {
    'NavigationTop': NavigationTop,
    'NavigationBottom': NavigationBottom
  }
}
</script>

<style scoped lang="scss">
#content {
  padding: 100px 25px;
}
</style>

<style lang="scss">
html {
  overflow-y: auto !important;
  overflow-x: hidden;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: $black;
  text-decoration: none;
}
</style>
