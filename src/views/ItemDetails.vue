<template>
  <b-container fluid>
    <br>
    <b-card no-body class="overflow-hidden" align="left">
      <b-row no-gutters>
        <b-col md="4">
          <b-card-img :src="item.images" class="rounded-0"></b-card-img>
        </b-col>
        <b-col md="8">
          <b-card-body>
            <b-card-text>
              <span class="brand">{{item.brand}}</span><br>
              <span class="name">{{item.item_name}}</span><br>
              <span class="seller">Sold by {{seller}}</span><br>
              <div class="rating">
                <star-rating :starStyle="starStyle" :rating="item.rating" :isIndicatorActive="false"></star-rating>
                ({{this.reviews.length}})
              </div>
              <div v-if="hasDiscount" class="item-price">
                <span class="discount-price displayed-price">{{discountPrice}}</span>
                <span class="old-price discount-info">{{regularPrice}}</span>
                <span class="discount-info discount-value">({{discountValue}} off)</span>
              </div>
              <div v-else class="item-price"> <!-- No discount -->
                <span class="regular-price displayed-price">{{regularPrice}}</span>
              </div>
              <div v-if="isAvailable" id="quantitySelect">
                <b-row no-gutters>
                  <b-col>
                    <span class="icon-text">Quantity: </span>
                  </b-col>
                  <b-col>
                    <b-select class="shadow-none" size="sm" v-model="selectedQty">
                      <option v-for="qty in availableQty" :key="qty" :value="qty">{{qty}}</option>
                    </b-select>
                  </b-col>
                  <b-col md="10"></b-col>
                </b-row>
              </div>
              <div v-else style="color: darkred; margin-bottom: 8px">Out of stock :(</div>
              <div class="buttons">
                <b-button  @click="$bvModal.show('addtocart')" class="button main-btn shadow-none" variant="outline" :disabled="!isAvailable"
                  title="Add to Cart">
                  <icon class="far" name="shopping-bag"></icon>
                  <span class="icon-text">ADD TO CART</span>
                </b-button>
                <!-- Start of modal section -->
                <b-modal id="addtocart" ref="addtocart">
                  <template slot="modal-title">
                    <span style="font-size: smaller">{{item.item_name}}</span>
                  </template>
                  <b-row no-gutters>
                    <b-col>
                      <div class="img-container">
                        <img :src="item.images"/>
                      </div>
                    </b-col>
                    <b-col>
                      Brand: {{item.brand}}<br>
                      Price: {{discountPrice}}<br>
                      Quantity: {{selectedQty}}
                    </b-col>
                    <b-col>
                      In cart: <br>
                      Items: (count)<br>
                      Total: ($$)
                    </b-col>
                  </b-row>
                  <template slot="modal-footer">
                    <b-button class="sec-btn" @click="keepShopping">KEEP SHOPPING</b-button>
                    <b-button class="main-btn" @click="goToCart">CHECKOUT</b-button>
                  </template>
                </b-modal>
                <!-- End of modal section -->
                <b-button class="button sec-btn shadow-none" @click="addToWishlist" variant="outline" title="Add to Wishlist">
                  <icon class="far" name="heart"></icon>
                  <span class="icon-text">WISHLIST</span>
                </b-button>
              </div>
              <hr />
              <div>
                <span class="desc" style="font-weight: bolder">Description</span><br>
                {{item.description}}
              </div>
            </b-card-text>
          </b-card-body>
        </b-col>
      </b-row>
    </b-card>
    <br>
    <h5 class="section">You might also like:</h5>
    <Recommendations :showHistory="false"></Recommendations>
    <hr/>
    <h5 class="section">Customer reviews</h5>
    <Review v-for="review in reviews" v-bind:key="review.review_id" :review="review"></Review>
    <span style="display: flex" v-if="reviews.length === 0">No reviews yet</span>
    <hr/>
    <h5 class="section">History:</h5>
    <Recommendations :showHistory="true"></Recommendations>
  </b-container>
</template>

<script>
import axios from 'axios'
import Review from '@/components/Review.vue'
import StarRating from 'vue-dynamic-star-rating'
import Recommendations from '@/components/Recommendations.vue'

export default {
  name: 'ItemDetails',
  components: {
    Review,
    StarRating,
    Recommendations
  },
  data () {
    return {
      item: this.$route.params.item,
      itemID: this.$route.params.itemID,
      seller: 'Seller',
      selectedQty: 1,
      reviews: [],
      starStyle: {
        starWidth: 20,
        starHeight: 20
      }
    }
  },
  watch: {
    // Refresh data when changing between ItemDetail pages
    $route (to, from) {
      if (to !== from) {
        let currentURL = window.location.href
        this.itemID = parseInt(currentURL.match(/item-details\/([0-9]+)/)[1])
        this.getItemData()
        this.updateVisitedItems()
      }
    }
  },
  computed: {
    regularPrice () {
      return '$' + this.item.price.toFixed(2)
    },
    discountPrice () {
      return '$' + (this.item.price - (this.item.price * this.item.discount)).toFixed(2)
    },
    discountValue () {
      return (this.item.discount * 100).toFixed() + '%'
    },
    hasDiscount () {
      return this.item.discount !== 0
    },
    isAvailable () {
      return this.item.quantity > 0
    },
    availableQty () {
      return parseInt(this.item.quantity)
    }
  },
  methods: {
    getItemData () {
      let url = 'api/resource/item/' + this.itemID
      axios
        .get(url)
        .then((response) => {
          let data = response.data
          this.seller = data.seller_name
          this.reviews = data.reviews
          this.item = data.item_info
        })
        .catch(error => alert(error))
    },
    goToCart () {
      this.addToCart()
      this.$refs['addtocart'].hide()
      this.$router.push('/cart')
    },
    keepShopping () {
      this.addToCart()
      this.$refs['addtocart'].hide()
    },
    addToCart () {
      if (this.$store.state.isLoggedIn) {
        let url = 'api/resource/shopping-cart/' + this.$store.state.uid + '/' + this.itemID + '/' + this.selectedQty
        axios
          .post(url)
          .catch(error => alert(error))
      } else { // visitor: add to cookies
        var cookie
        if (localStorage.cart) {
          let jsonCartCookie = localStorage.cart
          cookie = JSON.parse(jsonCartCookie)
          let itemInCart = false
          for (var data of cookie) {
            if (data.item.item_id === this.itemID) {
              data.qty = parseInt(data.qty) + this.selectedQty
              itemInCart = true
              break
            }
          }
          if (itemInCart === false) {
            cookie.push({'item': this.item, 'qty': this.selectedQty})
          }
        } else {
          cookie = [{'item': this.item, 'qty': this.selectedQty}]
        }
        var jsonItems = JSON.stringify(cookie)
        localStorage.cart = jsonItems
      }
    },
    addToWishlist () {
      if (this.$store.state.isLoggedIn) {
        // add to wishlist, change button for remove
      } else {
        this.$router.push('/login')
      }
    },
    updateVisitedItems () {
      var itemQueue
      if (localStorage.history) {
        let jsonViewedItemsCookie = localStorage.history
        itemQueue = JSON.parse(jsonViewedItemsCookie)
        itemQueue = itemQueue.filter(item => item != null)
        for (var i = 0; i < itemQueue.length; i++) {
          if (itemQueue[i].item_id === this.itemID) {
            itemQueue.splice(i, 1) // remove so we can put back at beginning of queue
            break
          }
        }
        if (itemQueue.length >= 10) {
          itemQueue.pop() // keep 10 last visited items
        }
        itemQueue.unshift(this.item) // add to 1st
      } else {
        itemQueue = [this.item]
      }
      var jsonItems = JSON.stringify(itemQueue)
      localStorage.history = jsonItems
    }
  },
  created () {
    this.getItemData()
    this.updateVisitedItems()
  }
}
</script>

<style scoped lang="scss">
.back {
  text-align: left;
  margin: 10px 0px;
  font-size: smaller;
}
.current {
  width: 50px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.brand {
  font-weight: bold;
  text-transform: uppercase;
}
.seller {
  font-size: smaller;
  color: $darkgray;
}
.rating {
  padding: 5px 0px;
  display: flex;
}
.item-price {
  margin-bottom: 6px;
}
.item-price > span {
  padding: 2px;
}
.displayed-price {
  font-weight: bolder;
  font-size: larger;
}
.discount-price {
  color: red;
}
.discount-info {
  color: $darkgray;
  font-size: smaller;
}
.old-price {
  text-decoration: line-through;
}
.icon-text {
  position: relative;
  top: 2px;
  margin-left: 5px;
}
.button {
  text-align: center;
  cursor: pointer;
  outline: none;
  padding-top: 3px;
  margin-right: 12px;
  margin-bottom: 10px;
}
.main-btn {
  background: $darkblue;
  color: white;
  border-color: $darkblue;
  &:hover {
    color: white;
    background: $mainblue;
    border-color: $mainblue;
  }
  &:active {
    position:relative;
    top:1px;
  }
}
.sec-btn {
  background: none;
  color: $darkblue;
  border-color: $darkblue;
  &:hover {
    color: $mainblue;
    background: none;
    border-color: $mainblue;
  }
  &:active {
    position:relative;
    top:1px;
  }
}
#quantitySelect {
  margin-top: 20px;
  margin-bottom: 25px;
  span {
    margin-right: 5px;
  }
}
.img-container {
  width: 100px;
  margin-bottom: 5px;
}
img {
  width: 100%;
  height: 100%;
  object-fit: scale-down;
}
.section {
  display: flex;
  padding-bottom: 20px;
}
</style>
