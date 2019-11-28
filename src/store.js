import axios from 'axios'
import Vue from 'vue'
import Vuex from 'vuex'
// import User from './user'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    // user: User
  },
  state: {
    // User login
    isLoggedIn: false,
    uid: null,
    username: null,
    email: null,
    role: null,

    // Cookie related (recommendations)
    cookieItems: [],
    similarItems: [],
    subcategories: []
  },
  mutations: {
    login (state, data) {
      state.isLoggedIn = true
      state.uid = data.id
      state.username = data.username
      state.email = data.email
      state.role = data.role
    },
    logout (state) {
      state.isLoggedIn = false
      state.uid = null
      state.username = null
      state.email = null
      state.role = null
    }
  },
  actions: {
    transferCartToUser ({state}) {
      if (localStorage.cart) {
        let jsonCartCookie = localStorage.cart
        let itemData = JSON.parse(jsonCartCookie)
        localStorage.removeItem('cart')

        let requests = []
        for (var data of itemData) {
          let url = 'api/resource/shopping-cart/' + state.uid + '/' + data.item.item_id + '?newQuantity=' + data.qty
          requests.push(axios.post(url))
        }
        axios.all(requests)
          .catch(error => { alert(error) })
      }
    },
    updateCookieItems ({state}) {
      if (localStorage.history) {
        let jsonViewedItemsCookie = localStorage.history
        let items = JSON.parse(jsonViewedItemsCookie)
        state.cookieItems = items.filter(item => item !== null)
      }
    },
    updateSimilarItems ({state}) {
      let paths = []
      if (state.cookieItems.length === 0) {
        paths.push('api/resource/item/deals') // if no cookie on client side, show deals until they visit items
      } else {
        var newCategory = getLastSubcategories(state.cookieItems, state.subcategories)
        if (newCategory === false) {
          return
        }
        for (var subcat of state.subcategories) {
          paths.push('api/resource/subcategory?subcategory=' + encodeURIComponent(subcat))
        }
      }
      var requests = []
      for (var path of paths) {
        requests.push(axios.get(path))
      }
      axios.all(requests)
        .then(axios.spread((...responses) => {
          state.similarItems = []
          for (var response of responses) {
            state.similarItems.push(...response.data)
          }
        }))
        .catch(error => { alert(error) })
    }
  }
})

// ------------------------
// Helper functions
// ------------------------

function getLastSubcategories (cookieItems, subcategories) {
  const maxSize = 3
  for (var item of cookieItems) {
    if (item !== null && subcategories.includes(item.subcategory) === false) {
      if (subcategories.length === maxSize) {
        subcategories.pop()
      }
      subcategories.unshift(item.subcategory)
      return true
    }
  }
  return false
}
