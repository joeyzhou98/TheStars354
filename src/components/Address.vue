<template>
  <div>
    <b-card-body class="text-left">
      <h2>Your Billing and Shipping Address</h2>
      <b-card v-if="hasAddress1">
        Address #1: {{address1}}<br/>
        <b-button variant="outline" title="delete" @click="deleteAddress(1)">
            <icon name="trash-alt"></icon>
        </b-button>
      </b-card>
      <b-card v-if="hasAddress2">
        Address #2: {{address2}}<br/>
        <b-button variant="outline" title="delete" @click="deleteAddress(2)">
            <icon name="trash-alt"></icon>
        </b-button>
      </b-card>
      <b-card v-if="hasAddress3">
        Address #3: {{address3}}<br/>
        <b-button variant="outline" title="delete" @click="deleteAddress(3)">
            <icon name="trash-alt"></icon>
        </b-button>
      </b-card>
      <br/>
      <b-button v-if="!(hasAddress1 && hasAddress2 && hasAddress3)" variant="outline-info" @click="findModal('addressModal')">
        <icon name="plus"></icon>
      </b-button>
    </b-card-body>

    <b-modal ref="addressModal" hide-footer title="Add or Edit Address">
      <form ref="form">
        <b-form-group
          :state="stateName"
          label="Name"
          label-for="name-input"
          :invalid-feedback="invalidFeedbackName"
        >
          <b-form-input
            id="name-input"
            v-model="addressInput.nameInput"
            :state="stateName"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="stateStreet"
          label="Street"
          label-for="street-input"
          :invalid-feedback="invalidFeedBackStreet"
        >
          <b-form-input
            id="street-input"
            v-model="addressInput.streetInput"
            :state="stateStreet"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-row><b-col>
        <b-form-group
          :state="stateCity"
          label="City"
          label-for="city-input"
          :invalid-feedback="invalidFeedbackCity"
        >
          <b-form-input
            id="city-input"
            v-model="addressInput.cityInput"
            :state="stateCity"
            trim
            required
          ></b-form-input>
        </b-form-group>
        </b-col>
        <b-col>
        <b-form-group
          :state="stateProvince"
          label="Province"
          label-for="province-input"
          :invalid-feedback="invalidFeedbackProvince"
        >
          <b-form-input
            id="provinve-input"
            v-model="addressInput.provinceInput"
            :state="stateProvince"
            trim
            required
          ></b-form-input>
        </b-form-group>
        </b-col>
        </b-row>
        <b-row><b-col>
        <b-form-group
          :state="statePC"
          label="Post Code"
          label-for="PC-input"
          :invalid-feedback="invalidFeedbackPostCode"
        >
          <b-form-input
            id="PC-input"
            v-model="addressInput.postCodeInput"
            :state="statePC"
            trim
            required
          ></b-form-input>
        </b-form-group>
        </b-col>
        <b-col>
        <b-form-group
          :state="stateCountry"
          label="Country"
          label-for="country-input"
          :invalid-feedback="invalidFeedbackCountry"
        >
          <b-form-input
            id="country-input"
            v-model="addressInput.countryInput"
            :state="stateCountry"
            trim
            required
          ></b-form-input>
        </b-form-group>
        </b-col>
        </b-row>
      </form>
      <b-button type="submit" variant="outline-success" @click.prevent="addAddress" block>Submit</b-button>
    </b-modal>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      hasAddress1: false,
      hasAddress2: false,
      hasAddress3: false,
      addressInput: {
        nameInput: '',
        streetInput: '',
        cityInput: '',
        provinceInput: '',
        postCodeInput: '',
        countryInput: ''
      },
      address1: '',
      address2: '',
      address3: ''
    }
  },
  mounted () {
    var url = 'api/resource/buyerInfo?uid=' + encodeURIComponent(this.$store.state.uid)
    axios
      .get(url)
      .then(response => {
        this.address1 = response.data['address1']
        this.address2 = response.data['address2']
        this.address3 = response.data['address3']

        if (this.address1 !== null) {
          this.hasAddress1 = true
        }
        if (this.address2 !== null) {
          this.hasAddress2 = true
        }
        if (this.address3 !== null) {
          this.hasAddress3 = true
        }
      })
      .catch(error => alert(error))
  },
  methods: {
    findModal (modal) {
      this.$refs[modal].show()
    },
    deleteAddress (num) {
      var url = 'api/resource/updateAddress/' + encodeURIComponent(this.$store.state.uid) + '/' + encodeURIComponent(num) + '?newAddress=' + encodeURIComponent('null')
      axios
        .put(url)
        .then(response => {
          if (num === 1) {
            this.address1 = response.data['address1']
            this.hasAddress1 = false
          }
          if (num === 2) {
            this.address2 = response.data['address2']
            this.hasAddress2 = false
          }
          if (num === 3) {
            this.address3 = response.data['address3']
            this.hasAddress3 = false
          }
        })
        .catch(error => alert(error))
    },
    addAddress () {
      var addressToPost = this.addressInput.nameInput + ' ' + this.addressInput.streetInput + ' ' + this.addressInput.cityInput + ' ' + this.addressInput.provinceInput + ' ' + this.addressInput.postCodeInput + ' ' + this.addressInput.countryInput
      var url = ''
      if (!this.hasAddress1) {
        url = 'api/resource/updateAddress/' + encodeURIComponent(this.$store.state.uid) + '/' + encodeURIComponent(1) + '?newAddress=' + encodeURIComponent(addressToPost)
        axios
          .put(url)
          .then(response => {
            this.address1 = addressToPost
            this.hasAddress1 = true
          })
          .catch(error => alert(error))
      } else if (!this.hasAddress2) {
        url = 'api/resource/updateAddress/' + encodeURIComponent(this.$store.state.uid) + '/' + encodeURIComponent(2) + '?newAddress=' + encodeURIComponent(addressToPost)
        axios
          .put(url)
          .then(response => {
            this.address2 = addressToPost
            this.hasAddress2 = true
          })
          .catch(error => alert(error))
      } else if (!this.hasAddress3) {
        url = 'api/resource/updateAddress/' + encodeURIComponent(this.$store.state.uid) + '/' + encodeURIComponent(3) + '?newAddress=' + encodeURIComponent(addressToPost)
        axios
          .put(url)
          .then(response => {
            this.address3 = addressToPost
            this.hasAddress3 = true
          })
          .catch(error => alert(error))
      }
      this.$refs['addressModal'].hide()
    }
  },
  computed: {
    stateName () {
      if (this.addressInput.nameInput.match(/^[A-Za-z\s]{1,25}$/)) {
        return true
      } else if (this.addressInput.nameInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackName () {
      if (this.addressInput.nameInput.match(/^[A-Za-z\s]{1,25}$/) || this.addressInput.nameInput === '') {
        return ''
      } else {
        return 'Please enter a valid name'
      }
    },
    stateStreet () {
      if (this.addressInput.streetInput.match(/^[A-Za-z\d\s#]{5,}$/)) {
        return true
      } else if (this.addressInput.streetInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedBackStreet () {
      if (this.addressInput.streetInput.match(/^[A-Za-z\d\s]#{5,}$/) || this.addressInput.streetInput === '') {
        return ''
      } else {
        return 'Please enter a valid street number and name'
      }
    },
    stateCity () {
      if (this.addressInput.cityInput.match(/^[A-Za-z-\s]{2,}$/)) {
        return true
      } else if (this.addressInput.cityInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackCity () {
      if (this.addressInput.cityInput.match(/^[A-Za-z-\s]{2,}$/) || this.addressInput.cityInput === '') {
        return ''
      } else {
        return 'Please enter a valid city'
      }
    },
    stateProvince () {
      if (this.addressInput.provinceInput.match(/^[A-Za-z]{2,}$/)) {
        return true
      } else if (this.addressInput.provinceInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackProvince () {
      if (this.addressInput.provinceInput.match(/^[A-Za-z]{2,}$/) || this.addressInput.provinceInput === '') {
        return ''
      } else {
        return 'Please enter a valid province'
      }
    },
    statePC () {
      if (this.addressInput.postCodeInput.match(/^[A-Za-z\d]{6,10}$/)) {
        return true
      } else if (this.addressInput.postCodeInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackPostCode () {
      if (this.addressInput.postCodeInput.match(/^[A-Za-z\d]{6,10}$/) || this.addressInput.postCodeInput === '') {
        return ''
      } else {
        return 'Please enter a valid name'
      }
    },
    stateCountry () {
      if (this.addressInput.countryInput.match(/^[A-Za-z\d]{3,15}$/)) {
        return true
      } else if (this.addressInput.countryInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackCountry () {
      if (this.addressInput.countryInput.match(/^[A-Za-z\d]{3,15}$/) || this.addressInput.countryInput === '') {
        return ''
      } else {
        return 'Please enter a valid country'
      }
    }
  }
}
</script>

<style scoped lang="scss">

</style>
