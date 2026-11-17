import api from './axios'
import type { Car, CarDraft } from '../types/car'

const CARS_PAGE_SIZE = 200

export const listCars = async () => {
  const cars: Car[] = []
  for (let page = 1; ; page += 1) {
    const response = await api.get('/cars', { params: { page, per_page: CARS_PAGE_SIZE } })
    const batch = (response.data?.cars ?? []) as Car[]
    cars.push(...batch)
    const total = Number(response.data?.meta?.total ?? cars.length)
    if (batch.length < CARS_PAGE_SIZE || cars.length >= total) return cars
  }
}

export const getCarById = async (id: number) => {
  const response = await api.get(`/cars/${id}`)
  return response.data as Car
}

export const createCar = async (payload: CarDraft) => {
  const response = await api.post('/cars', payload)
  return response.data as Car
}

export const updateCar = async (id: number, payload: Partial<CarDraft>) => {
  const response = await api.patch(`/cars/${id}`, payload)
  return response.data as Car
}

export const deleteCar = async (id: number) => {
  await api.delete(`/cars/${id}`)
}
