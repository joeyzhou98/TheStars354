<template>
  <div>
    <b-card-body class="text-left">
      <b-card>
        <b-row>Seller Name: {{membership_date}}</b-row>
        <b-row>Membership Date: {{membership_date}}</b-row>
        <b-row>Rating: {{membership_date}}</b-row>
        <b-row>Total Commission: {{membership_date}}</b-row>
      </b-card>
    </b-card-body>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      membership_date: '',
      total_commission: '' // more info
    }
  },
  methods: {

  },
  mounted: {
    getUserInfo () {
      var url = 'api/resource/sellerInfo?uid=' + encodeURIComponent(this.$store.state.uid)
      axios
        .get(url)
        .then(response => {
          this.membership_date = response.data['membership_date']
          this.total_commission = response.data['total_commission']
        })
        .catch(error => alert(error))
    }
  }
}
</script>

<style scoped lang="scss">

</style>
