<template>
  <b-container fluid>
    <div class="back">
      <router-link :to="previousRoute.path">&lt; {{previousRoute.name}} </router-link>
    </div>
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
                    <b-select size="sm" v-model="selectedQty">
                      <option v-for="qty in quantity" :key="qty" :value="qty">{{qty}}</option>
                    </b-select>
                  </b-col>
                  <b-col md="10"></b-col>
                </b-row>
              </div>
              <div v-else style="color: darkred; margin-bottom: 8px">Out of stock :(</div>
              <div class="buttons">
                <b-button class="button cart-btn shadow-none" variant="outline" :disabled="!isAvailable" title="Add to Cart">
                  <icon class="far" name="shopping-bag"></icon>
                  <span class="icon-text">ADD TO CART</span>
                </b-button>
                <b-button class="button fav-btn shadow-none" variant="outline" title="Add to Wishlist">
                  <icon class="far" name="heart"></icon>
                  <span class="icon-text">FAVORITE</span>
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
    <!-- Recommendation component here  -->
    <hr/>
    <span style="display: flex; font-size: 1.5rem; padding-bottom: 20px;">Customer reviews</span>
    <Review v-for="review in reviews" v-bind:key="review.review_id" :review="review"></Review>
    <span style="display: flex" v-if="reviews.length === 0">No reviews yet</span>
  </b-container>
</template>

<script>
import axios from 'axios'
import Review from '@/components/Review.vue'
import StarRating from 'vue-dynamic-star-rating'

export default {
  name: 'ItemDetails',
  components: {
    Review,
    StarRating
  },
  data () {
    return {
      item: this.$route.params.item,
      itemID: this.$route.params.itemID,
      previousRoute: this.$route.params.previousRoute,
      seller: 'Seller',
      selectedQty: 1,
      reviews: [],
      starStyle: {
        starWidth: 20,
        starHeight: 20
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
    quantity () {
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
        })
        .catch(error => alert(error))
    }
  },
  created () {
    this.getItemData()
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
  margin-right: 10px;
}
.cart-btn {
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
.fav-btn {
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
  margin-bottom: 12px;
  span {
    margin-right: 5px;
  }
}
</style>