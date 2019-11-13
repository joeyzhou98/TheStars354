<template>
  <div>
    <br/><br/>
    <b-card
      bg-variant="light"
      title="Create account"
      style="width: 25rem; display: inline-block;"
    >
    <b-form @submit="onSubmit">
      <b-form-group
      id="input-group-1"
      label="Enter your new password:"
      label-for="input-1"
      align="left"
      :invalid-feedback="invalidFeedbackPassword"
      >
        <b-form-input
          id="input-1"
          v-model="form.password"
          :state="statePassword"
          type="password"
          required
          placeholder="Enter new password"
        >
        </b-form-input>
        <small class="text-muted">Minimum 8 characters, at least 1 uppercase letter, 1 lowercase letter, 1 number and 1 special character</small>
      </b-form-group>

      <b-form-group
      id="input-group-2"
      label="Your new password again:"
      label-for="input-2"
      align="left"
      :invalid-feedback="invalidFeedbackPasswordAgain"
      >
        <b-form-input
          id="input-2"
          v-model="form.passwordAgain"
          :state="statePasswordAgain"
          type="password"
          required
          placeholder="Enter your new password again"
        >
        </b-form-input>
      </b-form-group>

      <b-button type="submit" variant="dark">Continue</b-button>
    </b-form>
  </b-card>
  </div>
</template>

<script>
import axios from 'axios'
import md5 from 'js-md5'

export default {
  data () {
    return {
      form: {
        password: '',
        passwordAgain: ''
      },
      username: ''
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      var url = 'api/authentication/changePassword?username=' + this.username + '&password=' + encodeURIComponent(md5(this.form.password))
      this.resetPassword(url)
    },
    resetPassword (url) {
      axios
        .put(url)
        .then((response) => {
          alert(JSON.stringify(response.data))
          this.$router.push('/login')
        })
        .catch(error => {
          if (error.response.status === 400) {
            console.log(JSON.stringify(error.response.data))
            this.$router.push('/')
          }
        })
    }
  },
  mounted () {
    var token = this.$route.params.token
    var url = 'api/authentication/changePassword/' + token
    this.username = this.$route.params.username
    alert(url)
    axios
      .get(url)
      .then((response) => {
        alert(JSON.stringify(response.data))
      })
      .catch(error => {
        if (error.response.status === 404) {
          console.log(JSON.stringify(error.response.data))
        }
      })
  },
  computed: {
    stateUserName () {
      if (this.form.userName.match(/^[A-Za-z\d]{5,15}$/)) {
        return true
      } else if (this.form.userName === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackUserName () {
      if (this.form.userName.match(/^[A-Za-z\d]{5,15}$/) || this.form.userName === '') {
        return ''
      } else {
        return 'Please enter a valid user name'
      }
    },
    stateEmail () {
      if (this.form.email.match(/^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$/)) {
        return true
      } else if (this.form.email === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackEmail () {
      if (this.form.email.match(/^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$/) || this.form.email === '') {
        return ''
      } else {
        return 'Please enter a valid email account'
      }
    },
    statePassword () {
      if (this.form.password.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/)) {
        return true
      } else if (this.form.password === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackPassword () {
      if (this.form.password.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/) || this.form.password === '') {
        return ''
      } else {
        return 'Please enter your password'
      }
    },
    statePasswordAgain () {
      if (this.form.passwordAgain === '') {
        return null
      } else if (this.form.passwordAgain === this.form.password) {
        return true
      } else {
        return false
      }
    },
    invalidFeedbackPasswordAgain () {
      if (this.form.passwordAgain === this.form.password || this.form.password === '') {
        return ''
      } else {
        return 'the password doesn\'t match'
      }
    }
  }
}
</script>

<style scoped lang="scss">
.error {
    color: red;
}
</style>
