<template>
  <div id="footer">
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
#footer{
  display: inline-block;
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  background-color: $lightblue;
}
nav {
  padding: 15px;
  a {
    margin: 10px;
    font-weight: bold;
    color: $black;
    &:hover {
      color: $mainblue;
    }
  }
}
</style>
