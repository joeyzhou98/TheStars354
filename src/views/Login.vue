<template>
  <div>
  <div id="loginPage">
    <h2>Login Page</h2>
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
    <button v-on:click="login">Login</button>
  </div>
  <div>
    <p>By continuing, you agree to 354 STARS's Conditions of Use and Privacy Notice. </p>
    <br/>
    <p>New to 354 STARS</p>
    <br/>
    <router-link to="/register">Create New Account</router-link>
  </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      name: 'Login'
    }
  },
  method: {
    login () {
      ;
    }
  }
}
</script>

<style scoped lang="scss">
#loginPage {
  margin: 32px 0px;
  width: 25vw;
  display: inline-block;
}
</style>
