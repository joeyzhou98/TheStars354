<template>
  <div>
    <b-card-body class="text-left">
      <h2>Your paypal Account</h2>
      <b-card no-body class="overflow-hidden" v-if="haspaypal">
        <b-card-body>{{paypal}}
          <b-button variant="outline" title="edit" @click="paypalModal('paypalEditModal')">
            <icon name="edit"></icon>
          </b-button>
          <b-button variant="outline" title="delete" @click="deletepaypal">
            <icon name="trash-alt"></icon>
          </b-button>
        </b-card-body>
      </b-card>

      <br/>
      <b-button variant="outline-info" @click="paypalModal('paypalAddModal')" v-if="!haspaypal">
        <icon name="plus"></icon>
      </b-button>
    </b-card-body>

    <b-modal ref="paypalAddModal" hide-footer title="Add paypal Account">
      <form ref="form" @submit="onSubmitAdd">
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
      <b-button type="submit" variant="outline-success" block>Add</b-button>
    </b-modal>

    <b-modal ref="paypalEditModal" hide-footer title="Edit paypal Account">
      <form ref="form" @submit="onSubmitEdit">
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
      <b-button type="submit" variant="outline-success" block>Edit</b-button>
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
  mounted: {
    getUserInfo () {
      var url = 'api/resource/buyerInfo'
      axios
        .get(url)
        .then(response => {
          this.paypal = response.data['paypal']
          if (this.paypal !== '') {
            this.haspaypal = true
          }
        })
        .catch(error => alert(error))
    }
  },
  methods: {
    onSubmitAdd (evt) {
      evt.preventDefault()
      this.addpaypal()
    },
    onSubmitEdit (evt) {
      evt.preventDefault()
      this.editpaypal()
    },
    paypalModal (modal) {
      this.$refs[modal].show()
    },
    addpaypal () {
      var url = 'api/resource/buyerInfo?paypal=' + encodeURIComponent(this.paypalInput)
      axios
        .post(url)
        .then(response => {
          this.paypal = response.data['paypal']
          this.haspaypal = true
        })
        .catch(error => alert(error))
    },
    editpaypal () {
      this.deletepaypal()
      this.addpaypal()
    },
    deletepaypal () {
      var url = 'api/resource/buyerInfo?paypal=' + encodeURIComponent('')
      axios
        .post(url)
        .then(response => {
          this.paypal = response.data['paypal']
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
