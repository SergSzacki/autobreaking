<template>
  <form @submit.prevent="submitForm">
    <div>
      <label>Name</label>
      <input v-model="form.name" required />
    </div>
    <div>
      <label>Category</label>
      <input v-model="form.category" placeholder="engine, brakes, body..." />
    </div>
    <div>
      <label>SKU</label>
      <input v-model="form.sku" placeholder="OF-2042" />
    </div>
    <div>
      <label>Quantity</label>
      <input v-model.number="form.quantity" type="number" min="0" />
    </div>
    <div>
      <label>Price</label>
      <input v-model.number="form.price" type="number" min="0" step="0.01" />
    </div>
    <div>
      <label>Description</label>
      <textarea v-model="form.description" rows="3" />
    </div>

    <div style="margin-top:8px;">
      <button type="submit">Save part</button>
      <button type="button" @click="onCancel">Cancel</button>
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
  price: 0,
  description: '',
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
    form.price = init.price ?? 0
    form.description = init.description ?? ''
    form.car_id = props.carId ?? init.car_id ?? null
  } else {
    const d = defaultForm()
    form.name = d.name
    form.category = d.category
    form.sku = d.sku
    form.quantity = d.quantity
    form.price = d.price
    form.description = d.description
    form.car_id = d.car_id
  }
}

watch(() => props.initial, resetForm, { immediate: true })
watch(() => props.carId, resetForm)

const submitForm = () => {
  const payload: PartDraft = {
    name: String(form.name).trim(),
    category: form.category ? String(form.category).trim() : null,
    sku: form.sku ? String(form.sku).trim() : null,
    quantity: Number(form.quantity || 0),
    price: Number(form.price || 0),
    description: form.description ? String(form.description).trim() : null,
    car_id: props.carId ?? form.car_id ?? null,
  }

  const id = (props.initial && (props.initial as any).id) as number | undefined
  emit('saved', { id, data: payload })
}

const onCancel = () => {
  emit('cancel')
}

const reset = () => {
  resetForm()
}

defineExpose({ reset })
</script>
