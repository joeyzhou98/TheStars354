<template>
  <div id="app">
    <NavigationTop></NavigationTop>
    <div id="content">
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
  created () {
    bus.$on('doStickyHeader', () => {
      document.getElementById('content').className = 'sticky'
    })
    bus.$on('undoStickyHeader', () => {
      document.getElementById('content').className = ''
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
#content {
  padding: 30px 0px;
}
.sticky#content {
  padding-top: 80px;
}
</style>
