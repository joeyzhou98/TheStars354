import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import FAQ from './views/FAQ.vue'
import About from './views/About.vue'
import Account from './views/Account.vue'
import Category from './views/Category.vue'

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
    }
  ]
})
