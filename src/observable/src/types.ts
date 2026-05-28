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

export type ViewMode = '3d' | 'faceA' | 'faceB' | 'faceC'

export interface CameraPreset {
  eye: { x: number; y: number; z: number }
  center: { x: number; y: number; z: number }
  up: { x: number; y: number; z: number }
}
