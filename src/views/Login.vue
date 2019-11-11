<template>
  <div>
    <br/><br/>
    <b-card
      bg-variant="light"
      title="Login"
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
          v-model="form.username"
          :state="stateUserName"
          trim
          required
          placeholder="Enter user name"
        >
        </b-form-input>
      </b-form-group>

      <b-form-group
      id="input-group-2"
      label="Password:"
      label-for="input-2"
      align="left"
      :invalid-feedback="invalidFeedbackPassword"
      >
        <b-form-input
          id="input-2"
          v-model="form.password"
          :state="statePassword"
          type="password"
          required
          placeholder="Enter password"
        >
        </b-form-input>
      </b-form-group>
      <p class="error" v-if="errors.message">{{ errors.message }}</p>

      <b-link href="#/findPassword">Forget your password?</b-link>
      <br/><br/>
      <b-link href="#/register">Create an account</b-link>
      <br/><br/>
      <b-button type="submit" variant="dark">Login</b-button>

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
        username: '',
        password: ''
      },
      errors: {
        message: ''
      }
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      // alert(JSON.stringify(this.form))
      var url = 'api/authentication/login?username=' + encodeURIComponent(this.form.username) + '&password=' + encodeURIComponent(md5(this.form.password))
      this.sendAxiosRequest(url)
    },
    sendAxiosRequest (url) {
      axios
        .post(url)
        .then((response) => {
          // alert(JSON.stringify(response.data))
          this.$store.commit('login', response.data)
          this.$router.push('/')
        })
        .catch(error => {
          if (error.response.status === 404) {
            console.log(JSON.stringify(error.response.data))
            this.errors.message = error.response.data['message']
          }
        })
    }
  },
  computed: {
    stateUserName () {
      if (this.form.username.match(/^[A-Za-z\d]{5,15}$/)) {
        return true
      } else if (this.form.username === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackUserName () {
      if (this.form.username.match(/^[A-Za-z\d]{5,15}$/) || this.form.username === '') {
        return ''
      } else {
        return 'Please enter a valid user name'
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
    }
  }
}
</script>

<style scoped lang="scss">
.error {
    color: red;
}
</style>
