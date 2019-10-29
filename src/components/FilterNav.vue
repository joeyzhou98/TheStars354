<template>
  <div id="filter-menu" role="tablist">
    <b-card no-body v-for="tab in tabsToDisplay" :key="tab.id">
      <b-card-header header-tag="header" class="p-0 m-0" role="tab">
        <b-button class="p-0 m-0 shadow-none"
                  block v-b-toggle="'accordion-'+(tab.id+1)" variant="outline">
          {{tab.tabName}}
        </b-button>
      </b-card-header>
      <b-collapse visible :id="tab.accordion" role="tabpanel">
        <b-card-body class="p-0 m-0">
          <b-form-group align="left" class="p-0 m-0">
            <b-form-checkbox-group
              v-model="tab.selected"
              :options="tab.options"
              :name="tab.name"
              stacked
            >
            </b-form-checkbox-group>
            </b-form-group>
        </b-card-body>
      </b-collapse>
    </b-card>
  </div>
</template>

<script>
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
          options: [],
          selected: []
        },
        {
          id: 3,
          tabName: 'Customer Rating',
          accordion: 'accordion-4',
          name: 'status',
          options: [
            { text: 'Orange', value: 'orange' },
            { text: 'Apple', value: 'apple' },
            { text: 'Pineapple', value: 'pineapple' },
            { text: 'Grape', value: 'grape' }
          ],
          selected: []
        }
      ]
    }
  },
  computed: {
    tabsToDisplay () {
      return this.tabs.filter(tab => tab.options.length !== 0)
    }
  },
  methods: {
    getCategories () {
      if (this.isSubcategory) { // Return because subcategories don't have sub-subcategories...
        return
      }
      var subcategories = []
      for (var item of this.items) {
        if (subcategories.includes(item.subcategory) === false) {
          subcategories.push(item.subcategory)
        }
      }
      this.tabs[0].options = []
      for (var subcategory of subcategories) {
        this.tabs[0].options.push({text: subcategory, value: subcategory})
      }
    },
    getBrands () {

    },
    getPrices () {

    },
    getFilters () {
      this.getCategories()
      this.getBrands()
      this.getPrices()
    }
  },
  watch: {
    // Refresh filters whenever the items list changes
    items () {
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
#filter-menu {
  width: 90%;
}
</style>
