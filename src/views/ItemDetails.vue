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
              <span class="seller">Sold by (seller)</span><br>
              <div class="rating">* * * * *</div>
              <div v-if="hasDiscount" class="item-price">
                <span class="discount-price displayed-price">{{discountPrice}}</span>
                <span class="old-price discount-info">{{regularPrice}}</span>
                <span class="discount-info discount-value">({{discountValue}} off)</span>
              </div>
              <div v-else class="item-price"> <!-- No discount -->
                <span class="regular-price displayed-price">{{regularPrice}}</span>
              </div>
              <div class="buttons">
                <b-button class="cart-btn shadow-none" variant="outline" title="Add to Cart">
                  <icon class="far" name="shopping-bag"></icon>
                  <span class="icon-text">ADD TO CART</span>
                </b-button>
                <b-button class="fav-btn shadow-none" variant="outline" title="Add to Wishlist">
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
    <!-- Review component here (last element of page)  -->
  </b-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ItemDetails',
  data () {
    return {
      item: this.$route.params.item,
      itemID: this.$route.params.itemID,
      previousRoute: this.$route.params.previousRoute
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
    }
  },
  methods: {
    getItem () {
      var url = 'api/resource/item/' + this.itemID
      axios
        .get(url)
        .then((response) => { return response.data })
        .catch(error => alert(error))
    }
  }
}
</script>

<style scoped lang="scss">
.back {
  text-align: left;
  margin: 10px 0px;
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
.cart-btn {
  background: $darkblue;
  text-align: center;
  cursor: pointer;
  outline: none;
  color: white;
  border-color: $darkblue;
  padding-top: 3px;
  margin-right: 10px;
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
  text-align: center;
  cursor: pointer;
  outline: none;
  color: $darkblue;
  border-color: $darkblue;
  padding-top: 3px;
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
</style>
