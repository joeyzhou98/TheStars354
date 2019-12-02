<template>
    <div>
        <b-card-body>
            <b-card>
                <b-row>Registered Date: {{membership_date.substring(0,16)}}</b-row>
                <b-row>Total Commission: ${{total_commission}}</b-row>
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
  methods: {},
  mounted () {
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
</script>

<style scoped lang="scss">

</style>
