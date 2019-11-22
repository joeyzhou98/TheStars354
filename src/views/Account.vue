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

    <keep-alive>
      <b-tabs lazy justified>
        <b-tab title="Buyer Profile"> <br />Buyer Profile</b-tab>
        <b-tab title="Seller Profile"> <br />Seller Profile</b-tab>
        <b-tab title="Admin Control Center" v-if=(isAdmin)>
          <b-card-group>
            <b-card-body>
              <p>All users registered in the database:</p>
              <b-row v-for="user in this.users" :key="user">
                <b-col>
                  <p>{{user.uid}}</p>
                </b-col>
                <b-col>
                  <p>{{user.username}}</p>
                </b-col>
                <b-col>
                  <p>{{user.useremail}}</p>
                </b-col>
                <b-col>
                  <b-button type="submit" variant="dark" @click="deleteUser(user.username)">Delete this user</b-button>
                </b-col>
              </b-row>
          </b-card-body>
          </b-card-group>
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

export default {
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
  mounted: function mounted () {
    if (this.isAdmin) {
      this.getAllUser()
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
    },
    getAllUser () {
      let url = 'api/authentication/allUser'
      axios
        .get(url)
        .then(response => {
          this.users = response.data
          console.log(this.users)
        })
        .catch(error => alert(error))
    },
    deleteUser (uid) {
      let url = 'api/authentication/deleteUser/' + uid
      axios
        .delete(url)
        .then(response => {
          this.getAllUser()
        })
        .catch(error => alert(error))
    }
  }
}
</script>

<style scoped lang="scss">

</style>
