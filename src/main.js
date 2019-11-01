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

/* let isRefreshing = false
let subscribers = []
axios.interceptors.response.use(
  response => {
    return response
  },
  err => {
    const {
      config,
      response: { status, data }
    } = err
    const originalRequest = config
    if (data.message === 'Missing token') {
      router.push('/login-register')
      return Promise.reject(false)
    }
    if (originalRequest.url.includes('api/authentication/login/')) {
      return Promise.reject(err)
    }
    if (status === 401 && data.message === 'Expired token') {
      if (!isRefreshing) {
        isRefreshing = true
        store
          .dispatch('REFRESH_TOKEN')
          .then(({ status }) => {
            if (status === 200 || status === 204) {
              isRefreshing = false
            }
            subscribers = []
          })
          .catch(error => {
            console.error(error)
          })
      }
      const requestSubscribers = new Promise(resolve => {
        subscribeTokenRefresh(() => {
          resolve(axios(originalRequest))
        })
      })
      onRefreshed()
      return requestSubscribers
    }
  }
)
function subscribeTokenRefresh (cb) {
  subscribers.push(cb)
}
function onRefreshed () {
  subscribers.map(cb => cb())
}
subscribers = [] */

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
