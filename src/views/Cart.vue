<template>
  <b-container fluid>
    <br><h4>My Shopping Cart</h4><br>
    <b-row>
      <b-col md="9">
        <b-card v-if="isEmpty" class="text-center">
          <div>
            Your shopping cart is empty.
          </div>
        </b-card>
        <b-list-group v-else>
          <b-list-group-item class="flex-column align-items-start"
            v-for="data in cartData" :key="data.item.item_id">
            <b-row>
              <b-col md="2">
                <div class="img-container">
                  <img :src="data.item.images"/>
                </div>
              </b-col>
              <b-col md="8">
                <div class="d-flex align-items-start flex-column">
                  <div style="text-align: left;">
                    <b-link :to="itemLink(data.item)"><span class="item-link">{{data.item.item_name}}</span></b-link>
                  </div><br>
                  <div class="mb-auto">
                    <small>
                      Qty:
                      <div style="display: inline-block; width: 50px">
                        <b-select class="shadow-none" size="sm" v-model="data.qty" @input="updateQty(data.item, data.qty)">
                          <option v-for="qty in data.item.quantity" :key="qty" :value="qty">{{qty}}</option>
                        </b-select>
                      </div>
                      <b-link class="item-link small-link" @click="remove(data.item)">Delete</b-link>
                      <b-link class="item-link small-link">Move to Wishlist</b-link>
                    </small>
                  </div>
                </div>
              </b-col>
              <b-col align-self="center">
                <span style="font-weight: bold">{{discountPrice(data.item)}}</span>
              </b-col>
            </b-row>
          </b-list-group-item>
        </b-list-group>
        <div style="text-align: right; margin: 10px">
          Items in cart: {{itemCount}}
        </div>
      </b-col>
      <b-col>
        <b-card align="left">
          <div>
            <div style="text-align: center; font-weight: bold; margin-bottom: 10px;">Order Summary</div>
            <div class="d-flex justify-content-between">
              <span>Subtotal:</span>
              <span style="font-weight: bold">{{subtotalTxt}}</span>
            </div>
            <div class="d-flex justify-content-between">
              <span>Shipping:</span>
              <small class="small-bold">FREE</small>
            </div>
            <div class="d-flex justify-content-between">
              <span>Taxes:</span>
              <small class="small-bold">TBD</small>
            </div>
            <hr/>
            <div class="d-flex justify-content-between">
              <span>Estimated Total:</span>
              <span style="font-weight: bold;">{{subtotalTxt}}</span>
            </div>
            <small class="text-muted">Taxes calculated during checkout</small>
            <hr/>
            <div>
              Coupon Code: <br>
              <b-input-group>
                <b-form-input class="shadow-none" v-model="couponCode"></b-form-input>
                <b-input-group-append>
                  <b-button class="shadow-none" size="sm" text="Apply">Apply</b-button>
                </b-input-group-append>
              </b-input-group>
            </div>
            <hr/>
            <b-button block variant="success"
              :to="checkoutLink">
              CHECKOUT
            </b-button>
          </div>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Cart',
  data () {
    return {
      cartData: [],
      previousQtyData: {},
      couponCode: ''
    }
  },
  computed: {
    isEmpty () {
      return this.cartData == null || this.cartData.length === 0
    },
    subtotal () {
      var subtotal = 0
      for (var data of this.cartData) {
        let price = data.item.price - (data.item.price * data.item.discount)
        subtotal += price * data.qty
      }
      return subtotal
    },
    subtotalTxt () {
      return '$' + this.subtotal.toFixed(2)
    },
    itemCount () {
      var count = 0
      for (var data of this.cartData) {
        count += data.qty
      }
      return count
    },
    checkoutLink () {
      if (this.$store.state.isLoggedIn) {
        return {name: 'PlaceOrder', params: {cartData: this.cartData, subtotal: this.subtotal, subtotalTxt: this.subtotalTxt}}
      }
      return '/login'
    }
  },
  methods: {
    getCartItems () {
      if (this.$store.state.isLoggedIn) {
        this.getItemsFromDB()
      } else {
        this.getItemsFromCookies()
      }
    },
    getItemsFromDB () {
      var url = 'api/resource/shopping-cart/' + this.$store.state.uid
      axios
        .get(url)
        .then((response) => {
          this.cartData = response.data
          for (var data of this.cartData) {
            this.previousQtyData[data.item.item_id] = data.qty
          }
        })
        .catch(error => alert(error))
    },
    getItemsFromCookies () {
      if (localStorage.cart) {
        let jsonCartCookie = localStorage.cart
        this.cartData = JSON.parse(jsonCartCookie)
      }
    },
    remove (item) {
      if (this.$store.state.isLoggedIn) {
        this.removeItemFromDB(item)
      } else {
        this.removeItemFromCookies(item)
      }
    },
    removeItemFromDB (item) {
      var url = 'api/resource/shopping-cart/' + this.$store.state.uid + '/' + item.item_id + '/' + 0
      axios
        .delete(url)
        .then((response) => {
          for (var i = 0; i < this.cartData.length; i++) {
            if (this.cartData[i].item.item_id === item.item_id) {
              this.cartData.splice(i, 1)
              break
            }
          }
        })
        .catch(error => alert(error))
    },
    removeItemFromCookies (item) {
      if (localStorage.cart) {
        let jsonCartCookie = localStorage.cart
        let cookie = JSON.parse(jsonCartCookie)
        for (var i = 0; i < cookie.length; i++) {
          if (cookie[i].item.item_id === item.item_id) {
            cookie.splice(i, 1)
            break
          }
        }
        var jsonItems = JSON.stringify(cookie)
        localStorage.cart = jsonItems
        this.cartData = cookie
      }
    },
    updateQty (item, qty) {
      if (this.$store.state.isLoggedIn) {
        this.updateQtyInDB(item, qty)
      } else {
        this.updateQtyInCookies(item, qty)
      }
    },
    updateQtyInDB (item, qty) {
      let diff = qty - this.previousQtyData[item.item_id]
      let url = 'api/resource/shopping-cart/' + this.$store.state.uid + '/' + item.item_id + '?newQuantity=' + diff
      axios
        .post(url)
        .then(() => {
          this.previousQtyData[item.item_id] = qty
        })
        .catch(error => alert(error))
    },
    updateQtyInCookies (item, qty) {
      if (localStorage.cart) {
        let jsonCartCookie = localStorage.cart
        let cookie = JSON.parse(jsonCartCookie)
        for (var data of cookie) {
          if (data.item.item_id === item.item_id) {
            data.qty = qty
            break
          }
        }
        var jsonItems = JSON.stringify(cookie)
        localStorage.cart = jsonItems
        this.cartData = cookie
      }
    },
    discountPrice (item) {
      return '$' + (item.price - (item.price * item.discount)).toFixed(2)
    },
    itemLink (item) {
      return 'item-details/' + item.item_id
    }
  },
  created () {
    this.getCartItems()
  }
}
</script>

<style lang="scss" scoped>
.img-container {
  width: 100%;
}
img {
  width: 100%;
  height: 100%;
  object-fit: scale-down;
}
.item-link {
  color: $darkblue;
}
.small-link {
  margin-left: 15px;
}
.small-bold {
  font-weight: bold;
  margin-top: 3px
}
</style>
