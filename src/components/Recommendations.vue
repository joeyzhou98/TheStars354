<template>
  <div>
    <b-row v-if="showSimilar">
      <b-col v-for="item in items" :key="item.item_id">
          <ItemTile :item="item" imgHeight="100px" titleSize="small"></ItemTile>
      </b-col>
    </b-row>
    <b-row v-else>
      <b-col v-for="item in items" :key="item.item_id">
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
import axios from 'axios'
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
  data () {
    return {
      cookieItems: [],
      similarItems: [],
      subcategories: [],
      maxItemCount: 7,
      maxCategories: 3
    }
  },
  watch: {
    // Refresh data when changing between pages that contain this component
    $route (to, from) {
      if (to !== from) {
        this.getCookieItems()
        if (this.showSimilar) {
          this.getSimilarItems()
        }
      }
    }
  },
  computed: {
    items () {
      if (this.showHistory) {
        return this.cookieItems.slice(1, this.maxItemCount + 2)
      } // else
      var similar = this.similarItems.slice(0, this.maxItemCount - 1)
      return this.shuffle(similar)
    },
    showSimilar () {
      return !this.showHistory
    }
  },
  methods: {
    getCookieItems () {
      if (localStorage.history) {
        let jsonViewedItemsCookie = localStorage.history
        this.cookieItems = JSON.parse(jsonViewedItemsCookie)
      }
    },
    getSimilarItems () {
      let paths = []
      if (this.cookieItems.length === 0) {
        paths.push('api/resource/item/deals') // if no cookie on client side, show deals until they visit items
      } else {
        var newCategory = this.getLastSubcategories()
        if (newCategory === false) {
          return
        }
        for (var subcat of this.subcategories) {
          paths.push('api/resource/subcategory?subcategory=' + encodeURIComponent(subcat))
        }
      }
      var requests = []
      for (var path of paths) {
        requests.push(axios.get(path))
      }
      axios.all(requests)
        .then(axios.spread((...responses) => {
          this.similarItems = []
          for (var response of responses) {
            this.similarItems.push(...response.data)
          }
          this.similarItems = this.shuffle(this.similarItems)
        }))
        .catch(error => { alert(error) })
    },
    getLastSubcategories () {
      console.log('before', this.subcategories)
      for (var item of this.cookieItems) {
        if (this.subcategories.includes(item.subcategory) === false) {
          if (this.subcategories.length === this.maxCategories) {
            console.log('popping')
            this.subcategories.pop()
          }
          this.subcategories.unshift(item.subcategory)
          console.log('pushing ' + item.subcategory)
          return true
        }
      }
      return false
    },
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
    this.getCookieItems()
    if (this.showSimilar) {
      this.getSimilarItems()
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
