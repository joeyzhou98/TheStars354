<template>
  <div>
    <b-card bg-variant='light' title='Login' style='width: 25rem; display: inline-block;'>
      <b-form @submit='onSubmit'>
        <b-form-group
          id='input-group-5'
          label='User name:'
          label-for='input-5'
          align='left'
          :invalid-feedback='invalidFeedbackUserName'
        >
          <b-form-input
            id='input-5'
            v-model='user.username'
            :state='stateUserName'
            trim
            required
            placeholder='Enter user name'
          ></b-form-input>
        </b-form-group>

        <b-form-group
          id='input-group-6'
          label='Password:'
          label-for='input-6'
          align='left'
          :invalid-feedback='invalidFeedbackPassword'
        >
          <b-form-input
            id='input-6'
            v-model='user.password'
            :state='statePassword'
            type='password'
            required
            placeholder='Enter password'
          ></b-form-input>
        </b-form-group>

        <b-link href='#/findPassword'>Forget your password?</b-link>
        <br />
        <br />
        <b-button type='submit' variant='dark' @click='login'>Login</b-button>
        <b-alert v-model='user.showDismissibleAlert' variant='danger' dismissible>The username or the password are incorrect.</b-alert>
      </b-form>
    </b-card>
  </div>
</template>

<script>
import md5 from 'js-md5'

export default {
  name: 'Login',
  data () {
    return {
      user: {
        username: '',
        password: '',
        showDismissibleAlert: false
      }
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      alert(JSON.stringify(this.user))
    },
    login () {
      this.$store.dispatch('LOGIN', {
        username: this.user.username,
        password: md5(this.user.password)
      })
      // .then(success => {
        .then(response => {
          this.$router.push('/account')
          this.user.showDismissibleAlert = false
        })
        .catch(error => {
          this.user.showDismissibleAlert = true
          console.log(error)
        })
    }
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
      if (this.user.password.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/) ||
        this.user.password === ''
      ) {
        return ''
      } else {
        return 'Please enter your password'
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
