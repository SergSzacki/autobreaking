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
            <button @click="toggleParts(car.id)">Parts</button>
          </td>
        </tr>

        <tr v-if="expandedCarId !== null" v-for="car in cars.filter(c => c.id === expandedCarId)" :key="'parts-' + car.id">
          <td colspan="8">
            <div style="background:#f7f7f7; padding:12px; border-radius:8px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <strong>Parts for {{ car.make }} {{ car.model }}</strong>
                <button @click="showPartForm(car.id)">Add part</button>
              </div>

              <div v-if="partFormCarId === car.id" style="margin-bottom:12px;">
                <PartForm :initial="editingPart" :car-id="car.id" @saved="handlePartSaved" @cancel="cancelPartForm" />
              </div>

              <table border="1" cellpadding="6" cellspacing="0" style="width:100%; background:white;">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Category</th>
                    <th>SKU</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Description</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-if="!partsByCar[car.id] || partsByCar[car.id].length === 0">
                    <td colspan="7">No parts yet.</td>
                  </tr>
                  <tr v-for="part in partsByCar[car.id] || []" :key="part.id">
                    <td>{{ part.name }}</td>
                    <td>{{ part.category || '-' }}</td>
                    <td>{{ part.sku || '-' }}</td>
                    <td>{{ part.quantity ?? 0 }}</td>
                    <td>{{ part.price ?? 0 }}</td>
                    <td>{{ part.description || '-' }}</td>
                    <td>
                      <button @click="editPart(car.id, part)">Edit</button>
                      <button @click="deletePartEntry(car.id, part.id)">Delete</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
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
import PartForm from '@/components/PartForm.vue'
import type { CarDraft, Car } from '@/types/car'
import type { Part, PartDraft } from '@/types/part'
import { listCars, createCar, updateCar, deleteCar } from '@/api/cars'
import { listPartsByCar, createPart, updatePart, deletePart } from '@/api/parts'

const cars = ref<any[]>([])
const loading = ref(false)
const showForm = ref(false)
const carFormRef = ref(null as any)
const editingData = ref<Partial<Car> | undefined>(undefined)

const expandedCarId = ref<number | null>(null)
const partsByCar = ref<Record<number, Part[]>>({})
const partFormCarId = ref<number | null>(null)
const editingPart = ref<Partial<Part> | undefined>(undefined)

async function fetchCars() {
  loading.value = true
  try {
    const data = await listCars()
    cars.value = data || []
    for (const car of cars.value) {
      if (car.id) {
        await fetchPartsForCar(car.id)
      }
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function fetchPartsForCar(carId: number) {
  try {
    const data = await listPartsByCar(carId)
    partsByCar.value[carId] = data || []
  } catch (err) {
    console.error(err)
  }
}

function openCreate() {
  editingData.value = undefined
  showForm.value = !showForm.value
  if (showForm.value && carFormRef.value && typeof carFormRef.value.reset === 'function') {
    carFormRef.value.reset()
  }
}

function toggleParts(carId: number) {
  expandedCarId.value = expandedCarId.value === carId ? null : carId
  if (expandedCarId.value !== null && !partsByCar.value[carId]) {
    fetchPartsForCar(carId)
  }
}

function showPartForm(carId: number) {
  editingPart.value = undefined
  partFormCarId.value = carId
}

function editPart(carId: number, part: Part) {
  editingPart.value = part
  partFormCarId.value = carId
}

function cancelPartForm() {
  editingPart.value = undefined
  partFormCarId.value = null
}

async function handlePartSaved(payload: { id?: number; data: PartDraft }) {
  try {
    if (!partFormCarId.value) return
    if (payload.id) {
      await updatePart(partFormCarId.value, payload.id, payload.data)
    } else {
      await createPart(partFormCarId.value, payload.data)
    }
    editingPart.value = undefined
    partFormCarId.value = null
    await fetchPartsForCar(partFormCarId.value)
  } catch (err) {
    console.error(err)
    alert('Save part failed')
  }
}

async function deletePartEntry(carId: number, partId?: number) {
  if (!partId) return
  if (!confirm('Delete this part?')) return
  try {
    await deletePart(carId, partId)
    await fetchPartsForCar(carId)
  } catch (err) {
    console.error(err)
    alert('Delete part failed')
  }
}

function startEdit(car: Car) {
  editingData.value = car
  showForm.value = true
}

async function onSaved(payload: { id?: number; data: CarDraft }) {
  try {
    if (payload.id) {
      await updateCar(payload.id, payload.data)
    } else {
      await createCar(payload.data)
    }
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
