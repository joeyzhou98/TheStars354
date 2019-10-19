<template>
  <div>
    <div class="columns is-multiline">
        <div class="column is-one-quarter" v-for="item in items" :key="item.id">
          <ItemTile :name="item.name"></ItemTile>
        </div>
    </div>
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
  }
}
</script>

<style scoped lang="scss">
</style>
