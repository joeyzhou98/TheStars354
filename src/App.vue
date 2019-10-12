<template>
  <div id="app">
    <NavigationTop></NavigationTop>
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
@import 'src/styles/bulma.scss';

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: $black;
}
</style>
