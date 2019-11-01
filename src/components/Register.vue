<template>
  <div>
    <b-card
      bg-variant='light'
      title='Create account'
      style='width: 25rem; display: inline-block;'
    >
    <b-form @submit='onSubmit'>
      <b-form-group
        id='input-group-1'
        label='User name:'
        label-for='input-1'
        align='left'
        :invalid-feedback='invalidFeedbackUserName'
      >
        <b-form-input
          id='input-1'
          v-model='user.username'
          :state='stateUserName'
          trim
          required
          placeholder='Enter user name'
        >
        </b-form-input>
        <small class='text-muted'>between 5 to 15 characters using numbers and letters only</small>
      </b-form-group>

      <b-form-group
        id='input-group-2'
        label='Email address:'
        label-for='input-2'
        align='left'
        :invalid-feedback='invalidFeedbackEmail'
      >
        <b-form-input
          id='input-2'
          v-model='user.email'
          :state='stateEmail'
          trim
          type='email'
          required
          placeholder='Enter email'
        >
        </b-form-input>
      </b-form-group>

      <b-form-group
      id='input-group-3'
      label='Password:'
      label-for='input-3'
      align='left'
      :invalid-feedback='invalidFeedbackPassword'
      >
        <b-form-input
          id='input-3'
          v-model='user.password'
          :state='statePassword'
          type='password'
          required
          placeholder='Enter password'
        >
        </b-form-input>
        <small class='text-muted'>Minimum 8 characters, at least 1 uppercase letter, 1 lowercase letter, 1 number and 1 special character(@$!%*?&)</small>
      </b-form-group>

      <b-form-group
      id='input-group-4'
      label='Password again:'
      label-for='input-4'
      align='left'
      :invalid-feedback='invalidFeedbackPasswordAgain'
      >
        <b-form-input
          id='input-4'
          v-model='user.passwordAgain'
          :state='statePasswordAgain'
          type='password'
          required
          placeholder='Enter password again'
        >
        </b-form-input>
      </b-form-group>

      <b-button type='submit' variant='dark' @click='register'>Register</b-button>
      <b-alert v-model='user.showDismissibleAlert' variant='danger' dismissible>The username already exist.</b-alert>
    </b-form>
  </b-card>
  </div>
</template>

<script>
import md5 from 'js-md5'
import axios from 'axios'

export default {
  name: 'Register',
  data () {
    return {
      user: {
        username: '',
        email: '',
        password: '',
        passwordAgain: '',
        showDismissibleAlert: false
      }
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      var url = 'api/authentication/registration?username=' + encodeURIComponent(this.user.username) + '&email=' + encodeURIComponent(this.user.email) + '&password=' + encodeURIComponent(md5(this.user.password))
      this.sendAxiosRequest(url)
    },
    sendAxiosRequest (url) {
      axios
        .post(url)
        .then(response => {
          this.$router.push('/login-register')
          alert('sucessfully regisetered')
          this.user.showDismissibleAlert = false
        })
        .catch(error => {
          this.user.showDismissibleAlert = true
          console.log(error)
        })
    }/* ,
    register () {
      if (this.stateUserName && this.stateEmail && this.statePassword && this.statePasswordAgain) {
        this.$store.dispatch('REGISTER', {
          username: this.user.username,
          email: this.user.email,
          password: md5(this.user.password)
        })
        // .then(({status}) => {
          .then(response => {
            this.$router.push('/login-register')
            this.user.showDismissibleAlert = false
          })
          .catch(error => {
            this.user.showDismissibleAlert = true
            console.log(error)
          })
      }
    } */
  },
  computed: {
    stateUserName () {
      if (this.user.username.match(/^[A-Za-z\d]{5,15}$/)) {
        return true
      } else if (this.user.username === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackUserName () {
      if (this.user.username.match(/^[A-Za-z\d]{5,15}$/) || this.user.username === '') {
        return ''
      } else {
        return 'Please enter a valid user name'
      }
    },
    stateEmail () {
      if (this.user.email.match(/^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$/)) {
        return true
      } else if (this.user.email === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackEmail () {
      if (this.user.email.match(/^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$/) || this.user.email === '') {
        return ''
      } else {
        return 'Please enter a valid email account'
      }
    },
    statePassword () {
      if (this.user.password.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/)) {
        return true
      } else if (this.user.password === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackPassword () {
      if (this.user.password.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/) || this.user.password === '') {
        return ''
      } else {
        return 'Please enter your password'
      }
    },
    statePasswordAgain () {
      if (this.user.passwordAgain === '') {
        return null
      } else if (this.user.passwordAgain.match(this.user.password)) {
        return true
      } else {
        return false
      }
    },
    invalidFeedbackPasswordAgain () {
      if (this.user.passwordAgain.match(this.user.password) || this.user.password === '') {
        return ''
      } else {
        return 'the password doesn\'t match'
      }
    }
  }
}
</script>

<style scoped lang='scss'>
/*@media screen{
  .column{
    background-color: yellowgreen;
  }
}*/
</style>
