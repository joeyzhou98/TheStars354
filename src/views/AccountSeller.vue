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

    <b-card no-body>
      <div v-if="tabNo===1">
      <b-card-header header-tag="nav">
        <b-nav card-header tabs fill>
          <b-nav-item @click="tabNo=1" active >Seller Profile</b-nav-item>
          <b-nav-item @click="tabNo=2">Selling Product Information</b-nav-item>
        </b-nav>
      </b-card-header>
      <Address></Address>
      <hr class="my-4">
      <PayingInfo></PayingInfo>
      <hr class="my-4">
      <PasswordReset></PasswordReset>
      </div>

      <div v-if="tabNo===2">
        <b-card-header header-tag="nav">
        <b-nav card-header tabs fill>
          <b-nav-item @click="tabNo=1">Seller Profile</b-nav-item>
          <b-nav-item @click="tabNo=2" active>Selling Product Information</b-nav-item>
        </b-nav>
      </b-card-header>
        <SellingInfo></SellingInfo>
      </div>
    </b-card>
    <br/>
    <b-button type="submit" variant="dark" @click="userLogout">Logout</b-button>
    </b-card>
  </div>
</template>

<script>
import axios from 'axios'
import App from '../App'
import Address from '@/components/Address.vue'
import PayingInfo from '@/components/PayingInfo.vue'
import PasswordReset from '@/components/PasswordReset.vue'
import SellingInfo from '@/components/SellingInfo.vue'

export default {
  components: {
    Address,
    PayingInfo,
    PasswordReset,
    SellingInfo
  },
  data () {
    return {
      user: {
        username: '',
        email: ''
      },
      tabNo: 1
    }
  },
  mounted () {
    this.getUserAuthInfo()
  },
  computed: {
    welcomeMessage () {
      return 'Welcome ' + this.user.username
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
        .then(response => { this.user.username = response.data['username'] })
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
