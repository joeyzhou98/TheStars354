<template>
  <b-link @click="goToItem">
    <img :src="adToShow.src" />
  </b-link>
</template>

<script>
export default {
  name: 'Advertisement',
  props: ['random'],
  data () {
    return {
      ad: [
        { src: require('@/assets/advertisement/macbook.png'), link: '/item-details/66' },
        { src: require('@/assets/advertisement/book.png'), link: '/item-details/115' },
        { src: require('@/assets/advertisement/shoes.png'), link: '/item-details/9' },
        { src: require('@/assets/advertisement/watch.png'), link: '/item-details/126' },
        { src: require('@/assets/advertisement/jeans.png'), link: '/item-details/24' },
        { src: require('@/assets/advertisement/wedding.png'), link: '/item-details/60' },
        { src: require('@/assets/advertisement/bag.png'), link: '/item-details/12' },
        { src: require('@/assets/advertisement/acer.png'), link: '/item-details/1' }
      ]
    }
  },
  computed: {
    adToShow () {
      return this.ad[this.random]
    }
  },
  methods: {
    goToItem () {
      this.$router.push(this.adToShow.link)
    }
  }
}
</script>

<style lang="scss" scoped>
img {
  width: 90%;
}
</style>
