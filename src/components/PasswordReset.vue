<template>
  <div>
    <b-card-body class="text-left">
      <h2>Password Reset</h2>
      <b-button variant="outline-info" @click="findModal('passwordReset')">
        <icon name="edit"></icon>
      </b-button>
    </b-card-body>

    <b-modal ref="passwordReset" hide-footer title="Password Reset">
      <form ref="form">
        <b-form-group
      id="input-group-3"
      label="Password:"
      label-for="input-3"
      align="left"
      :invalid-feedback="invalidFeedbackPassword"
      >
        <b-form-input
          id="input-3"
          v-model="password"
          :state="statePassword"
          type="password"
          required
          placeholder="Enter password"
        >
        </b-form-input>
        <small class="text-muted">Minimum 8 characters, at least 1 uppercase letter, 1 lowercase letter, 1 number and 1 special character</small>
      </b-form-group>

      <b-form-group
      id="input-group-4"
      label="Password again:"
      label-for="input-4"
      align="left"
      :invalid-feedback="invalidFeedbackPasswordAgain"
      >
        <b-form-input
          id="input-4"
          v-model="passwordAgain"
          :state="statePasswordAgain"
          type="password"
          required
          placeholder="Enter password again"
        >
        </b-form-input>
      </b-form-group>
      </form>
      <b-button type="submit" variant="outline-success" @click.prevent="resetPassword" block>Reset</b-button>
    </b-modal>
    <b-modal id="notification" ref="notification">
      <h5>Your password has been reset successfully!</h5>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'
import md5 from 'js-md5'

export default {
  data () {
    return {
      password: '',
      passwordAgain: ''
    }
  },
  methods: {
    findModal (modal) {
      this.$refs[modal].show()
    },
    resetPassword () {
      var url = 'api/authentication/changePassword?username=' + encodeURIComponent(this.$store.state.username) + '&password=' + encodeURIComponent(md5(this.password))
      axios
        .put(url)
        .then((response) => {
          this.$bvModal.show('notification')
        })
        .catch(error => {
          if (error.response.status === 404) {
            console.log(JSON.stringify(error.response.data))
            this.$router.push('/')
          }
        })
      this.$refs['passwordReset'].hide()
    }
  },
  computed: {
    statePassword () {
      if (this.password.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/)) {
        return true
      } else if (this.password === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackPassword () {
      if (this.password.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/) || this.password === '') {
        return ''
      } else {
        return 'Please enter your password'
      }
    },
    statePasswordAgain () {
      if (this.passwordAgain === '') {
        return null
      } else if (this.passwordAgain === this.password) {
        return true
      } else {
        return false
      }
    },
    invalidFeedbackPasswordAgain () {
      if (this.passwordAgain === this.password || this.password === '') {
        return ''
      } else {
        return 'the password doesn\'t match'
      }
    }
  }
}
</script>

<style scoped lang="scss">

</style>
