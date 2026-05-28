import type { CombinedData, TemperatureData } from '../types'

export async function loadCombinedData(): Promise<CombinedData> {
  const res = await fetch('/data/combined.json')
  return res.json()
}

export async function loadTemperatureData(): Promise<TemperatureData> {
  const res = await fetch('/data/temperature.json')
  return res.json()
}
