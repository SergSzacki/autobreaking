<template>
  <div class="details-shell">
    <div class="topbar"><button class="back-btn" @click="goBack">← Back</button></div>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="car" class="card">
      <div class="headline">
        <div><div class="eyebrow">Vehicle details</div><h2>{{ car.make }} {{ car.model }}</h2></div>
        <button class="primary" @click="goEdit">Edit car</button>
      </div>
      <div class="meta-grid">
        <div class="meta-item"><span>ID</span><strong>#{{ car.id }}</strong></div>
        <div class="meta-item"><span>Year</span><strong>{{ car.year }}</strong></div>
        <div class="meta-item"><span>Status</span><strong>{{ car.status || 'available' }}</strong></div>
        <div class="meta-item"><span>VIN</span><strong>{{ car.vin || '-' }}</strong></div>
        <div class="meta-item"><span>Mileage</span><strong>{{ car.mileage ?? 0 }}</strong></div>
        <div class="meta-item"><span>Color</span><strong>{{ car.color || '-' }}</strong></div>
      </div>
      <div class="parts-box">
        <div class="parts-header"><h3>Parts</h3><button class="primary small" @click="openCreateForm">{{ showPartForm ? 'Hide form' : 'Add part' }}</button></div>
        <div v-if="showPartForm" class="part-form-wrap">
          <PartForm :key="editingPart?.id ?? 'new'" :initial="editingPart" :car-id="car.id" @saved="handlePartSaved" @cancel="cancelPartForm" />
        </div>
        <table v-if="parts.length" class="parts-table">
          <thead><tr><th>Name</th><th>Category</th><th>SKU</th><th>Qty</th><th>Price</th><th>Notes</th><th>Actions</th></tr></thead>
          <tbody>
            <tr v-for="part in parts" :key="part.id">
              <td>{{ part.name }}</td><td>{{ part.category || '-' }}</td><td>{{ part.sku || '-' }}</td>
              <td>{{ part.quantity ?? 0 }}</td><td>{{ part.price ?? 0 }}</td><td>{{ part.notes ?? part.description ?? '-' }}</td>
              <td class="actions"><button class="ghost small" @click="editPart(part)">Edit</button><button class="ghost small danger" @click="removePart(part.id)">Delete</button></td>
            </tr>
          </tbody>
        </table>
        <div v-else-if="!showPartForm" class="empty-state">No parts added yet for this vehicle.</div>
      </div>
    </div>
    <div v-else class="not-found">Car not found.</div>
    <div v-if="errorMessage" class="error-message" role="alert">{{ errorMessage }}</div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PartForm from '@/components/PartForm.vue'
import { getCarById } from '@/api/cars'
import { listPartsByCar, createPart, updatePart, deletePart as deletePartApi } from '@/api/parts'
import type { Car } from '@/types/car'
import type { Part, PartDraft } from '@/types/part'

const route = useRoute()
const router = useRouter()
const car = ref<Car | null>(null)
const parts = ref<Part[]>([])
const loading = ref(true)
const showPartForm = ref(false)
const editingPart = ref<Partial<Part> | undefined>()
const errorMessage = ref('')
const carId = computed(() => Number(route.params.id))

async function fetchCar() {
  loading.value = true
  errorMessage.value = ''
  try {
    car.value = await getCarById(carId.value)
    await fetchParts()
  } catch (error) {
    console.error(error)
    car.value = null
    errorMessage.value = 'Не удалось загрузить автомобиль. Проверьте подключение к API.'
  } finally { loading.value = false }
}
async function fetchParts() {
  try { parts.value = await listPartsByCar(carId.value) }
  catch (error) { console.error(error); errorMessage.value = 'Не удалось загрузить запчасти.' }
}
function openCreateForm() { editingPart.value = undefined; showPartForm.value = !showPartForm.value }
function editPart(part: Part) { editingPart.value = part; showPartForm.value = true }
function cancelPartForm() { showPartForm.value = false; editingPart.value = undefined }
async function handlePartSaved(payload: { id?: number; data: PartDraft }) {
  try {
    if (payload.id) await updatePart(carId.value, payload.id, payload.data)
    else await createPart(carId.value, payload.data)
    cancelPartForm()
    await fetchParts()
  } catch (error) { console.error(error); errorMessage.value = 'Не удалось сохранить запчасть. Проверьте backend и его логи.' }
}
async function removePart(partId?: number) {
  if (!partId || !window.confirm('Delete this part?')) return
  try { await deletePartApi(carId.value, partId); await fetchParts() }
  catch (error) { console.error(error); errorMessage.value = 'Не удалось удалить запчасть.' }
}
function goBack() { router.push('/') }
function goEdit() { if (car.value?.id) router.push({ name: 'cars', query: { edit: String(car.value.id) } }) }
onMounted(fetchCar)
watch(carId, fetchCar)
</script>

<style scoped>
.details-shell { max-width:1100px; margin:0 auto; padding:24px 16px 40px; }
.topbar { display:flex; justify-content:flex-start; margin-bottom:16px; }
.back-btn,.primary,.ghost { border:0; border-radius:10px; padding:9px 14px; font-weight:600; cursor:pointer; }
.back-btn { background:#eef2ff; color:#1f2a44; }
.primary { background:#2563eb; color:#fff; }
.ghost { background:#f8fafc; border:1px solid #e5e7eb; color:#0f172a; }
.small { padding:7px 10px; font-size:.8rem; }
.card { background:#fff; border:1px solid #e5e7eb; border-radius:18px; box-shadow:0 10px 24px rgba(15,23,42,.05); padding:20px; }
.headline,.parts-header { display:flex; justify-content:space-between; align-items:center; gap:12px; margin-bottom:20px; }
.eyebrow { text-transform:uppercase; font-size:11px; letter-spacing:.12em; color:#64748b; }
h2 { margin:6px 0 0; font-size:2rem; }
.meta-grid { display:grid; grid-template-columns:repeat(3,minmax(180px,1fr)); gap:14px; margin-bottom:24px; }
.meta-item { background:#f8fafc; border:1px solid #edf2f7; border-radius:12px; padding:12px; display:flex; flex-direction:column; gap:6px; }
.meta-item span { color:#64748b; font-size:.7rem; text-transform:uppercase; letter-spacing:.08em; }
.parts-box { margin-top:20px; background:#f8fafc; border:1px solid #e7edf7; border-radius:14px; padding:14px; }
.part-form-wrap { margin-bottom:12px; background:#fff; border:1px solid #edf2f7; border-radius:12px; padding:12px; }
.parts-table { width:100%; border-collapse:collapse; background:#fff; }
.parts-table th,.parts-table td { border:1px solid #edf2f7; padding:10px 12px; text-align:left; }
.parts-table th { background:#f3f6fb; color:#475569; font-size:.75rem; text-transform:uppercase; }
.actions { display:flex; gap:8px; }
.empty-state,.loading,.error-message { padding:18px 10px; color:#64748b; }
.error-message { color:#991b1b; background:#fff1f2; border-radius:10px; }
.not-found { padding:30px 20px; color:#b91c1c; font-weight:600; }
@media(max-width:700px) { .meta-grid { grid-template-columns:repeat(2,minmax(130px,1fr)); } .headline,.parts-header { align-items:flex-start; flex-direction:column; } }
</style>
