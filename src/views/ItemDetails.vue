<template>
  <b-container v-if="showPage" fluid>
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
              <span class="seller" v-if="seller !== null">Sold by
                <router-link :to="{name: 'SellerDetails', params: {sellerID: item.seller_id}}">
                  {{seller}}
                </router-link>
              </span>
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
              <div v-if="isAvailable && seller!== null" id="quantitySelect">
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
                <b-button  v-if="seller !== null" @click="$bvModal.show('addtocart')" class="button main-btn shadow-none" variant="outline" :disabled="!isAvailable">
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
                  </b-row>
                  <template slot="modal-footer">
                    <b-button class="sec-btn" @click="keepShopping">KEEP SHOPPING</b-button>
                    <b-button class="main-btn" @click="goToCart">CHECKOUT</b-button>
                  </template>
                </b-modal>
                <!-- End of modal section -->
                <b-button v-if="seller !== null" class="button sec-btn shadow-none" @click="onWishlistClick" variant="outline"
                  v-b-tooltip.hover.right :title="wishlistTooltip">
                  <i :class="heartIconStyle" style="position: relative; top: 2px; color: red"></i>
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
    <h5 class="section">Customer reviews:</h5>
    <b-btn @click="showModal('review-modal')" variant="primary" style="display: flex; margin-bottom: 10px;" v-if="canReview">Add review</b-btn>
    <Review
       v-for="(review, index) in reviews"
       v-bind:key="review.review_id"
       :seller_id="item.seller_id"
       :review="review"
       v-on:delete-review="deleteReview(index)"
       v-on:edit-review="editReview(index)">
    </Review>
    <span style="display: flex" v-if="reviews.length === 0">No reviews yet</span>
    <b-modal ref="review-modal" hide-footer title="Review">
      <b-form-textarea
      id="textarea"
      v-model="reviewInput"
      placeholder="Enter your review here..."
      rows="3"
      max-rows="6"
      ></b-form-textarea>
      <b-form-group label="Rating">
        <b-form-radio-group v-model="ratingInput" :options="ratingOptions">
        </b-form-radio-group>
      </b-form-group>
      <b-form-group
              label="Images"
      >
          <b-form-file
                  v-for="(image, index) in imagesInput"
                  :key="index"
                  v-model="imagesInput[index]"
                  accept=".jpg, .png, .gif"
                  placeholder="Choose a file or drop it here..."
                  drop-placeholder="Drop file here..."
                  type="file"
                  style="margin-top: 5px;"
          ></b-form-file>
      </b-form-group>
      <br/>
      <b-button type="submit" variant="outline-success" @click.prevent="addReview" block>Add Review</b-button>
    </b-modal>
    <hr/>
    <div v-if="hasHistory">
      <h5 class="section">History:</h5>
      <Recommendations :showHistory="true"></Recommendations>
    </div>
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
      ratingOptions: [
        { text: '1', value: '1' },
        { text: '2', value: '2' },
        { text: '3', value: '3' },
        { text: '4', value: '4' },
        { text: '5', value: '5' }
      ],
      imagesInput: [null, null, null, null, null],
      reviewInput: '',
      ratingInput: '',
      item: this.$route.params.item,
      itemID: this.$route.params.itemID,
      seller: 'Seller',
      selectedQty: 1,
      reviews: [],
      starStyle: {
        starWidth: 20,
        starHeight: 20
      },
      showPage: false,
      wishlisted: false,
      hasOrdered: false
    }
  },
  watch: {
    // Refresh data when changing between ItemDetail pages
    $route (to, from) {
      if (to !== from) {
        let currentURL = window.location.href
        this.itemID = parseInt(currentURL.match(/item-details\/([0-9]+)/)[1])
        this.showPage = false
        this.getDataAndUpdateHistory()
      }
    }
  },
  computed: {
    canReview () {
      if (this.hasOrdered) {
        for (const review of this.reviews) {
          if (parseInt(this.$store.state.uid) === parseInt(review.buyer_id)) {
            return false
          }
        }
        return true
      }
      return false
    },
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
      return this.item.quantity - this.item.quantity_sold > 0
    },
    availableQty () {
      return parseInt(this.item.quantity - this.item.quantity_sold)
    },
    heartIconStyle () {
      if (this.wishlisted) {
        return 'fas fa-heart'
      }
      return 'far fa-heart'
    },
    wishlistTooltip () {
      if (this.wishlisted) {
        return 'Wishlisted'
      }
      return 'Add to wishlist'
    }
  },
  methods: {
    showModal (modal) {
      this.reviewInput = ''
      this.ratingInput = ''
      this.imageInput = [null, null, null, null, null]
      this.$refs[modal].show()
    },
    addReview () {
      this.reviews = []
      var formData = new FormData()
      for (var i = 0; i < 5; i++) {
        formData.append('image' + (i + 1), this.imagesInput[i])
      }
      var url = 'api/resource/review/' + this.itemID + '?content=' + encodeURIComponent(this.reviewInput) + '&rating=' + encodeURIComponent(this.ratingInput)
      axios
        .post(url, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
        .then(response => {
          this.getItemData()
        })
        .catch(error => alert(error))
      this.$refs['review-modal'].hide()
    },
    deleteReview (index) {
      this.reviews.splice(index, 1)
    },
    editReview (index) {
      this.reviewInput = this.reviews[index].content
      this.ratingInput = this.reviews[index].rating
      this.imageInput = [null, null, null, null, null]
      this.$refs['review-modal'].show()
    },
    async getDataAndUpdateHistory () {
      await this.getItemData()
      await this.$nextTick()
      await this.getHasOrdered()
      this.updateVisitedItems()
      if (this.$store.state.isLoggedIn) {
        this.isItemInWishlist()
      }
      this.showPage = true
    },
    hasHistory () {
      return localStorage.history
    },
    getHasOrdered () {
      if (this.$store.state.isLoggedIn) {
        let url = 'api/resource/user/' + this.$store.state.uid + '/ordered/' + this.itemID
        return axios
          .get(url)
          .then((response) => {
            this.hasOrdered = response.data
          })
          .catch(error => alert(error))
      }
    },
    getItemData () {
      let url = 'api/resource/item/' + this.itemID
      return axios
        .get(url)
        .then((response) => {
          let data = response.data
          this.seller = data.seller_name
          this.reviews = data.reviews
          this.item = data.item_info
        })
        .catch(error => alert(error))
    },
    isItemInWishlist () {
      let url = 'api/resource/wish-list/' + this.$store.state.uid + '/' + this.itemID
      return axios
        .get(url)
        .then((response) => {
          this.wishlisted = response.data
        })
        .catch(error => alert(error))
    },
    async goToCart () {
      this.$refs['addtocart'].hide()
      await this.addToCart()
      this.$router.push('/cart')
    },
    keepShopping () {
      this.addToCart()
      this.$refs['addtocart'].hide()
    },
    addToCart () {
      if (this.$store.state.isLoggedIn) {
        let url = 'api/resource/shopping-cart/' + this.$store.state.uid + '/' + this.itemID + '?newQuantity=' + this.selectedQty
        return axios
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
    onWishlistClick () {
      if (this.$store.state.isLoggedIn) {
        this.wishlisted = !this.wishlisted
        if (this.wishlisted) {
          this.addToWishlist()
        } else {
          this.removeFromWishlist()
        }
      } else {
        this.$router.push('/login')
      }
    },
    addToWishlist () {
      let url = 'api/resource/wish-list/' + this.$store.state.uid + '/' + this.itemID
      return axios
        .post(url)
        .then((response) => {
          this.wishlisted = true
        })
        .catch(error => alert(error))
    },
    removeFromWishlist () {
      let url = 'api/resource/wish-list/' + this.$store.state.uid + '/' + this.itemID
      return axios
        .delete(url)
        .then((response) => {
          this.wishlisted = false
        })
        .catch(error => alert(error))
    },
    updateVisitedItems () {
      if (this.item === null) {
        return
      }
      var itemQueue
      if (localStorage.history) {
        let jsonViewedItemsCookie = localStorage.history
        itemQueue = JSON.parse(jsonViewedItemsCookie)
        itemQueue = itemQueue.filter(item => item !== null)
        for (var i = 0; i < itemQueue.length; i++) {
          if (itemQueue[i].item_id === this.itemID) {
            itemQueue.splice(i, 1) // remove so we can put back at beginning of queue
            break
          }
        }
        itemQueue.unshift(this.item) // add to 1st
        if (itemQueue.length > 10) {
          itemQueue.pop() // keep 10 last visited items
        }
      } else {
        itemQueue = [this.item]
      }

      var jsonItems = JSON.stringify(itemQueue)
      localStorage.history = jsonItems
    }
  },
  created () {
    this.getDataAndUpdateHistory()
  }
}
</script>

<style scoped lang="scss">
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
  padding-bottom: 20px;
}
</style>
