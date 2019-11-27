<template>
  <div>
    <b-carousel
      id="carousel-1"
      :interval="4000"
      controls
      indicators
      background="#ababab"
      img-width="1024"
      img-height="480"
      @sliding-start="onSlideStart"
      @sliding-end="onSlideEnd"
    >
      <b-link v-for="slide in slides" :key="slide.id" :to="slide.link">
        <b-carousel-slide :img-src="slide.src">
        </b-carousel-slide>
      </b-link>
    </b-carousel>
    <br/>
    <div v-if="hasHistory">
      <h5 class="section">Recently viewed:</h5>
      <b-card>
        <Recommendations :showHistory="true"></Recommendations>
      </b-card>
    </div>
    <br />
    <h5 class="section">Shop by category</h5>
    <b-card-group deck>
      <b-card v-for="categoryCard in categoryCards" :key="categoryCard.id" no-body  :title="categoryCard.title">
        <b-link :href="categoryCard.cardLink">
          <b-card-img :src="categoryCard.src" />
        </b-link>
        <div style="font-size: large; margin: 10px;">{{categoryCard.title}}</div>
        <b-link :href="categoryCard.cardLink">see more products</b-link>
        <br />
      </b-card>
    </b-card-group>
    <br />
    <h5 class="section">You might like:</h5>
    <b-card>
      <Recommendations :showHistory="false"></Recommendations>
    </b-card>
    <br />
  </div>
</template>

<script>
import Recommendations from '@/components/Recommendations.vue'

export default {
  components: {
    Recommendations
  },
  data () {
    return {
      slides: [
        {
          id: 0,
          src: require('@/assets/home-banners/Sale.png'),
          link: '/deals'
        },
        {
          id: 1,
          src: require('@/assets/home-banners/Shipping.png'),
          link: '/FAQ'
        },
        {
          id: 2,
          src: require('@/assets/home-banners/Trending.png'),
          link: '/bestsellers'
        }
      ],
      categoryCards: [
        {
          id: 0,
          title: 'Automotives & Electronics',
          src: require('@/assets/home-categories/Electronics.png'),
          cardLink: '#/automotives-electronics'
        },
        {
          id: 1,
          title: 'Books',
          src: require('@/assets/home-categories/Books.png'),
          cardLink: '#/books'
        },
        {
          id: 2,
          title: 'Clothing, Shoes & Accessories',
          src: require('@/assets/home-categories/Clothing.png'),
          cardLink: '#/clothing-shoes-accessories'
        },
        {
          id: 3,
          title: 'Health & Beauty',
          src: require('@/assets/home-categories/Beauty.png'),
          cardLink: '#/health-beauty'
        },
        {
          id: 4,
          title: 'Home Supplies',
          src: require('@/assets/home-categories/Home.png'),
          cardLink: '#/home-supplies'
        },
        {
          id: 5,
          title: 'Jewellery & Watches',
          src: require('@/assets/home-categories/Jewellery.png'),
          cardLink: '#/jewellery-watches'
        }
      ]
    }
  },
  computed: {
    hasHistory () {
      return localStorage.history
    }
  }
}
</script>

<style lang="scss" scoped>
.section {
  text-align: left;
}
</style>
