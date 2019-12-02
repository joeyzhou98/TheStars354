<template>
  <div>
    <b-card-body>
        <p>All users registered in the database:</p>
        <b-row v-for="user in this.users" :key="user">
            <b-col><p>{{user.uid}}</p></b-col>
            <b-col><p>{{user.username}}</p></b-col>
            <b-col><p>{{user.useremail}}</p></b-col>
            <b-col>
                <b-button v-if="user.role !== 'admin'" type="submit" variant="dark" @click="deleteUser(user.username)">Delete this user</b-button>
            </b-col>
        </b-row>
    </b-card-body>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AllUser',
  data () {
    return {
      users: []
    }
  },
  mounted () {
    this.getAllUsers()
  },
  methods: {
    getAllUsers () {
      let url = 'api/authentication/allUser'
      axios
        .get(url)
        .then(response => {
          this.users = response.data
          console.log(this.users)
        })
        .catch(error => alert(error))
    },
    deleteUser (username) {
      let url = 'api/authentication/deleteUser/' + encodeURIComponent(username)
      axios
        .delete(url)
        .then(response => {
          this.getAllUsers()
        })
        .catch(error => alert(error))
    }
  }
}
</script>

<style scoped>

</style>
