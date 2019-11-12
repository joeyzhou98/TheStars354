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
                <div id="item-info">
                  <div>{{data.item.item_name}}</div><br>
                  <div id="item-info-change">
                    <small>
                      Qty:
                      <div style="display: inline-block; width: 50px">
                        <b-select size="sm" v-model="data.qty">
                            <option v-for="qty in data.item.quantity" :key="qty" :value="qty">{{qty}}</option>
                        </b-select>
                      </div>
                      <b-link class="item-link" @click="remove(data.item)">Delete</b-link>
                      <b-link class="item-link">Move to Wishlist</b-link>
                    </small>
                  </div>
                </div>
              </b-col>
              <b-col align-self="center">
                <h5 style="color: green">{{discountPrice(data.item)}}</h5>
              </b-col>
            </b-row>
          </b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col>
        <b-card class="text-center">
          <div>
            Order Summary
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
      cartData: null
    }
  },
  computed: {
    isEmpty () {
      return this.cartData == null || this.cartData.length === 0
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
        })
        .catch(error => alert(error))
    },
    getItemsFromCookies () {
      if (this.$cookies.isKey('cart')) {
        let jsonCartCookie = this.$cookies.get('cart')
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
      var url = 'api/resource/shopping-cart/' + this.$store.state.uid + '/' + item.item_id
      axios
        .delete(url)
        .catch(error => alert(error))
    },
    removeItemFromCookies (item) {
      if (this.$cookies.isKey('cart')) {
        let jsonCartCookie = this.$cookies.get('cart')
        let cookie = JSON.parse(jsonCartCookie)
        for (var i = 0; i < cookie.length; i++) {
          if (cookie[i].item.item_id === item.item_id) {
            cookie.splice(i, 1)
            break
          }
        }
        var jsonItems = JSON.stringify(cookie)
        this.$cookies.set('cart', jsonItems)
        this.cartData = cookie
      }
    },
    discountPrice (item) {
      return '$' + (item.price - (item.price * item.discount)).toFixed(2)
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
  margin-left: 15px;
  color: $darkblue;
}
#item-info {
  text-align: left;
  position: relative;
  width: 100%;
  height: 100%;
}
#item-info-change {
  position: absolute;
  bottom: 5px;
}
</style>
