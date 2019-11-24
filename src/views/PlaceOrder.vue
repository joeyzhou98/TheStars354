<template>
  <b-container fluid>
    <br><h4>Checkout</h4><br>
    <b-row>
      <b-col md="9">
        <div>
          <b-card align="left">
            <div class="minor-title">Select a shipping address</div>
            <b-form-radio-group stacked>
              <b-form-radio v-if="address1 !== null" v-model="selectedAddress" name="address1" value="1">{{address1}}</b-form-radio>
              <b-form-radio v-if="address2 !== null" v-model="selectedAddress" name="address2" value="2">{{address2}}</b-form-radio>
              <b-form-radio v-if="address3 !== null" v-model="selectedAddress" name="address3" value="3">{{address3}}</b-form-radio>
              <b-form-radio v-model="selectedAddress" name="custom" value="custom">Add or modify an address</b-form-radio>
            </b-form-radio-group>
            <div v-if="addNewAddress">
              <br>
              <b-form-group
                label-cols-sm="2"
                label="Name:"
                label-align-sm="right"
                label-for="nested-name"
              >
                <b-form-input id="nested-name" v-model="newAddress.name"></b-form-input>
              </b-form-group>

              <b-form-group
                label-cols-sm="2"
                label="Street address:"
                label-align-sm="right"
                label-for="nested-street"
              >
                <b-form-input id="nested-street" v-model="newAddress.street"></b-form-input>
              </b-form-group>

              <b-form-group
                label-cols-sm="2"
                label="City:"
                label-align-sm="right"
                label-for="nested-city"
              >
                <b-form-input id="nested-city" v-model="newAddress.city"></b-form-input>
              </b-form-group>

              <b-form-group
                label-cols-sm="2"
                label="State:"
                label-align-sm="right"
                label-for="nested-state"
              >
                <b-form-input id="nested-state" v-model="newAddress.state"></b-form-input>
              </b-form-group>

              <b-form-group
                label-cols-sm="2"
                label="Postal Code:"
                label-align-sm="right"
                label-for="nested-postalcode"
              >
                <b-form-input id="nested-postalcode" v-model="newAddress.postalCode"></b-form-input>
              </b-form-group>

              <b-form-group
                label-cols-sm="2"
                label="Country:"
                label-align-sm="right"
                label-for="nested-country"
              >
                <b-form-input id="nested-country" v-model="newAddress.country"></b-form-input>
              </b-form-group>
              <b-form-group
                label-cols-sm="2"
                label="Set to:"
                label-align-sm="right"
                label-for="nested-change"
              >
                <b-form-radio-group id="nested-change">
                  <b-form-radio v-model="addressToChange" name="change1" value="change1">Address 1</b-form-radio>
                  <b-form-radio v-model="addressToChange" name="change2" value="change2">Address 2</b-form-radio>
                  <b-form-radio v-model="addressToChange" name="change3" value="change3">Address 3</b-form-radio>
                </b-form-radio-group>
              </b-form-group>
              <b-button style="float: right" size="sm" @click="changeAddress()" :disabled="incompleteForm">
                Apply changes
              </b-button>
            </div>
          </b-card>
          <br>
          <b-card align="left">
            <div class="minor-title">Select a shipping method</div>
            <b-form-radio-group>
              <b-form-radio v-model="selectedMethod" name="regular" value="regular">Regular</b-form-radio>
              <b-form-radio v-model="selectedMethod" name="express" value="express">Express</b-form-radio>
            </b-form-radio-group>
          </b-card>
        </div>
      </b-col>
      <b-col>
        <b-card align="left">
          <div>
            <div class="minor-title">Order Summary</div>
            <div class="d-flex justify-content-between">
              <span>Subtotal:</span>
              <span style="font-weight: bold">{{subtotalTxt}}</span>
            </div>
            <div class="d-flex justify-content-between">
              <span>Shipping:</span>
              <span style="font-weight: bold">$0.00</span>
            </div>
            <div class="d-flex justify-content-between">
              <span>Taxes:</span>
              <span style="font-weight: bold">{{taxesTxt}}</span>
            </div>
            <hr/>
            <div class="d-flex justify-content-between">
              <span>Total:</span>
              <span style="font-weight: bold;">{{totalTxt}}</span>
            </div>
            <hr/>
            <b-button block variant="success" @click="placeOrder">PLACE ORDER</b-button>
          </div>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PlaceOrder',
  data () {
    return {
      cartData: this.$route.params.cartData,
      subtotal: this.$route.params.subtotal,
      subtotalTxt: this.$route.params.subtotalTxt,
      selectedAddress: '1',
      addressToChange: '',
      address1: 'Fetching address...',
      address2: 'Fetching address...',
      address3: 'Fetching address...',
      modifyRequest: false,
      newAddress: {
        name: '',
        street: '',
        city: '',
        state: '',
        postalCode: '',
        country: ''
      },
      selectedMethod: 'regular'
    }
  },
  computed: {
    taxes () {
      return this.subtotal * 0.15
    },
    taxesTxt () {
      return '$' + this.taxes.toFixed(2)
    },
    total () {
      return this.subtotal + this.taxes
    },
    totalTxt () {
      return '$' + this.total.toFixed(2)
    },
    addNewAddress () {
      return this.selectedAddress === 'custom' || this.modifyRequest === true
    },
    hasThreeAddresses () {
      return this.address1 != null && this.address2 != null && this.address3 != null
    },
    incompleteForm () {
      return this.addressToChange === '' || this.newAddress.name === '' || this.newAddress.street === '' || this.newAddress.city === '' ||
       this.newAddress.state === '' || this.newAddress.postalCode === '' || this.newAddress.country === ''
    },
    newAddressString () {
      return this.newAddress.name + ', ' + this.newAddress.street + ', ' + this.newAddress.city + ', ' + this.newAddress.state +
        ', ' + this.newAddress.postalCode + ', ' + this.newAddress.country
    },
    selectedAddressString () {
      switch (this.selectedAddress) {
        case '1':
          return this.address1
        case '2':
          return this.address2
        case '3':
          return this.address3
        default:
          return ''
      }
    },
    addressIndexToChange () {
      switch (this.addressToChange) {
        case 'change1':
          return 1
        case 'change2':
          return 2
        case 'change3':
          return 3
        default:
          return 0
      }
    }
  },
  methods: {
    getUserAddresses () {
      let url = 'api/resource/buyerInfo?username=' + this.$store.state.username
      return axios
        .get(url)
        .then((response) => {
          this.address1 = response.data.address1
          this.address2 = response.data.address2
          this.address3 = response.data.address3
        })
        .catch(error => alert(error))
    },
    changeAddress () {
      let url = 'api/resource/updateAddress/' + this.$store.state.uid + '/' + this.addressIndexToChange +
        '?newAddress=' + encodeURIComponent(this.newAddressString)
      axios
        .put(url)
        .then((response) => {
          this.updateAddress()
        })
        .catch(error => alert(error))
    },
    updateAddress () {
      switch (this.addressIndexToChange) {
        case 1:
          this.address1 = this.newAddressString
          this.selectedAddress = '1'
          break
        case 2:
          this.address2 = this.newAddressString
          this.selectedAddress = '2'
          break
        case 3:
          this.address3 = this.newAddressString
          this.selectedAddress = '3'
          break
        default:
          break
      }
    },
    placeOrder () {
      window.open('https://paypal.com', '_blank')
      this.postOrder()
    },
    postOrder () {
      let url = 'api/resource/place-order-in-shopping-cart/' + this.$store.state.uid + '/' + this.selectedAddress + '/' + this.selectedMethod
      return axios
        .post(url)
        .then((response) => {
          this.$router.push({name: 'OrderConfirmation',
            params: {
              order: response.data,
              address: this.selectedAddressString,
              subtotal: this.subtotalTxt,
              taxes: this.taxesTxt,
              total: this.totalTxt
            }
          })
          // send email
        })
        .catch(error => alert(error))
    }
  },
  created () {
    this.getUserAddresses()
  }
}
</script>

<style lang="scss" scoped>
.minor-title {
  text-align: center;
  font-weight: bold;
  margin-bottom: 10px;
}
</style>
