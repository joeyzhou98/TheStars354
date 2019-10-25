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
      <b-carousel-slide
        v-for="slide in slides"
        :key="slide.id"
        :img-src="slide.src"
      >
      </b-carousel-slide>
    </b-carousel>
    <br/>
    <b-card-group deck>
    <b-card v-for="categoryCard in categoryCards" :key="categoryCard.id" :title="categoryCard.title" :img-src="categoryCard.src" img-alt="Image" img-top>
      <b-link :href="categoryCard.cardLink">see more products</b-link>
    </b-card>
    </b-card-group>
  </div>
</template>

<script>
export default {
  data () {
    return {
      slides: [
        {
          id: 0,
          src: require('@/assets/home-banners/Sale.png')
        },
        {
          id: 1,
          src: require('@/assets/home-banners/Shipping.png')
        },
        {
          id: 2,
          src: require('@/assets/home-banners/Trending.png')
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
  }
}
</script>
