<template>
  <div id="bot_bar">
    <nav>
      <router-link v-for="route in links" v-bind:key="route.id"
                   :to="`${route.page}`">{{route.text}}</router-link>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'NavigationBottom',
  data () {
    return {
      links: [
        {
          id: 0,
          text: 'FAQ',
          page: '/faq'
        },
        {
          id: 1,
          text: 'About Us',
          page: '/about'
        }
      ]
    }
  }
}
</script>

<style scoped lang="scss">
nav {
  padding: 30px;
  a {
    margin: 10px;
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
