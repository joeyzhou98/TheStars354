<template>
  <div>
    <b-button class="category-button shadow-none" variant="outline"
              @click="openMenu">
              SHOP
    </b-button>
    <Slide noOverlay :isOpen="this.open" @closeMenu="closeMenu">
      <div id="category-block" v-for="category in categories" :key="category.id">
        <router-link class="main-category text-decoration-none" :to="category.route">
          <span class=main-category-name>{{category.name}}</span>
          <div v-for="subcategory in category.subcategories" :key="subcategory.id">
            <router-link class="subcategory text-decoration-none" :to="subcategory.route">
            <span class=subcategory-name>{{subcategory.name}}</span></router-link>
          </div>
        </router-link>
      </div>
    </Slide>
  </div>
</template>>

<script>
// vue-burger-menu source and help:
// https://vuejsexamples.com/an-off-canvas-sidebar-vue-component/
// https://github.com/mbj36/vue-burger-menu/wiki/FAQ

import { Slide } from 'vue-burger-menu'

export default {
  name: 'CategoriesMenu',
  components: {
    Slide
  },
  data () {
    return {
      open: false,
      categories: [
        {
          id: 0,
          name: 'Bestsellers',
          route: '/bestsellers',
          active: false,
          subcategories: []
        },
        {
          id: 1,
          name: 'Automotives & Electronics',
          route: '/automotives-electronics',
          active: true,
          subcategories: [
            { id: 0, name: 'Cellphones, Computers & Tablets', route: '/cellphones-computers-tablets' },
            { id: 1, name: 'Cameras & Video Games', route: '/cameras-videogames' },
            { id: 2, name: 'Motos & Car Supplies', route: '/motos-cars' }
          ]
        },
        {
          id: 2,
          name: 'Books',
          route: '/books',
          active: false,
          subcategories: []
        },
        {
          id: 3,
          name: 'Clothing, Shoes & Accessories',
          route: '/clothing-shoes-accessories',
          active: false,
          subcategories: [
            { id: 0, name: 'Women', route: '/womens-clothing' },
            { id: 1, name: 'Men', route: '/mens-clothing' },
            { id: 2, name: 'Children', route: '/childrens-clothing' },
            { id: 3, name: 'Shoes', route: '/shoes' },
            { id: 4, name: 'Bags & Accessories', route: '/bags-accessories' }
          ]
        },
        {
          id: 4,
          name: 'Health & Beauty',
          route: '/health-beauty',
          active: false,
          subcategories: [
            { id: 0, name: 'Makeup', route: '/makeup' },
            { id: 1, name: 'Creams', route: '/creams' },
            { id: 2, name: 'Sports', route: '/sports' }
          ]
        },
        {
          id: 5,
          name: 'Home Supplies',
          route: '/home-supplies',
          active: false,
          subcategories: [
            { id: 0, name: 'Appliances', route: '/appliances' },
            { id: 1, name: 'Furniture & Accessories', route: '/furniture-accessories' },
            { id: 2, name: 'Garden Supplies', route: '/garden-supplies' },
            { id: 3, name: 'Pet Supplies', route: '/pet-supplies' }
          ]
        },
        {
          id: 6,
          name: 'Jewellery & Watches',
          route: 'jewellery-watches',
          active: false,
          subcategories: [
            { id: 0, name: 'Women', route: '/womens-jewellery-watches' },
            { id: 1, name: 'Men', route: '/mens-jewellery-watches' }
          ]
        }
      ]
    }
  },
  methods: {
    openMenu () {
      this.open = true
    },
    closeMenu () {
      this.open = false
    }
  }
}
</script>

<style scoped lang="scss">
.category-button {
  background: none;
  text-align: center;
  cursor: pointer;
  outline: none;
  color: $darkblue;
  border-color: $darkblue;
  &:hover {
    background: none;
    color: $mainblue;
    border-color: $mainblue;
  }
  &:active {
    position:relative;
    top:1px;
  }
}
</style>

<style lang="scss"> // Unscoped section! These classes are defined in the Slide component
Slide {
  width: 300px;
}
.bm-burger-button {
  display: none;
}
.cross-style {
  position: absolute;
  top: 12px;
  right: 2px;
  cursor: pointer;
}
.bm-cross {
  background: $darkgray;
}
.bm-cross-button {
  height: 24px;
  width: 24px;
}
.bm-menu {
  height: 100%; /* 100% Full-height */
  width: 0; /* 0 width - change this with JavaScript */
  position: fixed; /* Stay in place */
  z-index: 1000; /* Stay on top */
  top: 0;
  left: 0;
  background-color: $lightgray;
  overflow-x: hidden; /* Disable horizontal scroll */
  padding-top: 20px; /* Place content from the top */
  transition: 0.5s; /*0.5 second transition effect to slide in the sidenav*/
  #category-block {
    display: block;
  }
  .main-category {
    font-size: 16px;
    font-weight: 300;
    color: $mainblue;
  }
  .main-category-name {
    &:hover {
      text-decoration: underline;
      color: $darkblue;
    }
  }
  .subcategory-name {
    font-size: 13px;
    color: $darkgray;
    &:hover {
      text-decoration: underline;
    }
  }
  .title {
    font-size: small;
    color: $darkgray;
  }
}
.bm-item-list > * {
  padding: 0.3em 0;
  display: inline-block;
}
</style>
