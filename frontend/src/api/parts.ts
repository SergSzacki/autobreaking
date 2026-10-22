import api from './axios'
import type { Part, PartDraft } from '../types/part'

export const listPartsByCar = async (carId: number) => {
  const response = await api.get(`/cars/${carId}/parts`)
  return (response.data || []) as Part[]
}

export const createPart = async (carId: number, payload: PartDraft) => {
  const response = await api.post(`/cars/${carId}/parts`, payload)
  return response.data as Part
}

export const updatePart = async (carId: number, partId: number, payload: Partial<PartDraft>) => {
  const response = await api.patch(`/cars/${carId}/parts/${partId}`, payload)
  return response.data as Part
}

export const deletePart = async (carId: number, partId: number) => {
  await api.delete(`/cars/${carId}/parts/${partId}`)
}
