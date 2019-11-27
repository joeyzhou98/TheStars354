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
                  <b-col sm="4"><b-link :to="'item-details/' + review.item_id">{{getItemName(review.item_id)}})</b-link></b-col>
                </b-row>
                <br/>
                <b-row>
                    <star-rating :starStyle="starStyle" :rating="review.rating" :isIndicatorActive="false"></star-rating>
                </b-row>
                <b-row v-if = "getImages(review).length !== 0">
                    <b-row v-for = "imageUrl in getImages(review)" :key="imageUrl">
                        <b-col>
                            <b-img height="150px" width="150px" :src="imageUrl" class="rounded-0"></b-img>
                        </b-col>
                    </b-row>
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

export default {
  data () {
    return {
      hasReviewHistory: false,
      perPage: 5,
      currentPage: 1,
      reviews: [],
      orders: []
    }
  },
  mounted () {
    var url = 'api/resource/buyerInfo?uid=' + encodeURIComponent(this.$store.state.uid)
    axios
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
  computed: {
    rows () {
      return this.reviews.length
    },
    reviewList () {
      return this.reviews.slice((this.currentPage - 1) * this.perPage, this.currentPage * this.perPage)
    }
  },
  methods: {
    getItemName (itemId) {
      var url = 'api/resource/item/' + encodeURIComponent(itemId)
      axios
        .get(url)
        .then(response => {
          return response.data['item_info']['item_name']
        })
        .catch(error => alert(error))
    },
    getImages (review) {
      var images = review.images
      var imagesUrls = images.split('&')
      return imagesUrls
    }
  }
}
</script>
