<template>
  <div>
    <b-card
      bg-variant="light"
      title="Create account"
      style="width: 25rem; display: inline-block;"
    >
    <b-form @submit="onSubmit">
      <b-form-group
        id="input-group-1"
        label="User name:"
        label-for="input-1"
        align="left"
        :invalid-feedback="invalidFeedbackUserName"
      >
        <b-form-input
          id="input-1"
          v-model="form.userName"
          :state="stateUserName"
          trim
          required
          placeholder="Enter user name"
        >
        </b-form-input>
        <small class="text-muted">between 5 to 15 characters using numbers and letters only</small>
      </b-form-group>

      <b-form-group
        id="input-group-2"
        label="Email address:"
        label-for="input-2"
        align="left"
        :invalid-feedback="invalidFeedbackEmail"
      >
        <b-form-input
          id="input-2"
          v-model="form.email"
          :state="stateEmail"
          trim
          type="email"
          required
          placeholder="Enter email"
        >
        </b-form-input>
      </b-form-group>

      <b-form-group
      id="input-group-3"
      label="Password:"
      label-for="input-3"
      align="left"
      :invalid-feedback="invalidFeedbackPassword"
      >
        <b-form-input
          id="input-3"
          v-model="form.password"
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
          v-model="form.passwordAgain"
          :state="statePasswordAgain"
          type="password"
          required
          placeholder="Enter password again"
        >
        </b-form-input>
      </b-form-group>

      <b-button type="submit" variant="dark">Resgiser</b-button>
    </b-form>
  </b-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      form: {
        userName: '',
        email: '',
        password: '',
        passwordAgain: ''
      }
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      alert(JSON.stringify(this.form))
      // for testing, make sure to pass the MD5 hashed password in the following line
      var url = 'api/authentication/registration?username=' + encodeURIComponent(this.form.userName) + '&email=' + encodeURIComponent(this.form.email) + '&password=' + encodeURIComponent(this.form.password)
      this.sendAxiosRequest(url)
    },
    // for testing purpose, make sure to add proper logic when the registration is successful (ex.redirect to homepage etc.)
    sendAxiosRequest (url) {
      axios
        .post(url)
        .then(response => { alert(JSON.stringify(response.data)) })
        .catch(error => alert(error))
    }
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
      } else if (this.form.passwordAgain.match(this.form.password)) {
        return true
      } else {
        return false
      }
    },
    invalidFeedbackPasswordAgain () {
      if (this.form.passwordAgain.match(this.form.password) || this.form.password === '') {
        return ''
      } else {
        return 'the password doesn\'t match'
      }
    }
  }
}
</script>

<style scoped lang="scss">
/*@media screen{
  .column{
    background-color: yellowgreen;
  }
}*/
</style>
