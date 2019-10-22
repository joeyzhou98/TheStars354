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
    {
      path: '/bestsellers', // categories
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
    {
      path: '/automotives-electronics/cellphones-computers-tablets', // subcatgories
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
      name: 'Clothing, Shoes & Accessories -- Women',
      component: Category
    },
    {
      path: '/clothing-shoes-accessories/men',
      name: 'Clothing, Shoes & Accessories -- Men',
      component: Category
    },
    {
      path: '/clothing-shoes-accessories/children',
      name: 'Clothing, Shoes & Accessories -- Children',
      component: Category
    },
    {
      path: '/clothing-shoes-accessories/shoes',
      name: 'Clothing, Shoes & Accessories -- Shoes',
      component: Category
    },
    {
      path: '/clothing-shoes-accessories/bags-accessories',
      name: 'Clothing, Shoes & Accessories -- Bages & Accessories',
      component: Category
    },
    {
      path: '/health-beauty/makeup',
      name: 'Health & Beauty -- Makeup',
      component: Category
    },
    {
      path: '/health-beauty/creams',
      name: 'Health & Beauty -- Creams',
      component: Category
    },
    {
      path: '/health-beauty/sports',
      name: 'Health & Beauty -- Sports',
      component: Category
    },
    {
      path: '/home-supplies/appliances',
      name: 'Home Supplies -- Appliances',
      component: Category
    },
    {
      path: '/home-supplies/furniture-accessories',
      name: 'Home Supplies -- Furniture & Accessories',
      component: Category
    },
    {
      path: '/home-supplies/gardonsupplies',
      name: 'Home Supplies -- Gardon Supplies',
      component: Category
    },
    {
      path: '/home-supplies/petsupplies',
      name: 'Home Supplies -- Pet Supplies',
      component: Category
    },
    {
      path: '/jewellery-watches/women',
      name: 'Jewellery & Watches -- Women',
      component: Category
    },
    {
      path: '/jewellery-watches/men',
      name: 'Jewellery & Watches -- Men',
      component: Category
    }
  ]
})
