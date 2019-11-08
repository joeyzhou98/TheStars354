<template>
  <b-card>
    <star-rating :starStyle="starStyle" :rating="review.rating" :isIndicatorActive="false"></star-rating>
    <b-card-text v-if="review.content !== null" style="display: flex; padding-top: 15px;">{{review.content}}</b-card-text>
  </b-card>
</template>

<script>
import StarRating from 'vue-dynamic-star-rating'

export default {
  name: 'Review',
  components: {
    StarRating
  },
  props: ['review'],
  data () {
    return {
      starStyle: {
        starWidth: 20,
        starHeight: 20
      }
    }
  }
}
</script>

<style scoped>

</style>
