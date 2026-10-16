export interface Car {
  id?: number
  make: string
  model: string
  year: number
  vin?: string | null
  mileage?: number | null
  color?: string | null
  status?: string | null
}

export type CarDraft = Omit<Car, 'id'>
