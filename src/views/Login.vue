<template>
  <div>
    <b-card
      bg-variant="light"
      title="Login"
      style="width: 25rem; display: inline-block;"
    >
    <b-form @submit="onSubmit">
      <b-form-group
        id="input-group-1"
        label="Email address:"
        label-for="input-1"
        align="left"
        :invalid-feedback="invalidFeedbackEmail"
      >
        <b-form-input
          id="input-1"
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

      <b-link href="#/findPassword">Forget your password?</b-link>
      <br/><br/>
      <b-button type="submit" variant="dark" href="#/Account">Login</b-button>

    </b-form>
  </b-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      form: {
        email: '',
        password: ''
      }
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      alert(JSON.stringify(this.form))
    }
  },
  computed: {
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
