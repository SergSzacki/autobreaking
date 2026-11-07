<template>
  <div class="cars-shell">
    <div class="topbar">
      <div>
        <div class="eyebrow">Fleet overview</div>
        <h2>Cars</h2>
      </div>
      <button class="primary" @click="openCreateCarForm">{{ showCarForm ? 'Hide form' : 'Add car' }}</button>
    </div>

    <div v-if="showCarForm" class="panel form-panel">
      <CarForm :initial="editingCar" ref="carFormRef" @saved="handleCarSaved" @cancel="cancelCarForm" />
    </div>

    <div class="toolbar">
      <div class="filters">
        <input v-model="searchTerm" class="search-input" type="text" placeholder="Search by make, model or VIN" />
        <select v-model="statusFilter" class="filter-select">
          <option value="all">All statuses</option>
          <option value="available">available</option>
          <option value="maintenance">maintenance</option>
          <option value="sold">sold</option>
        </select>
        <select v-model="carsSort" class="filter-select">
          <option value="make">Sort by: name</option>
          <option value="year">Sort by: year</option>
          <option value="status">Sort by: status</option>
          <option value="id">Sort by: ID</option>
        </select>
      </div>
      <div class="toolbar-right">
        <button class="secondary" @click="fetchCars">Refresh</button>
        <span class="counter">{{ filteredCars.length }} cars</span>
      </div>
    </div>

    <div v-if="errorMessage" class="error-message" role="alert">{{ errorMessage }}</div>
    <div v-if="!loading && filteredCars.length === 0" class="empty-state">No cars found.</div>

    <div class="list-wrap">
      <div v-for="car in filteredCars" :key="car.id" class="car-card">
        <div class="car-header">
          <div>
            <div class="car-name">{{ car.make }} {{ car.model }}</div>
            <div class="meta">{{ car.year }} • <span :class="['status-badge', statusClass(car.status)]">{{ car.status || 'available' }}</span></div>
          </div>
          <div class="actions">
            <button class="ghost" @click="openCarDetails(car.id)">Details</button>
            <button class="ghost" @click="startEditCar(car)">Edit</button>
            <button class="ghost danger" @click="confirmDeleteCar(car.id)">Delete</button>
            <button class="ghost" @click="toggleParts(car.id)">{{ expandedCarId === car.id ? 'Hide parts' : `Parts (${(partsByCar[car.id] || []).length})` }}</button>
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
            <div class="parts-tools">
              <select v-model="partsSort" class="filter-select small-select">
                <option value="name">Sort by name</option>
                <option value="quantity">Sort by qty</option>
                <option value="price">Sort by price</option>
                <option value="category">Sort by category</option>
              </select>
              <button class="small primary" @click="showPartForm(car.id)">Add part</button>
            </div>
          </div>
          <div v-if="partFormCarId === car.id" class="part-form-wrap">
            <PartForm :key="`${car.id}-${editingPart?.id ?? 'new'}`" :initial="editingPart" :car-id="car.id" @saved="handlePartSaved" @cancel="cancelPartForm" />
          </div>
          <table v-if="(partsByCar[car.id] || []).length" class="parts-table">
            <thead><tr><th>Name</th><th>Category</th><th>SKU</th><th>Qty</th><th>Price</th><th>Notes</th><th>Actions</th></tr></thead>
            <tbody>
              <tr v-for="part in sortParts(partsByCar[car.id] || [], partsSort)" :key="part.id">
                <td>{{ part.name }}</td><td>{{ part.category || '-' }}</td><td>{{ part.sku || '-' }}</td>
                <td>{{ part.quantity ?? 0 }}</td><td>{{ part.price ?? 0 }}</td><td>{{ part.notes ?? part.description ?? '-' }}</td>
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
    <div v-if="loading" class="loading">Loading cars...</div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import CarForm from '@/components/CarForm.vue'
import PartForm from '@/components/PartForm.vue'
import type { Car, CarDraft } from '@/types/car'
import type { Part, PartDraft } from '@/types/part'
import { listCars, createCar, updateCar, deleteCar } from '@/api/cars'
import { listPartsByCar, createPart, updatePart, deletePart } from '@/api/parts'

const router = useRouter()
const cars = ref<Car[]>([])
const loading = ref(false)
const errorMessage = ref('')
const searchTerm = ref('')
const statusFilter = ref('all')
const carsSort = ref<'make' | 'year' | 'status' | 'id'>('make')
const partsSort = ref<'name' | 'quantity' | 'price' | 'category'>('name')
const showCarForm = ref(false)
const editingCar = ref<Partial<Car> | undefined>()
const carFormRef = ref<{ reset?: () => void } | null>(null)
const expandedCarId = ref<number | null>(null)
const partsByCar = ref<Record<number, Part[]>>({})
const partFormCarId = ref<number | null>(null)
const editingPart = ref<Partial<Part> | undefined>()

const filteredCars = computed(() => {
  const query = searchTerm.value.trim().toLowerCase()
  const result = cars.value.filter((car) => {
    if (statusFilter.value !== 'all' && (car.status || 'available') !== statusFilter.value) return false
    return !query || `${car.make} ${car.model} ${car.vin || ''}`.toLowerCase().includes(query)
  })
  return result.sort((a, b) => {
    if (carsSort.value === 'year') return Number(b.year) - Number(a.year)
    if (carsSort.value === 'status') return String(a.status || '').localeCompare(String(b.status || ''))
    if (carsSort.value === 'id') return Number(a.id) - Number(b.id)
    return `${a.make} ${a.model}`.localeCompare(`${b.make} ${b.model}`)
  })
})

function statusClass(status?: string | null) {
  if (status === 'maintenance') return 'status-maintenance'
  if (status === 'sold') return 'status-sold'
  return 'status-available'
}

function sortParts(items: Part[], key: 'name' | 'quantity' | 'price' | 'category') {
  return [...items].sort((a, b) => {
    if (key === 'quantity') return Number(b.quantity ?? 0) - Number(a.quantity ?? 0)
    if (key === 'price') return Number(b.price ?? 0) - Number(a.price ?? 0)
    if (key === 'category') return String(a.category || '').localeCompare(String(b.category || ''))
    return String(a.name || '').localeCompare(String(b.name || ''))
  })
}

async function fetchCars() {
  loading.value = true
  errorMessage.value = ''
  try {
    cars.value = await listCars()
    await Promise.all(cars.value.filter((car) => car.id).map((car) => fetchPartsForCar(car.id!)))
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Не удалось загрузить автомобили. Проверьте, что backend запущен.'
  } finally {
    loading.value = false
  }
}

async function fetchPartsForCar(carId: number) {
  try {
    partsByCar.value[carId] = await listPartsByCar(carId)
  } catch (error) {
    console.error(error)
    partsByCar.value[carId] = []
  }
}

function openCreateCarForm() {
  editingCar.value = undefined
  showCarForm.value = !showCarForm.value
  if (showCarForm.value) carFormRef.value?.reset?.()
}
function startEditCar(car: Car) { editingCar.value = car; showCarForm.value = true }
function cancelCarForm() { showCarForm.value = false; editingCar.value = undefined }

async function handleCarSaved(payload: { id?: number; data: CarDraft }) {
  try {
    if (payload.id) await updateCar(payload.id, payload.data)
    else await createCar(payload.data)
    showCarForm.value = false
    editingCar.value = undefined
    await fetchCars()
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Не удалось сохранить автомобиль. Проверьте подключение к API.'
  }
}

async function confirmDeleteCar(id?: number) {
  if (!id || !window.confirm(`Delete car #${id}?`)) return
  try { await deleteCar(id); await fetchCars() }
  catch (error) { console.error(error); errorMessage.value = 'Не удалось удалить автомобиль.' }
}

async function toggleParts(carId?: number) {
  if (!carId) return
  if (expandedCarId.value === carId) { expandedCarId.value = null; return }
  expandedCarId.value = carId
  if (!partsByCar.value[carId]) await fetchPartsForCar(carId)
}
function showPartForm(carId?: number) { if (!carId) return; partFormCarId.value = carId; editingPart.value = undefined }
function editPart(carId: number | undefined, part: Part) { if (!carId) return; partFormCarId.value = carId; editingPart.value = part }
function cancelPartForm() { partFormCarId.value = null; editingPart.value = undefined }

async function handlePartSaved(payload: { id?: number; data: PartDraft }) {
  const carId = partFormCarId.value
  if (!carId) return
  try {
    if (payload.id) await updatePart(carId, payload.id, payload.data)
    else await createPart(carId, payload.data)
    cancelPartForm()
    await fetchPartsForCar(carId)
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Не удалось сохранить запчасть. Проверьте, что API запущен и данные соответствуют модели.'
  }
}

async function deletePartEntry(carId: number | undefined, partId?: number) {
  if (!carId || !partId || !window.confirm('Delete this part?')) return
  try { await deletePart(carId, partId); await fetchPartsForCar(carId) }
  catch (error) { console.error(error); errorMessage.value = 'Не удалось удалить запчасть.' }
}
function openCarDetails(carId?: number) { if (carId) router.push(`/cars/${carId}`) }

onMounted(fetchCars)
</script>

<style scoped>
.cars-shell { max-width: 1200px; margin: 0 auto; padding: 24px 16px 40px; font-family: Inter, Arial, sans-serif; }
.topbar,.toolbar,.car-header,.parts-header,.parts-tools { display:flex; align-items:center; justify-content:space-between; gap:12px; }
.topbar { margin-bottom:20px; }
.eyebrow { font-size:11px; letter-spacing:.12em; text-transform:uppercase; color:#7c8aa5; }
h2 { margin:4px 0 0; font-size:2rem; }
.panel,.car-card { background:#fff; border:1px solid #e7edf7; border-radius:16px; box-shadow:0 12px 30px rgba(15,23,42,.04); }
.form-panel { padding:18px; margin-bottom:18px; }
.toolbar { margin:18px 0; flex-wrap:wrap; }
.filters { display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
.search-input,.filter-select { border:1px solid #dfe7f3; border-radius:10px; padding:10px 12px; min-height:42px; background:#fff; color:#1f2937; }
.search-input { min-width:280px; }
.small-select { min-width:170px; min-height:36px; padding:6px 10px; }
.toolbar-right { display:flex; align-items:center; gap:12px; }
.counter { color:#53627b; font-size:.9rem; }
.list-wrap { display:grid; grid-template-columns:1fr; gap:18px; }
.car-card { padding:18px; }
.car-name { font-size:1.2rem; font-weight:700; color:#111827; }
.meta { margin-top:6px; display:flex; align-items:center; gap:8px; color:#64748b; font-size:.85rem; }
.status-badge { display:inline-block; padding:4px 8px; border-radius:999px; font-size:.72rem; font-weight:700; }
.status-available { background:#e0f2fe; color:#075985; }
.status-maintenance { background:#fef3c7; color:#92400e; }
.status-sold { background:#fee2e2; color:#991b1b; }
.actions { display:flex; flex-wrap:wrap; gap:8px; }
button { border:1px solid transparent; border-radius:10px; padding:8px 12px; background:#edf3ff; color:#1e293b; cursor:pointer; font-weight:600; }
button:hover { transform:translateY(-1px); }
button.primary { background:#2563eb; color:#fff; }
button.secondary { background:#f1f5f9; color:#0f172a; }
button.ghost { background:#f8fafc; border-color:#d8e1ef; }
button.danger { background:#fff1f2; color:#be123c; border-color:#fecdd3; }
button.small { padding:6px 10px; font-size:.8rem; }
.car-grid { margin-top:18px; display:grid; grid-template-columns:repeat(4,minmax(120px,1fr)); gap:12px; }
.car-grid div { background:#f8fafc; border:1px solid #edf2f7; border-radius:12px; padding:10px 12px; display:flex; flex-direction:column; gap:6px; }
.car-grid span { color:#72819a; font-size:.7rem; text-transform:uppercase; letter-spacing:.08em; }
.car-grid strong { color:#0f172a; font-size:.96rem; }
.parts-panel { margin-top:18px; background:#f8fafc; border:1px solid #e8eef8; border-radius:14px; padding:14px; }
.parts-header { margin-bottom:12px; }
.part-form-wrap { background:#fff; border:1px solid #edf2f7; border-radius:12px; padding:12px; margin-bottom:12px; }
.parts-table { width:100%; border-collapse:collapse; background:#fff; }
.parts-table th,.parts-table td { border:1px solid #edf2f7; padding:10px 12px; text-align:left; vertical-align:top; }
.parts-table th { background:#f3f6fb; color:#475569; font-size:.75rem; text-transform:uppercase; }
.cell-actions { display:flex; gap:8px; }
.empty-state,.loading,.error-message { padding:16px 10px; color:#64748b; }
.error-message { margin:12px 0; color:#991b1b; background:#fff1f2; border-radius:10px; }
@media(max-width:768px) { .car-grid { grid-template-columns:repeat(2,minmax(120px,1fr)); } .topbar,.toolbar,.car-header,.parts-header,.parts-tools { flex-direction:column; align-items:flex-start; } .search-input { min-width:100%; } }
</style>
