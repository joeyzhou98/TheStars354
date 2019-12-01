<template>
<div>
  <div v-if="!isLoggedIn" style="margin: 20px">
    Oops! You are not supposed to be here.<br>
    <router-link to="/login">Log In</router-link><br>
    <router-link to="/">Back to Home Page</router-link>
  </div>
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
    <hr class="my-4">

    <keep-alive>
      <b-tabs lazy justified>
        <b-tab title="Buyer Profile" v-if=!(isAdmin)>
          <Address></Address>
          <hr class="my-4">
          <PayingInfo></PayingInfo>
          <hr class="my-4">
          <PasswordReset></PasswordReset>
          <hr class="my-4">
          <OrderHistory></OrderHistory>
          <hr class="my-4">
          <ReviewHistory></ReviewHistory>
        </b-tab>
        <b-tab title="Seller Profile" v-if=!(isAdmin)>
          <SellerInfo></SellerInfo>
          <hr class="my-4">
          <SellingInfo></SellingInfo>
          <hr class="my-4">
          <SellerOrderHistory></SellerOrderHistory>
        </b-tab>
        <b-tab title="Admin Control Center" v-if=(isAdmin)>
          <AllUser></AllUser>
          <hr class="my-4">
          <AdminStat></AdminStat>
        </b-tab>
      </b-tabs>
    </keep-alive>
    <br/>
    <b-button type="submit" variant="dark" @click="userLogout">Logout</b-button>
    </b-card>
  </div>
</div>
</template>

<script>
import axios from 'axios'
import Address from '@/components/Address.vue'
import PayingInfo from '@/components/PayingInfo.vue'
import PasswordReset from '@/components/PasswordReset.vue'
import OrderHistory from '@/components/OrderHistory.vue'
import SellingInfo from '@/components/SellingInfo.vue'
import SellerInfo from '@/components/SellerInfo.vue'
import SellerOrderHistory from '@/components/SellerOrderHistory.vue'
import ReviewHistory from '../components/ReviewHistory'
import AllUser from '../components/AllUser'
import AdminStat from '../components/AdminStat'

export default {
  components: {
    AllUser,
    Address,
    PayingInfo,
    PasswordReset,
    OrderHistory,
    ReviewHistory,
    SellingInfo,
    SellerInfo,
    SellerOrderHistory,
    AdminStat
  },
  data () {
    return {
      users: {
        uid: '',
        username: '',
        useremail: '',
        role: ''
      }
    }
  },
  computed: {
    isLoggedIn () {
      return this.$store.state.isLoggedIn
    },
    welcomeMessage () {
      return 'Welcome ' + this.$store.state.username
    },
    isAdmin () {
      return this.$store.state.role === 'admin'
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
