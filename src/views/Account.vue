<template>
  <div>
    <b-card
    title="Welcome XXX"
    img-src="https://picsum.photos/600/300/?image=25"
    img-alt="Image"
    img-top
    tag="article"
    style="width: 60rem; display: inline-block;"
    class="mb-2"
  >
    <b-card-text>
      You can change your personal details, manage your orders, and much more.
    </b-card-text>

    <b-nav tabs justified>
      <b-nav-item active href="#/login/">PROFILE</b-nav-item>
      <b-nav-item active href="#/login/">ORDER HISTORY</b-nav-item>
      <b-nav-item active href="#/login/">XXXXXX</b-nav-item>
      <b-nav-item active href="#/login/">XXXXXX</b-nav-item>
    </b-nav>
    <br/>
    <b-button type="submit" variant="dark" @click='logout' href="#/">Logout</b-button>
    </b-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  methods: {
    logout (evt) {
      evt.preventDefault()
      var url = 'api/authentication/logout/access'
      this.sendAxiosRequest(url)
    },
    sendAxiosRequest (url) {
      axios
        .post(url)
        .then(response => {
          localStorage.removeItem('token')
          this.$router.push('/')
        })
        .catch(error => {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped lang="scss">

</style>
