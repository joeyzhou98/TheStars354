<template>
  <b-container v-if="gotData">
    <b-card
      img-height="180"
      img-width="300"
      img-src="https://i.stack.imgur.com/l60Hf.png"
      img-alt="Default picture"
      img-left
      class="mb-3"
      :title="sellerName">

      <b-card-text>
        <b-container fluid>
          <b-row class="justify-content-md-center">
            Member since {{ membership_date }} <br/>
          </b-row>
          <b-row class="justify-content-md-center">
            Average rating &nbsp; <star-rating :starStyle="starStyle" :rating="rating" :isIndicatorActive="false"></star-rating>
          </b-row>
        </b-container>
      </b-card-text>
    </b-card>

    <b-card title="Products sold:">
      <b-container fluid>
        <b-card v-for="item in items" :key="item.item_id">
          <b-row align-v="center">
            <b-col>
              <b-img width="100" height="100" :alt="item.item_name" :src="item.images"></b-img>
            </b-col>
            <b-col>
              <router-link :to="{name: 'ItemDetails', params: {itemID: item.item_id, item: item}}">
                {{ item.item_name }}
              </router-link>
            </b-col>
            <b-col>
              <star-rating style="display: inline-flex" :starStyle="starStyle" :rating="avgRating(item.reviews)" :isIndicatorActive="false"></star-rating>
            </b-col>
          </b-row>
        </b-card>
      </b-container>
    </b-card>

  </b-container>
  <b-spinner v-else style="width: 3rem; height: 3rem;" label="Large Spinner" variant="primary"></b-spinner>
</template>

<script>
import axios from 'axios'
import StarRating from 'vue-dynamic-star-rating'

export default {
  name: 'SellerDetails',
  components: {
    StarRating
  },
  data () {
    return {
      sellerID: this.$route.params.sellerID,
      sellerName: '',
      membership_date: '',
      items: [],
      rating: '',
      gotData: false,
      starStyle: {
        starWidth: 20,
        starHeight: 20
      }
    }
  },
  watch: {},
  computed: {},
  methods: {
    avgRating (reviews) {
      if (reviews.length === 0) {
        return 0
      } else {
        let sum = 0
        let count = 0
        for (let review of reviews) {
          sum += review['rating']
          count += 1
        }
        return sum / count
      }
    },
    getSellerData () {
      let url = 'api/resource/sellerInfo?uid=' + this.sellerID
      axios
        .get(url)
        .then(response => {
          this.items = response.data['offered_products']
          this.membership_date = response.data['membership_date']
          this.sellerName = response.data['seller_name']
          let sum = 0
          let count = 0
          for (let item of this.items) {
            for (let review of item['reviews']) {
              sum += review['rating']
              count += 1
            }
          }
          this.rating = sum / count
          this.gotData = true
        })
        .catch(error => alert(error))
    }
  },
  mounted () {
    this.getSellerData()
  }
}
</script>

<style scoped lang="scss">

</style>
