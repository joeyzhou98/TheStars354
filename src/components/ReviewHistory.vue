<template>
  <div>
    <b-card-body class="text-left">
      <h2>Your Review History: </h2>
      <b-card v-if="!hasReviewHistory">
        You haven't posted any reviews...
        <br/>
      </b-card>
      <b-card v-if="hasReviewHistory">
        <div class="overflow-auto">
          <b-pagination
            size="sm"
            align="center"
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
          ></b-pagination>

          <b-card v-for="review in reviewList" :key="review.review_id" no-body class="overflow-hidden"  :per-page="perPage" :current-page="currentPage">
            <b-card-body>
                <b-row>
                  <b-col sm="10"><b-link :to="'item-details/' + review.item_id">{{findItemName(review.item_id)}}</b-link></b-col>
                </b-row>
                <br/>
                <b-row>
                    <star-rating :starStyle="starStyle" :rating="review.rating" :isIndicatorActive="false"></star-rating>
                </b-row>
                <br/><br/>
                <b-row v-if = "getImages(review).length !== 0">
                    <b-row v-for = "imageUrl in getImages(review)" :key="imageUrl">
                        <b-col>
                            <b-img height="150px" width="150px" :src="imageUrl" class="rounded-0"></b-img>
                        </b-col>
                    </b-row>
                </b-row>
                <b-row>
                  <b-col>{{review.content}}</b-col>
                </b-row>
                <b-row v-if="hasSellerReply(review)">
                  <b-col>Seller reply: {{review.reply}}</b-col>
                </b-row>
                <br/>
            </b-card-body>
           </b-card>
        </div>
      </b-card>
    </b-card-body>
  </div>
</template>

<script>
import axios from 'axios'
import StarRating from 'vue-dynamic-star-rating'

export default {
  components: {
    StarRating
  },
  data () {
    return {
      hasReviewHistory: false,
      perPage: 5,
      currentPage: 1,
      reviews: [],
      orders: [],
      reviewItems: [],
      showpage: false,
      starStyle: {
        starWidth: 20,
        starHeight: 20
      }
    }
  },
  mounted () {
    this.getAllInfo()
  },
  computed: {
    rows () {
      return this.reviews.length
    },
    reviewList () {
      return this.reviews.slice((this.currentPage - 1) * this.perPage, this.currentPage * this.perPage)
    }
  },
  methods: {
    async getAllInfo () {
      await this.getBuyerInfo()
      await this.$nextTick()
      await this.getItemNames()
      this.showpage = true
    },
    getBuyerInfo () {
      var url = 'api/resource/buyerInfo?uid=' + encodeURIComponent(this.$store.state.uid)
      return axios
        .get(url)
        .then(response => {
          this.reviews = response.data['review_list']
          this.orders = response.data['order_history']
          if (this.reviews.length !== 0) {
            this.hasReviewHistory = true
          }
        })
        .catch(error => alert(error))
    },
    getItemNames () {
      let requests = []
      for (var review of this.reviews) {
        let url = 'api/resource/item/' + encodeURIComponent(review['item_id'])
        requests.push(axios.get(url))
      }
      return axios.all(requests)
        .then(axios.spread((...responses) => {
          for (var response of responses) {
            this.reviewItems.push(response.data)
          }
        }))
        .catch(error => { alert(error) })
    },
    getImages (review) {
      var images = review.images
      if (images !== null && images !== '') {
        return images.split('&')
      }
      return []
    },
    hasSellerReply (review) {
      return review.reply !== null && review.reply !== ''
    },
    findItemName (itemId) {
      for (var data of this.reviewItems) {
        if (data['item_info']['item_id'] === itemId) {
          return data['item_info']['item_name']
        }
      }
    }
  }
}
</script>
