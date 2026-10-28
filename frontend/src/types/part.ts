<template>
  <div class="details-shell">
    <div class="topbar">
      <button class="back-btn" @click="goBack">← Back</button>
    </div>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-else-if="car" class="card">
      <div class="headline">
        <div>
          <div class="eyebrow">Vehicle details</div>
          <h2>{{ car.make }} {{ car.model }}</h2>
        </div>
        <button class="primary" @click="goEdit">Edit car</button>
      </div>

      <div class="meta-grid">
        <div class="meta-item">
          <span>ID</span>
          <strong>#{{ car.id }}</strong>
        </div>
        <div class="meta-item">
          <span>Year</span>
          <strong>{{ car.year }}</strong>
        </div>
        <div class="meta-item">
          <span>Status</span>
          <strong>{{ car.status || 'available' }}</strong>
        </div>
        <div class="meta-item">
          <span>VIN</span>
          <strong>{{ car.vin || '-' }}</strong>
        </div>
        <div class="meta-item">
          <span>Mileage</span>
          <strong>{{ car.mileage ?? 0 }}</strong>
        </div>
        <div class="meta-item">
          <span>Color</span>
          <strong>{{ car.color || '-' }}</strong>
        </div>
      </div>

      <div class="parts-box">
        <div class="parts-header">
          <h3>Parts</h3>
          <button class="primary small" @click="showAddPart = !showAddPart">
            {{ showAddPart ? 'Hide form' : 'Add part' }}
          </button>
        </div>

        <div v-if="showAddPart" class="part-form-wrap">
          <PartForm :car-id="car.id" @saved="handlePartSaved" @cancel="hidePartForm" />
        </div>

        <div v-if="parts.length">
          <table class="parts-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Category</th>
                <th>SKU</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Notes</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="part in parts" :key="part.id">
                <td>{{ part.name }}</td>
                <td>{{ part.category || '-' }}</td>
                <td>{{ part.sku || '-' }}</td>
                <td>{{ part.quantity ?? 0 }}</td>
                <td>{{ part.price ?? 0 }}</td>
                <td>{{ part.notes ?? part.description ?? '-' }}</td>
                <td class="actions">
                  <button class="ghost small" @click="editPart(part)">Edit</button>
                  <button class="ghost small danger" @click="removePart(part.id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="empty-state">No parts added yet for this vehicle.</div>
      </div>
    </div>

    <div v-else class="not-found">Car not found.</div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
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
const showAddPart = ref(false)

const carId = computed(() => Number(route.params.id))

async function fetchCar() {
  loading.value = true
  try {
    car.value = await getCarById(carId.value)
    await fetchParts()
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function fetchParts() {
  try {
    const data = await listPartsByCar(carId.value)
    parts.value = data || []
  } catch (err) {
    console.error(err)
  }
}

async function handlePartSaved(payload: { id?: number; data: PartDraft }) {
  try {
    if (!car.value || !car.value.id) return

    if (payload.id) {
      await updatePart(car.value.id, payload.id, payload.data)
    } else {
      await createPart(car.value.id, payload.data)
    }

    showAddPart.value = false
    await fetchParts()
  } catch (err) {
    console.error(err)
    alert('Save part failed')
  }
}

function hidePartForm() {
  showAddPart.value = false
}

function editPart(part: Part) {
  showAddPart.value = true
  alert('Edit is available in the list panel currently.')
}

async function removePart(partId?: number) {
  if (!partId) return
  if (!confirm('Delete this part?')) return

  try {
    await deletePartApi(carId.value, partId)
    await fetchParts()
  } catch (err) {
    console.error(err)
    alert('Delete failed')
  }
}

function goBack() {
  router.push('/')
}

function goEdit() {
  if (!car.value) return
  router.push({ name: 'cars', query: { edit: String(car.value.id) } })
}

onMounted(() => {
  fetchCar()
})
</script>

<style scoped>
.details-shell {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px 16px 40px;
}

.topbar {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 16px;
}

.back-btn,
.primary,
.ghost {
  border: none;
  border-radius: 10px;
  padding: 9px 14px;
  font-weight: 600;
  cursor: pointer;
}

.back-btn {
  background: #eef2ff;
  color: #1f2a44;
}

.primary {
  background: #2563eb;
  color: white;
}

.ghost {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  color: #0f172a;
}

.small {
  padding: 7px 10px;
  font-size: 0.8rem;
}

.card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.05);
  padding: 20px;
}

.headline {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.eyebrow {
  text-transform: uppercase;
  font-size: 11px;
  letter-spacing: 0.12em;
  color: #64748b;
}

h2 {
  margin: 6px 0 0;
  font-size: 2rem;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(180px, 1fr));
  gap: 14px;
  margin-bottom: 24px;
}

.meta-item {
  background: #f8fafc;
  border: 1px solid #edf2f7;
  border-radius: 12px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.meta-item span {
  color: #64748b;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.parts-box {
  margin-top: 20px;
  background: #f8fafc;
  border: 1px solid #e7edf7;
  border-radius: 14px;
  padding: 14px;
}

.parts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.part-form-wrap {
  margin-bottom: 12px;
  background: white;
  border: 1px solid #edf2f7;
  border-radius: 12px;
  padding: 12px;
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
}

.parts-table th {
  background: #f3f6fb;
  color: #475569;
  font-size: 0.75rem;
  text-transform: uppercase;
}

.actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  padding: 18px 10px 10px;
  color: #64748b;
}

.not-found {
  padding: 30px 20px;
  color: #b91c1c;
  font-weight: 600;
}

.loading {
  padding: 24px 0;
  color: #475569;
}
</style>
