import Vue from 'vue'
import Router from 'vue-router'

import About from './views/About.vue'
import Account from './views/Account.vue'
import Category from './views/Category.vue'
import Cart from './views/Cart.vue'
import ChangePassword from './views/ChangePassword'
import FAQ from './views/FAQ.vue'
import ForgetPassword from './views/ForgetPassword'
import Home from './views/Home.vue'
import ItemDetails from './views/ItemDetails.vue'
import SellerDetails from './views/SellerDetails.vue'
import Login from './views/Login.vue'
import OrderConfirmation from './views/OrderConfirmation.vue'
import PlaceOrder from './views/PlaceOrder.vue'
import Register from './views/Register.vue'

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
      path: '/forgetPassword',
      name: 'ForgetPassword',
      component: ForgetPassword
    },
    {
      path: '/changePassword/:token/:username',
      name: 'ChangePassword',
      component: ChangePassword
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
      path: '/place-order',
      name: 'PlaceOrder',
      component: PlaceOrder
    },
    {
      path: '/order-confirmation',
      name: 'OrderConfirmation',
      component: OrderConfirmation
    },
    // Item display
    {
      path: '/item-details/:itemID',
      name: 'ItemDetails',
      component: ItemDetails
    },
    {
      path: '/seller-details/:sellerID',
      name: 'SellerDetails',
      component: SellerDetails
    },
    {
      path: '/bestsellers',
      name: 'Bestsellers',
      component: Category,
      meta: { children: [
        { name: 'Bestsellers', path: '' }
      ]}
    },
    {
      path: '/deals',
      name: 'Special Deals',
      component: Category,
      meta: { children: [
        { name: 'Special Deals', path: '' }
      ]}
    },
    {
      path: '/search',
      name: 'Search Results',
      component: Category,
      meta: { children: [
        { name: 'Search Results', path: '' }
      ]}
    },
    // Categories
    {
      path: '/automotives-electronics',
      name: 'Automotives & Electronics',
      component: Category,
      meta: { children: [
        { name: 'Cellphones, Computers & Tablets', path: '/cellphones-computers-tablets' },
        { name: 'Cameras & Video Games', path: '/cameras-videogames' },
        { name: 'Motos & Car Supplies', path: '/motos-carsupplies' }
      ]}
    },
    {
      path: '/books',
      name: 'Books',
      component: Category,
      meta: { children: [
        { name: 'Books', path: '' }
      ]}
    },
    {
      path: '/clothing-shoes-accessories',
      name: 'Clothing, Shoes & Accessories',
      component: Category,
      meta: { children: [
        { name: 'Women\'s Clothing', path: '/women' },
        { name: 'Men\'s Clothing', path: '/men' },
        { name: 'Children\'s Clothing', path: '/children' },
        { name: 'Shoes', path: '/shoes' },
        { name: 'Bags & Accessories', path: '/bags-accessories' }
      ]}
    },
    {
      path: '/health-beauty',
      name: 'Health & Beauty',
      component: Category,
      meta: { children: [
        { name: 'Makeup', path: '/makeup' },
        { name: 'Creams', path: '/creams' },
        { name: 'Sports', path: '/sports' }
      ]}
    },
    {
      path: '/home-supplies',
      name: 'Home Supplies',
      component: Category,
      meta: { children: [
        { name: 'Appliances', path: '/appliances' },
        { name: 'Furniture & Accessories', path: '/furniture-accessories' },
        { name: 'Garden Supplies', path: '/gardensupplies' },
        { name: 'Pet Supplies', path: '/petsupplies' }
      ]}
    },
    {
      path: '/jewellery-watches',
      name: 'Jewellery & Watches',
      component: Category,
      meta: { children: [
        { name: 'Men\'s Jewellery & Watches', path: '/men' },
        { name: 'Women\'s Jewellery & Watches', path: '/women' }
      ]}
    },
    // Subcategories
    {
      path: '/automotives-electronics/cellphones-computers-tablets',
      name: 'Cellphones, Computers & Tablets',
      component: Category,
      meta: { parent: 'Automotives & Electronics', path: '/automotives-electronics' }
    },
    {
      path: '/automotives-electronics/cameras-videogames',
      name: 'Cameras & Video Games',
      component: Category,
      meta: { parent: 'Automotives & Electronics', path: '/automotives-electronics' }
    },
    {
      path: '/automotives-electronics/motos-carsupplies',
      name: 'Motos & Car Supplies',
      component: Category,
      meta: { parent: 'Automotives & Electronics', path: '/automotives-electronics' }
    },
    {
      path: '/clothing-shoes-accessories/women',
      name: 'Women\'s Clothing',
      component: Category,
      meta: { parent: 'Clothing, Shoes & Accessories', path: '/clothing-shoes-accessories' }
    },
    {
      path: '/clothing-shoes-accessories/men',
      name: 'Men\'s Clothing',
      component: Category,
      meta: { parent: 'Clothing, Shoes & Accessories', path: '/clothing-shoes-accessories' }
    },
    {
      path: '/clothing-shoes-accessories/children',
      name: 'Children\'s Clothing',
      component: Category,
      meta: { parent: 'Clothing, Shoes & Accessories', path: '/clothing-shoes-accessories' }
    },
    {
      path: '/clothing-shoes-accessories/shoes',
      name: 'Shoes',
      component: Category,
      meta: { parent: 'Clothing, Shoes & Accessories', path: '/clothing-shoes-accessories' }
    },
    {
      path: '/clothing-shoes-accessories/bags-accessories',
      name: 'Bags & Accessories',
      component: Category,
      meta: { parent: 'Clothing, Shoes & Accessories', path: '/clothing-shoes-accessories' }
    },
    {
      path: '/health-beauty/makeup',
      name: 'Makeup',
      component: Category,
      meta: { parent: 'Health & Beauty', path: '/health-beauty' }
    },
    {
      path: '/health-beauty/creams',
      name: 'Creams',
      component: Category,
      meta: { parent: 'Health & Beauty', path: '/health-beauty' }
    },
    {
      path: '/health-beauty/sports',
      name: 'Sports',
      component: Category,
      meta: { parent: 'Health & Beauty', path: '/health-beauty' }
    },
    {
      path: '/home-supplies/appliances',
      name: 'Appliances',
      component: Category,
      meta: { parent: 'Home Supplies', path: '/home-supplies' }
    },
    {
      path: '/home-supplies/furniture-accessories',
      name: 'Furniture & Accessories',
      component: Category,
      meta: { parent: 'Home Supplies', path: '/home-supplies' }
    },
    {
      path: '/home-supplies/gardensupplies',
      name: 'Garden Supplies',
      component: Category,
      meta: { parent: 'Home Supplies', path: '/home-supplies' }
    },
    {
      path: '/home-supplies/petsupplies',
      name: 'Pet Supplies',
      component: Category,
      meta: { parent: 'Home Supplies', path: '/home-supplies' }
    },
    {
      path: '/jewellery-watches/women',
      name: 'Women\'s Jewellery & Watches',
      component: Category,
      meta: { parent: 'Jewellery & Watches', path: '/jewellery-watches' }
    },
    {
      path: '/jewellery-watches/men',
      name: 'Men\'s Jewellery & Watches',
      component: Category,
      meta: { parent: 'Jewellery & Watches', path: '/jewellery-watches' }
    }
  ],
  scrollBehavior (to, from, savedPosition) {
    return { x: 0, y: 0 }
  }
})
