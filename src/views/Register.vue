<template>
  <div>
    <section id="registerSection">
    <h1>Create account</h1>
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

    <button v-on:click="creatAccount">Create your 354 STARS account</button>
    </section>
    <p>By creating an account, you agree to 354 STARS's Conditions of Use and Privacy Notice. </p>
    <section id="loginSection">
    <p>Already have an account?
      <router-link to="/login">Sign In</router-link>
    </p>
    </section>
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
  margin: 32px 0px;
  width: 25vw;
  display: inline-block;
}
#loginSection {
  margin: 32px 0px;
  width: 25vw;
  display: inline-block;
}
</style>
