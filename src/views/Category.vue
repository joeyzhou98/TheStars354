<template>
  <div>
    <div class="level columns">
      <div class="level-right column is-one-fifth">
        <div id="filter-menu">Filter menu here.</div>
      </div>
      <div class="level-left column">
        <div id="page-title">
          <h2>{{$route.name}}</h2>
        </div>
        <div id="item-info" class="level">
          <div id="item-count" class="level-left">
            {{itemStart}} - {{itemEnd}} of {{itemData.length}} items in
            <span id="category">{{$route.name}}</span>
          </div>
          <div class="pagination">
            <Pagination :pageNumber="pageNumber" :pageCount="pageCount"></Pagination>
          </div>
          <div id="sort" class="level-right">
            <span id="sort-text">Sort by:</span>
            <b-select placeholder="Bestselling">
              <option>Bestselling</option>
              <option>Newest</option>
              <option>Price: Low to High</option>
              <option>Price: High to Low</option>
            </b-select>
          </div>
        </div>
        <div id="grid">
          <ItemGrid :items="paginatedData"></ItemGrid>
        </div>
        <div class="pagination">
          <Pagination :pageNumber="pageNumber" :pageCount="pageCount"></Pagination>
        </div>
      </div>
    </div>
    </div>
</template>

<script>
import ItemGrid from '@/components/ItemGrid.vue'
import Pagination from '@/components/Pagination.vue'
import { bus } from '../main'

export default {
  name: 'Category',
  components: {
    ItemGrid,
    Pagination
  },
  data () {
    return {
      pageNumber: 0,
      pageSize: 20,
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
  background-color: turquoise;
  position: top;
  margin: 10px
}
.level {
  width: 100%;
}
#page-title {
  display: block;
  margin: 10px 0px 30px 0px;
}
#grid {
  display: block;
}
#category {
  color: $mainblue;
  font-weight: bold;
  margin-left: 5px;
}
#sort-text {
  margin: 0px 5px;
}
.pagination {
  display: block;
  margin: 20px;
}
</style>
