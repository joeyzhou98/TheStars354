<template>
  <b-container fluid>
    <b-row>
      <b-col>
        <b-row>
          <div id="navigation-links">
              <router-link v-for="link in relatedLinks" v-bind:key="link.name"
                :to="link.path"><span class="navigation-link">{{navBracket}} {{link.name}}</span>
              </router-link>
          </div>
        </b-row>
        <b-row>
          <FilterNav :items="itemData" :isSubcategory="isSubcategory"></FilterNav>
        </b-row>
        <br>
        <br>
        <Advertisement :random="advertisement"></Advertisement>
      </b-col>
      <b-col cols="10">
        <b-row id="page-title" class="text-center">
          <b-col>
          <span :v-if="isSubcategory">{{$route.meta.parent}}</span>
          <h1>{{$route.name}}</h1>
          </b-col>
        </b-row>
        <b-row id="item-info" align-v="center">
          <b-col class="item-count">
            {{itemStart}} - {{itemEnd}} of {{displayedItems.length}} items in
            <span class="category">{{$route.name}}</span>
          </b-col>
          <b-col class="pagination">
            <Pagination :pageNumber="pageNumber" :pageCount="pageCount"></Pagination>
          </b-col>
          <b-col>
            <div id="sort">
              <span id="sort-text">Sort by:</span>
              <b-select id="sort-menu" size="sm" v-model="selectedSort" :options="sortOptions" @change="onSortChanged">
              </b-select>
            </div>
          </b-col>
        </b-row>
        <b-row id="grid">
          <ItemGrid v-if="validItems" :items="paginatedData"></ItemGrid>
          <div v-if="validItems == false">{{noItemsMsg}}</div>
        </b-row>
        <b-row class="pagination">
          <Pagination :pageNumber="pageNumber" :pageCount="pageCount" :needScrollTop="true"></Pagination>
        </b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Advertisement from '@/components/Advertisement.vue'
import ItemGrid from '@/components/ItemGrid.vue'
import Pagination from '@/components/Pagination.vue'
import FilterNav from '@/components/FilterNav.vue'
import axios from 'axios'
import { bus } from '../main'

export default {
  name: 'Category',
  components: {
    Advertisement,
    ItemGrid,
    Pagination,
    FilterNav
  },
  data () {
    return {
      pageNumber: 0,
      pageSize: 20,
      selectedSort: 'Bestselling',
      sortOptions: [
        { value: 'Bestselling', text: 'Bestselling' },
        { value: 'Discount Value', text: 'Discount Value' },
        { value: 'Price: Low to High', text: 'Price: Low to High' },
        { value: 'Price: High to Low', text: 'Price: High to Low' }
      ],
      itemData: [], // items fetched from the API request
      filteredData: null, // items filtered by FilterNav component
      noItemsMsg: 'Sorry, there are no products to display here :(',
      advertisement: 0
    }
  },
  watch: {
    // Refresh data when changing categories
    $route (to, from) {
      if (to !== from) {
        this.getItemData()
        this.advertisement = Math.floor(Math.random() * 8)
      }
    }
  },
  computed: {
    displayedItems () {
      if (this.filteredData !== null) {
        return this.filteredData
      }
      return this.itemData
    },
    pageCount () {
      return Math.ceil(this.displayedItems.length / this.pageSize)
    },
    itemStart () {
      return this.pageNumber * this.pageSize
    },
    itemEnd () {
      return Math.min(this.itemStart + this.pageSize, this.displayedItems.length)
    },
    paginatedData () {
      return this.displayedItems.slice(this.itemStart, this.itemEnd)
    },
    isSubcategory () {
      return this.$route.meta.parent != null
    },
    categoryName () {
      return this.$route.name
    },
    validItems () {
      return this.displayedItems != null && this.displayedItems.length !== 0
    },
    relatedLinks () {
      if (this.isSubcategory) {
        return [{name: this.$route.meta.parent, path: this.$route.meta.path}]
      } else {
        var subcategories = []
        for (var subcategory of this.$route.meta.children) {
          subcategories.push({name: subcategory.name, path: this.$route.path + subcategory.path})
        }
        return subcategories
      }
    },
    navBracket () {
      if (this.isSubcategory) {
        return '<'
      } else {
        return '>'
      }
    }
  },
  methods: {
    sendAxiosRequest (url) {
      this.noItemsMsg = 'Fetching items...'
      axios
        .get(url)
        .then((response) => {
          this.itemData = this.getSortedItems(response.data)
          this.noItemsMsg = 'Sorry, there are no products to display here :('
        })
        .catch(error => alert(error))
    },
    getItemData () {
      var url = null
      if (this.categoryName === 'Bestsellers') {
        url = 'api/resource/item/best'
      } else if (this.categoryName === 'Special Deals') {
        url = 'api/resource/item/deals'
      } else if (this.isSubcategory) {
        url = 'api/resource/subcategory?subcategory=' + encodeURIComponent(this.categoryName)
      } else {
        url = 'api/resource/category?category=' + encodeURIComponent(this.categoryName)
      }
      this.sendAxiosRequest(url)
    },
    getSortedItems (data) {
      switch (this.selectedSort) {
        case 'Bestselling':
          return data.sort((a, b) => { return b.quantity_sold - a.quantity_sold })
        case 'Discount Value':
          return data.sort((a, b) => { return b.discount - a.discount })
        case 'Price: Low to High':
          return data.sort((a, b) => { return this.getRealPrice(a) - this.getRealPrice(b) })
        case 'Price: High to Low':
          return data.sort((a, b) => { return this.getRealPrice(b) - this.getRealPrice(a) })
        default:
          return data
      }
    },
    getRealPrice (item) {
      return item.price - item.price * item.discount
    },
    onSortChanged () {
      this.displayedItems = this.getSortedItems(this.displayedItems)
    },
    onSearch (query) {
      var url = 'api/resource/search?query=' + encodeURIComponent(query)
      this.sendAxiosRequest(url)
    }
  },
  // LIFECYCLE //
  // Note that Created is only called when transitioning from a non-category view
  // (not called when switching between categories or doing multiple searches)
  created () {
    if (this.$route.path === '/search') {
      this.noItemsMsg = 'Fetching items...' // transitioning from a non-category view to search result takes longer
    } else {
      this.getItemData()
    }
    // Event listeners for page change
    bus.$on('page:next', () => { this.pageNumber++ })
    bus.$on('page:previous', () => { this.pageNumber-- })
    bus.$on('page:first', () => { this.pageNumber = 0 })
    bus.$on('page:last', () => { this.pageNumber = this.pageCount - 1 })
    bus.$on('page:number', (page) => { this.pageNumber = page })
    // Event listener for search
    bus.$on('search', (query) => { this.onSearch(query) })
    // Event listener for filters
    bus.$on('filter_change', (filteredData) => {
      this.pageNumber = 0
      this.filteredData = filteredData
    })

    this.advertisement = Math.floor(Math.random() * 8)
  }
}
</script>

<style scoped lang="scss">
#filter-space {
  padding-top: 170px;
  padding-bottom: 10px;
}
#filter-menu {
  position: top;
}
.level {
  width: 100%;
}
#page-title {
color: white;
padding: 30px;
background: linear-gradient(180deg, rgba(0,127,181,1) 0%, rgba(0,162,232,1) 50%,
          rgba(123,215,255,1) 100%);
}
.item-count {
  font-size: smaller;
  text-align: left;
}
#grid {
  display: block;
}
.category {
  color: $darkblue;
  font-weight: bold;
  margin-left: 3px;
}
#sort {
  margin-left: 100px;
}
#sort-text {
  margin: 0px 5px;
  font-size: smaller;
}
#sort-menu {
  width: 160px;
}
.pagination {
  display: block;
  margin: 20px;
}
#navigation-links {
  padding: 20px;
}
.navigation-link {
  display: block;
  text-align: left;
  font-size: smaller;
}
</style>
