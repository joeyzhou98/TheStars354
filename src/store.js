import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isLoggedIn: false,
    uid: null,
    username: null,
    email: null
  },
  mutations: {
    login (state, data) {
      state.isLoggedIn = true
      state.uid = data.id
      state.username = data.username
      state.email = data.email
    },
    logout (state) {
      state.isLoggedIn = false
      state.uid = null
      state.username = null
      state.email = null
    }
  },
  actions: {

  }
})
