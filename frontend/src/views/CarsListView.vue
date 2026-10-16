<template>
  <div class="p-4">
    <h2>Cars</h2>
    <button @click="fetchCars">Refresh</button>
    <table border="1" cellpadding="6" cellspacing="0">
      <thead>
        <tr>
          <th>ID</th>
          <th>VIN</th>
          <th>Make</th>
          <th>Model</th>
          <th>Year</th>
          <th>Mileage</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="car in cars" :key="car.id">
          <td>{{ car.id }}</td>
          <td>{{ car.vin }}</td>
          <td>{{ car.make }}</td>
          <td>{{ car.model }}</td>
          <td>{{ car.year }}</td>
          <td>{{ car.mileage }}</td>
          <td>{{ car.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import api from '@/api/axios'

export default defineComponent({
  name: 'CarsListView',
  setup() {
    const cars = ref([] as any[])

    async function fetchCars() {
      try {
        const res = await api.get('/cars')
        // backend returns { cars: [...] }
        cars.value = res.data.cars || []
      } catch (err) {
        console.error(err)
      }
    }

    fetchCars()

    return { cars, fetchCars }
  },
})
</script>
