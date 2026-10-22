<template>
  <div class="inventory-shell">
    <div class="topbar">
      <div>
        <div class="eyebrow">Warehouse</div>
        <h2>Inventory</h2>
      </div>

      <button class="primary" @click="addItem">Add stock item</button>
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
        placeholder="Search by name or SKU"
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
            <td>{{ item.sku }}</td>
            <td>{{ item.category }}</td>
            <td>{{ item.quantity }}</td>
            <td>{{ item.min_quantity }}</td>
            <td>
              <span :class="['badge', badgeClass(item)]">
                {{ statusLabel(item) }}
              </span>
            </td>
            <td>{{ item.price }} $</td>
            <td>{{ item.supplier || '-' }}</td>
            <td>{{ item.location || '-' }}</td>
            <td>{{ item.car_id ? `#${item.car_id}` : '-' }}</td>
            <td class="actions">
              <button class="ghost small" @click="editItem(item)">Edit</button>
              <button class="ghost small danger" @click="deleteItem(item.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { getStockLabel, getStockStatus, type InventoryItem } from '@/utils/stock'

const inventory = ref<InventoryItem[]>([
  {
    id: 1,
    name: 'Brake pads',
    sku: 'BR-001',
    category: 'brakes',
    quantity: 12,
    min_quantity: 4,
    price: 120,
    supplier: 'AutoLine',
    location: 'A1',
    car_id: 1,
  },
  {
    id: 2,
    name: 'Oil filter',
    sku: 'OF-125',
    category: 'engine',
    quantity: 2,
    min_quantity: 4,
    price: 35,
    supplier: 'MotorPro',
    location: 'B2',
    car_id: null,
  },
  {
    id: 3,
    name: 'Spark plug',
    sku: 'SP-500',
    category: 'engine',
    quantity: 0,
    min_quantity: 2,
    price: 15,
    supplier: 'FireSpark',
    location: 'C1',
    car_id: 2,
  },
  {
    id: 4,
    name: 'Headlight bulb',
    sku: 'HL-408',
    category: 'electrical',
    quantity: 8,
    min_quantity: 3,
    price: 26,
    supplier: 'VoltLab',
    location: 'D3',
    car_id: null,
  },
])

const search = ref('')
const statusFilter = ref<'all' | 'in_stock' | 'low_stock' | 'out_of_stock'>('all')
const inventorySort = ref<'name' | 'quantity' | 'min_quantity' | 'price' | 'category' | 'status'>('name')

const filteredInventory = computed(() => {
  const term = search.value.trim().toLowerCase()

  let result = inventory.value.filter((item) => {
    const status = getStockStatus(item.quantity, item.min_quantity)
    const matchesStatus = statusFilter.value === 'all' || status === statusFilter.value
    const matchesSearch =
      !term ||
      item.name.toLowerCase().includes(term) ||
      item.sku.toLowerCase().includes(term)

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

function addItem() {
  alert('Add stock item form coming soon')
}

function editItem(item: InventoryItem) {
  alert(`Edit ${item.name}`)
}

function deleteItem(id: number) {
  inventory.value = inventory.value.filter((item) => item.id !== id)
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
.toolbar {
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
  .toolbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .search-input {
    min-width: 100%;
  }
}
</style>
