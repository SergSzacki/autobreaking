<template>
  <div class="p-4">
    <h2>Cars</h2>

    <div style="margin-bottom: 12px;">
      <button @click="openCreate">{{ showForm ? 'Hide' : 'Add car' }}</button>
    </div>

    <div v-if="showForm" style="margin-bottom: 16px;">
      <CarForm :initial="editingData" ref="carFormRef" @saved="onSaved" @cancel="onCancel" />
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
            <button @click="startEdit(car)">Edit</button>
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
import type { CarDraft, Car } from '@/types/car'
import { listCars, createCar, updateCar, deleteCar } from '@/api/cars'

const cars = ref<any[]>([])
const loading = ref(false)
const showForm = ref(false)
const carFormRef = ref(null as any)
const editingData = ref<Partial<Car> | undefined>(undefined)

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

function openCreate() {
  editingData.value = undefined
  showForm.value = !showForm.value
  // reset form if hiding and showing again
  if (showForm.value && carFormRef.value && typeof carFormRef.value.reset === 'function') {
    carFormRef.value.reset()
  }
}

function startEdit(car: Car) {
  editingData.value = car
  showForm.value = true
  // CarForm watches initial prop and will fill fields
}

async function onSaved(payload: { id?: number; data: CarDraft }) {
  try {
    if (payload.id) {
      await updateCar(payload.id, payload.data)
    } else {
      await createCar(payload.data)
    }
    // reset form
    if (carFormRef.value && typeof carFormRef.value.reset === 'function') {
      carFormRef.value.reset()
    }
    showForm.value = false
    editingData.value = undefined
    await fetchCars()
  } catch (err) {
    console.error(err)
  }
}

function onCancel() {
  showForm.value = false
  editingData.value = undefined
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
