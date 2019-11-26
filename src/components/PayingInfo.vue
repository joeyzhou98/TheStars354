<template>
  <div>
    <b-card-body class="text-left">
      <h2>Your PayPal Account</h2>
      <b-card no-body class="overflow-hidden" v-if="haspaypal">
        <b-card-body>{{paypal}}
          <b-button variant="outline" title="edit" @click="paypalModal('paypalModal')">
            <icon name="edit"></icon>
          </b-button>
          <b-button variant="outline" title="delete" @click="deletepaypal">
            <icon name="trash-alt"></icon>
          </b-button>
        </b-card-body>
      </b-card>

      <br/>
      <b-button variant="outline-info" @click="paypalModal('paypalModal')" v-if="!haspaypal">
        <icon name="plus"></icon>
      </b-button>
    </b-card-body>

    <b-modal ref="paypalModal" hide-footer title="Add or Edit paypal Account">
      <form ref="paypalForm">
        <b-form-group
          :state="paypalState"
          label="paypal"
          label-for="paypal-input"
          :invalid-feedback="invalidFeedbackpaypal"
        >
          <b-form-input
            id="paypal-input"
            v-model="paypalInput"
            :state="paypalState"
            trim
            required
            placeholder="Enter Your paypal Account"
          ></b-form-input>
        </b-form-group>
      </form>
      <b-button type="submit" variant="outline-success" @click.prevent="addpaypal" block>Submit</b-button>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      paypal: '',
      paypalInput: '',
      haspaypal: false
    }
  },
  mounted () {
    var url = 'api/resource/buyerInfo?username=' + encodeURIComponent(this.$store.state.username)
    axios
      .get(url)
      .then(response => {
        this.paypal = response.data['paypal']
        if (this.paypal !== '' && this.paypal !== null) {
          this.haspaypal = true
        }
      })
      .catch(error => alert(error))
  },
  methods: {
    paypalModal (modal) {
      this.$refs[modal].show()
    },
    addpaypal () {
      var url = 'api/resource/updatePaypal/' + encodeURIComponent(this.$store.state.uid) + '?paypal=' + encodeURIComponent(this.paypalInput)
      axios
        .put(url)
        .then(response => {
          this.paypal = this.paypalInput
          this.haspaypal = true
        })
        .catch(error => alert(error))
      this.$refs['paypalModal'].hide()
    },
    deletepaypal () {
      var url = 'api/resource/updatePaypal/' + encodeURIComponent(this.$store.state.uid) + '?paypal=' + encodeURIComponent('')
      axios
        .put(url)
        .then(response => {
          this.paypal = ''
          this.haspaypal = false
        })
        .catch(error => alert(error))
    }
  },
  computed: {
    paypalState () {
      if (this.paypalInput.match(/^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$/)) {
        return true
      } else if (this.paypalInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackpaypal () {
      if (this.paypalInput.match(/^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$/) || this.paypalInput === '') {
        return ''
      } else {
        return 'Please enter a valid paypal account'
      }
    }
  }
}
</script>

<style scoped lang="scss">

</style>
