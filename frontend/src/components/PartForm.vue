<template>
  <form class="part-form" @submit.prevent="submitForm">
    <div class="field-grid">
      <div class="field">
        <label for="part-name">Name</label>
        <input id="part-name" v-model="form.name" required />
      </div>

      <div class="field">
        <label for="part-category">Category</label>
        <select id="part-category" v-model="form.category">
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
        <label for="part-sku">SKU</label>
        <input id="part-sku" v-model="form.sku" placeholder="OF-2042" />
      </div>

      <div class="field">
        <label for="part-quantity">Quantity</label>
        <input id="part-quantity" v-model.number="form.quantity" type="number" min="0" />
      </div>

      <div class="field">
        <label for="part-min-quantity">Min quantity</label>
        <input id="part-min-quantity" v-model.number="form.min_quantity" type="number" min="0" />
      </div>

      <div class="field">
        <label for="part-price">Price</label>
        <input id="part-price" v-model.number="form.price" type="number" min="0" step="0.01" />
      </div>

      <div class="field">
        <label for="part-supplier">Supplier</label>
        <input id="part-supplier" v-model="form.supplier" placeholder="OEM / supplier" />
      </div>

      <div class="field">
        <label for="part-location">Location</label>
        <input id="part-location" v-model="form.location" placeholder="A1 / Shelf B" />
      </div>

      <div class="field wide">
        <label for="part-notes">Notes</label>
        <textarea id="part-notes" v-model="form.notes" rows="3" />
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
const emit = defineEmits<{
  (event: 'saved', payload: { id?: number; data: PartDraft }): void
  (event: 'cancel'): void
}>()

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

function resetForm() {
  const initial = props.initial
  if (initial) {
    form.name = initial.name ?? ''
    form.category = initial.category ?? ''
    form.sku = initial.sku ?? ''
    form.quantity = initial.quantity ?? 0
    form.min_quantity = initial.min_quantity ?? 0
    form.price = initial.price ?? 0
    form.supplier = initial.supplier ?? ''
    form.location = initial.location ?? ''
    form.notes = initial.notes ?? initial.description ?? ''
    form.car_id = props.carId ?? initial.car_id ?? null
    return
  }

  Object.assign(form, defaultForm())
}

watch(() => props.initial, resetForm, { immediate: true })
watch(() => props.carId, resetForm)

function submitForm() {
  const payload: PartDraft = {
    name: form.name.trim(),
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

  emit('saved', { id: props.initial?.id, data: payload })
}

function onCancel() {
  emit('cancel')
}

defineExpose({ reset: resetForm })
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

input,
textarea,
select {
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

@media (max-width: 520px) {
  .field-grid {
    grid-template-columns: 1fr;
  }

  .field.wide {
    grid-column: auto;
  }
}
</style>
