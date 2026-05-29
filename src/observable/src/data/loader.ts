import type { CombinedData, TemperatureData } from '../types'

const BASE = import.meta.env.BASE_URL

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`Failed to load ${url}: ${res.status}`)
  return res.json()
}

export function loadCombinedData(): Promise<CombinedData> {
  return fetchJSON<CombinedData>(`${BASE}data/combined.json`)
}

export function loadTemperatureData(): Promise<TemperatureData> {
  return fetchJSON<TemperatureData>(`${BASE}data/temperature.json`)
}
