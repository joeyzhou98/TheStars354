<template>
  <div id="loginSection" class="column is-one-third">
    <div class="box">
    <h1 class="title">Login</h1>
    <b-field label="Email Address"
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
    <router-link to="/findPasswords">Forget your password?</router-link>
    <br/>
    <b-button v-on:click="login" tag="router-link"
                to="/account"
                type="is-link is-dark">Login</b-button>
  </div>
  <div class="box">
    <h1 class="subtitle">New to 354 STARS</h1>
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
#loginSection {
  display: inline-block;
}
</style>
