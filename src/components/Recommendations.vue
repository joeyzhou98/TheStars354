<template>
  <div>
    <b-row v-if="showSimilar">
      <b-col v-for="item in similarItems" :key="item.item_id">
          <ItemTile :item="item" imgHeight="100px" titleSize="small"></ItemTile>
      </b-col>
    </b-row>
    <b-row v-else>
      <b-col v-for="item in historyItems" :key="item.item_id">
        <router-link :to="{name: 'ItemDetails', params: {itemID: item.item_id, item: item}}">
          <div style="height: 100px; margin-bottom: 5px; text-align:left">
            <img :src="item.images"/>
          </div>
          <span id="item-title" :class="titleSize">{{name}}</span>
        </router-link>
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
  props: {
    showHistory: {
      type: Boolean,
      required: true
    }
  },
  watch: {
    // Refresh data when changing between pages that contain this component
    $route (to, from) {
      if (to !== from) {
        this.$store.dispatch('updateCookieItems')
        if (this.showSimilar) {
          this.$store.dispatch('updateSimilarItems')
        }
      }
    }
  },
  computed: {
    historyItems () {
      return this.$store.state.cookieItems.slice(1)
    },
    similarItems () {
      var similar = this.shuffle(this.$store.state.similarItems)
      return similar.slice(0, 7)
    },
    showSimilar () {
      return !this.showHistory
    }
  },
  methods: {
    shuffle (a) {
      var j, x, i
      for (var k = a.length - 1; k > 0; k--) {
        j = Math.floor(Math.random() * (i + 1))
        x = a[i]
        a[i] = a[j]
        a[j] = x
      }
      return a
    }
  },
  mounted () {
    this.$store.dispatch('updateCookieItems')
    if (this.showSimilar) {
      this.$store.dispatch('updateSimilarItems')
    }
  }
}
</script>

<style lang="scss" scoped>
img {
  width: 100%;
  height: 100%;
  object-fit: scale-down;
}
</style>
