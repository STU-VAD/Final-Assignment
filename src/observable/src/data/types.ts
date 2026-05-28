export interface CO2Data {
  years: number[]
  mean: number[]
  unc: number[]
}

export interface TemperatureData {
  years: number[]
  latitudeBands: string[]
  anomalies: number[][]
}

export interface YearData {
  year: number
  co2: number
  co2Unc: number
  temperatures: Record<string, number>
}

export interface CombinedData {
  years: number[]
  data: YearData[]
}

export interface VisualizationState {
  currentYear: number
  isPlaying: boolean
  playbackSpeed: number
  granularity: 'fine' | 'medium' | 'hemisphere'
  selectedBands: string[]
}
