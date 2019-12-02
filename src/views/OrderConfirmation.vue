<template>
  <b-container fluid>
    <br>
    <div style="width: 60%; display: inline-block">
      <b-card>
        <h4>We've received your order! :)</h4><br>
        <div style="font-weight: bold; font-size: large">Order # {{order.order_id}}</div><br>
        <div>Confirmation will be sent to <span class="boldTxt">{{email}}</span></div>
        <hr />
        <div class="alignLeft"><span class="boldTxt">Order placed on:</span> {{order.purchase_date}}</div><br>
        <div class="alignLeft"><span class="boldTxt">Shipped to:</span> {{address}}</div><br>
        <div class="alignLeft"><span class="boldTxt">Shipping method:</span> {{order.shipping_method}}</div><br>
        <div class="alignLeft"><span class="boldTxt">Payment method:</span> PayPal</div>
        <hr />
        <div class="boldTxt alignLeft">Ordered items:</div><br>
        <b-row v-for="item in order.items" :key="item.item.item_id" align-content="left">
          <b-col md="8">
            <div class="alignLeft">{{item.item.item_name}} (x{{item.order_item_quantity}})</div><br>
          </b-col>
          <b-col>
            <div>{{itemPriceTxt(item.item, item.order_item_quantity)}}</div><br>
          </b-col>
        </b-row><br>
        <div class="alignLeft">Subtotal: {{subtotal}}</div>
        <div class="alignLeft">Discount: {{couponDiscount}}</div>
        <div class="alignLeft">Shipping: $0.00</div>
        <div class="alignLeft">Taxes: {{taxes}}</div>
        <div class="alignLeft"><span class="boldTxt">Total: {{total}}</span></div><br>

        <div></div>
      </b-card>
    </div>
  </b-container>
</template>

<script>
export default {
  name: 'OrderConfirmation',
  data () {
    return {
      address: this.$route.params.address,
      order: this.$route.params.order,
      subtotal: this.$route.params.subtotal,
      taxes: this.$route.params.taxes,
      total: this.$route.params.total,
      couponDiscount: this.$route.params.couponDiscount
    }
  },
  computed: {
    email () {
      return this.$store.state.email
    }
  },
  methods: {
    itemPriceTxt (item, qty) {
      let price = (item.price - (item.price * item.discount)) * qty
      return '$' + price.toFixed(2)
    }
  }
}
</script>

<style lang="scss" scoped>
.boldTxt {
  font-weight: bold
}
.alignLeft {
  text-align: left
}
</style>
