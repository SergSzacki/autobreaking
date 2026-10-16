import api from './axios'
import type { Car, CarDraft } from '../types/car'

export const listCars = async () => {
  const response = await api.get('/cars')
  // Support older backend responses that return { cars: [...] } or directly an array
  if (response.data && Array.isArray(response.data)) return response.data as Car[]
  if (response.data && Array.isArray(response.data.cars)) return response.data.cars as Car[]
  return [] as Car[]
}

export const createCar = async (payload: CarDraft) => {
  const response = await api.post('/cars', payload)
  return response.data as Car
}

export const deleteCar = async (id: number) => {
  await api.delete(`/cars/${id}`)
}
