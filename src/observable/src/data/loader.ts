import type { CO2Data, TemperatureData, CombinedData } from './types'

export async function loadCO2Data(): Promise<CO2Data> {
  const response = await fetch('/data/co2.json')
  return response.json()
}

export async function loadTemperatureData(): Promise<TemperatureData> {
  const response = await fetch('/data/temperature.json')
  return response.json()
}

export async function loadCombinedData(): Promise<CombinedData> {
  const response = await fetch('/data/combined.json')
  return response.json()
}
