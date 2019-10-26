import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import FAQ from './views/FAQ.vue'
import About from './views/About.vue'
import Account from './views/Account.vue'
import Category from './views/Category.vue'
import Cart from './views/Cart.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/faq',
      name: 'FAQ',
      component: FAQ
    },
    {
      path: '/about',
      name: 'About',
      component: About
    },
    {
      path: '/account',
      name: 'Account',
      component: Account
    },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart
    },
    // Categories
    {
      path: '/bestsellers',
      name: 'Bestsellers',
      component: Category
    },
    {
      path: '/automotives-electronics',
      name: 'Automotives & Electronics',
      component: Category
    },
    {
      path: '/books',
      name: 'Books',
      component: Category
    },
    {
      path: '/clothing-shoes-accessories',
      name: 'Clothing, Shoes & Accessories',
      component: Category
    },
    {
      path: '/health-beauty',
      name: 'Health & Beauty',
      component: Category
    },
    {
      path: '/home-supplies',
      name: 'Home Supplies',
      component: Category
    },
    {
      path: '/jewellery-watches',
      name: 'Jewellery & Watches',
      component: Category
    },
    // Subcategories
    {
      path: '/automotives-electronics/cellphones-computers-tablets',
      name: 'Cellphones, Computers & Tablets',
      component: Category
    },
    {
      path: '/automotives-electronics/cameras-videogames',
      name: 'Cameras & Video Games',
      component: Category
    },
    {
      path: '/automotives-electronics/motos-carsupplies',
      name: 'Motos & Car Supplies',
      component: Category
    },
    {
      path: '/clothing-shoes-accessories/women',
      name: 'Women\'s Clothing',
      component: Category
    },
    {
      path: '/clothing-shoes-accessories/men',
      name: 'Men\'s Clothing',
      component: Category
    },
    {
      path: '/clothing-shoes-accessories/children',
      name: 'Children\'s Clothing',
      component: Category
    },
    {
      path: '/clothing-shoes-accessories/shoes',
      name: 'Shoes',
      component: Category
    },
    {
      path: '/clothing-shoes-accessories/bags-accessories',
      name: 'Bags & Accessories',
      component: Category
    },
    {
      path: '/health-beauty/makeup',
      name: 'Makeup',
      component: Category
    },
    {
      path: '/health-beauty/creams',
      name: 'Creams',
      component: Category
    },
    {
      path: '/health-beauty/sports',
      name: 'Sports',
      component: Category
    },
    {
      path: '/home-supplies/appliances',
      name: 'Appliances',
      component: Category
    },
    {
      path: '/home-supplies/furniture-accessories',
      name: 'Furniture & Accessories',
      component: Category
    },
    {
      path: '/home-supplies/gardensupplies',
      name: 'Garden Supplies',
      component: Category
    },
    {
      path: '/home-supplies/petsupplies',
      name: 'Pet Supplies',
      component: Category
    },
    {
      path: '/jewellery-watches/women',
      name: 'Women\'s Jewellery & Watches',
      component: Category
    },
    {
      path: '/jewellery-watches/men',
      name: 'Men\'s Jewellery & Watches',
      component: Category
    }
  ]
})
