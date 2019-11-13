<template>
  <div>
    <b-row>
      <b-col v-for="item in items" :key="item.item_id">
          <ItemTile :item="item" imgHeight="100px" titleSize="small"></ItemTile>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import ItemTile from '@/components/ItemTile.vue'

export default {
  name: 'Recommendations',
  components: {
    ItemTile
  },
  data () {
    return {
      cookieItems: [],
      maxItemCount: 6
    }
  },
  watch: {
    // Refresh data when changing between pages that contain this component
    $route (to, from) {
      if (to !== from) {
        this.getCookieItems()
      }
    }
  },
  computed: {
    items () {
      return this.cookieItems.slice(0, this.maxItemCount)
    }
  },
  methods: {
    getCookieItems () {
      if (this.$cookies.isKey('viewedItems')) {
        let jsonViewedItemsCookie = this.$cookies.get('viewedItems')
        this.cookieItems = JSON.parse(jsonViewedItemsCookie)
      }
    }
  },
  created () {
    alert('created')
    this.getCookieItems()
  }
}
</script>
