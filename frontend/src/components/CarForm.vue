<template>
  <form @submit.prevent="submitForm">
    <div>
      <label>Make</label>
      <input v-model="form.make" required />
    </div>
    <div>
      <label>Model</label>
      <input v-model="form.model" required />
    </div>
    <div>
      <label>Year</label>
      <input v-model.number="form.year" type="number" min="1900" max="2100" required />
    </div>
    <div>
      <label>VIN</label>
      <input v-model="form.vin" />
    </div>
    <div>
      <label>Mileage</label>
      <input v-model.number="form.mileage" type="number" min="0" />
    </div>
    <div>
      <label>Color</label>
      <input v-model="form.color" />
    </div>
    <div>
      <label>Status</label>
      <select v-model="form.status">
        <option value="available">available</option>
        <option value="maintenance">maintenance</option>
        <option value="sold">sold</option>
      </select>
    </div>
    <div style="margin-top:8px;">
      <button type="submit">Save</button>
      <button type="button" @click="onCancel">Cancel</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, watch, toRaw } from 'vue'
import type { CarDraft, Car } from '@/types/car'

const props = defineProps<{ initial?: Partial<Car> }>()
const emit = defineEmits<{ (e: 'saved', payload: { id?: number; data: CarDraft }): void; (e: 'cancel'): void }>()

const defaultForm = (): CarDraft => ({
  make: '',
  model: '',
  year: new Date().getFullYear(),
  vin: null,
  mileage: 0,
  color: null,
  status: 'available',
})

const form = reactive<CarDraft>(defaultForm())

// initialize with props.initial when provided
const resetForm = () => {
  const init = props.initial
  if (init) {
    form.make = (init.make as string) || ''
    form.model = (init.model as string) || ''
    form.year = (init.year as number) || new Date().getFullYear()
    form.vin = init.vin ?? null
    form.mileage = init.mileage ?? 0
    form.color = init.color ?? null
    form.status = init.status ?? 'available'
  } else {
    const d = defaultForm()
    form.make = d.make
    form.model = d.model
    form.year = d.year
    form.vin = d.vin
    form.mileage = d.mileage
    form.color = d.color
    form.status = d.status
  }
}

watch(() => props.initial, resetForm, { immediate: true })

const submitForm = async () => {
  const payload: CarDraft = {
    make: String(form.make).trim(),
    model: String(form.model).trim(),
    year: Number(form.year),
    vin: form.vin ? String(form.vin).trim() : null,
    mileage: Number(form.mileage || 0),
    color: form.color ? String(form.color).trim() : null,
    status: form.status || 'available',
  }

  // include id if editing via props.initial
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
