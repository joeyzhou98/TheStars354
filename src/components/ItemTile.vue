<template>
  <div class="tile">
    {{name}}
  </div>
</template>

<script>
export default {
  name: 'ItemTile',
  props: [
    'name',
    'image',
    'price',
    'brand',
    'desc',
    'rating',
    'category'
  ]
}
</script>

<style scoped lang="scss">
.tile {
  background-color: lightslategray;
  color: white;
  height: 200px;
}
</style>
