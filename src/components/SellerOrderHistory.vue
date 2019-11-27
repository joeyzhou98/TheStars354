<template>
  <div v-if="showPage">
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
                  <b-col md="8">Buyer: {{findBuyerName(order.order.buyer_id)}}</b-col>
                </b-row>
                <b-row>
                  <b-col>Shipped to: {{findBuyerAddress(order.order.buyer_id,order.order.buyer_address_index)}}</b-col>
                </b-row>
                <br/>
                <b-row v-for="item in order.order.items" :key="item">
                  <b-card-group v-if="isSeller(item.item.seller_id)">
                      <b-col>
                          <b-img height="150px" width="150px" :src="item.item.images" class="rounded-0"></b-img>
                      </b-col>
                      <b-col><b-link :to="'item-details/' + item.item.item_id">{{item.item.item_name}})</b-link></b-col>
                      <b-col>Ordered quantity: {{item.order_item_quantity}}</b-col>
                      <b-col><b-button variant="outline-info" title="Status">Shipped</b-button></b-col>
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
      orders: [],
      order_buyer: [],
      order_buyer_name: [],
      order_address: [],
      showPage: false
    }
  },
  mounted () {
    this.populateAllInfo()
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
    async populateAllInfo () {
      await this.getSellerInfo()
      await this.$nextTick()
      await this.getBuyerNames()
      await this.$nextTick()
      await this.getOrderAddress()
      this.showPage = true
    },
    getSellerInfo () {
      var url = 'api/resource/sellerInfo?uid=' + encodeURIComponent(this.$store.state.uid)
      return axios
        .get(url)
        .then(response => {
          this.orders = response.data['orders']
          if (this.orders.length !== 0) {
            this.hasOrderHistroy = true
          }
        })
        .catch(error => alert(error))
    },
    getBuyerNames () {
      let requests = []
      for (var order of this.orders) {
        let url = 'api/resource/user/' + encodeURIComponent(order['order']['buyer_id'])
        requests.push(axios.get(url))
      }
      return axios.all(requests)
        .then(axios.spread((...responses) => {
          for (var response of responses) {
            this.order_buyer_name.push(response.data)
          }
        }))
        .catch(error => { alert(error) })
    },
    getOrderAddress () {
      let requests = []
      for (var order of this.orders) {
        let url = 'api/resource/buyerInfo?uid=' + encodeURIComponent(order['order']['buyer_id'])
        requests.push(axios.get(url))
      }
      return axios.all(requests)
        .then(axios.spread((...responses) => {
          for (var response of responses) {
            this.order_address.push(response.data)
          }
        }))
        .catch(error => { alert(error) })
    },
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
      for (var data of this.order_buyer_name) {
        if (data.uid === buyerId) {
          return data.username
        }
      }
    },
    findBuyerAddress (buyerId, addressIndex) {
      for (var data of this.order_address) {
        if (data.uid === buyerId) {
          var addressString = 'address' + addressIndex.toString()
          return data[addressString]
        }
      }
    },
    isSeller (itemSellerId) {
      console.log(itemSellerId)
      return itemSellerId === this.$store.state.uid
    }
  }
}
</script>
