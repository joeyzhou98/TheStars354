<template>
  <b-card>
    <star-rating style="padding-bottom: 10px;" :starStyle="starStyle" :rating="review.rating" :isIndicatorActive="false"></star-rating>
    <b-card-text v-if="review.content !== null" style="display: flex;">{{review.content}}</b-card-text>
    <b-card-text v-if="review.reply !== null" style="display: flex;"><strong>Seller's reply:</strong>{{review.reply}}</b-card-text>
    <b-button v-if="isReviewBuyer" size="sm" variant="danger" style="float: left; margin-right: 10px;" @click="deleteReview">Delete</b-button>
    <b-button v-if="sellerItem" size="sm" variant="primary" style="float: left;" @click="$bvModal.show(review.review_id)">Reply</b-button>
    <b-modal @ok="submitReply" :id="review.review_id" title="Reply to review">
      <b-form-textarea
        id="textarea"
        v-model="text"
        placeholder="Enter reply..."
        rows="3"
        max-rows="6"
      ></b-form-textarea>
    </b-modal>
  </b-card>
</template>

<script>
import StarRating from 'vue-dynamic-star-rating'
import axios from 'axios'

export default {
  name: 'Review',
  components: {
    StarRating
  },
  props: ['review', 'seller_id'],
  data () {
    return {
      starStyle: {
        starWidth: 20,
        starHeight: 20
      },
      text: ''
    }
  },
  methods: {
    deleteReview () {
      let url = 'api/resource/review/' + this.review.item_id + '/' + this.review.review_id
      axios
        .delete(url)
        .then(response => {
          this.$router.push('/')
        })
        .catch(error => alert(error))
    },
    submitReply () {
      if (this.text !== '') {
        let url = 'api/resource/review/' + this.review.item_id + '/' + this.review.review_id + '?response=' + this.text
        axios
          .put(url)
          .then(response => {
            this.review.reply = this.text
          })
          .catch(error => alert(error))
      }
    }
  },
  computed: {
    isReviewBuyer () {
      return this.$store.state.uid === this.review.buyer_id
    },
    sellerItem () {
      return this.$store.state.uid === this.seller_id
    }
  }
}
</script>

<style scoped>

</style>
