import { computed, onMounted, ref, watch } from 'vue'
import { getStockLabel, getStockStatus, type InventoryItem } from '@/utils/stock'
import { listInventory } from '@/api/parts'

const inventory = ref<InventoryItem[]>([])
const search = ref('')
const statusFilter = ref<'all' | 'in_stock' | 'low_stock' | 'out_of_stock'>('all')
const inventorySort = ref<'name' | 'quantity' | 'min_quantity' | 'price' | 'category' | 'status'>('name')

async function loadInventory() {
  const term = search.value.trim()
  inventory.value = await listInventory(term)
}

onMounted(() => {
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
      item.sku,
      item.category,
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

function addItem() {
  alert('Add stock item form coming soon')
}

function editItem(item: InventoryItem) {
  alert(`Edit ${item.name}`)
}

function deleteItem(id: number) {
  inventory.value = inventory.value.filter((item) => item.id !== id)
}
