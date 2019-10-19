<template>
  <div id="app">
    <NavigationTop></NavigationTop>
    <div id="content" :style="style">
      <router-view/>
    </div>
    <NavigationBottom></NavigationBottom>
  </div>
</template>

<script>
import NavigationTop from '@/components/NavigationTop.vue'
import NavigationBottom from '@/components/NavigationBottom.vue'
import { bus } from './main'

export default {
  name: 'App',
  components: {
    'NavigationTop': NavigationTop,
    'NavigationBottom': NavigationBottom
  },
  data () {
    return {
      headerOffset: 30,
      isSticky: false
    }
  },
  computed: {
    style () {
      return 'padding-top: ' + this.headerOffset + 'px; padding-bottom: 30px;'
    }
  },
  created () {
    bus.$on('doStickyHeader', (offset) => {
      this.isSticky = true
      this.headerOffset = 2 * offset
    })
    bus.$on('undoStickyHeader', () => {
      this.isSticky = false
      this.headerOffset = 30
    })
  }
}
</script>

<style lang="scss">
@import 'src/styles/bulma.scss';
html {
  overflow-y: auto !important;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: $black;
}
</style>
