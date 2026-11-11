<template>
  <div class="part-photos" :aria-label="label">
    <a
      v-for="(photo, index) in normalizedPhotos"
      :key="`${photo}-${index}`"
      class="part-photo-link"
      :href="photo"
      target="_blank"
      rel="noopener noreferrer"
      :aria-label="`${label} — фото ${index + 1}`"
    >
      <img
        class="part-photo"
        :src="photo"
        :alt="`${label} — фото ${index + 1}`"
        loading="lazy"
        @error="hideBrokenImage"
      />
    </a>
    <span v-if="!normalizedPhotos.length" class="no-photos">{{ emptyLabel }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  photos?: string[] | null
  label?: string
  emptyLabel?: string
}>(), {
  photos: () => [],
  label: 'Part photos',
  emptyLabel: 'No photos',
})

const normalizedPhotos = computed(() =>
  (props.photos ?? []).filter((photo) => typeof photo === 'string' && photo.trim().length > 0),
)

function hideBrokenImage(event: Event) {
  const image = event.target as HTMLImageElement
  image.closest('.part-photo-link')?.classList.add('is-broken')
}
</script>

<style scoped>
.part-photos {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  min-width: 90px;
}

.part-photo-link {
  display: block;
  width: 72px;
  height: 60px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #f8fafc;
}

.part-photo-link.is-broken {
  display: none;
}

.part-photo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-photos {
  color: #64748b;
  font-size: 0.8rem;
}
</style>
