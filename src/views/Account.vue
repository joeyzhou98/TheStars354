<template>
  <div id="registerSection" class="column is-one-third">
    <div class="box">
    <h1 class="title">Account page!!!</h1>
    <b-field label="Your name"
      type="is-success"
      message="This username is available">
      <b-input  pack="fas" icon="user" value="name" maxlength="30"></b-input>
    </b-field>

    <b-field label="Email"
      type="is-danger"
      message="This email is invalid">
      <b-input placeholder="Email"
        type="email"
        icon-pack="fas"
        icon="envelope"
        maxlength="30">
      </b-input>
    </b-field>

    <b-field label="Password"  type="is-warning"
      :message="['Password is too short', 'Password must have at least 8 characters']">
      <b-input type="password"
        value="iwantmytreasure"
        password-reveal>
      </b-input>
    </b-field>

    <b-field label="Password again"  type="is-warning"
      :message="['Password is too short', 'Password must have at least 8 characters']">
      <b-input type="password"
        value="iwantmytreasure">
      </b-input>
    </b-field>
    <b-button v-on:click="creatAccount" tag="router-link"
                to="/account"
                type="is-link is-dark">Register</b-button>
    <p>By creating an account, you agree to 354 STARS's Conditions of Use and Privacy Notice. </p>
    </div>
    <div class="box">
    <h1 class="subtitle">Already have an account?</h1>
    <router-link to="/login">Sign In</router-link>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      name: 'Register'
    }
  },
  method: {
    creatAccount () {
      ;
    }
  }
}
</script>

<style scoped lang="scss">
#registerSection {
  display: inline-block;
}
</style>
