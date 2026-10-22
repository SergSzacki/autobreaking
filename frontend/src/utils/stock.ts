export type StockStatus = 'in_stock' | 'low_stock' | 'out_of_stock'

export interface InventoryItem {
  id: number
  name: string
  sku: string
  category: string
  quantity: number
  min_quantity: number
  price: number
  supplier: string
  location: string
  car_id?: number | null
  notes?: string
}

export function getStockStatus(quantity: number, minQuantity = 0): StockStatus {
  if (quantity <= 0) return 'out_of_stock'
  if (quantity <= minQuantity) return 'low_stock'
  return 'in_stock'
}

export function getStockLabel(status: StockStatus): string {
  switch (status) {
    case 'in_stock':
      return 'In stock'
    case 'low_stock':
      return 'Low stock'
    case 'out_of_stock':
      return 'Out of stock'
    default:
      return 'Unknown'
  }
}
