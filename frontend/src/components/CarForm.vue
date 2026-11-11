<template>
  <form @submit.prevent="submitForm">
    <div>
      <label>Make</label>
      <input v-model="form.make" list="car-makes-list" placeholder="Select or type a brand" required />
      <datalist id="car-makes-list">
        <option v-for="brand in carMakes" :key="brand" :value="brand" />
      </datalist>
    </div>
    <div>
      <label>Model</label>
      <input
        v-model="form.model"
        list="car-models-list"
        placeholder="Select or type a model"
        required
      />
      <datalist id="car-models-list">
        <option v-for="model in carModels" :key="model" :value="model" />
      </datalist>
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
import { computed, reactive, watch } from 'vue'
import type { CarDraft, Car } from '@/types/car'

const props = defineProps<{ initial?: Partial<Car> }>()
const emit = defineEmits<{ (e: 'saved', payload: { id?: number; data: CarDraft }): void; (e: 'cancel'): void }>()

const defaultCarModelsByMake: Record<string, string[]> = {
  Audi: ['A1', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'Q2', 'Q3', 'Q5', 'Q7', 'Q8', 'TT', 'e-tron'],
  BMW: ['1 Series', '2 Series', '3 Series', '4 Series', '5 Series', '7 Series', 'X1', 'X3', 'X5', 'X6', 'X7', 'Z4', 'i3', 'i4', 'iX'],
  Chevrolet: ['Aveo', 'Camaro', 'Captiva', 'Cruze', 'Malibu', 'Spark', 'Tahoe', 'Traverse'],
  Citroen: ['Berlingo', 'C1', 'C3', 'C4', 'C5', 'Jumper', 'Jumpy'],
  Dodge: ['Challenger', 'Charger', 'Durango', 'Journey', 'Ram'],
  Ford: ['Bronco', 'EcoSport', 'Edge', 'Escape', 'Explorer', 'Fiesta', 'Focus', 'Kuga', 'Mondeo', 'Mustang', 'Ranger', 'Transit'],
  Honda: ['Accord', 'Civic', 'CR-V', 'HR-V', 'Jazz', 'Pilot'],
  Hyundai: ['Accent', 'Elantra', 'i10', 'i20', 'i30', 'Kona', 'Santa Fe', 'Tucson'],
  Kia: ['Ceed', 'Niro', 'Optima', 'Picanto', 'Rio', 'Sorento', 'Sportage', 'Stonic'],
  Lexus: ['ES', 'GS', 'IS', 'LC', 'LS', 'NX', 'RX', 'UX'],
  Mazda: ['2', '3', '5', '6', 'CX-3', 'CX-30', 'CX-5', 'CX-9', 'MX-5'],
  'Mercedes-Benz': ['A-Class', 'B-Class', 'C-Class', 'E-Class', 'S-Class', 'CLA', 'CLS', 'GLA', 'GLB', 'GLC', 'GLE', 'GLS', 'Sprinter'],
  Mitsubishi: ['ASX', 'Eclipse Cross', 'L200', 'Lancer', 'Outlander', 'Pajero'],
  Nissan: ['Juke', 'Leaf', 'Micra', 'Navara', 'Qashqai', 'X-Trail'],
  Peugeot: ['208', '2008', '308', '3008', '508', '5008', 'Partner', 'Rifter'],
  Porsche: ['718', '911', 'Cayenne', 'Macan', 'Panamera', 'Taycan'],
  Renault: ['Clio', 'Captur', 'Kadjar', 'Kangoo', 'Megane', 'Scenic', 'Trafic'],
  Subaru: ['Forester', 'Impreza', 'Legacy', 'Outback', 'XV'],
  Suzuki: ['Alto', 'Baleno', 'Jimny', 'Swift', 'Vitara'],
  Tesla: ['Model 3', 'Model S', 'Model X', 'Model Y'],
  Toyota: ['Auris', 'Avensis', 'Aygo', 'Camry', 'Corolla', 'Hilux', 'Land Cruiser', 'Prius', 'RAV4', 'Yaris'],
  Volkswagen: ['Arteon', 'Caddy', 'Golf', 'ID.3', 'ID.4', 'Passat', 'Polo', 'Tiguan', 'Touareg', 'Touran', 'Transporter'],
  Volvo: ['C30', 'S60', 'S90', 'V40', 'V60', 'V90', 'XC40', 'XC60', 'XC90'],
}

const carOptionsStorageKey = 'autobreaking.carModelsByMake'

function loadCarModelsByMake(): Record<string, string[]> {
  const options = Object.fromEntries(
    Object.entries(defaultCarModelsByMake).map(([make, models]) => [make, [...models]]),
  )

  try {
    const stored = localStorage.getItem(carOptionsStorageKey)
    if (!stored) return options

    const savedOptions: unknown = JSON.parse(stored)
    if (!savedOptions || typeof savedOptions !== 'object' || Array.isArray(savedOptions)) return options

    for (const [savedMake, savedModels] of Object.entries(savedOptions)) {
      const make = savedMake.trim()
      if (!make || !Array.isArray(savedModels)) continue

      const existingMake = Object.keys(options).find((item) => item.toLowerCase() === make.toLowerCase())
      const makeKey = existingMake || make
      options[makeKey] ??= []

      for (const savedModel of savedModels) {
        if (typeof savedModel !== 'string' || !savedModel.trim()) continue
        const model = savedModel.trim()
        if (!options[makeKey].some((item) => item.toLowerCase() === model.toLowerCase())) {
          options[makeKey].push(model)
        }
      }
    }
  } catch {
    // Keep the built-in options if browser storage is unavailable or invalid.
  }

  return options
}

const carModelsByMake = reactive(loadCarModelsByMake())
const carMakes = computed(() => Object.keys(carModelsByMake).sort((a, b) => a.localeCompare(b)))
const carModels = computed(() => {
  const make = form.make.trim().toLowerCase()
  const matchingMake = Object.keys(carModelsByMake).find((brand) => brand.toLowerCase() === make)
  return matchingMake ? carModelsByMake[matchingMake] : []
})

function rememberCarOptions(makeValue: string, modelValue: string) {
  const make = makeValue.trim()
  const model = modelValue.trim()
  if (!make || !model) return

  const existingMake = Object.keys(carModelsByMake).find((brand) => brand.toLowerCase() === make.toLowerCase())
  const makeKey = existingMake || make
  carModelsByMake[makeKey] ??= []
  if (!carModelsByMake[makeKey].some((item) => item.toLowerCase() === model.toLowerCase())) {
    carModelsByMake[makeKey].push(model)
  }

  try {
    localStorage.setItem(carOptionsStorageKey, JSON.stringify(carModelsByMake))
  } catch {
    // The car can still be saved when browser storage is unavailable.
  }
}

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
watch(() => form.make, (newMake, oldMake) => {
  if (newMake.trim().toLowerCase() !== oldMake.trim().toLowerCase()) {
    form.model = ''
  }
})

const submitForm = () => {
  const payload: CarDraft = {
    make: String(form.make).trim(),
    model: String(form.model).trim(),
    year: Number(form.year),
    vin: form.vin ? String(form.vin).trim() : null,
    mileage: Number(form.mileage || 0),
    color: form.color ? String(form.color).trim() : null,
    status: form.status || 'available',
  }

  rememberCarOptions(payload.make, payload.model)
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
