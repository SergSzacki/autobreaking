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
