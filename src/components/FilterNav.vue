<template>
  <div id="content">
    <div class="clear-container">
      <b-button class="clear-filter shadow-none" size="sm" variant="outline" @click="clearFilters">
        clear filters [x]
      </b-button>
    </div><br>
    <div id="filter-menu" role="tablist">
      <b-card no-body v-for="tab in tabsToDisplay" :key="tab.id">
        <b-card-header header-tag="header" class="p-0 m-0" role="tab">
          <b-button class="p-0 m-0 shadow-none category"
                    block v-b-toggle="'accordion-'+(tab.id+1)" variant="outline">
            {{tab.tabName}}
          </b-button>
        </b-card-header>
        <b-collapse visible :id="tab.accordion" role="tabpanel">
          <b-card-body class="p-0 m-0">
            <b-form-group align="left" class="p-0 m-0">
              <b-form-checkbox-group class="checkboxes"
                v-model="tab.selected"
                :options="tab.options"
                :name="tab.name"
                stacked
                @input="onFilterChange">
              </b-form-checkbox-group>
              </b-form-group>
          </b-card-body>
        </b-collapse>
      </b-card>
    </div>
    <div class="clear-container">
      <b-button class="clear-filter shadow-none" size="sm" variant="outline" @click="clearFilters">
        clear filters [x]
      </b-button>
    </div>
  </div>
</template>

<script>
import { bus } from '../main'

export default {
  props: {
    items: {
      type: Array,
      required: true
    },
    isSubcategory: {
      type: Boolean,
      required: true
    }
  },
  data () {
    return {
      tabs: [
        {
          id: 0,
          tabName: 'Categories',
          accordion: 'accordion-1',
          name: 'categories',
          options: [],
          selected: []
        },
        {
          id: 1,
          tabName: 'Brands',
          accordion: 'accordion-2',
          name: 'brands',
          options: [],
          selected: []
        },
        {
          id: 2,
          tabName: 'Price',
          accordion: 'accordion-3',
          name: 'price',
          options: [ // Value is the minimum price in the range
            { text: 'Under $25', value: 0 },
            { text: '$25 - $50', value: 25 },
            { text: '$50 - $100', value: 50 },
            { text: '$100 - $200', value: 100 },
            { text: '$200 & Above', value: 200 }
          ],
          selected: []
        },
        {
          id: 3,
          tabName: 'Customer Rating',
          accordion: 'accordion-4',
          name: 'rating',
          options: [],
          selected: []
        }
      ]
    }
  },
  computed: {
    tabsToDisplay () {
      return this.tabs.filter(tab => tab.options.length !== 0)
    },
    filteredResult () {
      var fromCategories = this.filteredCategories(this.items)
      var fromBrands = this.filteredBrands(fromCategories)
      return this.filteredPrices(fromBrands)
    }
  },
  methods: {
    getCategories () {
      this.tabs[0].options = []
      if (this.isSubcategory) { // Return because subcategories don't have sub-subcategories...
        return
      }
      var subcategories = []
      for (var item of this.items) {
        if (subcategories.includes(item.subcategory) === false) {
          subcategories.push(item.subcategory)
        }
      }
      subcategories.sort()
      for (var subcategory of subcategories) {
        this.tabs[0].options.push({text: subcategory, value: subcategory})
      }
    },
    getBrands () {
      var brands = []
      for (var item of this.items) {
        if (brands.includes(item.brand) === false) {
          brands.push(item.brand)
        }
      }
      brands.sort()
      this.tabs[1].options = []
      for (var brand of brands) {
        this.tabs[1].options.push({text: brand, value: brand})
      }
    },
    getFilters () {
      this.getCategories()
      this.getBrands()
    },
    clearFilters () {
      for (var tab of this.tabs) {
        tab.selected = []
      }
    },
    onFilterChange () {
      bus.$emit('filter_change', this.filteredResult)
    },
    filteredCategories (itemsToFilter) {
      if (this.tabs[0].selected.length === 0) {
        return itemsToFilter
      }
      return itemsToFilter.filter(item => this.tabs[0].selected.includes(item.subcategory))
    },
    filteredBrands (itemsToFilter) {
      if (this.tabs[1].selected.length === 0) {
        return itemsToFilter
      }
      return itemsToFilter.filter(item => this.tabs[1].selected.includes(item.brand))
    },
    filteredPrices (itemsToFilter) {
      if (this.tabs[2].selected.length === 0) {
        return itemsToFilter
      }
      var priceMin = Math.min(...this.tabs[2].selected) // min value already specified
      var filterMax = Math.max(...this.tabs[2].selected)
      var priceMax
      if (filterMax === 0) {
        priceMax = 25
      } else if (filterMax === 200) { // then it's 200 & above - no limit
        priceMax = Number.MAX_VALUE
      } else {
        priceMax = filterMax * 2
      }
      return itemsToFilter.filter(item => (item.price - item.price * item.discount) >= priceMin &&
       (item.price - item.price * item.discount) <= priceMax)
    }
  },
  watch: {
    // Refresh filters whenever the items list changes
    items () {
      this.clearFilters()
      this.getFilters()
    }
  },
  // Lifecycle //
  mounted () {
    this.getFilters()
  }
}
</script>

<style scoped lang="scss">
#content {
  width: 90%;
}
.clear-container {
  display: block;
  margin-bottom: 8px;
}
.clear-filter {
  position: absolute;
  right: 20px;
  color: gray;
  &:hover {
    color: red;
  }
}
.checkboxes {
  margin: 5px;
  font-size: smaller;
}
.category {
  background-color: $lightblue;
  font-weight: bold;
  font-size: smaller;
}
</style>
