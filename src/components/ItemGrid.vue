<template>
<div>
  <b-row v-for="items in chunkedItems" :key="items">
    <b-col v-for="item in items" :key="item.item_id" lg="3" md="2" s="1" xs="1">
        <ItemTile :item="item"></ItemTile>
    </b-col>
  </b-row>
</div>
</template>

<script>
import ItemTile from './ItemTile'

export default {
  name: 'ItemGrid',
  components: {
    ItemTile
  },
  props: {
    items: {
      type: Array,
      required: true
    }
  },
  computed: {
    chunkedItems () {
      return this.chunk(this.items, 4)
    }
  },
  methods: {
    chunk (arr, chunkSize = 1, cache = []) {
      const tmp = [...arr]
      if (chunkSize <= 0) return cache
      while (tmp.length) cache.push(tmp.splice(0, chunkSize))
      return cache
    }
  }
}
</script>

<style scoped lang="scss">
.panel {
  padding: 10px 0px;
}
</style>
