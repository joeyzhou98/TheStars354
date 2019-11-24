<template>
  <div>
    <b-card-body class="text-left">
      <h2>Your billing and shipping address</h2>
      <b-card v-for="address in addresses" :key="address.id" no-body class="overflow-hidden">
        <b-card-body>{{address.name}}<br/>
          {{address.street}}<br/>
          {{address.city}}, {{address.province}} {{address.postCode}}<br/>
          {{address.country}}
          <b-button variant="outline" title="edit" @click="findModal('editModal')">
            <icon name="edit"></icon>
          </b-button>
          <b-button variant="outline" title="delete" @click="deleteAddress">
            <icon name="trash-alt"></icon>
          </b-button>
        </b-card-body>
      </b-card>

      <br/>
      <b-button variant="outline-info" @click="findModal('addModal')">
        <icon name="plus"></icon>
      </b-button>
    </b-card-body>

    <b-modal ref="editModal" hide-footer title="Edit Your Address">
      <form ref="form" @submit="onSubmitEdit">
        <b-form-group
          :state="nameState"
          label="Name"
          label-for="name-input"
          :invalid-feedback="invalidFeedbackName"
        >
          <b-form-input
            id="name-input"
            v-model="addressInput.nameInput"
            :state="nameState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="streetState"
          label="Street"
          label-for="steet-input"
          :invalid-feedback="invalidFeedbackStreet"
        >
          <b-form-input
            id="street-input"
            v-model="addressInput.streetInput"
            :state="streetState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="cityState"
          label="City"
          label-for="city-input"
          :invalid-feedback="invalidFeedbackCity"
        >
          <b-form-input
            id="city-input"
            v-model="addressInput.cityInput"
            :state="cityState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="provinveState"
          label="Province"
          label-for="province-input"
          :invalid-feedback="invalidFeedbackProvince"
        >
          <b-form-input
            id="provinve-input"
            v-model="addressInput.provinceInput"
            :state="provinceState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="PCState"
          label="Post Code"
          label-for="PC-input"
          :invalid-feedback="invalidFeedbackPCstate"
        >
          <b-form-input
            id="PC-input"
            v-model="addressInput.postCodeInput"
            :state="PCState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="countryState"
          label="Country"
          label-for="country-input"
          invalid-feedback="invalidFeedbackCountry"
        >
          <b-form-input
            id="country-input"
            v-model="addressInput.countryInput"
            :state="countryState"
            trim
            required
          ></b-form-input>
        </b-form-group>
      </form>
      <b-button type="submit" variant="outline-success" block>Edit</b-button>
    </b-modal>

    <b-modal ref="addModal" hide-footer title="Add New Address">
      <form ref="form" @submit="onSubmitAdd">
        <b-form-group
          :state="nameState"
          label="Name"
          label-for="name-input"
          invalid-feedback="Name is required"
        >
          <b-form-input
            id="name-input"
            v-model="addressInput.nameInput"
            :state="nameState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="streetState"
          label="Street"
          label-for="steet-input"
          invalid-feedback="Street is required"
        >
          <b-form-input
            id="street-input"
            v-model="addressInput.streetInput"
            :state="streetState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="cityState"
          label="City"
          label-for="city-input"
          invalid-feedback="City is required"
        >
          <b-form-input
            id="city-input"
            v-model="addressInput.cityInput"
            :state="cityState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="provinveState"
          label="Province"
          label-for="province-input"
          invalid-feedback="Province is required"
        >
          <b-form-input
            id="provinve-input"
            v-model="addressInput.provinceInput"
            :state="provinceState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="PCState"
          label="Post Code"
          label-for="PC-input"
          invalid-feedback="Post Code is required"
        >
          <b-form-input
            id="PC-input"
            v-model="addressInput.postCodeInput"
            :state="PCState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="countryState"
          label="Country"
          label-for="country-input"
          invalid-feedback="Country is required"
        >
          <b-form-input
            id="country-input"
            v-model="addressInput.countryInput"
            :state="countryState"
            trim
            required
          ></b-form-input>
        </b-form-group>
      </form>
      <b-button type="submit" variant="outline-success" block>Add</b-button>
    </b-modal>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      hasAddress: false,
      addressInput: {
        nameInput: '',
        streetInput: '',
        cityInput: '',
        provinceInput: '',
        postCodeInput: '',
        countryInput: ''
      },
      addresses: [
        {
          id: 0,
          name: 'MRS/Ms. XXXX XXX',
          street: '2658 Payene Cres',
          city: 'Saint-Laurent',
          province: 'QC',
          postCode: 'H7O 0A3',
          country: 'Canada'
        },
        {
          id: 1,
          name: 'MRS/Ms. 1321',
          street: '1234 Payene Cres',
          city: 'Saint-Laurent',
          province: 'QC',
          postCode: 'H7O 0A3',
          country: 'Canada'
        }
      ]
    }
  },
  mounted: {
    getUserInfo () {
      var url = 'api/resource/buyerInfo'
      axios
        .get(url)
        .then(response => {
          this.name = response.data['name']
          this.street = response.data['street']
          this.city = response.data['city']
          this.province = response.data['province']
          this.postCode = response.data['postCode']
          this.country = response.data['country']
          if (this.response.data !== '') {
            this.hasAddress = true
          }
        })
        .catch(error => alert(error))
    }
  },
  methods: {
    findModal (modal) {
      this.$refs[modal].show()
    },
    onSubmitAdd (evt) {
      evt.preventDefault()
      this.addAddress()
    },
    onSubmitEdit (evt) {
      evt.preventDefault()
      this.editAddress()
    },
    deleteAddress () {
      let addressToPost = ' '
      var url = 'api/resource/buyerInfo?address=' + encodeURIComponent(addressToPost)
      axios
        .post(url)
        .then(response => {
          this.name = response.data['name']
          this.street = response.data['street']
          this.city = response.data['city']
          this.province = response.data['province']
          this.postCode = response.data['postCode']
          this.country = response.data['country']
          if (this.response.data !== '') {
            this.hasAddress = true
          }
        })
        .catch(error => alert(error))
    },
    addAddress () {
      let addressToPost = this.addressInput.nameInput + ' ' + this.addressInput.streetInput + ' ' + this.addressInput.cityInput + ' ' + this.addressInput.provinceInput + ' ' + this.addressInput.postCodeInput + ' ' + this.addressInput.countryInput
      var url = 'api/resource/buyerInfo?address=' + encodeURIComponent(addressToPost)
      axios
        .post(url)
        .then(response => {
          this.name = response.data['name']
          this.street = response.data['street']
          this.city = response.data['city']
          this.province = response.data['province']
          this.postCode = response.data['postCode']
          this.country = response.data['country']
          this.hasAddress = true
        })
        .catch(error => alert(error))
    },
    editAddress () {
      this.deleteAddress()
      this.addresses()
    }
  },
  computed: {
    stateName () {
      if (this.addressInput.nameInput.match(/^[A-Za-z]{1,25}$/)) {
        return true
      } else if (this.addressInput.nameInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackName () {
      if (this.addressInput.nameInput.match(/^[A-Za-z]{1,25}$/) || this.addressInput.nameInput === '') {
        return ''
      } else {
        return 'Please enter a valid name'
      }
    },
    stateStreet () {
      if (this.addressInput.streetInput.match(/^[A-Za-z\d]{5,}$/)) {
        return true
      } else if (this.addressInput.streetInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedStreet () {
      if (this.addressInput.streetInput.match(/^[A-Za-z\d]{5,}$/) || this.addressInput.streetInput === '') {
        return ''
      } else {
        return 'Please enter a valid street number and name'
      }
    },
    stateCity () {
      if (this.addressInput.cityInput.match(/^[A-Za-z-]{2,}$/)) {
        return true
      } else if (this.addressInput.cityInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackCity () {
      if (this.addressInput.cityInput.match(/^[A-Za-z-]{2,}$/) || this.addressInput.cityInput === '') {
        return ''
      } else {
        return 'Please enter a city'
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
    statePCstate () {
      if (this.addressInput.postCodeInput.match(/^[A-Za-z\d]{6,10}$/)) {
        return true
      } else if (this.addressInput.postCodeInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackPCstate () {
      if (this.addressInput.postCodeInput.match(/^[A-Za-z\d]{6,10}$/) || this.addressInput.postCodeInput === '') {
        return ''
      } else {
        return 'Please enter a valid name'
      }
    },
    stateCountry () {
      if (this.addressInput.countryInput.match(/^[A-Za-z\d]{5,15}$/)) {
        return true
      } else if (this.addressInput.countryInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackCountry () {
      if (this.addressInput.countryInput.match(/^[A-Za-z\d]{5,15}$/) || this.addressInput.countryInput === '') {
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
