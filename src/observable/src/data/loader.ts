import type { CombinedData, TemperatureData } from '../types'

const BASE = import.meta.env.BASE_URL

export async function loadCombinedData(): Promise<CombinedData> {
  const res = await fetch(`${BASE}data/combined.json`)
  return res.json()
}

export async function loadTemperatureData(): Promise<TemperatureData> {
  const res = await fetch(`${BASE}data/temperature.json`)
  return res.json()
}
