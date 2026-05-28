export interface CombinedDataItem {
  year: number
  co2: number
  co2Unc: number
  temperatures: Record<string, number>
}

export interface CombinedData {
  years: number[]
  data: CombinedDataItem[]
}

export interface TemperatureData {
  years: number[]
  latitudeBands: string[]
  anomalies: number[][]
}
