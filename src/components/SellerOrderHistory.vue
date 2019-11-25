<template>
  <div>
    <b-card-body class="text-left">
      <h2>Your Order History: </h2>
      <b-card v-if="!hasOrderHistroy">
        You have no order History...
        <br/>
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
                      <b-col>Review: {{item.review}}</b-col>
                    </b-row>
                    <b-row>
                      <b-col span="2"><b-link :href="item.link">Click to see details</b-link></b-col>
                      <b-col span="2"><b-link @click="findModal('reply')">Replay to a review</b-link></b-col>
                    </b-row>
                  </b-card-text>
                </b-card-body>
              </b-col>
             </b-row>
           </b-card>
        </div>
      </b-card>
    </b-card-body>
    <b-modal ref="reply" hide-footer title="Reply">
      <b-form-textarea
      id="textarea"
      v-model="reviewInput"
      placeholder="Enter your reply here..."
      rows="3"
      max-rows="6"
      ></b-form-textarea>
      <br/>
      <b-button type="submit" variant="outline-success" @click.prevent="addReply" block>Add Reoly</b-button>
    </b-modal>
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
      reviewInput: '',
      ratingInput: '',
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
      ] // for test purpose, delete
    }
  },
  mounted: {
    getOrderInfo () {
      var url = 'api/resource/buyerInfo?username=' + encodeURIComponent(this.$store.state.username)
      axios
        .get(url)
        .then(response => {
          this.items = response.data['orders']
          if (this.items.length !== 0) {
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
      return this.items.slice((this.currentPage - 1) * this.perPage, this.currentPage * this.perPage)
    }
  },
  methods: {
    findModal (modal) {
      this.$refs[modal].show()
    },
    addReply () { // to be added
      var url = 'api/resource/review/' + encodeURIComponent(this.item.id) + '?content=' + encodeURIComponent(this.reviewInput) + '&rating=' + encodeURIComponent(this.ratingInput)
      axios
        .post(url)
        .then(response => {
        })
        .catch(error => alert(error))
      this.$refs['review'].hide()
    }
  }
}
</script>
