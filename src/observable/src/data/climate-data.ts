export interface BandDef {
  key: string
  label: string
  yPos: number
  color: string
}

export const BAND_8: BandDef[] = [
  { key: '90S-64S',  label: '南极 (90S-64S)',   yPos: -77, color: '#2b8cbe' },
  { key: '64S-44S',  label: '高纬南 (64S-44S)',  yPos: -54, color: '#7bccc4' },
  { key: '44S-24S',  label: '中纬南 (44S-24S)',  yPos: -34, color: '#a8ddb5' },
  { key: '24S-EQU',  label: '赤南 (24S-EQU)',    yPos: -12, color: '#ccebc5' },
  { key: 'EQU-24N',  label: '赤北 (EQU-24N)',    yPos: 12,  color: '#fee5a0' },
  { key: '24N-44N',  label: '中纬北 (24N-44N)',   yPos: 34,  color: '#fdae6b' },
  { key: '44N-64N',  label: '高纬北 (44N-64N)',   yPos: 54,  color: '#fb6a4a' },
  { key: '64N-90N',  label: '北极 (64N-90N)',     yPos: 77,  color: '#e31a1c' },
]

export const TEMP_COLORSCALE: [number, string][] = [
  [0.0, 'rgb(5,48,97)'],
  [0.1, 'rgb(33,102,172)'],
  [0.2, 'rgb(67,147,195)'],
  [0.3, 'rgb(146,197,222)'],
  [0.4, 'rgb(209,229,240)'],
  [0.5, 'rgb(247,247,247)'],
  [0.6, 'rgb(253,219,199)'],
  [0.7, 'rgb(244,165,130)'],
  [0.8, 'rgb(214,96,77)'],
  [0.9, 'rgb(178,24,43)'],
  [1.0, 'rgb(103,0,31)'],
]

export const TEMP_MIN = -3.0
export const TEMP_MAX = 3.0

export const CO2_MIN = 330
export const CO2_MAX = 435
