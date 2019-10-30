import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './filters'

import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'vue-awesome/icons'
import Icon from 'vue-awesome/components/Icon'
import lineClamp from 'vue-line-clamp'

Vue.config.productionTip = false
Vue.use(BootstrapVue)
Vue.use(lineClamp)
Vue.component('icon', Icon)

export const bus = new Vue()

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
