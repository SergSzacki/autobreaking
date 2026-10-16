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
    <button type="submit">Save car</button>
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import type { CarDraft } from '@/types/car'

const emit = defineEmits<{ (e: 'saved'): void }>()

const form = reactive<CarDraft>({
  make: '',
  model: '',
  year: new Date().getFullYear(),
  vin: '',
  mileage: 0,
  color: '',
  status: 'available',
})

const submitForm = async () => {
  const payload: CarDraft = {
    make: form.make.trim(),
    model: form.model.trim(),
    year: Number(form.year),
    vin: form.vin?.trim() || null,
    mileage: Number(form.mileage || 0),
    color: form.color?.trim() || null,
    status: form.status || 'available',
  }

  emit('saved', payload)
}

const reset = () => {
  form.make = ''
  form.model = ''
  form.year = new Date().getFullYear()
  form.vin = ''
  form.mileage = 0
  form.color = ''
  form.status = 'available'
}

defineExpose({ reset })
</script>
