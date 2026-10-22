export interface Part {
  id?: number
  name: string
  category?: string | null
  sku?: string | null
  quantity?: number | null
  price?: number | null
  description?: string | null
  car_id?: number | null
}

export type PartDraft = Omit<Part, 'id'>
