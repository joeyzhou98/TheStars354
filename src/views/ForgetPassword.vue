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
        label="Enter the email address associated with your account:"
        label-for="input-1"
        align="left"
        :invalid-feedback="invalidFeedbackEmail"
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          :state="stateEmail"
          trim
          required
          placeholder="Enter your email address"
        >
        </b-form-input>
      </b-form-group>
      <p class="error" v-if="errors.message">{{ errors.message }}</p>

      <br/><br/>
      <b-button type="submit" variant="dark">Continue</b-button>
    </b-form>
      <div class="Popup">
        <!-- Start of modal section -->
        <b-modal id="notification" ref="notification">
          <h5 class="notification_text">An email that contains the password reset link has been sent to the email address you provided, please check your email inbox.</h5>
          <template slot="modal-footer">
            <b-button class="continue-btn" @click="GoToHomePage">Continue</b-button>
          </template>
        </b-modal>
        <!-- End of modal section -->
      </div>
  </b-card>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      form: {
        email: ''
      },
      errors: {
        message: ''
      }
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      var url = 'api/authentication/password/forget?email=' + encodeURIComponent(this.form.email)
      this.sendAxiosRequest(url)
    },
    sendAxiosRequest (url) {
      axios
        .post(url)
        .then((response) => {
          // alert(JSON.stringify(response.data))
          this.$bvModal.show('notification')
        })
        .catch(error => {
          if (error.response.status === 404) {
            console.log(JSON.stringify(error.response.data))
            this.errors.message = error.response.data['message']
          }
        })
    },
    GoToHomePage () {
      this.$router.push('/')
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
    }
  }
}
</script>

<style scoped lang="scss">
.error {
    color: red;
}
.continue-btn {
  background: none;
  color: $darkblue;
  border-color: $darkblue;
  &:hover {
    color: $mainblue;
    background: none;
    border-color: $mainblue;
  }
  &:active {
    position:relative;
    top:1px;
  }
}
h5.notification_text{
  color: $darkgray;
  font-size: larger;
 }
</style>
