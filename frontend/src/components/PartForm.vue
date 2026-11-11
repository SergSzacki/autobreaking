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

      <div class="field wide">
        <label for="part-photos">Photos</label>
        <textarea id="part-photos" v-model="form.photosText" rows="4" placeholder="https://example.com/a.jpg&#10;https://example.com/b.jpg" />
        <small>One URL per line or comma-separated</small>
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

const form = reactive<PartDraft & { photosText: string }>({
  name: '',
  category: '',
  sku: '',
  quantity: 0,
  min_quantity: 0,
  price: 0,
  supplier: '',
  location: '',
  notes: '',
  description: '',
  photos: [],
  photosText: '',
  car_id: props.carId ?? null,
  make: '',
  model: '',
})

const normalizePhotos = (value: string): string[] =>
  [...new Set(
    value
      .split(/[\n,]+/)
      .map((item) => item.trim())
      .filter(Boolean),
  )]

function resetForm() {
  const initial = props.initial ?? {}
  const nextPhotos = Array.isArray(initial.photos) ? initial.photos : []

  Object.assign(form, {
    name: initial.name ?? '',
    category: initial.category ?? '',
    sku: initial.sku ?? '',
    quantity: initial.quantity ?? 0,
    min_quantity: initial.min_quantity ?? 0,
    price: initial.price ?? 0,
    supplier: initial.supplier ?? '',
    location: initial.location ?? '',
    notes: initial.notes ?? '',
    description: initial.description ?? '',
    photos: nextPhotos,
    photosText: nextPhotos.join('\n'),
    car_id: props.carId ?? initial.car_id ?? null,
    make: initial.make ?? '',
    model: initial.model ?? '',
  })
}

watch(() => props.initial, resetForm, { immediate: true })
watch(
  () => props.carId,
  () => {
    if (!props.initial?.id) form.car_id = props.carId ?? null
  },
)

function submitForm() {
  const { photosText, ...rest } = form
  const payload: PartDraft = {
    ...rest,
    photos: normalizePhotos(photosText),
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
.part-form { display:flex; flex-direction:column; gap:16px; }
.field-grid { display:grid; grid-template-columns:repeat(2,minmax(180px,1fr)); gap:14px; }
.field { display:flex; flex-direction:column; gap:6px; }
.field.wide { grid-column:1 / -1; }
label { font-size:.8rem; color:#41526b; font-weight:600; }
input,select,textarea { width:100%; border:1px solid #dfe7f3; border-radius:10px; padding:10px 12px; background:white; color:#1f2937; font:inherit; box-sizing:border-box; }
textarea { resize:vertical; min-height:92px; }
small { color:#64748b; font-size:.75rem; }
.actions-row { display:flex; gap:10px; }
button { border:1px solid transparent; border-radius:10px; padding:9px 12px; background:#edf3ff; color:#1e293b; cursor:pointer; font-weight:600; }
button.primary { background:#2563eb; color:white; }
button.ghost { background:#f8fafc; border-color:#d8e1ef; }
@media (max-width:520px) { .field-grid { grid-template-columns:1fr; } .field.wide { grid-column:auto; } }
</style>
