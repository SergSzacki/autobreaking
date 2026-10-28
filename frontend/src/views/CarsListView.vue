<template>
  <form class="part-form" @submit.prevent="submitForm">
    <div class="field-grid">
      <div class="field">
        <label>Name</label>
        <input v-model="form.name" required />
      </div>

      <div class="field">
        <label>Category</label>
        <select v-model="form.category">
          <option value="">Select category</option>
          <option value="engine">Engine</option>
          <option value="brakes">Brakes</option>
          <option value="suspension">Suspension</option>
          <option value="electrical">Electrical</option>
          <option value="body">Body</option>
          <option value="interior">Interior</option>
          <option value="tires">Tires</option>
          <option value="fluids">Fluids</option>
          <option value="filters">Filters</option>
        </select>
      </div>

      <div class="field">
        <label>SKU</label>
        <input v-model="form.sku" placeholder="OF-2042" />
      </div>

      <div class="field">
        <label>Quantity</label>
        <input v-model.number="form.quantity" type="number" min="0" />
      </div>

      <div class="field">
        <label>Min quantity</label>
        <input v-model.number="form.min_quantity" type="number" min="0" />
      </div>

      <div class="field">
        <label>Price</label>
        <input v-model.number="form.price" type="number" min="0" step="0.01" />
      </div>

      <div class="field">
        <label>Supplier</label>
        <input v-model="form.supplier" placeholder="OEM / supplier" />
      </div>

      <div class="field">
        <label>Location</label>
        <input v-model="form.location" placeholder="A1 / Shelf B" />
      </div>

      <div class="field wide">
        <label>Notes</label>
        <textarea v-model="form.notes" rows="3" />
      </div>
    </div>

    <div class="actions-row">
      <button type="submit" class="primary">Save part</button>
      <button type="button" class="ghost" @click="onCancel">Cancel</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import type { Part, PartDraft } from '@/types/part'

const props = defineProps<{ initial?: Partial<Part>; carId?: number | null }>()
const emit = defineEmits<{ (e: 'saved', payload: { id?: number; data: PartDraft }): void; (e: 'cancel'): void }>()

const defaultForm = (): PartDraft => ({
  name: '',
  category: '',
  sku: '',
  quantity: 0,
  min_quantity: 0,
  price: 0,
  supplier: '',
  location: '',
  notes: '',
  car_id: props.carId ?? null,
})

const form = reactive<PartDraft>(defaultForm())

const resetForm = () => {
  const init = props.initial

  if (init) {
    form.name = init.name ?? ''
    form.category = init.category ?? ''
    form.sku = init.sku ?? ''
    form.quantity = init.quantity ?? 0
    form.min_quantity = init.min_quantity ?? 0
    form.price = init.price ?? 0
    form.supplier = init.supplier ?? ''
    form.location = init.location ?? ''
    form.notes = init.notes ?? init.description ?? ''
    form.car_id = props.carId ?? init.car_id ?? null
    return
  }

  const d = defaultForm()
  form.name = d.name
  form.category = d.category
  form.sku = d.sku
  form.quantity = d.quantity
  form.min_quantity = d.min_quantity
  form.price = d.price
  form.supplier = d.supplier
  form.location = d.location
  form.notes = d.notes
  form.car_id = d.car_id
}

watch(() => props.initial, resetForm, { immediate: true })
watch(() => props.carId, resetForm)

const submitForm = () => {
  const payload: PartDraft = {
    name: String(form.name).trim(),
    category: form.category ? String(form.category).trim() : null,
    sku: form.sku ? String(form.sku).trim() : null,
    quantity: Number(form.quantity || 0),
    min_quantity: Number(form.min_quantity || 0),
    price: Number(form.price || 0),
    supplier: form.supplier ? String(form.supplier).trim() : null,
    location: form.location ? String(form.location).trim() : null,
    notes: form.notes ? String(form.notes).trim() : null,
    car_id: props.carId ?? form.car_id ?? null,
  }

  const id = (props.initial && (props.initial as any).id) as number | undefined
  emit('saved', { id, data: payload })
}

const onCancel = () => emit('cancel')

const reset = () => resetForm()

defineExpose({ reset })
</script>

<style scoped>
.part-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(180px, 1fr));
  gap: 12px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field.wide {
  grid-column: 1 / -1;
}

label {
  font-weight: 600;
  color: #41526b;
  font-size: 0.85rem;
}

input, textarea, select {
  width: 100%;
  border: 1px solid #d7e0ee;
  border-radius: 10px;
  padding: 10px 12px;
  font: inherit;
  background: white;
  box-sizing: border-box;
}

textarea {
  min-height: 90px;
  resize: vertical;
}

.actions-row {
  display: flex;
  gap: 10px;
}

button {
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 8px 14px;
  font-weight: 600;
  cursor: pointer;
}

button.primary {
  background: #2563eb;
  color: white;
}

button.ghost {
  background: #f8fafc;
  border-color: #dfe7f3;
  color: #1f2937;
}
</style>
