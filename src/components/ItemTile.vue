<template>
  <div class="tile">
    <div>
      <span v-line-clamp="2" style="word-break: normal !important;">
        <router-link :to="{name: 'ItemDetails', params: {itemID: item.item_id, item: item}}">
          <div :style="imgStyle">
            <img :src="item.images"/>
          </div>
          <span id="item-title" :class="titleSize">{{name}}</span>
        </router-link>
      </span>
    </div>
    <div v-if="hasDiscount" class="item-price">
      <span class="discount-price">{{discountPrice}}</span>
      <span v-if="hasGoodDiscount"><br/></span>
      <span class="discount-info old-price">{{regularPrice}}</span>
      <span v-if="hasGoodDiscount" class="discount-info">({{discountValue}} off)</span>
    </div>
    <div v-else class="item-price"> <!-- No discount -->
      <span>{{regularPrice}}</span>
    </div>
    <div class="item-rating">
      <star-rating :starStyle="starStyle" :rating="item.rating" :isIndicatorActive="false"></star-rating>
    </div>
  </div>
</template>

<script>
import StarRating from 'vue-dynamic-star-rating'

export default {
  name: 'ItemTile',
  props: {
    item: {
      required: true
    },
    imgHeight: {
      type: String,
      required: false,
      default: '200px'
    },
    titleSize: {
      type: String,
      required: false,
      default: 'normal'
    }
  },
  components: {
    StarRating
  },
  data () {
    return {
      starStyle: {
        starWidth: 15,
        starHeight: 15
      }
    }
  },
  computed: {
    name () {
      return this.item.item_name
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
    hasGoodDiscount () {
      return this.item.discount >= 0.15
    },
    imgStyle () {
      return 'height: ' + this.imgHeight + '; margin-bottom: 5px;'
    }
  }
}
</script>

<style scoped lang="scss">
.tile {
  color: $black;
  padding: 10px 0px;
}
img {
  width: 100%;
  height: 100%;
  object-fit: scale-down;
}
#item-title {
  font-weight: bold;
  color: $black;
  &:hover {
    color: $darkblue;
  }
}
.small {
  font-size: smaller;
}
.item-price > span {
  padding: 2px;
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
.item-rating {
  display: inline-flex;
}
</style>
