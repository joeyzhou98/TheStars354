<template>
  <div role="tablist">
    <b-card no-body v-for="tab in tabs" :key="tab.id">
      <b-card-header header-tag="header" class="p-0 m-0" role="tab">
        <b-button class="p-0 m-0" block v-b-toggle="'accordion-'+(tab.id+1)" variant="info">{{tab.tabName}}</b-button>
      </b-card-header>
      <b-collapse :id="tab.accordion" role="tabpanel">
        <b-card-body class="p-0 m-0">
          <b-form-group align="left" class="p-0 m-0">
            <b-form-checkbox-group
              v-model="selected"
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
  data () {
    return {
      tabs: [
        {
          id: 0,
          tabName: 'Categories',
          accordion: 'accordion-1',
          name: 'categories',
          options: [
            { text: 'new Arrivals', value: 'newArrivals' },
            { text: 'Best Seller', value: 'bestSellers' }
          ]
        },
        {
          id: 1,
          tabName: 'Current Offers',
          accordion: 'accordion-2',
          name: 'currentOffers',
          options: [
            { text: 'On Sale', value: 'onSale' },
            { text: 'Refurbished', value: 'refurbished' },
            { text: 'Online Only', value: 'onlineOnly' },
            { text: 'OpenBox', value: 'openBox' }
          ]
        },
        {
          id: 2,
          tabName: 'Discount',
          accordion: 'accordion-3',
          name: 'discounts',
          options: [
            { text: '60% Off or More', value: '60' },
            { text: '50% Off or More', value: '50' },
            { text: '40% Off or More', value: '40' },
            { text: '30% Off or More', value: '30' },
            { text: '20% Off or More', value: '20' },
            { text: 'All DIscounted Items', value: 'all' }
          ]
        },
        {
          id: 3,
          tabName: 'Status',
          accordion: 'accordion-4',
          name: 'status',
          options: [
            { text: 'Orange', value: 'orange' },
            { text: 'Apple', value: 'apple' },
            { text: 'Pineapple', value: 'pineapple' },
            { text: 'Grape', value: 'grape' }
          ]
        },
        {
          id: 4,
          tabName: 'Brands',
          accordion: 'accordion-5',
          name: 'brands',
          options: [
            { text: 'Orange', value: 'orange' },
            { text: 'Apple', value: 'apple' },
            { text: 'Pineapple', value: 'pineapple' },
            { text: 'Grape', value: 'grape' }
          ]
        },
        {
          id: 5,
          tabName: 'Price',
          accordion: 'accordion-6',
          name: 'prices',
          options: [
            { text: 'Less than $200', value: '200' },
            { text: '$200-$299.99', value: '300' },
            { text: '$300-$399.99', value: '400' },
            { text: '$400-$499.99', value: '500' },
            { text: '$500-$599.99', value: '600' },
            { text: '$500 and Up', value: 'allUp' }
          ]
        },
        {
          id: 6,
          tabName: 'Customer Rating',
          accordion: 'accordion-7',
          name: 'customerRatings',
          options: [
            { text: '5', value: '5' },
            { text: '4', value: '4' },
            { text: '3', value: '3' },
            { text: '2', value: '2' },
            { text: '1', value: '1' }
          ]
        }
      ],
      slected: []
    }
  },
  methods: {

  }
}
</script>

<style scoped>

</style>
