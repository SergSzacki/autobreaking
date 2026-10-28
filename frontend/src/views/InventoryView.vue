<template>
  <div class="inventory-shell">
    <div class="topbar">
      <div>
        <div class="eyebrow">Warehouse</div>
        <h2>Inventory</h2>
      </div>

      <button class="primary" @click="addItem">Add stock item</button>
    </div>

    <div v-if="showForm" class="panel form-panel">
      <div class="form-header">
        <h3>{{ editingItem ? 'Edit stock item' : 'Add stock item' }}</h3>
      </div>

      <div class="form-field select-field">
        <label for="stock-car-select">Car</label>
        <select id="stock-car-select" v-model="selectedCarId" class="filter-select">
          <option :value="null" disabled>Select a car</option>
          <option v-for="car in carOptions" :key="car.id" :value="car.id">
            {{ car.make }} {{ car.model }} ({{ car.year }})
          </option>
        </select>
      </div>

      <PartForm
        :key="formKey"
        :initial="editingItem"
        :car-id="selectedCarId"
        @saved="handleSaved"
        @cancel="cancelForm"
      />
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <span>Total</span>
        <strong>{{ inventory.length }}</strong>
      </div>
      <div class="stat-card success">
        <span>In stock</span>
        <strong>{{ countByStatus('in_stock') }}</strong>
      </div>
      <div class="stat-card warning">
        <span>Low stock</span>
        <strong>{{ countByStatus('low_stock') }}</strong>
      </div>
      <div class="stat-card danger">
        <span>Out of stock</span>
        <strong>{{ countByStatus('out_of_stock') }}</strong>
      </div>
    </div>

    <div class="toolbar">
      <input
        v-model="search"
        class="search-input"
        type="text"
        placeholder="Search by name, SKU, make or model"
      />

      <select v-model="statusFilter" class="filter-select">
        <option value="all">All statuses</option>
        <option value="in_stock">In stock</option>
        <option value="low_stock">Low stock</option>
        <option value="out_of_stock">Out of stock</option>
      </select>

      <select v-model="inventorySort" class="filter-select">
        <option value="name">Sort by name</option>
        <option value="quantity">Sort by quantity</option>
        <option value="min_quantity">Sort by min qty</option>
        <option value="price">Sort by price</option>
        <option value="category">Sort by category</option>
        <option value="status">Sort by status</option>
      </select>
    </div>

    <div class="table-wrap">
      <table class="inventory-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>SKU</th>
            <th>Category</th>
            <th>Qty</th>
            <th>Min</th>
            <th>Status</th>
            <th>Price</th>
            <th>Supplier</th>
            <th>Location</th>
            <th>Car</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="item in filteredInventory" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.sku || '-' }}</td>
            <td>{{ item.category || '-' }}</td>
            <td>{{ item.quantity ?? 0 }}</td>
            <td>{{ item.min_quantity ?? 0 }}</td>
            <td>
              <span :class="['badge', badgeClass(item)]">
                {{ statusLabel(item) }}
              </span>
            </td>
            <td>{{ formatPrice(item.price) }}</td>
            <td>{{ item.supplier || '-' }}</td>
            <td>{{ item.location || '-' }}</td>
            <td>{{ item.make && item.model ? `${item.make} ${item.model}` : item.car_id ? `#${item.car_id}` : '-' }}</td>
            <td class="actions">
              <button class="ghost small" @click="editItem(item)">Edit</button>
              <button class="ghost small danger" @click="deleteItem(item)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { getStockLabel, getStockStatus, type InventoryItem } from '@/utils/stock'
import { listInventory, createPart, updatePart, deletePart } from '@/api/parts'
import { listCars } from '@/api/cars'
import PartForm from '@/components/PartForm.vue'
import type { Car } from '@/types/car'
import type { Part, PartDraft } from '@/types/part'

const inventory = ref<InventoryItem[]>([])
const search = ref('')
const statusFilter = ref<'all' | 'in_stock' | 'low_stock' | 'out_of_stock'>('all')
const inventorySort = ref<'name' | 'quantity' | 'min_quantity' | 'price' | 'category' | 'status'>('name')
const showForm = ref(false)
const editingItem = ref<Part | null>(null)
const selectedCarId = ref<number | null>(null)
const carOptions = ref<Car[]>([])
const formKey = ref(0)

async function loadCars() {
  try {
    const data = await listCars()
    carOptions.value = data || []
    if (!selectedCarId.value && carOptions.value[0]) {
      selectedCarId.value = carOptions.value[0].id ?? null
    }
  } catch (err) {
    console.error(err)
  }
}

async function loadInventory() {
  const term = search.value.trim()
  try {
    const data = await listInventory(term)
    inventory.value = (data || []) as InventoryItem[]
  } catch (err) {
    console.error(err)
    inventory.value = []
  }
}

async function addItem() {
  await loadCars()
  selectedCarId.value = selectedCarId.value ?? carOptions.value[0]?.id ?? null
  editingItem.value = null
  showForm.value = true
  formKey.value += 1
}

function cancelForm() {
  showForm.value = false
  editingItem.value = null
  formKey.value += 1
}

function editItem(item: InventoryItem) {
  const selected = item.car_id ?? selectedCarId.value ?? carOptions.value[0]?.id ?? null
  selectedCarId.value = selected
  editingItem.value = {
    id: item.id,
    name: item.name,
    sku: item.sku,
    category: item.category,
    quantity: item.quantity,
    min_quantity: item.min_quantity,
    price: item.price,
    supplier: item.supplier,
    location: item.location,
    notes: item.notes,
    car_id: item.car_id,
    make: item.make,
    model: item.model,
  }
  showForm.value = true
  formKey.value += 1
}

async function handleSaved(payload: { id?: number; data: PartDraft }) {
  const carId = selectedCarId.value
  if (!carId) {
    alert('Please select a car before saving the stock item.')
    return
  }

  try {
    if (payload.id) {
      await updatePart(carId, payload.id, payload.data)
    } else {
      await createPart(carId, payload.data)
    }

    showForm.value = false
    editingItem.value = null
    formKey.value += 1
    await loadInventory()
  } catch (err) {
    console.error(err)
    alert('Failed to save stock item.')
  }
}

async function deleteItem(item: InventoryItem) {
  if (!item.id) return
  if (!item.car_id) {
    alert('This stock item has no associated car, so it cannot be deleted from the inventory API.')
    return
  }

  const confirmed = window.confirm(`Delete '${item.name}' from inventory?`)
  if (!confirmed) return

  try {
    await deletePart(item.car_id, item.id)
    await loadInventory()
  } catch (err) {
    console.error(err)
    alert('Delete stock item failed.')
  }
}

onMounted(() => {
  loadCars()
  loadInventory()
})

watch(search, () => {
  loadInventory()
})

const filteredInventory = computed(() => {
  const term = search.value.trim().toLowerCase()

  let result = inventory.value.filter((item) => {
    const status = getStockStatus(item.quantity, item.min_quantity)
    const matchesStatus = statusFilter.value === 'all' || status === statusFilter.value
    const haystack = [
      item.name,
      item.sku || '',
      item.category || '',
      item.make || '',
      item.model || '',
    ]
      .join(' ')
      .toLowerCase()

    const matchesSearch = !term || haystack.includes(term)

    return matchesStatus && matchesSearch
  })

  result = [...result].sort((a, b) => {
    switch (inventorySort.value) {
      case 'quantity':
        return Number(b.quantity ?? 0) - Number(a.quantity ?? 0)
      case 'min_quantity':
        return Number(b.min_quantity ?? 0) - Number(a.min_quantity ?? 0)
      case 'price':
        return Number(b.price ?? 0) - Number(a.price ?? 0)
      case 'category':
        return String(a.category || '').localeCompare(String(b.category || ''))
      case 'status': {
        const statusA = getStockStatus(a.quantity, a.min_quantity)
        const statusB = getStockStatus(b.quantity, b.min_quantity)
        return statusA.localeCompare(statusB)
      }
      case 'name':
      default:
        return String(a.name || '').localeCompare(String(b.name || ''))
    }
  })

  return result
})

function countByStatus(status: 'in_stock' | 'low_stock' | 'out_of_stock') {
  return inventory.value.filter((item) => getStockStatus(item.quantity, item.min_quantity) === status).length
}

function statusLabel(item: InventoryItem) {
  return getStockLabel(getStockStatus(item.quantity, item.min_quantity))
}

function badgeClass(item: InventoryItem) {
  const status = getStockStatus(item.quantity, item.min_quantity)
  switch (status) {
    case 'in_stock':
      return 'badge-green'
    case 'low_stock':
      return 'badge-yellow'
    case 'out_of_stock':
      return 'badge-red'
    default:
      return 'badge-neutral'
  }
}

function formatPrice(value?: number | null) {
  const num = Number(value ?? 0)
  return `$${num.toFixed(2)}`
}
</script>

<style scoped>
.inventory-shell {
  max-width: 1280px;
  margin: 0 auto;
  padding: 24px 16px 40px;
  font-family: Inter, Arial, sans-serif;
}

.topbar,
.toolbar,
.form-header {
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
  margin: 6px 0 0;
  font-size: 2rem;
}

h3 {
  margin: 0;
  font-size: 1.25rem;
}

.panel {
  background: #fff;
  border: 1px solid #e7edf7;
  border-radius: 16px;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.04);
}

.form-panel {
  margin-bottom: 18px;
  padding: 18px;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin: 12px 0 18px;
}

.form-field label {
  color: #41526b;
  font-weight: 600;
  font-size: 0.85rem;
}

.select-field {
  max-width: 420px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(140px, 1fr));
  gap: 12px;
  margin-bottom: 18px;
}

.stat-card {
  background: #fff;
  border: 1px solid #e7edf7;
  border-radius: 14px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-card span {
  color: #64748b;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.stat-card strong {
  font-size: 1.8rem;
  color: #0f172a;
}

.stat-card.success {
  background: #ecfdf5;
}

.stat-card.warning {
  background: #fff7ed;
}

.stat-card.danger {
  background: #fef2f2;
}

.toolbar {
  margin-bottom: 18px;
  flex-wrap: wrap;
}

.search-input,
.filter-select {
  border: 1px solid #dfe7f3;
  border-radius: 10px;
  padding: 10px 12px;
  min-height: 42px;
  background: white;
  color: #1f2937;
}

.search-input {
  min-width: 260px;
}

.table-wrap {
  background: white;
  border: 1px solid #e7edf7;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.04);
}

.inventory-table {
  width: 100%;
  border-collapse: collapse;
}

.inventory-table th,
.inventory-table td {
  border-bottom: 1px solid #edf2f7;
  padding: 12px 14px;
  text-align: left;
  vertical-align: middle;
}

.inventory-table th {
  background: #f8fafc;
  color: #475569;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 5px 10px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 700;
}

.badge-green {
  background: #dcfce7;
  color: #166534;
}

.badge-yellow {
  background: #fef3c7;
  color: #92400e;
}

.badge-red {
  background: #fee2e2;
  color: #991b1b;
}

.actions {
  display: flex;
  gap: 8px;
}

button {
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 9px 12px;
  background: #edf3ff;
  color: #1e293b;
  cursor: pointer;
  font-weight: 600;
}

button.primary {
  background: #2563eb;
  color: white;
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
  font-size: 0.75rem;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(140px, 1fr));
  }

  .topbar,
  .toolbar,
  .form-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-input {
    min-width: 100%;
  }
}
</style>
