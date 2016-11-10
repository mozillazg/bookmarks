import Vue from 'vue'
import Router from 'vue-router'
import Resource from 'vue-resource'

import App from './App.vue'
import Categories from './components/Categories.vue'
import Tags from './components/Tags.vue'
import Bookmarks from './components/Bookmarks.vue'

Vue.use(Router)
Vue.use(Resource)

const routes = [
  {path: '/bookmarks', name: 'bookmarks', component: Bookmarks},
  {path: '/tags', name: 'tags', component: Tags},
  {path: '/categories', name: 'categories', component: Categories},
  {path: '/', redirect: '/bookmarks'}
]

const router = new Router({
  linkActiveClass: 'is-active',
  routes: routes
})

/* eslint-disable no-new */
new Vue({
  router: router,
  el: '#app',
  render: h => h(App)
})
