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
import NavigationTop from '@/components/NavigationTop.vue'
import NavigationBottom from '@/components/NavigationBottom.vue'

export default {
  name: 'App',
  components: {
    'NavigationTop': NavigationTop,
    'NavigationBottom': NavigationBottom
  },
  loginStatus: {
    debug: true,
    state: {
      login: false
    },
    setLoginStatus (newValue) {
      if (this.debug) console.log('setMessageAction triggered with', newValue)
      this.state.login = newValue
    }
  }
}
</script>

<style scoped lang="scss">
#content {
  padding: 70px 25px;
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
