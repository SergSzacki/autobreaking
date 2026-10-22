<template>
  <div class="cars-shell">
    <div class="topbar">
      <div>
        <div class="eyebrow">Fleet overview</div>
        <h2>Cars</h2>
      </div>

      <button class="primary" @click="openCreateCarForm">
        {{ showCarForm ? 'Hide form' : 'Add car' }}
      </button>
    </div>

    <div v-if="showCarForm" class="panel form-panel">
      <CarForm :initial="editingCar" ref="carFormRef" @saved="handleCarSaved" @cancel="cancelCarForm" />
    </div>

    <div class="toolbar">
      <button class="secondary" @click="fetchCars">Refresh</button>
      <span class="counter">{{ cars.length }} cars</span>
    </div>

    <div class="list-wrap">
      <div v-for="car in cars" :key="car.id" class="car-card">
        <div class="car-header">
          <div>
            <div class="car-name">{{ car.make }} {{ car.model }}</div>
            <div class="meta">{{ car.year }} • {{ car.status || 'available' }}</div>
          </div>

          <div class="actions">
            <button class="ghost" @click="startEditCar(car)">Edit</button>
            <button class="ghost danger" @click="confirmDeleteCar(car.id)">Delete</button>
            <button class="ghost" @click="toggleParts(car.id)">
              {{ expandedCarId === car.id ? 'Hide parts' : `Parts (${(partsByCar[car.id] || []).length})` }}
            </button>
          </div>
        </div>

        <div class="car-grid">
          <div><span>ID</span><strong>#{{ car.id }}</strong></div>
          <div><span>VIN</span><strong>{{ car.vin || '-' }}</strong></div>
          <div><span>Mileage</span><strong>{{ car.mileage ?? 0 }}</strong></div>
          <div><span>Color</span><strong>{{ car.color || '-' }}</strong></div>
        </div>

        <div v-if="expandedCarId === car.id" class="parts-panel">
          <div class="parts-header">
            <strong>Parts for {{ car.make }} {{ car.model }}</strong>
            <button class="small primary" @click="showPartForm(car.id)">Add part</button>
          </div>

          <div v-if="partFormCarId === car.id" class="part-form-wrap">
            <PartForm :initial="editingPart" :car-id="car.id" @saved="handlePartSaved" @cancel="cancelPartForm" />
          </div>

          <table class="parts-table" v-if="(partsByCar[car.id] || []).length">
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
              <tr v-for="part in partsByCar[car.id] || []" :key="part.id">
                <td>{{ part.name }}</td>
                <td>{{ part.category || '-' }}</td>
                <td>{{ part.sku || '-' }}</td>
                <td>{{ part.quantity ?? 0 }}</td>
                <td>{{ part.price ?? 0 }}</td>
                <td>{{ part.description || '-' }}</td>
                <td class="cell-actions">
                  <button class="small ghost" @click="editPart(car.id, part)">Edit</button>
                  <button class="small ghost danger" @click="deletePartEntry(car.id, part.id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>

          <div v-else class="empty-state">No parts added for this car yet.</div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
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

const showCarForm = ref(false)
const editingCar = ref<Partial<Car> | undefined>(undefined)
const carFormRef = ref(null as any)

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

function openCreateCarForm() {
  editingCar.value = undefined
  showCarForm.value = !showCarForm.value

  if (showCarForm.value && carFormRef.value && typeof carFormRef.value.reset === 'function') {
    carFormRef.value.reset()
  }
}

function startEditCar(car: Car) {
  editingCar.value = car
  showCarForm.value = true
}

function cancelCarForm() {
  showCarForm.value = false
  editingCar.value = undefined
}

async function handleCarSaved(payload: { id?: number; data: CarDraft }) {
  try {
    if (payload.id) {
      await updateCar(payload.id, payload.data)
    } else {
      await createCar(payload.data)
    }

    if (carFormRef.value && typeof carFormRef.value.reset === 'function') {
      carFormRef.value.reset()
    }

    showCarForm.value = false
    editingCar.value = undefined
    await fetchCars()
  } catch (err) {
    console.error(err)
  }
}

async function confirmDeleteCar(id: number) {
  if (!confirm('Delete car #' + id + '?')) return

  try {
    await deleteCar(id)
    await fetchCars()
  } catch (err) {
    console.error(err)
    alert('Delete failed')
  }
}

function toggleParts(carId: number) {
  if (expandedCarId.value === carId) {
    expandedCarId.value = null
    return
  }

  expandedCarId.value = carId

  if (!partsByCar.value[carId]) {
    fetchPartsForCar(carId)
  }
}

function showPartForm(carId: number) {
  partFormCarId.value = carId
  editingPart.value = undefined
}

function editPart(carId: number, part: Part) {
  partFormCarId.value = carId
  editingPart.value = part
}

function cancelPartForm() {
  partFormCarId.value = null
  editingPart.value = undefined
}

async function handlePartSaved(payload: { id?: number; data: PartDraft }) {
  try {
    const carId = partFormCarId.value
    if (!carId) return

    if (payload.id) {
      await updatePart(carId, payload.id, payload.data)
    } else {
      await createPart(carId, payload.data)
    }

    const currentCarId = carId
    partFormCarId.value = null
    editingPart.value = undefined

    await fetchPartsForCar(currentCarId)
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

fetchCars()
</script>

<style scoped>
.cars-shell {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px 40px;
  font-family: Inter, Arial, sans-serif;
}

.topbar,
.toolbar,
.car-header,
.parts-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.topbar {
  margin-bottom: 20px;
}

.eyebrow {
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #7c8aa5;
}

h2 {
  margin: 4px 0 0;
  font-size: 2rem;
}

.panel,
.car-card {
  background: #ffffff;
  border: 1px solid #e7edf7;
  border-radius: 16px;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.04);
}

.form-panel {
  padding: 18px;
  margin-bottom: 18px;
}

.toolbar {
  margin: 18px 0;
}

.counter {
  color: #53627b;
  font-size: 0.9rem;
}

.list-wrap {
  display: grid;
  grid-template-columns: 1fr;
  gap: 18px;
}

.car-card {
  padding: 18px;
}

.car-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
}

.meta {
  margin-top: 4px;
  color: #64748b;
  font-size: 0.8rem;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

button {
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 8px 12px;
  background: #edf3ff;
  color: #1e293b;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s ease;
}

button:hover {
  transform: translateY(-1px);
}

button.primary {
  background: #2563eb;
  color: white;
}

button.secondary {
  background: #f1f5f9;
  color: #0f172a;
}

button.ghost {
  background: #f8fafc;
  border-color: #d8e1ef;
}

button.danger {
  background: #fff1f2;
  color: #be123c;
  border-color: #fecdd3;
}

button.small {
  padding: 6px 10px;
  font-size: 0.8rem;
}

.car-grid {
  margin-top: 18px;
  display: grid;
  grid-template-columns: repeat(4, minmax(120px, 1fr));
  gap: 12px;
}

.car-grid div {
  background: #f8fafc;
  border: 1px solid #edf2f7;
  border-radius: 12px;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.car-grid span {
  color: #72819a;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.car-grid strong {
  color: #0f172a;
  font-size: 0.96rem;
}

.parts-panel {
  margin-top: 18px;
  background: #f8fafc;
  border: 1px solid #e8eef8;
  border-radius: 14px;
  padding: 14px;
}

.parts-header {
  margin-bottom: 12px;
}

.part-form-wrap {
  background: white;
  border: 1px solid #edf2f7;
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 12px;
}

.parts-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.parts-table th,
.parts-table td {
  border: 1px solid #edf2f7;
  padding: 10px 12px;
  text-align: left;
  vertical-align: top;
}

.parts-table th {
  background: #f3f6fb;
  color: #475569;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.cell-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  padding: 18px 10px 8px;
  color: #64748b;
}

.loading {
  margin-top: 18px;
  color: #475569;
}
</style>
