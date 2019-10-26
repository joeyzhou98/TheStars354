<template>
  <b-container fluid>
    <b-row>
      <b-col>
        <b-row>
          <div id="filter-info">
            Refine by...
          </div>
        </b-row>
        <b-row>
          <FilterNav></FilterNav>
        </b-row>
      </b-col>
      <b-col cols="10">
        <b-row id="page-title" class="text-center">
          <b-col>
          <span :v-if="isSubcategory">{{$route.meta.parent}}</span>
          <h1>{{$route.name}}</h1>
          </b-col>
        </b-row>
        <b-row id="item-info" align-v="center">
          <b-col id="item-count">
            {{itemStart}} - {{itemEnd}} of {{itemData.length}} items in
            <span id="category">{{$route.name}}</span>
          </b-col>
          <b-col class="pagination">
            <Pagination :pageNumber="pageNumber" :pageCount="pageCount"></Pagination>
          </b-col>
          <b-col>
            <div id="sort">
              <span id="sort-text">Sort by:</span>
              <b-select id="sort-menu" size="sm" :v-model="selectedSort" :options="sortOptions">
              </b-select>
            </div>
          </b-col>
        </b-row>
        <b-row id="grid">
          <ItemGrid :items="paginatedData"></ItemGrid>
        </b-row>
        <b-row class="pagination">
          <Pagination :pageNumber="pageNumber" :pageCount="pageCount" :needScrollTop="true"></Pagination>
        </b-row>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import ItemGrid from '@/components/ItemGrid.vue'
import Pagination from '@/components/Pagination.vue'
import FilterNav from '@/components/FilterNav.vue'
import axios from 'axios'
import { bus } from '../main'

export default {
  name: 'Category',
  components: {
    ItemGrid,
    Pagination,
    FilterNav
  },
  data () {
    return {
      pageNumber: 0,
      pageSize: 20,
      selectedSort: 0,
      sortOptions: [
        { value: 0, text: 'Bestselling' },
        { value: 1, text: 'Newest' },
        { value: 2, text: 'Price: Low to High' },
        { value: 3, text: 'Price: High to Low' }
      ],
      itemData: null
    }
  },
  watch: {
    // Refresh data when changing categories
    $route (to, from) {
      if (to !== from) {
        this.getItemData()
      }
    }
  },
  computed: {
    pageCount () {
      return Math.ceil(this.itemData.length / this.pageSize)
    },
    itemStart () {
      return this.pageNumber * this.pageSize
    },
    itemEnd () {
      return this.itemStart + this.pageSize
    },
    paginatedData () {
      return this.itemData.slice(this.itemStart, this.itemEnd)
    },
    isSubcategory () {
      return this.$route.meta.parent != null
    },
    categoryName () {
      return this.$route.name
    }
  },
  methods: {
    getItemData () {
      var url = null
      if (this.categoryName === 'Bestsellers') {
        url = 'http://localhost:5000/api/resource/item/best'
      } else if (this.isSubcategory) {
        url = 'http://localhost:5000/api/resource/subcategory?subcategory=' + encodeURIComponent(this.categoryName)
      } else {
        url = 'http://localhost:5000/api/resource/category?category=' + encodeURIComponent(this.categoryName)
      }

      axios
        .get(url)
        .then(response => (this.itemData = response.data))
        .catch(error => alert(error))
    }
  },
  mounted () {
    this.getItemData()
  },
  created () {
    // Event listeners for page change
    bus.$on('page:next', () => { this.pageNumber++ })
    bus.$on('page:previous', () => { this.pageNumber-- })
    bus.$on('page:first', () => { this.pageNumber = 0 })
    bus.$on('page:last', () => { this.pageNumber = this.pageCount - 1 })
    bus.$on('page:number', (page) => { this.pageNumber = page })
  }
}
</script>

<style scoped lang="scss">
#filter-info {
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
#item-count {
  font-size: smaller;
  text-align: left;
}
#grid {
  display: block;
}
#category {
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
</style>
