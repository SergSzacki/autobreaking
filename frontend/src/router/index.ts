import { createRouter, createWebHistory } from 'vue-router'
import CarsListView from '@/views/CarsListView.vue'
import CarDetailsView from '@/views/CarDetailsView.vue'
import InventoryView from '@/views/InventoryView.vue'

const routes = [
  { path: '/', name: 'cars', component: CarsListView },
  { path: '/cars/:id', name: 'car-details', component: CarDetailsView, props: true },
  { path: '/inventory', name: 'inventory', component: InventoryView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
