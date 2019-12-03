<template>
    <div>
    <b-card-body>
        <p>Choose the time frame to see all orders and commissions made during that period of time:</p>
        <b-row align-h="center">
            <b-col cols="2">Starting date: </b-col>
            <b-col cols="8">End date: </b-col>
        </b-row>
        <b-row align-h="center">
            <b-col cols="5"><datepicker :format="format" v-model="startingDate" name="startingDate"></datepicker></b-col>
            <b-col cols="5"><datepicker :format="format" v-model="endDate" name="endDate"></datepicker></b-col>
            <b-col>
                <b-button variant="outline-success" title="Search" @click="search">Search</b-button>
            </b-col>
        </b-row>
        <br/><br/>
        <b-card v-if="showResult">
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
                  <b-col>Order Number: {{order.order_id}}</b-col>
                  <b-col>Order placed: {{order.purchase_date.substring(0,16)}}</b-col>
                </b-row>
                <br/>
                <b-row>
                    <b-col>Shipped to: {{order.buyer_id}}</b-col>
                    <b-col>Shipped to: {{order.buyer_address_index}}</b-col>
                </b-row>
                <br/>
                <b-row v-for="item in order.items" :key="item">
                  <b-col>
                    <b-img height="150px" width="150px" :src="item.item.images" class="rounded-0"></b-img>
                  </b-col>
                  <b-col sm="4"><b-link :to="'item-details/' + item.item.item_id">{{item.item.item_name}} (x{{item.order_item_quantity}})</b-link></b-col>
                  <b-col sm="3">${{(item.item.price*(1.0-item.item.discount)).toFixed(2)}}</b-col>
                </b-row>
                <br/>
                <b-row>
                  <b-col>Subtotal: ${{subtotal(order.items)}}</b-col>
                </b-row>
                <b-row>
                  <b-col>Tax: ${{(subtotal(order.items)*0.15).toFixed(2)}}</b-col>
                </b-row>
                <b-row>
                  <b-col>Total: ${{(subtotal(order.items)*1.15).toFixed(2)}}</b-col>
                </b-row>
            </b-card-body>
           </b-card>
        </div>
            <b-card-text v-if="showResult">Commission made during this time is : {{getCommission()}}</b-card-text>
      </b-card>
    </b-card-body>
  </div>
</template>

<script>
import Datepicker from 'vuejs-datepicker'
import moment from 'moment'
import axios from 'axios'

export default {
  name: 'AdminStat',
  components: {
    Datepicker
  },
  data () {
    return {
      startingDate: '',
      endDate: '',
      format: 'yyyy-MM-dd',
      showResult: false,
      orders: [],
      commission: 0,
      perPage: 5,
      currentPage: 1
    }
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
    format_date (value) {
      if (value) {
        console.log(moment(String(value)).format('YYYY-MM-DD'))
        return moment(String(value)).format('YYYY-MM-DD')
      }
    },
    search () {
      var start = this.format_date(this.startingDate)
      var end = this.format_date(this.endDate)
      console.log(start)
      console.log(end)
      let url = 'api/resource/orders/' + encodeURIComponent(start) + '/' + encodeURIComponent(end)
      axios
        .get(url)
        .then(response => {
          this.orders = response.data
        })
        .catch(error => alert(error))
      url = 'api/resource/commission/' + encodeURIComponent(start) + '/' + encodeURIComponent(end)
      axios
        .get(url)
        .then(response => {
          this.commission = response.data
        })
        .catch(error => alert(error))
      this.showResult = true
    },
    subtotal (orderItems) {
      var subtotal = 0
      for (var data of orderItems) {
        let price = data.item.price * (1.0 - data.item.discount).toFixed(2)
        subtotal += price * data.order_item_quantity
      }
      return subtotal.toFixed(2)
    },
    getCommission () {
      return this.commission.toFixed(2)
    }
  }
}
</script>

<style scoped>

</style>
