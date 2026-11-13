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
        <label>Photos</label>

        <div class="photo-tools">
          <button type="button" class="ghost small" @click="triggerPhotoPicker">Add photo</button>
          <input
            ref="photoInput"
            type="file"
            accept="image/*"
            multiple
            class="hidden-file-input"
            @change="handlePhotoSelect"
          />
        </div>

        <div v-if="photoPreviewList.length" class="photo-preview-list">
          <div v-for="(photo, index) in photoPreviewList" :key="`${photo}-${index}`" class="photo-preview-item">
            <img :src="photo" :alt="`Photo ${index + 1}`" />
            <button type="button" class="mini-btn" @click="removePhoto(index)">Remove</button>
          </div>
        </div>

        <textarea
          id="part-photos"
          v-model="form.photosText"
          rows="4"
          placeholder="https://example.com/a.jpg&#10;data:image/png;base64,..."
        />
        <small>One URL per line or comma-separated. You can also add files from disk.</small>
      </div>
    </div>

    <div class="actions-row">
      <button type="submit" class="primary">Save part</button>
      <button type="button" class="ghost" @click="onCancel">Cancel</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import type { Part, PartDraft } from '@/types/part'

const props = defineProps<{ initial?: Partial<Part>; carId?: number | null }>()
const emit = defineEmits<{
  (event: 'saved', payload: { id?: number; data: PartDraft }): void
  (event: 'cancel'): void
}>()

const photoInput = ref<HTMLInputElement | null>(null)

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

const photoPreviewList = computed(() => normalizePhotos(form.photosText))

function normalizePhotos(value: string): string[] {
  const entries = value
    .split(/\r?\n/)
    .flatMap((line) => {
      const trimmed = line.trim()
      if (!trimmed) return []

      if (trimmed.startsWith('data:')) {
        return [trimmed]
      }

      return trimmed
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean)
    })

  return [...new Set(entries.filter(Boolean))]
}

function triggerPhotoPicker() {
  photoInput.value?.click()
}

function removePhoto(index: number) {
  const photos = normalizePhotos(form.photosText)
  photos.splice(index, 1)
  form.photosText = photos.join('\n')
}

function readFileAsDataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(String(reader.result))
    reader.onerror = () => reject(new Error(`Failed to read file: ${file.name}`))
    reader.readAsDataURL(file)
  })
}

async function handlePhotoSelect(event: Event) {
  const input = event.target as HTMLInputElement
  const files = Array.from(input.files ?? []).filter((file) => file.type.startsWith('image/'))

  if (!files.length) {
    input.value = ''
    return
  }

  try {
    const urls = await Promise.all(files.map((file) => readFileAsDataUrl(file)))
    const merged = [...normalizePhotos(form.photosText), ...urls]
    form.photosText = [...new Set(merged.filter(Boolean))].join('\n')
  } catch (error) {
    console.error(error)
  } finally {
    input.value = ''
  }
}

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
.photo-tools { display:flex; align-items:center; gap:10px; }
.hidden-file-input { display:none; }
.photo-preview-list { display:flex; flex-wrap:wrap; gap:8px; margin:8px 0; }
.photo-preview-item { position:relative; width:72px; height:60px; overflow:hidden; border-radius:8px; border:1px solid #dfe7f3; background:#f8fafc; }
.photo-preview-item img { display:block; width:100%; height:100%; object-fit:cover; }
.mini-btn { position:absolute; right:4px; top:4px; border:0; border-radius:999px; background:rgba(15, 23, 42, 0.7); color:#fff; font-size:.65rem; padding:3px 6px; cursor:pointer; }
.actions-row { display:flex; gap:10px; }
button { border:1px solid transparent; border-radius:10px; padding:9px 12px; background:#edf3ff; color:#1e293b; cursor:pointer; font-weight:600; }
button.primary { background:#2563eb; color:white; }
button.ghost { background:#f8fafc; border-color:#d8e1ef; }
button.small { padding:7px 10px; font-size:.8rem; }
@media (max-width:520px) { .field-grid { grid-template-columns:1fr; } .field.wide { grid-column:auto; } }
</style>
