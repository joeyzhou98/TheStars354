<template>
 <b-navbar-nav>
    <b-nav-item-dropdown no-caret ref="dropdown">
      <template slot="button-content">
        <b-button class="category-button shadow-none" variant="outline">
                  <icon name="bars"></icon>
                  <span class="icon-text">SHOP</span>
        </b-button>
      </template>
      <b-dropdown-text id="dropdown-context" style="width: 95vw;">
        <b-row>
          <b-col class="column" :cols="columnSize(category.name)" v-for="category in categories" :key="category.name">
            <b-row align-h="center">
              <router-link class="main-category text-decoration-none" :to="category.route" @click.native="onClick">
                <span class=main-category-name>{{category.name}}</span>
              </router-link>
            </b-row>
            <div v-for="subcategory in category.subcategories" :key="subcategory.id">
              <b-row align-h="center">
                <router-link class="subcategory text-decoration-none" :to="subcategory.route" @click.native="onClick">
                <span class=subcategory-name>{{subcategory.name}}</span></router-link>
              </b-row>
            </div>
          </b-col>
        </b-row>
      </b-dropdown-text>
    </b-nav-item-dropdown>
  </b-navbar-nav>
</template>

<script>
export default {
  name: 'MainMenu',
  data () {
    return {
      categories: [
        {
          name: 'Automotives & Electronics',
          route: '/automotives-electronics',
          subcategories: [
            { id: 0, name: 'Cellphones, Computers & Tablets', route: '/automotives-electronics/cellphones-computers-tablets' },
            { id: 1, name: 'Cameras & Video Games', route: '/automotives-electronics/cameras-videogames' },
            { id: 2, name: 'Motos & Car Supplies', route: '/automotives-electronics/motos-carsupplies' }
          ]
        },
        {
          name: 'Books',
          route: '/books',
          subcategories: []
        },
        {
          name: 'Clothing, Shoes & Accessories',
          route: '/clothing-shoes-accessories',
          subcategories: [
            { id: 0, name: 'Women\'s Clothing', route: '/clothing-shoes-accessories/women' },
            { id: 1, name: 'Men\'s Clothing', route: '/clothing-shoes-accessories/men' },
            { id: 2, name: 'Children\'s Clothing', route: '/clothing-shoes-accessories/children' },
            { id: 3, name: 'Shoes', route: '/clothing-shoes-accessories/shoes' },
            { id: 4, name: 'Bags & Accessories', route: '/clothing-shoes-accessories/bags-accessories' }
          ]
        },
        {
          name: 'Health & Beauty',
          route: '/health-beauty',
          subcategories: [
            { id: 0, name: 'Makeup', route: '/health-beauty/makeup' },
            { id: 1, name: 'Creams', route: '/health-beauty/creams' },
            { id: 2, name: 'Sports', route: '/health-beauty/sports' }
          ]
        },
        {
          name: 'Home Supplies',
          route: '/home-supplies',
          subcategories: [
            { id: 0, name: 'Appliances', route: '/home-supplies/appliances' },
            { id: 1, name: 'Furniture & Accessories', route: '/home-supplies/furniture-accessories' },
            { id: 2, name: 'Garden Supplies', route: '/home-supplies/gardensupplies' },
            { id: 3, name: 'Pet Supplies', route: '/home-supplies/petsupplies' }
          ]
        },
        {
          name: 'Jewellery & Watches',
          route: '/jewellery-watches',
          subcategories: [
            { id: 0, name: 'Women\'s Jewellery & Watches', route: '/jewellery-watches/women' },
            { id: 1, name: 'Men\'s Jewellery & Watches', route: '/jewellery-watches/men' }
          ]
        }
      ]
    }
  },
  methods: {
    columnSize (category) {
      if (category === 'Books') {
        return 1
      } else if (category === 'Clothing, Shoes & Accessories') {
        return 3
      } else {
        return 2
      }
    },
    onClick () {
      this.$refs.dropdown.hide()
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
  padding-top: 3px;
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
.icon-text {
  position: relative;
  top: 2px;
  margin-left: 5px;
}
.column {
  border-right: 1px solid $lightblue;
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
</style>
