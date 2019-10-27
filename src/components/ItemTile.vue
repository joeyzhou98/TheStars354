<template>
  <div class="tile">
    <div class="img-container">
      <img :src="item.images"/>
    </div>
    <div id="item-title">
      <span v-line-clamp="2" style="word-break: normal !important;">{{name}}</span>
    </div>
    <div v-if="hasDiscount" class="item-price">
      <span id="discount-price">{{discountPrice}}</span>
      <span v-if="hasGoodDiscount"><br/></span>
      <span id="old-price" class="discount-info">{{regularPrice}}</span>
      <span v-if="hasGoodDiscount" id="discount-value" class="discount-info">({{discountValue}} off)</span>
    </div>
    <div v-else class="item-price"> <!-- No discount -->
      <span id="regular-price">{{regularPrice}}</span>
    </div>
    <div class="item-rating">
      * * * * *
    </div>
  </div>
</template>

<script>
export default {
  name: 'ItemTile',
  props: ['item'],
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
    }
  },
  methods: {
    truncate () {
      const itemName = document.getElementById('item-title')
      var divh = itemName.clientWidth
      var span = itemName.querySelector('span')
      while (span.width > divh) {
        span.textContent = span.textContent.replace(/\W*\s(\S)*$/, '...')
      }
    }
  }
}
</script>

<style scoped lang="scss">
.tile {
  color: $black;
  padding: 10px 0px;
}
.img-container {
  height: 200px;
  margin-bottom: 5px;
}
img {
  width: 100%;
  height: 100%;
  object-fit: scale-down;
}
#item-title {
  font-weight: bold;
}
.item-price > span {
  padding: 2px;
}
#discount-price {
  color: red;
}
.discount-info {
  color: $darkgray;
  font-size: smaller;
}
#old-price {
  text-decoration: line-through;
}
</style>
