<template>
<div>
  <div v-if="!isLoggedIn" style="margin: 20px">
    Oops! You are not supposed to be here.<br>
    <router-link to="/login">Log In</router-link><br>
    <router-link to="/">Back to Home Page</router-link>
  </div>
  <div v-else>
    <b-card
    :title="welcomeMessage"
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
    <b-button type="submit" variant="dark" @click="userLogout">Logout</b-button>
    </b-card>
  </div>
</div>
</template>

<script>
import axios from 'axios'

export default {
  computed: {
    isLoggedIn () {
      return this.$store.state.isLoggedIn
    },
    welcomeMessage () {
      return 'Welcome ' + this.$store.state.username
    }
  },
  methods: {
    userLogout () {
      let url1 = 'api/authentication/logout/access'
      let url2 = 'api/authentication/logout/refresh'
      axios
        .post(url1)
        .then(response => {
          console.log('access token revoke', response.data)
        })
        .catch(error => alert(error))
      axios
        .post(url2)
        .then(response => {
          console.log('refresh token revoke', response.data)
        })
        .catch(error => alert(error))
      this.$store.commit('logout')
      console.log('isLoggedIn', this.isLoggedIn)
      this.$router.push('/')
    }
  }
}
</script>

<style scoped lang="scss">

</style>
