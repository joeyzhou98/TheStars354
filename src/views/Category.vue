<template>
  <b-container fluid>
    <b-row>
      <b-col>
        <div id="filter-menu">
          <FilterNav></FilterNav>
        </div>
      </b-col>
      <b-col cols="10">
        <b-row id="page-title" class="text-center">
          <b-col>
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
      itemData: this.createFakeData(80)
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
    }
  },
  methods: {
    createFakeData (count) { // DELETE THIS LATER
      let data = []
      for (let i = 0; i < count; i++) {
        data.push({id: i, name: 'Tile ' + (i + 1)})
      }
      return data
    }
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
  color: $mainblue;
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
