<template>
  <div>
    <b-card-body class="text-left">
      <h2>Order Received: </h2>
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

          <b-card v-for="order in orderList" :key="order.order_id" no-body class="overflow-hidden"  :per-page="perPage" :current-page="currentPage">
            <b-card-body>
                <b-row>
                  <b-col>Order Number: {{order.order.order_id}}</b-col>
                  <b-col>Order placed: {{order.order.purchase_date.substring(0,16)}}</b-col>
                </b-row>
                <br/>
                <b-row>
                  <b-col>Buyer: {{findBuyerName(order.order.buyer_id)}}</b-col>
                </b-row>
                <b-row>
                  <b-col>Shipped to: {{findBuyerAddress(order.order.buyer_id,order.order.buyer_address_index)}}</b-col>
                </b-row>
                <b-row>
                  <b-col>Status: Shipped</b-col> #get real status from db
                </b-row>
                <br/>
                <b-row v-for="item in order.order.items" :key="item">
                  <b-card-group v-if="item.item.seller_id === this.$store.state.uid">
                  <b-col>
                    <b-img height="150px" width="150px" :src="item.item.images" class="rounded-0"></b-img>
                  </b-col>
                  <b-col sm="4"><b-link :to="'item-details/' + item.item.item_id">{{item.item.item_name}} (x{{item.order_item_quantity}})</b-link></b-col>
                  <b-col sm="3">${{(item.item.price*(1.0-item.item.discount)).toFixed(2)}}</b-col>
                  <!-- Will be better to move to another page that can be used at here and on the item detail page -->
                  </b-card-group>
                </b-row>
            </b-card-body>
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
      orders: []
    }
  },
  mounted () {
    var url = 'api/resource/sellerInfo?uid=' + encodeURIComponent(this.$store.state.uid)
    axios
      .get(url)
      .then(response => {
        this.orders = response.data['orders']
        if (this.orders.length !== 0) {
          this.hasOrderHistroy = true
        }
      })
      .catch(error => alert(error))
  },
  computed: {
    rows () {
      return this.orders.length
    },
    orderList () {
      return this.orders.slice((this.currentPage - 1) * this.perPage, this.currentPage * this.perPage)
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
    },
    findBuyerName (buyerId) {
      var url = 'api/resource/user/' + encodeURIComponent(buyerId)
      axios
        .get(url)
        .then(response => {
          return response.data['username']
        })
        .catch(error => alert(error))
    },
    findBuyerAddress (buyerId, addressIndex) {
      var url = 'api/resource/buyerInfo?uid=' + encodeURIComponent(buyerId)
      axios
        .get(url)
        .then(response => {
          var addressString = 'address' + addressIndex.toString()
          return response.data[addressString]
        })
        .catch(error => alert(error))
    }
  }
}
</script>
