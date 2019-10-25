<template>
  <div class="tile">
    <div class="img-container">
      <img :src="item.image"/>
    </div>
    <div class="item-title">
      {{item.name}}
    </div>
    <div class="item-price">
      1,200.00$
    </div>
    <div class="item-rating">
      * * * * *
    </div>
  </div>
</template>

<script>
export default {
  name: 'ItemTile',
  props: ['item']
}
</script>

<style scoped lang="scss">
.tile {
  color: $black;
  padding: 10px 0px;
}
.img-container {
  height: 200px;
}
img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.item-title {
  padding: 5px;
  font-weight: bold;
}
</style>
