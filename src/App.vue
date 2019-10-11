<template>
  <div id="app">
    <div id="header">
      <NavigationTop></NavigationTop>
      <div id="logo">
        <img src="@/assets/temp-logo.png">
      </div>
    </div>
    <router-view/>
    <NavigationBottom></NavigationBottom>
  </div>
</template>

<script>
import NavigationTop from '@/components/NavigationTop.vue'
import NavigationBottom from '@/components/NavigationBottom.vue'

export default {
  name: 'App',
  components: {
    'NavigationTop': NavigationTop,
    'NavigationBottom': NavigationBottom
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#logo {
  img {
    width: 20%;
    height: 20%
  }
}

</style>
