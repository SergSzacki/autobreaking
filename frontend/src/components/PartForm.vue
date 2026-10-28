export interface Part {
  id?: number
  name: string
  category?: string | null
  sku?: string | null
  quantity?: number | null
  min_quantity?: number | null
  price?: number | null
  supplier?: string | null
  location?: string | null
  notes?: string | null
  description?: string | null
  car_id?: number | null
  make?: string | null
  model?: string | null
}

export type PartDraft = Omit<Part, 'id'>

export const normalizePartDraft = (input: Partial<Part>): Partial<Part> => ({
  name: input.name ?? '',
  category: input.category ?? null,
  sku: input.sku ?? null,
  quantity: input.quantity ?? 0,
  min_quantity: input.min_quantity ?? 0,
  price: input.price ?? 0,
  supplier: input.supplier ?? null,
  location: input.location ?? null,
  notes: input.notes ?? input.description ?? null,
  car_id: input.car_id ?? null,
})

export const getPartNotes = (part?: Partial<Part> | null) =>
  part?.notes ?? part?.description ?? ''

export const getPartDisplayName = (part?: Partial<Part> | null) =>
  part?.name ?? 'Unnamed part'

export const getPartStatus = (part?: Partial<Part> | null) => {
  const qty = Number(part?.quantity ?? 0)
  const min = Number(part?.min_quantity ?? 0)

  if (qty <= 0) return 'out_of_stock'
  if (qty <= min) return 'low_stock'
  return 'in_stock'
}
