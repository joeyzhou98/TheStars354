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
      style="text-shadow: 1px 1px 2px #333;"
      @sliding-start="onSlideStart"
      @sliding-end="onSlideEnd"
    >
      <b-carousel-slide
        v-for="slide in slides"
        :key="slide.id"
        :caption="slide.caption"
        :text="slide.text"
        :img-src="slide.src"
      >
      </b-carousel-slide>
    </b-carousel>
    <br/>
    <b-card-group deck>
    <b-card v-for="categoryCard in categoryCards" :key="categoryCard.id" :title="categoryCard.title" :img-src="categoryCard.src" img-alt="Image" img-top>
      <b-card-text>
        {{categoryCard.text}}
      </b-card-text>
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
          caption: 'Deal of the week',
          text: 'Save Save Save',
          src: 'https://picsum.photos/1024/480/?image=52'
        },
        {
          id: 1,
          caption: 'Best Sellers',
          text: 'Save Save Save',
          src: 'https://picsum.photos/1024/480/?image=55'
        },
        {
          id: 2,
          caption: 'Hot New Releases',
          text: 'Save Save Save',
          src: 'https://picsum.photos/1024/480/?image=58'
        }
      ],
      categoryCards: [
        {
          id: 0,
          title: 'Automotives & Electronics',
          src: 'https://picsum.photos/300/300/?image=41',
          text: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
          cardLink: '#/automotives-electronics'
        },
        {
          id: 1,
          title: 'Books',
          src: 'https://picsum.photos/300/300/?image=41',
          text: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
          cardLink: '#/books'
        },
        {
          id: 2,
          title: 'Clothing, Shoes & Accessories',
          src: 'https://picsum.photos/300/300/?image=41',
          text: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
          cardLink: '#/clothing-shoes-accessories'
        },
        {
          id: 3,
          title: 'Health & Beauty',
          src: 'https://picsum.photos/300/300/?image=41',
          text: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
          cardLink: '#/health-beauty'
        },
        {
          id: 4,
          title: 'Home Suppiles',
          src: 'https://picsum.photos/300/300/?image=41',
          text: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
          cardLink: '#/home-suppiles'
        },
        {
          id: 5,
          title: 'Jewellery & Watches',
          src: 'https://picsum.photos/300/300/?image=41',
          text: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
          cardLink: '#/jewellery-watches'
        }
      ]
    }
  },
  methods: {

  }
}
</script>
