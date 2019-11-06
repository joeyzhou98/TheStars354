<template>
  <div>
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
</template>

<script>
import axios from 'axios'
import App from '../App'

export default {
  data () {
    return {
      username: '',
      email: ''
    }
  },
  mounted () {
    this.getUserAuthInfo()
  },
  computed: {
    welcomeMessage () {
      return 'Welcome ' + this.username
    }
  },
  methods: {
    getUserAuthInfo () {
      var url = 'api/resource/user'
      this.sendAxiosRequest(url)
    },
    sendAxiosRequest (url) {
      axios
        .get(url)
        .then(response => { this.username = response.data['username'] })
        .catch(error => alert(error))
    },
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
      App.loginStatus.setLoginStatus(false)
      console.log('loginStatus', App.loginStatus.state)
      this.$router.push('/')
    }
  }
}
</script>

<style scoped lang="scss">

</style>
