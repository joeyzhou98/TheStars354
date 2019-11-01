<template>
  <div>
    <b-button type="submit" variant="dark" @click='logout' href="#/">Logout</b-button>
  </div>
</template>

<script>

export default {
  name: 'Logout',
  methods: {
    logout () {
      this.$store.dispatch('LOGOUT')
        .then(response => {
          this.$router.push('/')
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped lang='scss'>
/*@media screen{
  .column{
    background-color: yellowgreen;
  }
}*/
</style>
