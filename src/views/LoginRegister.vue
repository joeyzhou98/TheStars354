<template>
  <div>
    <b-row>
      <b-col>
        <Register></Register>
      </b-col>

      <b-col>
        <Login></Login>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'

export default {
  components: {
    Login,
    Register
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
