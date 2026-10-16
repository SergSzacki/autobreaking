import { createRouter, createWebHistory } from 'vue-router'
import CarsListView from '@/views/CarsListView.vue'

const routes = [
  { path: '/', name: 'cars', component: CarsListView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
