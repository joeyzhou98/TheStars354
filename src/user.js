import axios from 'axios'

export default {
  state: {
    token: localStorage.getItem('access_token') || null
  },
  getters: {
    loggedIn (state) {
      return state.token !== null
    }
  },
  mutations: {
    LOGIN (state, token) {
      state.token = token
    },
    LOGOUT (state) {
      state.token = null
    }
  },
  actions: {
    LOGIN (context, credentials) {
      return new Promise((resolve, reject) => {
        axios
          .post('api/authentication/login/', {
            username: credentials.username,
            password: credentials.password
          })
          .then(response => {
            const token = response.data.access_token
            localStorage.setItem('access_token', token)
            context.commit('LOGIN', token)
            resolve(response)
          })
          .catch(error => {
            reject(error)
          })
      })
    },
    LOGOUT (context) {
      if (context.getters.loggedIn) {
        return new Promise((resolve, reject) => {
          axios
            .post('api/authentication/logout/access')
            .then(response => {
              localStorage.removeItem('access_token')
              context.commit('LOGOUT')
              resolve(response)
            })
            .catch(error => {
              reject(error)
            })
        })
      }
    },
    REGISTER (context, data) {
      return new Promise((resolve, reject) => {
        axios
          .post('api/authentication/registration', {
            username: data.username,
            email: data.email,
            password: data.password
          })
          .then(response => {
            resolve(response)
          })
          .catch(error => {
            reject(error)
          })
      })
    }
  }
}
