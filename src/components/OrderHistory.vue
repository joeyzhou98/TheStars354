<template>
  <div>
    <b-card-body class="text-left">
      <h2>Your Order History: </h2>
      <b-card v-if="!hasOrderHistroy">
        You have no order History...
        <br/>
        <b-link href="/">Go to shopping</b-link>
      </b-card>
      <b-card v-if="hasOrderHistroy">
        <div class="overflow-auto">
          <b-pagination
            size="sm"
            align="center"
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
          ></b-pagination>

          <b-card v-for="item in itemList" :key="item.id" no-body class="overflow-hidden"  :per-page="perPage" :current-page="currentPage">
            <b-row no-gutters>
              <b-col md="3">
                <b-img height="150px" width="150px" src="https://picsum.photos/400/400/?image=20" class="rounded-0"></b-img>
              </b-col>
              <b-col md="8">
                <b-card-body>
                  <b-card-text>
                    <b-row>
                      <b-col>Item Name: {{item.name}}</b-col>
                      <b-col>Quantity: {{item.quantity}}</b-col>
                    </b-row>
                    <b-row>
                      <b-col>Price: {{item.price}}</b-col>
                      <b-col>Total Price: {{item.price*item.quantity}}</b-col>
                    </b-row>
                    <b-row>
                      <b-col>Purchase Date: {{item.date}}</b-col>
                    </b-row>
                    <b-row>
                      <b-col span="2"><b-link :href="item.link">Click to see details</b-link></b-col>
                      <b-col span="2"><b-link :href="item.link">Write a review</b-link></b-col>
                    </b-row>
                  </b-card-text>
                </b-card-body>
              </b-col>
             </b-row>
           </b-card>
        </div>
      </b-card>
    </b-card-body>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      hasOrderHistroy: false,
      perPage: 5,
      currentPage: 1,
      items: [
        { id: 1, name: 'Fred', date: 'Flintstone' },
        { id: 2, name: 'Wilma', date: 'Flintstone' },
        { id: 3, name: 'Barney', date: 'Rubble' },
        { id: 4, name: 'Betty', date: 'Rubble' },
        { id: 5, name: 'Pebbles', date: 'Flintstone' },
        { id: 6, name: 'Bamm Bamm', date: 'Rubble' },
        { id: 7, name: 'The Great', date: 'Gazzoo' },
        { id: 8, name: 'Rockhead', date: 'Slate' },
        { id: 9, name: 'Pearl', date: 'Slaghoople' }
      ]
    }
  },
  mounted: {
    getOrderInfo () {
      var url = 'api/resource/buyerInfo'
      axios
        .get(url)
        .then(response => {
          this.items = response.data['items']
          if (this.items !== '') {
            this.hasOrderHistroy = true
          }
        })
        .catch(error => alert(error))
    }
  },
  computed: {
    rows () {
      return this.items.length
    },
    itemList () {
      // const items = this.$store.getters.loadedLists
      return this.items.slice((this.currentPage - 1) * this.perPage, this.currentPage * this.perPage)
    }
  }
}
</script>
