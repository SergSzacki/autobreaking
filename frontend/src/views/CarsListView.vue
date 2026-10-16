<template>
  <div class="p-4">
    <h2>Cars</h2>

    <div style="margin-bottom: 12px;">
      <button @click="showForm = !showForm">{{ showForm ? 'Hide' : 'Add car' }}</button>
    </div>

    <div v-if="showForm" style="margin-bottom: 16px;">
      <CarForm ref="carFormRef" @saved="onSaved" />
    </div>

    <button @click="fetchCars">Refresh</button>

    <table border="1" cellpadding="6" cellspacing="0" style="margin-top:12px; width:100%;">
      <thead>
        <tr>
          <th>ID</th>
          <th>VIN</th>
          <th>Make</th>
          <th>Model</th>
          <th>Year</th>
          <th>Mileage</th>
          <th>Status</th>
          <th>Actions</th>
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
          <td>
            <button @click="confirmDelete(car.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="loading" style="margin-top:8px;">Loading...</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CarForm from '@/components/CarForm.vue'
import type { CarDraft } from '@/types/car'
import { listCars, createCar, deleteCar } from '@/api/cars'

const cars = ref<any[]>([])
const loading = ref(false)
const showForm = ref(false)
const carFormRef = ref(null as any)

async function fetchCars() {
  loading.value = true
  try {
    const data = await listCars()
    cars.value = data || []
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function onSaved(payload: CarDraft) {
  try {
    await createCar(payload)
    // reset form
    if (carFormRef.value && typeof carFormRef.value.reset === 'function') {
      carFormRef.value.reset()
    }
    showForm.value = false
    await fetchCars()
  } catch (err) {
    console.error(err)
  }
}

async function confirmDelete(id: number) {
  if (!confirm('Delete car #' + id + '?')) return
  try {
    await deleteCar(id)
    await fetchCars()
  } catch (err) {
    console.error(err)
    alert('Delete failed')
  }
}

fetchCars()
</script>
