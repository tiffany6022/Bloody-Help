import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import './registerServiceWorker'
// import router from './router'
import store from './store'
import VeLine from 'v-charts/lib/line.common'

Vue.config.productionTip = false
Vue.use(VueRouter)
Vue.component(VeLine.name, VeLine)

const router = new VueRouter({ routes: [
  { component: App, path: '/:page' },
  //{ component: App, path: '/:page/:id' },
]})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
